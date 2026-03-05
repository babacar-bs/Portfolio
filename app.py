import json
import os
import sqlite3

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# ─────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────

def load_projets():
    """Charge les projets depuis le fichier JSON."""
    path = os.path.join(os.path.dirname(__file__), "projets.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


DB_PATH = os.path.join(os.path.dirname(__file__), "static", "faostat.db")


def get_db():
    """Retourne une connexion SQLite avec row_factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ─────────────────────────────────────────
# CV data (centralisé ici, facile à modifier)
# ─────────────────────────────────────────

CURRENT_SKILLS = [
    {"name": "Python",    "logo": "python.png"},
    {"name": "SQL",       "logo": "sql.png"},
    {"name": "Power BI",  "logo": "powerbi.png"},
    {"name": "Looker",    "logo": "looker.png"},
    {"name": "Flask",     "logo": "flask.png"},
    {"name": "Postgres",  "logo": "postgres.png"},
    {"name": "Snowflake", "logo": "snowflake.png"},
    {"name": "GCP",       "logo": "gcp.png"},
    {"name": "Git",       "logo": "git.png"},
]

PAST_SKILLS = [
    {"name": "Talend",      "logo": "talend.png"},
    {"name": "Docker",      "logo": "docker.png"},
    {"name": "Airflow",     "logo": "airflow.png"},
    {"name": "Oracle",      "logo": "oracle.png"},
    {"name": "Golang",      "logo": "golang.png"},
    {"name": "C",           "logo": "c.png"},
    {"name": "Luigi",       "logo": "luigi.png"},
    {"name": "R",           "logo": "r.png"},
    {"name": "JavaScript",  "logo": "js.png"},
    {"name": "Java",        "logo": "java.png"},
    {"name": "PHP",         "logo": "php.png"},
]

CERTIFICATIONS = [
    {"name": "Derive Insights from BigQuery Data – Google",     "logo": "img/google_logo.jpeg"},
    {"name": "dbt Fundamentals – dbt Labs",                     "logo": "img/dbtlabs_logo.jpeg"},
    {"name": "Hands-On Essentials – Snowflake",                 "logo": "img/snowflake_computing_logo.jpeg"},
    {"name": "Cloud Computing Fundamentals – IBM",              "logo": "img/ibm_logo.jpg"},
    {"name": "INSIDE LVMH CERTIFICATE – LVMH",                  "logo": "img/lvmh_logo.jpg"},
    {"name": "SeveUp App / BIM data visualisation – SeveUp",    "logo": "img/seveup_logo.jpg"},
]


# ─────────────────────────────────────────
# Routes
# ─────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cv")
def resume():
    return render_template(
        "resume.html",
        current_skills=CURRENT_SKILLS,
        past_skills=PAST_SKILLS,
        certifications=CERTIFICATIONS,
    )


@app.route("/projets")
def projets():
    return render_template("projet.html", projets=load_projets())


# ─────────────────────────────────────────
# AgriData Explorer
# ─────────────────────────────────────────

@app.route("/projets/agridataexplorer")
def agridataexplorer():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT DISTINCT Country FROM observations ORDER BY Country")
    countries = [r["Country"] for r in cur.fetchall()]

    cur.execute("SELECT DISTINCT Item FROM observations ORDER BY Item")
    items = [r["Item"] for r in cur.fetchall()]

    cur.execute("SELECT MIN(Year) as min_year, MAX(Year) as max_year FROM observations")
    row = cur.fetchone()
    conn.close()

    return render_template(
        "agri_data.html",
        countries=countries,
        items=items,
        min_year=row["min_year"],
        max_year=row["max_year"],
        selected_country=countries[0],
        selected_item=items[0],
        start_year=row["min_year"],
        end_year=row["max_year"],
    )


@app.route("/get_data", methods=["POST"])
def get_data():
    req = request.get_json()
    country = req.get("country")
    item = req.get("item")
    start_year = req.get("start_year")
    end_year = req.get("end_year")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT Year, SUM(Value) AS production
        FROM observations
        WHERE Country = ? AND Item = ? AND Element = 'Production'
          AND Value IS NOT NULL AND Year BETWEEN ? AND ?
        GROUP BY Year ORDER BY Year
    """, (country, item, start_year, end_year))
    prod_rows = cur.fetchall()

    cur.execute("""
        SELECT Year, AVG(Value) AS yield
        FROM observations
        WHERE Country = ? AND Item = ? AND Element = 'Yield'
          AND Value IS NOT NULL AND Year BETWEEN ? AND ?
        GROUP BY Year ORDER BY Year
    """, (country, item, start_year, end_year))
    yield_rows = cur.fetchall()
    conn.close()

    prod_data  = [{"Year": r["Year"], "value": r["production"]} for r in prod_rows]
    yield_data = [{"Year": r["Year"], "value": r["yield"]}      for r in yield_rows]

    message = (
        f"Aucune donnée disponible pour {item} au {country} entre {start_year} et {end_year}."
        if not prod_data and not yield_data else ""
    )

    return jsonify({"production": prod_data, "yield": yield_data, "message": message})


# ─────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────

if __name__ == "__main__":
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))        
    
