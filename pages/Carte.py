# Import des bibliothèques
import streamlit as st
from PIL import Image
import pandas as pd
from bibliotheque.lib import  *
from st_pages import Page, show_pages, add_page_title
from datetime import datetime 
from plotly.offline import iplot
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import folium
import streamlit as st
from streamlit_folium import st_folium

# config de pages
st.set_page_config(
    page_title="Localisation des associations",
    page_icon="📊",
    menu_items={
        "Get Help": "https://www.cefim.eu/",
        "About" : "https://www.linkedin.com/in/melody-duplaix-391672265"
    }
)

st.title("Localisation des associations")

# Création de la sidebar
st.sidebar.header("filtre")
option = st.sidebar.selectbox("Département", ("37","45","tous"))

datasetnettoye = charger_les_fichiers()
datasetfiltre = filtrer_dataset_dep(datasetnettoye, option)
datasetactif = filtrer_dataset_actif(datasetfiltre)
dataset_prospets = tri_des_prospets(datasetactif)
datasetjoint = nettoyage_nomemclature(dataset_prospets)
dataset_sans_na = enlever_les_na(datasetjoint)
domaine = creation_filtre_domaine(datasetjoint)
datasetfiltre_location = nettoyage_carte(dataset_sans_na, domaine)

affichage_carte(datasetfiltre_location, domaine)