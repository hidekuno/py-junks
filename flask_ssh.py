# pip install flask flask-cors

from flask.logging import logging as flask_logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import paramiko
from os.path import basename, dirname, join, sep
import sys
import stat
import traceback
import io
import argparse


SSH_TIMEOUT = 5
KEY_FILE = "/app/keyfile"
on_local = False
app = Flask(__name__)
CORS(app)


class AwsEcsFilter(flask_logging.Filter):
    def filter(record):
        return 'GET /healthcheck' not in record.getMessage()


flask_logging.getLogger("werkzeug").addFilter(AwsEcsFilter)


class ValidationError(Exception):
    def __init__(self, err_msg):
        self.err_msg = err_msg
        super(ValidationError, self).__init__(
            err_msg
        )

    def __str__(self):
        return "ValidationError"


def validate_json(data):
    dir_path = data.get("path")
    if not dir_path:
        raise ValidationError("Directory path is not specified.")

    if ';' in dir_path:
        raise ValidationError("Illegal characters are used.")

    ssh_server = data.get("host")
    if not ssh_server:
        raise ValidationError("No server specified.")

    ssh_user = data.get("user")
    if not ssh_user:
        raise ValidationError("No user name specified")

    ssh_port = data.get("port")
    if not ssh_port:
        raise ValidationError("No port number specified")
    if not ssh_port.isdigit():
        raise ValidationError("No port number specified")


def ssh_list_directory(data, ssh_client):
    dir_path = data.get("path")

    # Don't show anything above the home directory.
    if dir_path[0] == sep:
        dir_path = dir_path[1:]
    dir_path = join('${HOME}', dir_path)
    command = f'/usr/bin/find {dir_path} -maxdepth 1 -a -type d'

    stdin, stdout, stderr = ssh_client.exec_command(command)
    ret = stdout.channel.recv_exit_status()

    if ret != 0:
        err = stderr.read().decode().split('\n')
        return jsonify({"error": err[0]}), 400

    # delete empty record.
    dirs = sorted(stdout.read().decode().split('\n'))[1:]
    result = {
        "current_dir": dirname(dirs[0] + sep),
        "dirs": [basename(d) for d in dirs[1:]]
    }
    return jsonify(result)


def sftp_list_directory(data, ssh_client):
    sftp_con = ssh_client.open_sftp()

    files = sftp_con.chdir(data.get("path"))
    files = sftp_con.listdir_attr(".")

    result = {
        "current_dir": sftp_con.getcwd(),
        "dirs": [f.filename for f in files if f.st_mode & stat.S_IFDIR]
    }
    return jsonify(result)


def connect_on_local(ssh_client, data):
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(data.get("host"),
                       port=data.get("port"),
                       username=data.get("user"),
                       # key_filename=data.get(KEY_FILE),
                       timeout=SSH_TIMEOUT)


def connect_on_ecs(ssh_client, data):
    with open(KEY_FILE) as fd:
        pk = paramiko.RSAKey.from_private_key(io.StringIO(fd.read()))

    ssh_client.set_missing_host_key_policy(paramiko.WarningPolicy())
    ssh_client.connect(data.get("host"),
                       port=data.get("port"),
                       username=data.get("user"),
                       pkey=pk,
                       timeout=SSH_TIMEOUT)


def core_proc(listdir, ssh_connect):
    ssh_client = paramiko.SSHClient()

    try:
        data = request.get_json()
        validate_json(data)
        ssh_connect(ssh_client, data)

        return listdir(data, ssh_client)

    except ValidationError as e:
        return jsonify({"error": e.err_msg}), 400

    except paramiko.SSHException as e:
        traceback.print_exc()
        return jsonify({"error": f"SSH Error: {str(e)}"}), 500

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Error: {str(e)}"}), 500

    finally:
        ssh_client.close()


@app.route('/list_dir/ssh', methods=['GET', 'POST'])
def list_dir_ssh():
    return core_proc(ssh_list_directory,
                     connect_on_local if on_local else connect_on_ecs)


@app.route('/list_dir/sftp', methods=['GET', 'POST'])
def list_dir_sftp():
    return core_proc(sftp_list_directory,
                     connect_on_local if on_local else connect_on_ecs)


@app.route('/healthcheck', methods=['GET', 'POST'])
def healthcheck():
    return jsonify("OK")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l", "--local", default=False, action="store_true", required=False
    )
    args = parser.parse_args(sys.argv[1:])
    if args.local:
        on_local = True

    app.run(debug=True, host='0.0.0.0', port=8000, threaded=True)
