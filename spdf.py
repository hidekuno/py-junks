#!/usr/bin/env python
#
# This is a personal tool what I need for my working.
#
# hidekuno@gmail.com
#
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import mm

import sys
import os
import argparse
from PIL import Image
import PIL

ADDRESS = 'Hyogo Kobe'
MYNAME = 'Test Taro'

def create_img():
    path = os.path.join(os.environ['HOME'], "sign.png")
    img = Image.open(path)
    return img.resize((25, 25), PIL.Image.Resampling.LANCZOS)

def make_pdf(infile, outfile):
    pdf = PdfReader(infile, decompress=False)
    page = pdf.pages[0]

    ctx = canvas.Canvas(outfile, pagesize=portrait(A4))
    ctx.doForm(makerl(ctx, pagexobj(page)))

    font_name = "HeiseiKakuGo-W5"
    pdfmetrics.registerFont(UnicodeCIDFont(font_name))
    ctx.setFont(font_name, 10)

    ctx.drawString(140*mm, 250*mm, ADDRESS)
    ctx.drawString(179*mm, 240*mm, MYNAME)
    ctx.drawInlineImage(create_img(), 179*mm, 228*mm)

    ctx.showPage()
    ctx.save()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-in", "--infile", type=str, dest="infile", required=True)
    parser.add_argument("-out", "--outfile", type=str, dest="outfile", required=True)
    args = parser.parse_args(sys.argv[1:])

    make_pdf(args.infile, args.outfile)
