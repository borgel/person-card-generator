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

MARGIN = 36 * 2

FONT_NAME = 'Georgia.ttf'
FONT_SIZE_BIG     = 60
FONT_SIZE_MEDIUM  = 40
FONT_SIZE_SMALL   = 20

GRAD_CAP = u"\U0001F393"

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
   i = Image.open(HEADSHOTS_DIR + filename)
   #TODO refine these to make the image as large as possible
   i.thumbnail((460, 700))
   return i

def GenerateSidebar(person):
   '''
   Render name + school w/ number of degrees, then rotate it vertically and return
   '''
   fontBig = ImageFont.truetype(FONT_NAME, FONT_SIZE_BIG)
   #fontMed = ImageFont.truetype("Arial Unicode.ttf", FONT_SIZE_MEDIUM)
   fontMed = ImageFont.truetype(FONT_NAME, FONT_SIZE_MEDIUM)

   size = tuple(reversed(IMAGE_SIZE))
   size = (1000, 200)
   print(size)
   base = Image.new("RGBA", size, "white")

   name = ImageDraw.Draw(base)
   name.fontmode = "1" # this apparently sets (anti)aliasing for text

   formattedName = person['First'] + " " + person['Last']
   if person['Nick']:
      formattedName = person['First'] + " \"" + person['Nick'] + "\" " + person['Last']
   w, h = name.textsize(formattedName, font=fontBig)
   name.text((0, 0), formattedName, align="center", font=fontBig, fill="black")

   degrees = int(person["Number Of Degrees"])
   print("degs = " + str(degrees))
   school = person["Alma Mater"] + " " + GRAD_CAP
   for i in range(degrees):
      print("adding deg")
      school = school + GRAD_CAP
   school = school + " - " + person['Field']
   print(school)
   name.text((0, 5 + h), school, align="center", font=fontMed, fill="black")

   return base

def GenerateCard(idx, person):
   '''
   Dict of a person's info.
   Assume we're in the right target directory already and write to .
   '''
   print(person)

   # empty image we will work on top of
   base = Image.new("RGB", IMAGE_SIZE)

   back = ImageDraw.Draw(base)
   back.rectangle([(0, 0), IMAGE_SIZE], fill='White')

   sidebar = GenerateSidebar(person)
   # center origin is upper left
   #sidebar = sidebar.rotate(90, expand=1, center=(0, 0))
   #sidebar.rotate(90, expand=1, center=(0, 0))
   sidebar = sidebar.rotate(270, expand=1)
   topRight = (IMAGE_SIZE[0] - MARGIN - 200, MARGIN)
   base.paste(sidebar, topRight)

   # find this person's headshot
   headshot = GetHeadshot(person)
   #base.paste(headshot, (100, 100))
   #4-tuple defining the left, upper, right, and lower pixel coordinate
   # resize headshot to a known size. Takes MAX width, height
   # add to the left to move inside the card number
   base.paste(headshot, (MARGIN + 100, MARGIN))

   # get a font
   fontBig = ImageFont.truetype(FONT_NAME, FONT_SIZE_BIG)
   fontMed = ImageFont.truetype(FONT_NAME, FONT_SIZE_MEDIUM)
   fontSm = ImageFont.truetype(FONT_NAME, FONT_SIZE_SMALL)

   info = ImageDraw.Draw(base)
   info.fontmode = "1" # this apparently sets (anti)aliasing for text

   meta = '''Spouse:
        {}
Parents:
        {}'''.format(person['Partner'], person['Parent'])
   info.multiline_text((MARGIN, MARGIN + 700 + 30), meta, align="left", font=fontBig, fill="Black")

   # composite the final image
   title = str(idx) + "-" + person['First'] + " " + person['Last']
   base.save(OUTPUT_DIR + title + "." + IMAGE_FORMAT, IMAGE_FORMAT)

for f in glob.glob("*.csv"):
   INPUT_FILE = f
   break

print("Working on [" + str(INPUT_FILE) + "] and writing to [" + OUTPUT_DIR + "]")

count = 0
with open(INPUT_FILE) as f:
   # move to the output dir now that the CSV is open
   try:
      os.mkdir(HEADSHOTS_DIR)
   except:
      # TODO make this less permissive
      pass

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

