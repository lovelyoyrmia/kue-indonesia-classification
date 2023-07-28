import io
from PIL import Image
import requests
import streamlit as st
from model import Model
from json import load
import requests
import googlemaps
import webbrowser
import os

class Utils():
    def __init__(self, 
                 error_upload="Cannot Upload Your Image !",
                 error_url="Please Input The Valid URL",
                 error_file="Cannot Upload File. Please try again !",
                 error_maps="Cannot get locations",
                 api_key=st.secrets.get('API_KEY_MAPS')):
        self.error_upload = error_upload
        self.error_url = error_url
        self.error_file = error_file
        self.error_maps = error_maps
        self.api_key = api_key

    def loadImageUrl(self, url):
        try:
            response = requests.get(url, stream=True)
            imageStream = io.BytesIO(response.content)
            try:
                return Image.open(imageStream)
            except:
                st.error(self.error_upload)
                return None
        except Exception:
            st.error(self.error_url)
            return None
    
    def loadImageFile(self, img):
        try:
            return Image.open(img)
        except Exception:
            st.error(self.error_file)
            return None
    
    def getPrediction(self, img, lng):
        model = Model()
        f = open('datasets.json')
        data = load(f)
        prediction = model.predict(img)
        label = prediction.replace('_', ' ').title()
        description = data[prediction][lng]['description']
        url = data[prediction][lng]['url']
        return label, description, url
    
    def getCurrentLoc(self):
        try:
            gmaps = googlemaps.Client(key=self.api_key)
            loc = gmaps.geolocate()
            latitude = loc['location']['lat']
            longitude = loc['location']['lng']
            return latitude, longitude
        except Exception:
            st.error(self.error_maps)
            return None, None
    
    def extractRestaurantInfo(self, restaurants):
        name = restaurants.get("name")
        latitude = restaurants.get("geometry").get("location").get("lat")
        longitude = restaurants.get("geometry").get("location").get("lng")
        vicinity = restaurants.get("vicinity")
        rating = restaurants.get("rating")
        return {
            "name": name, 
            "latitude": latitude, 
            "longitude": longitude,
            "vicinity": vicinity, 
            "rating": float(rating)
        }
    
    def getRestaurant(self, keyword, lat, lng):
        try:
            url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&keyword={keyword}&opennow=true&radius=2000&type=restaurant&key={self.api_key}'
            response = requests.get(url)
            data = response.json()['results']
            
            restaurants = []
            for resto in data:
                restoInfo = self.extractRestaurantInfo(resto)
                restaurants.append(restoInfo)
            
            return restaurants
        except Exception:
            return []
    
    def openGmaps(self, lat, lng):
        url = f'https://www.google.com/maps/search/?api=1&query={lat},{lng}'
        webbrowser.open_new_tab(url)
    