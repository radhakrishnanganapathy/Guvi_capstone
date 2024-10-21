import streamlit as st
from PIL import Image
import pytesseract
from sqlalchemy.orm import Session
import re
# from models import *
from BizCardX.models import *
# from db import get_db, CreateTables
from BizCardX.db import get_db, CreateTables

from BizCardX import db
import pandas as pd
def main():
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
               # image = cv2.imread(image)
               # image_np = cv2.cvtColor(cv2.imread(image), cv2.COLOR_BGR2RGB)
               text = pytesseract.image_to_string(image)
               upper_string = text.upper()
               # st.write(text)
               name_pattern = r"^[A-Z][A-Z\s]+"
               position_pattern = r"^[A-Z][A-Z\s0-9]+$"
               # mobile_pattern = r'^\+?[0-9]+(?:-[0-9]+)+$'
               # mobile_pattern  = r'\+[\d-]+'
               mobile_pattern = r'\+\d+(?:[-\s—]?\d+)*'
               website_pattern = r"www\.[A-Za-z0-9]+\.[a-z]+"
               email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}"
               address_pattern = r"\n([\s\S]*?)\n\s*E\s"

               card = text
                    
               name_match = re.search(name_pattern, upper_string, re.MULTILINE)
               st.write('```',name_match)
               lines = upper_string.splitlines()
               non_empty_lines = [line for line in lines if line.strip()]
               st.write(non_empty_lines)
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
               if name_match :
                    name = name_match.group().strip()
                    card_dir['name'] = non_empty_lines[0]
                    
               else:
                    card_dir['name'] = None
               mobile_list = []
               mobile = re.search(mobile_pattern, text).group() if re.search(mobile_pattern, text) else None
               try:
                    mobile = ''.join(mobile.replace('—',''))
                    m_no = ''
                    for m in mobile:
                         m_no = m_no+m
                    if m_no not in mobile_list:
                         mobile_list.append(m_no)
                    # st.write(mobile_list)
                    card_dir['mobile'] = mobile_list
               except Exception as e:
                    card_dir['mobile'] = None
                    
               website = re.search(website_pattern, text).group() if re.search(website_pattern, text) else None
               card_dir['website'] = website
               email = re.search(email_pattern, text).group() if re.search(email_pattern, text) else None
               card_dir['email'] = email
               address = re.search(address_pattern, text).group() if re.search(address_pattern, text) else None
               card_dir['address'] = address
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
     # if st.button("Save Full text"):
     #      db = next(get_db())
     #      data,card = extract(image)
     #      full_card = CardInfo.full_card(db,card)
     #      st.write("Data saved to db")
     # if tab == 'Retrive Data':
          # output = []
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

     # if tab == "Retrive Full text":
     #      output = []
     #      db = next(get_db())
     #      db_return = CardInfo.full_text(db)
     #      for data in db_return:
     #           result = {
     #                'card' : data.card
     #           }
     #           output.append(result)
     #      st.write(pd.DataFrame(output))
