import streamlit as st
from utils import Utils

class Components(Utils):

    def __init__(self, 
                 error_file, error_upload, error_url,
                 choose_title="Choose option to upload",
                 choose_type="Choose Type",
                 drag_drop="Drag and Drop",
                 upload_url="Upload From Url",
                 file_input = "Upload Image",
                 text_input="Input Url Image",
                 camera_input="Take a Picture"):
        self.choose_title = choose_title
        self.choose_type = choose_type
        self.drag_drop = drag_drop
        self.upload_url = upload_url
        self.text_input = text_input
        self.file_input = file_input
        self.camera_input = camera_input
        self.error_file = error_file
        self.error_upload = error_upload
        self.error_url = error_url
        

    def uploader(self):
        imgSt = None
        img = None

        choose_upload = st.selectbox(
            self.choose_title, [self.choose_type, self.drag_drop, self.upload_url, self.camera_input]
        )

        if choose_upload == self.choose_type:
            imgSt = None
            img = None

        elif choose_upload == self.drag_drop:
            imgSt = st.file_uploader(self.file_input, type=["png", "jpg", "jpeg"])
            img = self.loadImageFile(imgSt) if imgSt is not None else None

        elif choose_upload == self.camera_input:
            imgSt = st.camera_input(self.camera_input)
            img = self.loadImageFile(imgSt) if imgSt is not None else None

        else:
            imgSt = st.text_input(self.text_input)
            img = self.loadImageUrl(imgSt) if imgSt != '' else None

        return img, imgSt