# Import des bibliothèques
import streamlit as st
from PIL import Image
import pandas as pd
from bibliotheque.lib import  *
from datetime import datetime 
from plotly.offline import iplot
import plotly.graph_objs as go
import plotly.express as px
import numpy as np


# config de pages
st.set_page_config(
    page_title="Localisation des associations",
    layout="wide",
    page_icon="📊",
    menu_items={
        "Get Help": "https://www.cefim.eu/",
        "About" : "https://www.linkedin.com/in/melody-duplaix-391672265"
    }
)

st.title("Liste des associations par villes")

dataset = charger_les_fichiers()

liste_commune = dataset['commune'].unique().tolist()

commune = st.selectbox("Commune", options=liste_commune)


dataset = dataset[dataset["commune"]==commune]
st.dataframe(dataset, hide_index=True)
