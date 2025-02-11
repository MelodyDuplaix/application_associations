# Import des bibliothèques
import streamlit as st
from bibliotheque.lib import  *


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

texte = """
# À propos de l'Application\n

## Introduction\n
Bienvenue sur cette application d'analyse des associations dans le 37 et le 45 ! Cette application a été créée par Melody, une étudiante en formation Data Analyste, dans le cadre de son parcours d'apprentissage. L'objectif principal de cette application est de fournir des informations sur les associations en France en utilisant des données publiques gouvernementales.

## Source des Données\n
Les données utilisées dans cette application proviennent d'une source publique gouvernementale du Répertoire National des Associations . Ces données sont régulièrement mises à jour par le gouvernement pour garantir leur exactitude. Vous pouvez consulter ces données directement sur https://www.data.gouv.fr/fr/datasets/repertoire-national-des-associations/  pour plus d'informations.

## Fonctionnalités de l'Application\n

### Répertoire des Associations\n
- L'application offre un répertoire complet des associations dans le 37 et le 45, regroupées par villes.

### Visualisation Cartographique\n
- Une carte interactive est disponible pour afficher l'emplacement des associations sur une carte de la France.\n
- cette carte est filtrée par domaine d'activités et région.

### Statistiques\n

- L'application fournit des statistiques détaillées sur le nombre d'associations par domaine d'activité.\n
- Elle permet de connaître le nombre d'associations avec services payant ou avec site web\n
- Des graphiques permettent de connaître l'évolution de la création et de la dissolution d'associations.\n
- Vous pouvez obtenir des informations précieuses sur la répartition des associations en France.

## Motivation\n
Cette application a été créée dans le cadre de ma formation en tant que Data Analyste. Elle vise à mettre en pratique les compétences acquises tout au long de mon parcours d'apprentissage. Mon objectif était de créer une application utile et informative pour le public tout en explorant des données réelles.

## Contact\n
Si vous avez des questions, des commentaires ou des suggestions concernant cette application, n'hésitez pas à me contacter sur mon profil LinkedIn : https://www.linkedin.com/in/melody-duplaix-391672265.

## Remerciements\n
Je tiens à exprimer ma gratitude envers le CEFIM pour la formation et son soutien tout au long de mon parcours.

Merci de votre visite sur l'application d'analyse des associations !
"""

st.markdown(texte)
