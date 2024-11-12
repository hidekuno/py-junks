# pip install flask flask-cors

from flask import Flask, request, jsonify
from flask_cors import CORS
import paramiko
from os.path import basename,dirname,join,sep
import stat

SSH_TIMEOUT = 5

app = Flask(__name__)
CORS(app)


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
        err =  stderr.read().decode().split('\n')
        return jsonify({"error": err[0]}), 400

    # delete empty record.
    dirs = sorted(stdout.read().decode().split('\n'))[1:]
    result = {
        "current_dir": dirname(dirs[0]+sep),
        "dirs": [ basename(d) for d in dirs[1:] ]
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

@app.route('/list_dir', methods=['GET','POST'])
def list_directory():
    ssh_client = paramiko.SSHClient()

    try:
        data = request.get_json()
        validate_json(data)

        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(data.get("host"),
                           port=data.get("port"),
                           username=data.get("user"),
                           timeout=SSH_TIMEOUT)

        return sftp_list_directory(data, ssh_client)

    except ValidationError as e:
        return jsonify({"error": e.err_msg}), 400

    except paramiko.SSHException as e:
        return jsonify({"error": f"SSH Error: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500

    finally:
        ssh_client.close()

if __name__ == '__main__':
    app.run(debug=True, port=8000,)
