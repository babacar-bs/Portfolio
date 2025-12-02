from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import sqlite3 
import os


app = Flask(__name__)
# app.config["MYSQL_HOST"] = "localhost"
# app.config["MYSQL_USER"] = "root"
# app.config["MYSQL_PASSWORD"] = "root"
# app.config["MYSQL_DB"] = "portfolio"
# mysql = MySQL(app)


@app.route('/', methods=['POST', 'GET'])
def index(): 
    if request.method == 'POST':
        pass
    else:
        return render_template('index.html')


# @app.route('/resume')
# def resume(): 
#         return render_template('resume.html')
# @app.route('/resume')
# def resume():
#     skills = [
#         {"name": "Python", "logo": "uca.png"},
#         {"name": "Java", "logo": "uca.png"},
#         {"name": "SQL", "logo": "uca.png"},
#         {"name": "Flask", "logo": "uca.png"},
#         {"name": "Scikit-learn", "logo": "uca.png"},
#         {"name": "Power BI", "logo": "uca.png"},
#         {"name": "IA - OpenClassrooms", "logo": "uca.png"},
#         {"name": "Google Data Analytics", "logo": "uca.png"}
#     ]
#     return render_template('resume.html', skills=skills)
@app.route('/cv')
def resume():
    current_skills = [
        {"name": "Python", "logo": "python.png"},
        {"name": "SQL", "logo": "sql.png"},
        {"name": "Power BI", "logo": "powerbi.png"},
       # {"name": "Excel", "logo": "excel.png"},
        {"name": "Looker", "logo": "looker.png"},
        {"name": "Flask", "logo": "flask.png"},
        {"name": "Postgres", "logo": "postgres.png"},
        {"name": "Snowflake", "logo": "snowflake.png"},
        #{"name": "Sqlite", "logo": "sqlite.png"},
        {"name": "GCP", "logo": "gcp.png"},
        {"name": "Git", "logo": "git.png"},
        #{"name": "Github", "logo": "github.png"},
        
    ]

    past_skills = [
        {"name": "Talend", "logo": "talend.png"},
        {"name": "Docker", "logo": "docker.png"},
        {"name":"Airflow", "logo": "airflow.png"},
        {"name": "Oracle", "logo": "oracle.png"},
        {"name": "Golang", "logo": "golang.png"},
        {"name": "C", "logo": "c.png"},
        {"name":"Luigi", "logo": "luigi.png"},
        {"name": "R", "logo": "r.png"},
        {"name": "JavaScript", "logo": "js.png"},
        {"name": "Java", "logo": "java.png"},
        {"name": "PHP", "logo": "php.png"},


    ]

    certifications = [
        {"name": "Derive Insights from BigQuery Data \n Google", "logo": "img/google_logo.jpeg"},
        {"name": "dbt Fundamentals \n dbt Labs", "logo": "img/dbtlabs_logo.jpeg"},
        {"name": "Hands-On Essentials \n Snowflake", "logo": "img/snowflake_computing_logo.jpeg"},
        {"name": "Cloud Computing Fundamentals \n IBM", "logo": "img/ibm_logo.jpg"},
        {"name": "INSIDE LVMH CERTIFICATE \n LVMH", "logo": "img/lvmh_logo.jpg"},
        {"name": "SeveUp App / BIM data visualisation \n SeveUp", "logo": "img/seveup_logo.jpg"}
    ]

    return render_template('resume.html',
                           current_skills=current_skills,
                           past_skills=past_skills,
                           certifications=certifications)


