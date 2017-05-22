## PySuricata

This the Python 3.x version of our general tools. It comprehends several helpful scripts and modules to help make dataset annotation, read data or more general stuff.

### To install

Just do ```sudo pip3 install --upgrade .``` in the main folder

### Contents

- Modules:
-- video_stream: used to read different types of stream input such as video, camera ip, image sequence, etc.;

- Scripts:
-- extract_frames: read from a camera and sample some frames (ugly version);
-- keep_or_gone: separate an image folder into yes or no to remove bad samples in the dataset;
-- yes_no_reject: separate into positive and negative classes or fully reject the sample;

