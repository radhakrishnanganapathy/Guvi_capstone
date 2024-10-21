import streamlit as st
from BizCardX import app
from project import test
from YoutubeHarversting import main
from DS_Phonepe.app import main

st.sidebar.title('My Capstone Project')

selection = st.sidebar.radio("Go to",['BizCardX','YoutubeHarversting','DS_Phonepe'])


if selection == 'BizCardX':
     app.main()
elif selection == 'YoutubeHarversting':
     main.youtube_main()
elif selection == 'DS_Phonepe':
     main.phonepe_main()