# Xkcapt
This project provides tools for downloading, preparing, analyzing datasets for training a neural network to annotate images in different languages.

## Anchors
- [Description](#Description)
- - [Download scripts](#Download-scripts)
- - [Analysis scripts](#Analysis-scripts)
- - - [dload_dataset](#dload_dataset)
- - - [merge_mscoco_jsons](#merge_mscoco_jsons)
- - - [raw2mscoco](#raw2mscoco)
- - - [count_word_frequency](#count_word_frequency)
- [Requirements](#Requirements)
- [Installation](#Installation)
- - [General](#General)
- - - [nltk installation](#nltk-installation)
- - [Russian annotations](#Russian-annotations)
- - - [OpenNMT-py installation](#OpenNMT-py-installation)
- - - [En-ru-onmt](#En-ru-onmt)

## Description

### Download scripts
This section based on downloading google's [Conceptual Captions Dataset](https://ai.google.com/research/ConceptualCaptions) and merging it with MSCOCO dataset.

Why exactly google dataset? Because it has more than 3 millions captioned images while MSCOCO has only ~200-300k. The scripts below allow you to download a dataset from Google and merge it with MSCOCO dataset, thereby increasing the total size of the training sample by ~10 times.

-----
#### dload_dataset
This module reads .tsv file with cells separated by tabs **"/t"** with following format:

**Template:**

Cell_1|Cell_2|
--- | ---
*annotation* | *URL*

**Example:**

Cell_1|Cell_2|
--- | ---
"a very typical bus station" | http://some_site_1.com/some_pic.jpg
"gangsta rap artist attends sports team vs playoff game in the borough ." | http://some_site_2.com/some_pic.jpg
"traditional ornamental floral paisley bandanna ." | http://some_site_3.com/some_pic.jpg

Script goes though all the cells and tries to download every picture. If the program fails to access then the cell number is added to the list of unloaded.

**Result JSON-file view:**

````JSON
{
    "tsv_source_fname": "string",
    "time spent": "int",
    "downloaded_flist": [
        {
          "cell_number": "int",
          "filename": "string",
          "caption": "string"
        }
    ],
    "error_clist":  [ "int", "int", "..." ]
}
````
-----
#### merge_mscoco_jsons
This module merges two MSCOCO json files into one. It takes two paths to json files as arguments.
It is worth noting that original MSCOCO dataset has the following feature: one picture may have two or more annotations so this module implements logic that preserves the correct annotation links to images.

It is understood that MSCOCO json files will have following format:

**Example:**
````JSON
{
      "info": {
          "description": "This is stable 1.0 version..",
          "url": "http://any_url.com",
          "version": "1.0",
          "year": 2017,
          "contributor": "Microsoft COCO.group",
          "date_created": "2017-01-27 09:11:52.357474",
      "images": [
              {
                  "licence": "int",
                  "file_name": "filename.jpg",
                  "coco_url": "http://any_url.com",
                  "height": 360,
                  "width": 640,
                  "date_captured": "2017-11-14 11:18:45",
                  "flick_url": "http://any_url.com",
                  "id": 391895
              }
          ],
      "licenses": [
              {
                  "url": "http://any_url.com",
                  "id": 1,
                  "name": "Attribution-NonCommercial-ShareAlike Licence"
              }
          ],
      "annotations": [
              {
                  "image_id": 203564,
                  "id": 37,
                  "caption": "A bicycle replica with a clock as the front wheel."
              }
          ]
      }
}
````
-----
#### raw2mscoco
This module simply converts .json generated by dload_dataset.py to mscoco .json format.

Since we do not know some information about the downloaded images (for example, year of creation, license), these cells are filled with the text "unknown".

**For the brevity of the code the output json will have only one license:**
````JSON
{
    "url": "http://flickr.com/commons/usage/",
    "id": 7,
    "name": "No known copyright restrictions"
}
````

**Template of source file (generated by [dload_dataset](dload_dataset)):**
````JSON
{
    "tsv_source_fname": "string",
    "time spent": "int",
    "downloaded_flist": [
        {
          "cell_number": "int",
          "filename": "string",
          "caption": "string"
        }
    ],
    "error_clist":  [ "int", "int", "..." ]
}
````
**Template of destination file (MSCOCO .json standard):**
````JSON
{
      "info": {
          "description": "This is stable 1.0 version..",
          "url": "http://any_url.com",
          "version": "1.0",
          "year": 2017,
          "contributor": "Microsoft COCO.group",
          "date_created": "2017-01-27 09:11:52.357474",
      "images": [
              {
                  "licence": "int",
                  "file_name": "filename.jpg",
                  "coco_url": "http://any_url.com",
                  "height": 360,
                  "width": 640,
                  "date_captured": "2017-11-14 11:18:45",
                  "flick_url": "http://any_url.com",
                  "id": 391895
              }
          ],
      "licenses": [
              {
                  "url": "http://any_url.com",
                  "id": 1,
                  "name": "Attribution-NonCommercial-ShareAlike Licence"
              }
          ],
      "annotations": [
              {
                  "image_id": 203564,
                  "id": 37,
                  "caption": "A bicycle replica with a clock as the front wheel."
              }
          ]
      }
}
````

### Analysis scripts
-----
#### count_word_frequency

This module counts word frequency in .json or .tsv files. After finishing it saves the results to a file.

MSCOCO source .json files must have following fields:
````JSON
{
    "annotations":[
        {
            "caption": "string"
        }
    ]
}
````

Google source .tsv files must have [following format](#dload_dataset) described above.

**Example of results in .json format:**
````JSON
{
   "a": 41137,
   ".": 18778,
   "on": 9076,
   "of": 8619,
   "the": 8416,
   "in": 7661,
   "with": 6415,
   "and": 5847,
   "is": 4209
}
````
**Example of results in .tsv format:**

- a\t41137\n
.\t18778\n
on\t9076\n
of\t8619\n
the\t8416\n
in\t7661\n
with\t6415\n
and\t5847\n
is\t4209\n

word | frequency
---|---
a |  41137
. |  18778
on |  9076
of |  8619
the |  8416
in |  7661
with |  6415
and |  5847
is |  4209

## Requirements
### General
- python 3.8
- - nltk (3.4.5)

### Russian annotations
- [OpenNMT-py](https://opennmt.net/OpenNMT-py/main.html#installation)
- [Translator (Ru) -> (En)](https://github.com/ManiaCello/en-ru-onmt)

## Installation
### General
#### nltk installation
````shell
pip install nltk
````
After that write and execute the following code:
````PYTHON
import nltk
nltk.download()
````
When GUI will launch choose **install all** and exit.

### Russian annotations
#### OpenNMT-py installation
````shell
pip install OpenNMT-py
````
*or from the sources:*
````shell
git clone https://github.com/OpenNMT/OpenNMT-py.git
cd OpenNMT-py
python setup.py install
````
#### En-ru-onmt
Install [OpenNMT-py](#OpenNMT-py-installation) described above.

Then download [en-ru-onmt](https://github.com/ManiaCello/en-ru-onmt) repository:
````shell
git clone https://github.com/ManiaCello/en-ru-onmt
````
Download [**this**](https://drive.google.com/open?id=11gJr4c06wgVuV5Jb1I2CWVKhyNtYFxPY) model and place it to **en-ru-onmt/models** folder.
