import streamlit as st
import pandas as pd
import re
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



# Définitions des fonctions
def formatage_de_la_page(fichier_css):
    with open(fichier_css) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def charger_le_fichier():
    """
    Nom : charger_le_fichier
    Paramètres : 0
    Traitement : charger un fichier au format csv grâce à file_uploader
    Retour : retourne le fichier csv dans la variable fichier_charge
    """
    fichier_charge = st.file_uploader("Choisissez un fichier csv", type=["csv"])
    if fichier_charge:
        st.write(f"Vous venez de charger le fichier : {fichier_charge.name}")
    return(fichier_charge)

def creer_le_jeu_de_donnes(f_fichier_donnee):
    """
    Nom : creer_le_jeu_de_donnes
    Paramètres : 1 - Type : chaine de caractère
    Traitement : charger un dataset à partir d'un fichier csv
    Retour : retourne le dataset dans la variable dataset
    """
    dataset = pd.read_csv(f_fichier_donnee,encoding="latin", sep=";", decimal=",", thousands=" ")
    return(dataset)

def rechercher_par_code_postal(f_dataset):
    """
    Nom : rechercher_par_code_postal
    Paramètres : 1 - Type : dataset
    Traitement : affiche un input permettant à l'utilisateur de rentrer un code postal, vérifie la forme du code postal, filtre le dataset sur ce code postal, et affiche le dataset filtré
    Retour : retourne un input, un texte et un dataset dans la variable dataset
    """
    pattern = re.compile(r'\d{5}')
    text_input = st.text_input("Taper le code postal :", placeholder="Code Postal", max_chars=5, help="Veuillez entrer le code postal pour filtrer les associations dans ce code postal.")
    if text_input and not pattern.search(text_input):
        st.write("Ce code postal n'est pas valide.")
        
    f_dataset["adrs_codepostal"] = f_dataset["adrs_codepostal"].apply(str)
    if text_input and pattern.search(text_input):
        st.write("Liste des associations du : " + text_input)
        dataset_codepostal = f_dataset[f_dataset["adrs_codepostal"]==text_input]
        return(dataset_codepostal)



# ---------- Définition des fonctions --------------- #

def charger_les_fichiers():
    """
    Nom : charger_les_fichiers
    Paramètres : 0
    Traitement : charge les fichiers 37 et 45, les nettoient et les combinent
    Retour : un dataFrame
    """
    # Chargement du fichier
    dataset37 = pd.read_csv("data/projet_asso37.geocoded.csv", encoding="latin")
    dataset45 = pd.read_csv("data/projet_asso45.geocoded.csv", encoding="latin")
    # Nettoyage du fichier
    ## Garder les bonnes colonnes
    dataset37 = dataset37[["id", "siret", "date_publi","date_disso","nom_asso","nom_asso_abrege","objet_social1","objet_social2","adresse","codepostal","commune","siteweb","autorisation_web","etat","latitude","longitude"]]
    dataset45 = dataset45[["id", "siret", "date_publi","date_disso","nom_asso","nom_asso_abrege","objet_social1","objet_social2","adresse","codepostal","commune","siteweb","autorisation_web","etat","latitude","longitude"]]
    # Concatenation des 2 datasets
    dataset = pd.concat([dataset37, dataset45])
    ## copie du fichier
    datasetnettoye = dataset.copy()
    datasetnettoye["siret"] = datasetnettoye["siret"].astype(str)
    datasetnettoye["objet_social1"] = datasetnettoye["objet_social1"].astype(str)
    datasetnettoye["objet_social2"] = datasetnettoye["objet_social2"].astype(str)
    datasetnettoye["date_publi"] = pd.to_datetime(datasetnettoye['date_publi'], format="mixed")
    datasetnettoye["date_disso"] = pd.to_datetime(datasetnettoye['date_disso'], format="mixed")
    datasetnettoye["codepostal"] = datasetnettoye["codepostal"].astype(str)
    return(datasetnettoye)