# @app.route('/projets')
# def projets():
#     projets = [
#         {
#             "titre": "Site web de location de voitures",
#             "associe": "Ecole Supérieure Polytechnique de Dakar",
#             "description": "Conception d'un site web pour gérer un parc automobile (modélisation et développement).",
#             "competences": "Java · J2EE · HTML · CSS · JavaScript · UML",
#             "image": "voiture.png"
#         },
#         {
#             "titre": "Site pour gérer des concours d'entrée",
#             "associe": "Ecole Supérieure Polytechnique de Dakar",
#             "description": "Faciliter les concours avec interface pour élèves et écoles (gestion, épreuves, résultats).",
#             "competences": "HTML · CSS · Bootstrap · JavaScript · AJAX · jQuery · PHP · MySQL",
#             "image": "concours.png"
#         },
#         {
#             "titre": "Jeu 2048",
#             "associe": "Université Clermont Auvergne",
#             "description": "Implémentation du jeu 2048 en C avec SDL.",
#             "competences": "C · SDL",
#             "image": "2048.png"
#         },
#         {
#             "titre": "Protocole de communication graphique",
#             "associe": "Université Clermont Auvergne",
#             "description": "Protocole inspiré du QR-code avec correction d'erreur, supporte des messages avec logo.",
#             "competences": "Python · Pillow",
#             "image": "qr.png"
#         },
#         {
#             "titre": "Analyse de sentiments",
#             "associe": "Université de Lorraine / LCOMS",
#             "description": "Approche incrémentale d’analyse des sentiments pour AIRxTOUCH. Études, conception, déploiement.",
#             "competences": "NLTK · joblib · Scikit-learn · Flask · JavaScript",
#             "image": "sentiments.png"
#         }
#     ]
#     return render_template('projets.html', projets=projets)

