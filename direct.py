import pytesseract as tess
import sys
import re
import csv
from PIL import Image
import os
from pathlib import Path

name_of_file = sys.argv[2]

path_to_download_folder = str(Path.home() / "Downloads/")

completeName = os.path.join(path_to_download_folder, name_of_file + ".csv")


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


img = Image.open(sys.argv[1])
text = tess.image_to_string(img)
result = re.split("\n", text)
resultList = [float(i.replace(",", "")) for i in result[::-1] if isfloat(i)]

f = open(completeName, "w")

with f:

    writer = csv.writer(f)
    resultList = [[item] for item in resultList]
    writer.writerows(resultList)