def filtrer_dataset_dep(f_dataset_dep, option):
    """
    Nom : filtrer_dataset_dep
    Paramètres : 2, 1 - dataFrame, 2 - string
    Traitement : filtre un dataFrame sur une string
    Retour : un dataFrame
    """
    ## Filtrer les données sur le département
    if option == "tous":
        datasetfiltre = f_dataset_dep
    else:
        datasetfiltre = f_dataset_dep[f_dataset_dep["codepostal"].str.startswith(option)]
    return(datasetfiltre)

def filtrer_dataset_actif(f_dataset_actif_ou_non):
    """
    Nom : filtrer_dataset_actif
    Paramètres : 1, dataFrame
    Traitement : filtre un dataFrame sur les etat = Actif
    Retour : un dataFrame
    """
    ## Filtrer les données sur les actives
    datasetfiltre = f_dataset_actif_ou_non[f_dataset_actif_ou_non["etat"]=="A"]
    return(datasetfiltre)


def KPI(f_dataset_pour_kpi):
    """
    Nom : KPI
    Paramètres : 1, dataFrame
    Traitement : créer 3 KPI sur les nombres d'associations total, avec services payant, et avec site web
    Retour : un dataFrame
    """
    ## Calcul des KPIs
    nb_asso = f_dataset_pour_kpi["nom_asso"].unique().size
    dataset_prestations = f_dataset_pour_kpi[f_dataset_pour_kpi["siret"]!="nan"]
    nb_assos_services = dataset_prestations["siret"].unique().size
    dataset_siteweb = f_dataset_pour_kpi[f_dataset_pour_kpi["siteweb"]!="nan"]
    nb_assos_site = dataset_siteweb["siteweb"].unique().size
    # KPI
    colonne_global, colonne_services, colonne_site = st.columns(3)
    with colonne_global:
        st.markdown('<p class="kpi">Nombres d\'associations<br>total</p>', unsafe_allow_html=True)
        st.write(nb_asso)
    with colonne_services:
        st.markdown('<p class="kpi">Nombre d\'associations<br>avec services payant</p>', unsafe_allow_html=True)
        st.write(nb_assos_services)
    with colonne_site:
        st.markdown('<p class="kpi">Nombres d\'associations<br>avec site web</p>', unsafe_allow_html=True)
        st.write(nb_assos_site)
    return()

def annee_filtre():
    """
    Nom : annee_filtre
    Paramètres : 0
    Traitement : calcule l'année il y a 10 ans
    Retour : un nombre
    """
    current_year = pd.Timestamp.now().year
    ten_years_ago = current_year - 10
    return(ten_years_ago)

def nettoyage_graphiques_creation(f_dataset_creation):
    """
    Nom : nettoyage_graphiques_creation
    Paramètres : 1, dataFrame
    Traitement : filtre  et groupe le dataFrame sur les 10 dernières années
    Retour : un dataFrame
    """
    ### traitement pour la création
    data_creation_filtre_10_dernieres_annees = f_dataset_creation[f_dataset_creation['date_publi'].dt.year >= annee_filtre()]
    ### Groupez les données par année et comptez le nombre d'associations créées chaque année :
    association_creation_count_by_year = data_creation_filtre_10_dernieres_annees.groupby(data_creation_filtre_10_dernieres_annees['date_publi'].dt.year)['id'].count()
    return(association_creation_count_by_year)

def nettoyage_graphiques_dissolution(f_dataset_creation):
    """
    Nom : nettoyage_graphiques_dissolution
    Paramètres : 1, dataFrame
    Traitement : filtre et groupe le dataFrame sur les 10 dernières années
    Retour : un dataFrame
    """
    ### traitement pour la création
    data_creation_filtre_10_dernieres_annees = f_dataset_creation[f_dataset_creation['date_disso'].dt.year >= annee_filtre()]
    ### Groupez les données par année et comptez le nombre d'associations créées chaque année :
    association_creation_count_by_year = data_creation_filtre_10_dernieres_annees.groupby(data_creation_filtre_10_dernieres_annees['date_disso'].dt.year)['id'].count()
    return(association_creation_count_by_year)


