import streamlit as st
from json import load
from pages import Pages
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    st.set_page_config(page_title="Indonesian (Manado) Cakes Classification", page_icon="🍰" ,layout="wide")
    hide_menu_style = """
    <style>
        #MainMenu {display: none; }
        footer {visibility: hidden;}
        .css-fk4es0 {display: none;}
        #stStatusWidget {display: none;}
        .css-r698ls {display: none;}

        [data-testid="stAppViewContainer"] {
            background: linear-gradient(calc(20 * 1deg), #0f0514 calc(40 * 1%), #0d0c64 calc(40 * 1%));
        }

        [data-testid="stSidebar"] {
            background-color: #0f0514
        }

        [data-testid="stHeader"] {
            background-color: transparent
        }
    </style>
    """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

    languages = ['Bahasa Indonesia', 'English']
    pagesType = ['Home', 'Predict']

    st.sidebar.title('Indonesian (Manado) Cakes')
    st.session_state.pages = st.sidebar.selectbox(
        "Pages", pagesType
    )
    st.session_state.languages = st.sidebar.radio(
        "Select Languages", languages
    )
    f = open('datasets/languages.json')
    data_languages = load(f)

    lng = 'en' if 'English' in st.session_state.languages else 'id'
    data_lng = data_languages[lng] if 'English' in st.session_state.languages else data_languages[lng]
    
    page = Pages(data_lng=data_lng, lang=lng)
    if 'Home' in st.session_state.pages:
        page.home()
    else:
        page.predict()

if __name__ == "__main__":
    main()