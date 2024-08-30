#!/usr/bin/env python
#
# This is a personal tool what I need for my working.
#
# hidekuno@gmail.com
#
# how to install
#
# sudo apt install tesseract-ocr libtesseract-dev tesseract-ocr-jpn
# pip install matplotlib
# pip install scipy
# pip install pdf2image
# pip install sympy
# pip install xlrd
# pip install cv-3
# pip install pyocr
# pip install easyocr

from PIL import Image
import pyocr
import cv2
import argparse
import sys

tools = pyocr.get_available_tools()
tool = tools[0]
print(tool.get_name())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, dest="imgfile", required=True)
    args = parser.parse_args(sys.argv[1:])

    try:
        img = Image.open(args.imgfile)
        txt = tool.image_to_string(img,lang='jpn+eng',builder=pyocr.builders.TextBuilder(tesseract_layout=4))
        print(txt)
    except Exception as e:
        print(e)
        sys.exit(1)