@app.route('/projets')
def projet():
    projets_data = [
        {
            "id": "automatisation_permis",
            "titre": "Automatisation de la vérification des permis de construire",
            "associe": "SeveUp et A26 Architecture",
            "description": (
                "Ce projet visait à expérimenter l'automatisation du processus de vérification des permis de construire, "
                "qui pouvait auparavant prendre jusqu’à 10 mois. Grâce à l’utilisation de SeveUp, "
                "d’un programme développé sur mesure, et de Power BI pour la visualisation, nous avons réduit le temps "
                "de traitement à seulement quelques minutes. Cette initiative modernise et fluidifie les processus administratifs, "
                "tout en renforçant la précision et l'efficacité des démarches.\n"
                "L'automatisation permet de vérifier des critères réglementaires à grande échelle, assurant ainsi "
                "rapidité, fiabilité et traçabilité dans l'analyse des dossiers."
            ),
            "competences": "Power BI · SeveUp · Python · Automatisation . IFC",
            "medias": [
                {"type": "image", "src": "img/Projets/verif_permis1.png"},
                {"type": "image", "src": "img/Projets/verif_permis2.png"}
            ],
            "lien": "https://app.powerbi.com/view?r=eyJrIjoiNTU0NThkMWItNTRhMS00YzM0LTgzNmUtYmRmZmRhYTNkNTlmIiwidCI6IjE1ODcxNmNmLTQ2YjktNDhjYS04YzQ5LWM3YmI2N2U1NzVmMyIsImMiOjh9"
        },

        {
            "id": "logistics-data-pipeline-bigquery-looker",
            "titre": "Pipeline Data Logistique sur GCP",
            "description": (
                  "Conception et déploiement d’un pipeline complet de traitement des données logistiques selon l'architecture en medaillon\n"
                    "Les fichiers CSV bruts sont stockés dans Google Cloud Storage transformés, "
                    "chargés dans BigQuery, puis raffinés et normalisés, "
                    "avant d’être modélisés en tables dimensionnelles et faits.\n"
                    "Les données sont exposées via une vue sécurisée dédiée, permettant une visualisation performante dans Looker. "
                    "Les KPI clés suivent les volumes de commandes, les ventes, les délais de livraison, ainsi que l’analyse des meilleurs clients.\n "
                    "L’architecture intègre les bonnes pratiques de sécurité et de gestion des accès IAM, garantissant un contrôle strict sur les dashboards."
            ),
            "competences": "Python · GCP · Cloud Storage · BigQuery · SQL · Data Modeling · Looker · IAM · Logistique",
            "medias": [
                {"type": "image", "src": "img/Projets/logi1.png"},
                {"type": "image", "src": "img/Projets/logi2.png"}
                
            ],
        },

        {
            "id": "bigdata_hadoop",
            "titre": "Experience avec Spark et Power BI",
            "associe": "Université de Lorraine",
            "description": (
                "Le but de ce projet était de reproduire et améliorer l'expérience issue de l’article "
                "« Big Data Intelligence in Logistics Based on Hadoop and MapReduce ».\n"
                "Le projet utilise le dataset public des vitesses relevées par les voitures radars en France (2023), "
                "avec pour objectif l’analyse de comportements routiers grace au big data."
            ),
            "competences": "Big Data · Spark · Power BI",
            "medias": [
                {"type": "image", "src": "img/Projets/p1-1.png"},
                {"type": "image", "src": "img/Projets/p1-2.png"},
                {"type": "image", "src": "img/Projets/p1-3.png"}
            ],
            "lien": "https://app.powerbi.com/view?r=eyJrIjoiM2Q0ZWQ1NTQtZTRlNi00ZDZkLWFhYjMtZTczZGQ0NzZhZTJhIiwidCI6IjE1ODcxNmNmLTQ2YjktNDhjYS04YzQ5LWM3YmI2N2U1NzVmMyIsImMiOjh9"  # Remplace par l’URL réelle si tu l’as
        },



        {
            "id": "optimisation_tournee_vehicules",
            "titre": "Optimisation des tournées logistiques multi-compartiments",
            "associe": "Université de Lorraine",
            "description": (
                 "Dans ce projet, j’ai travaillé en équipe sur l’optimisation des tournées de véhicules multi-compartiments pour un prestataire logistique (3PL),"
                 "afin d’acheminer différents types de produits (surgelés, frais, ambiants) vers les clients d’un magasin sur une journée.\n"
                 "Le problème a été modélisé en PLNE sous IBM CPLEX, puis complété par une heuristique ALNS pour "
                 "traiter les instances trop volumineuses.\nLes solutions obtenues sont proches de l’optimum, "
                 "respectent les contraintes opérationnelles et permettent une réduction significative des coûts, "
                 "y compris lorsque la méthode exacte atteint ses limites."
            ),
            "competences": "Logistique · Optimisation · Python · ALNS · IBM CPLEX",
            "medias": [
                {"type": "image", "src": "img/Projets/alns1.png"},
                {"type": "image", "src": "img/Projets/alns2.png"},
                {"type": "image", "src": "img/Projets/alns3.png"},
                {"type": "image", "src": "img/Projets/alns4.png"},
                {"type": "image", "src": "img/Projets/alns5.png"},
                {"type": "image", "src": "img/Projets/alns6.png"},
                {"type": "image", "src": "img/Projets/alns7.png"},
                {"type": "image", "src": "img/Projets/alns8.png"},
                
            ],
        },



        
        {
    "id": "accent-audio-classification",
    "titre": "Classification d’accents anglais (Indien, Britannique, Américain)",
    "description": (
        "Développement d’un modèle de classification des accents anglophones à partir de fichiers audio "
        "collectés sur YouTube (podcasts, conférences, livres audio). Les étapes clés incluent le prétraitement "
        "des fichiers (nettoyage, conversion, découpage), l’extraction de caractéristiques audio (MFCC, "
        "Chroma, Spectral Contrast, Tonnetz) et l’entraînement de plusieurs modèles d’apprentissage supervisé "
        "(Random Forest, CART, AdaBoost, XGBoost).\n\n"
        "Le meilleur modèle (Random Forest), parmi ceux choisis, atteint une précision de 78% pour distinguer les accents américain, "
        "britannique et indien."
    ),
    "competences": "Python · Scikit-learn · Librosa · Machine Learning ",
    "medias": [
        {"type": "image", "src": "img/Projets/a1.png"},
        {"type": "image", "src": "img/Projets/a2.png"},
        {"type": "image", "src": "img/Projets/a3.png"},
        {"type": "image", "src": "img/Projets/a4.png"},
        {"type": "image", "src": "img/Projets/a5.png"},
    ],
},
{
    "id": "sentiment-analysis-incremental",
    "titre": "Analyse de sentiments avec apprentissage incrémental",
    "associe": "Université de Lorraine – Projet de recherche",
    "description": (
        "Dans un contexte de croissance exponentielle des contenus en ligne, ce projet vise à proposer "
        "une approche d’analyse des sentiments évolutive, capable de s’adapter à un flux continu de données. "
        "Nous avons d’abord implémenté des modèles (SVM, Naive Bayes, etc.), puis développé un outil "
        "d’apprentissage incrémental permettant la mise à jour continue du modèle avec de nouvelles données textuelles.\n\n"
        "Notre système est déployé via une interface web interactive et exploitable sur dispositifs tactiles comme l’AIRxTOUCH. "
        "L'utilisateur peut interagir en prédictant ou corrigeant un tweet, ce qui alimente l’apprentissage en temps réel. "
        "Les résultats expérimentaux montrent de bonnes performances, notamment avec le modèle SVM.\n\n"
        "Ce travail mêle NLP, machine learning, vectorisation et apprentissage incrémental."
    ),
    "competences": "Python · NLP · SVM · Scikit-learn · Apprentissage incrémental · Interfaces tactiles",
    "medias": [
        {"type": "image", "src": "img/Projets/as1.png"},
        {"type": "image", "src": "img/Projets/as2.png"},
        {"type": "image", "src": "img/Projets/as3.png"},
        {"type": "image", "src": "img/Projets/as4.png"},
    ],
},


        {
            "id": "dashboard-healthcare",
            "titre": "Dashboard Power BI – Secteur Santé",
            "associe": "Formation Power BI – Projet personnel",
            "description": (
                "Réalisation d’un tableau de bord interactif dans le domaine de la santé, inspiré de la vidéo "
                "« Elevate Your Dashboard Design » (YouTube).\n\n"
                "Ce projet explore la performance financière d’un centre de santé ainsi que les performances des prestataires, "
                "à l’aide d’indicateurs clés et de visualisations avancées dans Power BI.\n"
                "Ce projet m’a permis de consolider mes compétences en modélisation de données et storytelling visuel."
                "Il m'a permis la pratique de Power Query, DAX et PowerPoint pour la conception graphique."

            ),
            "competences": "Reporting · Power BI · DAX · Power Query ",
            "medias": [
                {"type": "image", "src": "img/Projets/h1-1.png"},
            ],
            "lien":"https://app.powerbi.com/view?r=eyJrIjoiYzFkNDE2ZTEtMzc5Yy00MzBkLWEyMjYtZjFhMGQ1ODdkYmQ1IiwidCI6IjE1ODcxNmNmLTQ2YjktNDhjYS04YzQ5LWM3YmI2N2U1NzVmMyIsImMiOjh9"
        },
        {
    "id": "dgpre-eau",
    "titre": "Suivi intelligent des ressources en eau au Sénégal",
    "associe": "ProSE SARL / DGPRE",
    "description": (
        "Dans le cadre de mon stage de 2e année de DUT à ProSE SARL, mon binôme et moi avons développé une application "
        "permettant à la DGPRE de suivre en temps réel les niveaux et débits d’eau des stations hydrologiques "
        "du Sénégal. L’objectif était de remplacer les campagnes manuelles coûteuses par un système connecté "
        "basé sur le dispositif LevelSender + Levelogger, capable de télétransmettre les données vers une base "
        "de données et de générer des alertes automatiques en cas d’anomalie. Le système inclut une cartographie interactive "
        "des points de mesure, un tableau de bord de suivi en temps réel et un module CRUD pour la gestion des stations."
    ),
    "competences": "Python · Flask · JavaScript · Leaflet.js · Highcharts · SQLite · UML · Dashboard · Télémetrie",
    "medias": [
        {"type": "image", "src": "img/Projets/s2.png"},
        {"type": "image", "src": "img/Projets/s3.png"},
        {"type": "image", "src": "img/Projets/s1.png"},
        {"type": "image", "src": "img/Projets/s4.png"},
        {"type": "image", "src": "img/Projets/s5.png"},
        {"type": "image", "src": "img/Projets/s6.png"},
        {"type": "image", "src": "img/Projets/s7.png"}

        
    ],
}



        # Tu peux ajouter d'autres projets ici...
    ]
    return render_template("projet.html", projets=projets_data)

#MAIN
if __name__ == "__main__":
    # app.run(debug=True,port=5005)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))        
