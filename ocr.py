# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 14:54:14 2022

@author: Yalda
"""

#install tesseract-ocr-w64-setup-v5.0.1.20220118.exe
#run pip install pytesseract to install pytesseract 
from PIL import Image
from pytesseract import pytesseract
import re
  
# Defining paths to tesseract.exe
# and the image we would be using
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
image_path = r'./Brilliant_AC.jpg'
  
# Opening the image & storing it in an image object
img = Image.open(image_path)
 
# Providing the tesseract executable
# location to pytesseract library
pytesseract.tesseract_cmd =  r'C:\Program Files\Tesseract-OCR\tesseract' 
#print(pytesseract.image_to_string(image_path))

# Passing the image object to image_to_string() function
# This function will extract the text from the image
text = pytesseract.image_to_string(img)
  
# Displaying the extracted text
#print(text[:-1])
#print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

#Read line by line
details = pytesseract.image_to_data(img, output_type='data.frame')
text = details[details.conf != -1]
lines = text.groupby('block_num')['text'].apply(list)


import cv2


# Grayscale, Gaussian blur, Otsu's threshold
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3,3), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Morph open to remove noise and invert image
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
invert = 255 - opening

# Perform text extraction
data = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')
#print(data)

#cv2.imshow('thresh', thresh)
#cv2.imshow('opening', opening)
#cv2.imshow('invert', invert)
#cv2.waitKey()

#Contains each line of on the image 
lines = data.split("\n")


#extract requested data from text 
company_name = lines[1]
document_date = lines[2]
location = re.findall('the\s?(.{10,15})\s? office', lines[5])[0]
dates_between = lines[6].split("between",1)[1][:-1] 
contact_person = re.findall('contact\s?(.{10,15})\s? on', lines[7])[0]
contact_email = re.findall('\S+@\S+', lines[8])[0]
contact_number = lines[7].split(" on ",1)[-1][:-1] 
guaranteed = re.findall('[0-9]+', lines[12])[0]

print(f"company_name: {company_name}")
print(f"document_date: {document_date}")
print(f"location: {location}")
print(f"dates_between: {dates_between}")
print(f"contact_person: {contact_person}")
print(f"contact_email: {contact_email}")
print(f"contact_number: {contact_number}")
print(f"guaranteed: {guaranteed}")
