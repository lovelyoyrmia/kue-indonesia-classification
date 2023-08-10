import streamlit as st
from utils import Utils
from components import Components
from PIL import Image
import pandas as pd
import numpy as np

class Pages():
    def __init__(self, data_lng, lang):
        self.data_lng = data_lng
        self.lang = lang

    def home(self):
        st.title(self.data_lng['title'])
        st.write(self.data_lng['title_desc'])
        img = Image.open('assets/kue.webp')
        st.image(img)
            
    def predict(self):
        st.title(self.data_lng['title_predict'])
        utils = Utils(
            error_upload=self.data_lng['error_upload'],
            error_url=self.data_lng['error_url'],
            error_file=self.data_lng['error_file'],
            error_maps=self.data_lng['error_maps']
        )

        component = Components(
            error_upload=self.data_lng['error_upload'],
            error_url=self.data_lng['error_url'],
            error_file=self.data_lng['error_file'],
            choose_title=self.data_lng['choose_title'],
            choose_type=self.data_lng['choose_type'],
            drag_drop=self.data_lng['drag_drop'],
            file_input=self.data_lng['file_input'],
            text_input=self.data_lng['text_input'],
            camera_input=self.data_lng['camera_input'],
            upload_url=self.data_lng['upload_url']
        )
        img, imgSt = component.uploader()
        
        if imgSt and img:

            name = imgSt.split('/')[-1] if type(imgSt) == str else imgSt.name    
            if st.button('Predict'):
                label, description, url, probabilities = utils.getPrediction(img, self.lang)
                if probabilities >= 0.85:
                    col1, col2 = st.columns([2, 2])
                    col1.subheader(self.data_lng['prediction_result'])
                    col1.image(imgSt, use_column_width=True, clamp=True)
                    col2.subheader(label)
                    col2.write(description)
                    if url is not None:
                        col2.markdown(f'''<a href="{url}" target="_blank">{self.data_lng['label_link']}</a>''', unsafe_allow_html=True)
                    
                    lat, lng = utils.getCurrentLoc()
                    if lat is None or lng is None:
                        return

                    st.subheader(self.data_lng['nearby_resto'])

                    restaurants = utils.getRestaurant(label, lat, lng)
                    
                    col3, col4 = st.columns([2, 2])
                    if len(restaurants) != 0:
                        df = pd.DataFrame(restaurants, columns=['name', 'latitude', 'longitude', 'vicinity', 'rating']).set_index('name')
                        col3.map(df, zoom=12)

                        for resto in restaurants:
                            url_resto = f"https://www.google.com/maps/search/?api=1&query={resto['latitude']},{resto['longitude']}"
                            with col4.expander(resto['name']):
                                st.write(f"📍 {resto['vicinity']}")
                                st.write(f"⭐ {resto['rating']}")
                                st.markdown(f'''<a href="{url_resto}" target="_blank">{self.data_lng['gmaps']}</a>''', unsafe_allow_html=True)

                    else:
                        st.write(self.data_lng['not_found_resto'])
                else:
                    st.subheader(self.data_lng['cake_not_found'])
                    st.image(imgSt, name, use_column_width=True, clamp=True)
            else: 
                st.subheader(self.data_lng['image'])
                st.image(imgSt, name, use_column_width=True, clamp=True)

        else:
            st.info(self.data_lng['info_upload'])