def graph_creation(f_dataset_graph_creation, option):
    """
    Nom : graph_creation
    Paramètres : 1, dataFrame
    Traitement : crée un graphique de l'évolution des créations
    Retour : un graphique
    """
    fig_creation = px.line(
    x=f_dataset_graph_creation.index,
    y=f_dataset_graph_creation.values,
    labels={'x': 'Année', 'y': 'Nombre d\'associations créées'}
    )
    # Personnalisez l'axe y pour avoir une plage de 0 à 650
    if option == "tous":
        fig_creation.update_yaxes(range=[0, 1400])
    else:
        fig_creation.update_yaxes(range=[0, 700])
    # Personnalisez l'axe x pour avoir toutes las années affichées
    fig_creation.update_layout(xaxis_dtick=1)
    return(fig_creation)

def graph_dissolution(f_dataset_graph_dissolution, option):
    """
    Nom : graph_dissolution
    Paramètres : 1, dataFrame
    Traitement : crée un graphique de l'évolution des dissolutions
    Retour : un graphique
    """
    fig_dissolution = px.line(
    x=f_dataset_graph_dissolution.index,
    y=f_dataset_graph_dissolution.values,
    labels={'x': 'Année', 'y': 'Nombre d\'associations dissoutes'}
    )
    # Personnalisez l'axe y pour avoir une plage de 0 à 650
    if option == "tous":
        fig_dissolution.update_yaxes(range=[0, 1400])
    else:
        fig_dissolution.update_yaxes(range=[0, 700])
    # Personnalisez l'axe x pour avoir toutes las années affichées
    fig_dissolution.update_layout(xaxis_dtick=1)
    return(fig_dissolution)

def affichages_graphiques_lignes(f_graph_creation, f_graph_dissolution):
    """
    Nom : affichages_graphiques_lignes
    Paramètres : 2, 1-graphique-creation,  2-graphique-dissolution
    Traitement : affiche les 2 graphiques l'un à coté de l'autre
    Retour : un affichage
    """
    colonne_creation, colonne_dissolution = st.columns(2)
    with colonne_creation:
        st.markdown(f'<p class="titre">Evolution de la création d\'associations</p>', unsafe_allow_html=True)
        st.plotly_chart(f_graph_creation, use_container_width= True)
    with colonne_dissolution:
        st.markdown(f'<p class="titre">Evolution de la dissolution d\'associations</p>', unsafe_allow_html=True)
        st.plotly_chart(f_graph_dissolution, use_container_width= True)

def tri_des_prospets(f_dataset_associations_potentielles):
    """
    Nom : tri_des_prospets
    Paramètres : 1 dataFrame
    Traitement : filtre le dataFrame sur les prospets
    Retour : un dataFrame
    """
    dataset_prospets = f_dataset_associations_potentielles[f_dataset_associations_potentielles["autorisation_web"]==1]
    return(dataset_prospets)

def liste_prospets(f_dataset_prospect):
    """
    Nom : liste_prospets
    Paramètres : 1 dataFrame
    Traitement : affiche le dataframe
    Retour : un affichage
    """
    st.markdown('<p class="titre" style="text-align: center">Liste des associations pertinentes</p>', unsafe_allow_html=True)
    st.write(f_dataset_prospect[["nom_asso", "adresse", "siret","codepostal","siteweb"]])


