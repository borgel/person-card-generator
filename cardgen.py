#!/usr/local/bin/python

import sys, os, glob, csv
from PIL import Image, ImageDraw, ImageFont

INPUT_FILE = ""
OUTPUT_DIR = "./cards/"
HEADSHOTS_DIR = "headshots/"

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
def GetHeadshot(person):
   first = person['First'].lower()
   last = person['Last'].lower()
   print("Finding " + first + " " + last)

   # dumb find the first match
   filename = None
   for f in os.listdir(HEADSHOTS_DIR):
      f = f.lower()
      print(f)
      if first in f and last in f:
         filename = f
         break
   if not filename:
      raise Exception("No headshot found for " + first + " " + last)

   # generate a drawable canvas and return it
   return Image.open(HEADSHOTS_DIR + filename)

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

   # find this person's headshot
   headshot = GetHeadshot(person)
   #base.paste(headshot, (100, 100))
   #4-tuple defining the left, upper, right, and lower pixel coordinate
   # resize headshot to a known size. Takes MAX width, height
   headshot.thumbnail((IMAGE_SIZE[0], IMAGE_SIZE[1] / 1))
   img_w, img_h = headshot.size
   bg_w, bg_h = base.size
   bg_h = bg_h / 2
   topCenter = ((bg_w - img_w) / 2, ((bg_h - img_h) / 2) + 140)
   base.paste(headshot, topCenter)

   # get a font
   fontBig = ImageFont.truetype(FONT_NAME, FONT_SIZE_BIG)
   fontMed = ImageFont.truetype(FONT_NAME, FONT_SIZE_MEDIUM)
   fontSm = ImageFont.truetype(FONT_NAME, FONT_SIZE_SMALL)

   name = ImageDraw.Draw(base)
   name.fontmode = "1" # this apparently sets (anti)aliasing for text

   formattedName = person['First'] + " " + person['Last']
   if person['Nick']:
      formattedName = person['First'] + " \"" + person['Nick'] + "\" " + person['Last']
   w, h = name.textsize(formattedName, font=fontBig)
   print("width = " + str(w))
   w = (IMAGE_SIZE[0] - w) / 2
   name.multiline_text((w, 15), formattedName, align="center", font=fontBig, fill="Black")

   #TODO title

   # composite the final image
   base.save(OUTPUT_DIR + title + "." + IMAGE_FORMAT, IMAGE_FORMAT)

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
   #os.chdir(OUTPUT_DIR)

   # TODO use class csv.Sniffer to check if there is a header. If so use a csv.DictReader
   # first row will be used as keys
   reader = csv.DictReader(f)

   for person in reader:
      GenerateCard(count, person)
      count = count + 1

