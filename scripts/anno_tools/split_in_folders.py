#!/usr/bin/env python

import sys
sys.path.insert(0, "../../")


from pysuricata import video_stream
import argparse
import cv2
import json
import os
from shutil import copyfile




parser = argparse.ArgumentParser(description='Split the images (manually) into several folders.')
parser.add_argument('--config', type=str, help='Json config file, should have a video_stream and also a list of labels', required=True)

args = parser.parse_args()

print(args.config)

def scale_image(image, height = 1000):
    scale = height/image.shape[0]
    return cv2.resize(image, (0,0), fx=scale, fy=scale)


def put_text(image, ith_line, text):
    text_line_offset = 30
    colors = [(225,20,20), (20,225,20), (20,20,192), (225,180,20), (225,20,180), (20,225,180)]
    c = colors[ith_line % len(colors)]
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, "{0} - {1}".format(ith_line+1, text), (10, (ith_line+1)*text_line_offset), font, 0.8, c, 2, cv2.LINE_AA)
    return image



with open(args.config) as data_file:    
    config_data = json.load(data_file)
    v = video_stream.load_from_config(config_data["input_sequence"])

    output_dir = config_data["output_folder"]
    labels = config_data["labels"]
    for lbl in labels:
        if not os.path.exists(os.path.join(output_dir, lbl)):
            os.makedirs(os.path.join(output_dir, lbl))
        
    while not v.has_ended():
        img = v.get_next_frame()
        img = scale_image(img)
        valid_keys = {}
        for i,lbl in enumerate(labels):
            img = put_text(img, i, lbl)
            valid_keys[49+i] = lbl
        cv2.imshow("frame, press a key", img)

        key = 0
        while key not in valid_keys.keys():
            key = cv2.waitKey(0)
            
        onlyfilename = v.get_curr_filename()[v.get_curr_filename().rfind("/")+1:]
        copyfile(v.get_curr_filename(), os.path.join(output_dir,valid_keys[key],onlyfilename))
        

