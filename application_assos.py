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
    page_title="Analyse associations",
    page_icon="📊",
    menu_items={
        "Get Help": "https://www.cefim.eu/",
        "About" : "https://www.linkedin.com/in/melody-duplaix-391672265"
    }
)

show_pages(
    [
        Page("application_assos.py", "Home", "🏠"),
        Page("pages/Carte.py", "Carte","🗺️"),
        Page("pages/par_ville.py", "Par Villes", "🗾"),
        Page("pages/1_A_propos.py", "A propos", "?")
    ]
)

# Application du style css
formatage_de_la_page("style.css")


# Création de la sidebar
st.sidebar.header("filtre")
option = st.sidebar.selectbox("Département", ("37","45","tous"))



# titre, contexte et logos
contexte = "Cette application a pour objectif d'analyser les associations au sein des départements 37 et 45."
colonne_logo, colonne_titre = st.columns([1,5])
with colonne_logo:
    logo = Image.open("images/photoprofillinkedIn.excalidraw.png")
    logo_reduit = logo.resize([70,50])
    st.image(logo_reduit)
with colonne_titre:
    st.title(":red[Application d'analyse des associations] :bar_chart:")
st.write(contexte)
st.write()


# Code principal

datasetnettoye = charger_les_fichiers()
datasetfiltre = filtrer_dataset_dep(datasetnettoye, option)
datasetactif = filtrer_dataset_actif(datasetfiltre)

KPI(datasetactif)

## Ecriture de blancs pour laisser de la place
for i in range(5):
    st.write("")
    
# graphiques

association_creation_count_by_year = nettoyage_graphiques_creation(datasetfiltre)
association_dissolution_count_by_year = nettoyage_graphiques_dissolution(datasetfiltre)

fig_creation = graph_creation(association_creation_count_by_year, option)
fig_dissolution = graph_dissolution(association_dissolution_count_by_year, option)

st.write('## Graphiques')
st.write('Visualisation des associations crées et dissoutes au cours des 10 dernières années sous forme de courbe.')
affichages_graphiques_lignes(fig_creation, fig_dissolution)

# liste des prospect
dataset_prospets = tri_des_prospets(datasetactif)
import streamlit as st



liste_prospets(dataset_prospets)
boutton_telecharger(dataset_prospets, "tableau_prospects.csv")

# Camembert
datasetjoint = nettoyage_nomemclature(dataset_prospets)

st.markdown(f'<p class="titre" style="text-align: center">Proportion d\'associations par domaines</p>', unsafe_allow_html=True)
st.plotly_chart(camembert(dataset_prospets))