def nettoyage_nomemclature(f_dataset_a_joindre):
    """
    Nom : nettoyage_nomemclature
    Paramètres : 1 dataFrame
    Traitement : joint le dataframe avec les nomenclatures, et nettoit
    Retour : un dataFrame
    """
    ## Lecture et nettoyage du fichier des nomenclatues
    data_nomenclature = pd.read_csv("data/rna-associations-nomenclature-waldec@orleansmetropole.csv", encoding="utf-8", delimiter=";")
    data_nomenclature.rename(columns={"Identifiant objet social":"objet_social1"}, inplace=True)
    data_nomenclature["objet_social1"] = data_nomenclature["objet_social1"].astype(str)

    ## jointure des fichiers
    datasetjoint = f_dataset_a_joindre.merge(data_nomenclature, on="objet_social1", how="left")

    ## création d'une colonne avec les domaines d'activités autres fusionnées
    liste_autres = []
    tableau = pd.DataFrame(datasetjoint["Libellé objet social parent"].value_counts()/datasetjoint["Identifiant objet social parent"].count())
    liste = tableau[tableau['count']<0.02]
    liste = liste.reset_index()
    for nom in liste["Libellé objet social parent"]:
        liste_autres.append(nom)
    datasetjoint["objet_social"] = datasetjoint["Libellé objet social parent"]
    datasetjoint["objet_social"] = datasetjoint.apply(lambda row: "AUTRES" if row["Libellé objet social parent"] in liste_autres else row["objet_social"], axis=1)
    return(datasetjoint)

def camembert(f_dataset_par_domaines):
    """
    Nom : camembert
    Paramètres : 1 dataFrame
    Traitement : crée un camembert avec un dataframe selon les domaines d'activitées
    Retour : un graphique
    """
    datasetjoint = nettoyage_nomemclature(f_dataset_par_domaines)
    ## creation du dataset pour le camembert
    frequence_domaine = datasetjoint["objet_social"].value_counts().reset_index()
    frequence_domaine.columns = ["objet_social", "nom_asso"]
    ## camembert
    camembert = px.pie(frequence_domaine, names="objet_social", values="nom_asso", color_discrete_sequence=px.colors.sequential.RdBu)
    camembert.update_traces(textinfo='percent+label', textfont_size=10)
    camembert.update_layout(showlegend=False)
    return(camembert)

def enlever_les_na(f_dataset_tout_domaines):
    """
    Nom : filtre_domaine
    Paramètres : 1 dataFrame
    Traitement : crée un filtre possible sur un domaine
    Retour : un string
    """
    datasetfiltre_location = f_dataset_tout_domaines[(f_dataset_tout_domaines["latitude"].notna()) & (f_dataset_tout_domaines["longitude"].notna())]
    dataset_sans_na = datasetfiltre_location[datasetfiltre_location["Libellé objet social parent"].notna()]
    return(dataset_sans_na)

def creation_filtre_domaine(f_dataset_sans_na):
    liste_domaines = f_dataset_sans_na["Libellé objet social parent"].unique().tolist()
    domaine = st.sidebar.selectbox("Domaine d'activité de la carte", options=liste_domaines)
    return(domaine)

def nettoyage_carte(f_dataset_carte, domaine):
    """
    Nom : nettoyage_carte
    Paramètres : 2, 1-dataFrame, 2-string
    Traitement : filtre un dataFrame sur un domaine
    Retour : un dataFrame
    """
    dataset = f_dataset_carte[f_dataset_carte["Libellé objet social parent"]==domaine]
    return(dataset)


def affichage_carte(f_dataset_carte_filtre, domaine):
    """
    Nom : affichage_carte
    Paramètres : 2, 1-dataFrame, 2-string
    Traitement : créer et affiche une carte selon un domaine 
    Retour : un dataFrame
    """
    m = folium.Map(location=[47.38822593648433, 0.6829262540339268], zoom_start=8)
    for i, row in f_dataset_carte_filtre.iterrows():
        nom = row["nom_asso"]
        lat = row["latitude"]
        lon = row["longitude"]
        folium.Marker([lat, lon], tooltip=nom+row["codepostal"]).add_to(m) 
    st.markdown(f'<p class="titre" style="text-align: center">Cartes des associations dans le domaine {domaine}</p>', unsafe_allow_html=True)
    st_data = st_folium(m, width=725)


def convert_df(df):
    return df.to_csv().encode('utf-8')


def boutton_telecharger(dataframe, nom):
    fichier = convert_df(dataframe)
    st.download_button(
        label="Download data as CSV ",
        data=fichier,
        file_name=nom,
        mime='text/csv',
    )
