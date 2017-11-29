#!/usr/local/bin/python

import sys, os, glob, csv
from PIL import Image, ImageDraw, ImageFont

INPUT_FILE = ""
OUTPUT_DIR = "./cards/"

MIN_IMAGE_SIZE = (411, 561)
SIZE_MULT = 2
IMAGE_SIZE = tuple([SIZE_MULT * x for x in MIN_IMAGE_SIZE])
IMAGE_FORMAT = "png"

FONT_NAME = 'Georgia.ttf'
FONT_SIZE_BIG     = 60
FONT_SIZE_MEDIUM  = 40
FONT_SIZE_SMALL   = 20

# TODO get headshot (in drawable we can mix)
# TODO allow add stroke or boder

def GenerateCard(idx, person):
   '''
   Dict of a person's info.
   Assume we're in the right target directory already and write to .
   '''
   title = str(idx) + "-" + person['First'] + "-" + person['Last']
   print(person)

   # empty image we will work on top of
   base = Image.new("RGB", IMAGE_SIZE)

   back = ImageDraw.Draw(base)
   back.rectangle([(0, 0), IMAGE_SIZE], fill='White')

   # get a font
   fontBig = ImageFont.truetype(FONT_NAME, FONT_SIZE_BIG)

   name = ImageDraw.Draw(base)
   name.fontmode = "1" # this apparently sets (anti)aliasing
   name.text((0, 0), person['First'], font=fontBig, fill="Black")

   # composite the final image
   #out = Image.alpha_composite(base, name)
   out = base
   out.save(title + "." + IMAGE_FORMAT, IMAGE_FORMAT)

for f in glob.glob("*.csv"):
   INPUT_FILE = f
   break

print("Working on [" + str(INPUT_FILE) + "] and writing to [" + OUTPUT_DIR + "]")

count = 0
with open(INPUT_FILE) as f:
   # move to the output dir now that the CSV is open
   try:
      os.mkdir(OUTPUT_DIR)
   except:
      # fine, it already exists
      # TODO make this less permissive
      pass
   os.chdir(OUTPUT_DIR)

   # TODO use class csv.Sniffer to check if there is a header. If so use a csv.DictReader
   # first row will be used as keys
   reader = csv.DictReader(f)

   for person in reader:
      GenerateCard(count, person)
      count = count + 1

