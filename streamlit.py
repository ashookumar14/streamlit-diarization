import streamlit as st
import os
import requests
import json

path = "./resampled/"

def file_selector(folder_path=path):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)


filename = file_selector()
st.write(filename)
file_name = os.path.join(path, filename)
audio_file = open(file_name, 'rb')
audio_bytes = audio_file.read()
st.audio(audio_bytes, format='audio/ogg')

url = "https://mldev.servicepack.ai:8081/diarize/"

payload={}
files=[
  ('file',(filename,open(file_name,'rb'),'audio/wav'))
]
headers = {}

response = requests.request("POST", url, headers=headers, data=payload, files=files,verify=False)

#print(response.text)

data = json.loads(response.text)
data1 = []
for i in data:
    x = i['speaker']
    #print(x)
    if (x == 1) and (i['text'] != ""):
        data1.append({"customer":i['text']})
    elif (x == 2) and (i['text'] != ""):
        data1.append({"agent":i['text']})

for i in data1:
    st.write(i)
