#!/usr/bin/env python

import logging
from shutil import copyfile
import os
import json
import argparse
import sys

import cv2
import numpy as np
import pdf2image
sys.path.insert(0, "../../")


parser = argparse.ArgumentParser(
    description='Split the images (manually) into several folders.')
parser.add_argument('--input_dir', type=str,
                    help='A directory with a bunch of pdfs', required=True)
parser.add_argument('--output_dir', type=str,
                    help='A directory where the outputs will be', required=True)
parser.add_argument('--labels', nargs='+',
                    help='A bunch of labels to divide stuff', required=True)

args = parser.parse_args()
print(args)


def pil2cv(image):
    return np.array(image)[:, :, ::-1].copy()


def scale_image(image, scale_to_w_size):
    scale = scale_to_w_size / image.shape[1]
    return cv2.resize(image, (0, 0), fx=scale, fy=scale)

def extract_page_images_from_pdf(pdf_filepath, scale_to_w_size=None):
    images = []
    try:
        images = list(
            map(pil2cv, pdf2image.convert_from_path(pdf_filepath)))
        if scale_to_w_size is not None:
            images = [scale_image(im, scale_to_w_size) for im in images]
    except Exception as error:
        logging.error(str(error))
    return images

def put_text(image, ith_line, text):
    text_line_offset = 30
    colors = [(225, 20, 20), (20, 225, 20), (20, 20, 192),
              (225, 180, 20), (225, 20, 180), (20, 225, 180)]
    c = colors[ith_line % len(colors)]
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, "{0} - {1}".format(ith_line+1, text), (10,
                                                              (ith_line+1)*text_line_offset), font, 0.8, c, 2, cv2.LINE_AA)
    return image


output_dir = args.output_dir
labels = args.labels
for lbl in labels:
    if not os.path.exists(os.path.join(output_dir, lbl)):
        os.makedirs(os.path.join(output_dir, lbl))


pdfs_filenames = [f for f in os.listdir(args.input_dir) if f.endswith(".pdf")]
for pdf_filename in pdfs_filenames:
    pdf_path = "{0}/{1}".format(args.input_dir, pdf_filename)
    images = extract_page_images_from_pdf(pdf_path, 1000)
    
    img = images[0]
    valid_keys = {}
    for i, lbl in enumerate(labels):
        img = put_text(img, i, lbl)
        valid_keys[49+i] = lbl
    cv2.imshow("frame, press a key", img)

    key = 0
    while key not in valid_keys.keys():
        key = cv2.waitKey(0)

    onlyfilename = pdf_filename
    copyfile(pdf_path, os.path.join(output_dir, valid_keys[key], onlyfilename))
