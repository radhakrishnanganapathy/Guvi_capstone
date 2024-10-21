import streamlit as st
from PIL import Image
import pytesseract
from sqlalchemy.orm import Session
import re
from models import *
from db import get_db, CreateTables
import db
import pandas as pd

st.markdown(
     """
     <style>
     .title{
     position: relative;
     color: green;
     font-size:25px
     }
     .deff{
     color: #fce303
     }
     .ocr{
     color: red;
     font-size : 50px;
     }
     
     </style>
     """,unsafe_allow_html=True
)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'  # Replace with your Tesseract path
# pytesseract.pytesseract.tessdata_dir_config = '--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata"'  # Adjust to your setup
st.title("BizCardX: Extracting Business Card Data with OCR")
st.sidebar.markdown('<div class = "deff"> &nbsp &nbsp The OCR(Optical character recognition  or optical character reader) electronic or mechanical conversion of images of typed, handwritten or printed text into machine-encoded text, whether from a scanned document, a photo of a document, a scene photo or from subtitle text superimposed on an image. </div>',unsafe_allow_html=True)
CreateTables()

def extract(image):
     card_dir = {}
     if image is not None:
          image = Image.open(image)
          text = pytesseract.image_to_string(image)
          upper_string = text.upper()
          name_pattern = r"^[A-Z][A-Z\s]+"
          mobile_pattern = r'\+\d+(?:[-\s—]?\d+)*'
          website_pattern = r"www\.[A-Za-z0-9]+\.[a-z]+"
          email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}"
          address_pattern = r"\n([\s\S]*?)\n\s*E\s"

          card = text
               
          #split to multi line
          name_match = re.search(name_pattern, upper_string, re.MULTILINE)
          lines = upper_string.splitlines()
          non_empty_lines = [line for line in lines if line.strip()]
          st.write(non_empty_lines)

          #find position 
          if len(non_empty_lines)>1:
               position_line = non_empty_lines[1]
               cleaned_position = re.sub(r'[^A-Z\s]','',position_line).strip()
               if cleaned_position in ['GENERAL MANAGER', 'MANAGER', 'DATA MANAGER', 'DATA MANAGER', 'CEO', 'FOUNDER', 'CEO & FOUNDER', 'MARKETING EXECUTE', 'TECHNICAL MANAGER']:
                    position = cleaned_position
               else:
                    position = None
          else:
               position = None
          card_dir['position'] = position

          #find name
          if name_match :
               name = name_match.group().strip()
               card_dir['name'] = non_empty_lines[0]
               
          else:
               card_dir['name'] = None
          card_dir['mobile'] = non_empty_lines[2]
          #find mobile
          st.write(card_dir)
          return (card_dir, card)
     else:
          st.write("Updoad a card Image") 


image = st.file_uploader("upload your image here", type=["jpg","png","jpeg"])


if st.button('Save to db'):
     try:
          db = next(get_db())
          data,cards = extract(image)
          card = Card.create_card(db,data['name'],data['position'],data['mobile'],data['website'],data['email'],data['address'])
          full_card = CardInfo.full_card(db,cards)
          st.write("Data saved to db")
     except Exception as e:
          st.warning(e)

db = next(get_db())
db_return = Card.get_card(db)
output = []
for data in db_return:
     result = {
          'name' : data.name,
          'position' : data.position,
          'mobile' : data.mobile,
          'website' : data.website,
          'email' : data.email,
          'address' : data.address,
     }
     output.append(result)
st.write(pd.DataFrame(output))


