from flask import Flask, render_template, request, jsonify
import sqlite3
import json
import os

app = Flask(__name__)

# ─── Data ───────────────────────────────────────────────────────────────────

def load_projets():
    """Load projects from projets.json (static/projets.json in production)."""
    json_path = os.path.join(os.path.dirname(__file__), "static", "projets.json")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


CERTIFICATIONS = [
    {
        "name": "Derive Insights from BigQuery Data\nGoogle",
        "logo": "img/google_logo.jpeg"
    },
    {
        "name": "dbt Fundamentals\ndbt Labs",
        "logo": "img/dbtlabs_logo.jpeg"
    },
    {
        "name": "Hands-On Essentials\nSnowflake",
        "logo": "img/snowflake_computing_logo.jpeg"
    },
    {
        "name": "Cloud Computing Fundamentals\nIBM",
        "logo": "img/ibm_logo.jpg"
    },
    {
        "name": "INSIDE LVMH CERTIFICATE\nLVMH",
        "logo": "img/lvmh_logo.jpg"
    },
    {
        "name": "SeveUp App / BIM data visualisation\nSeveUp",
        "logo": "img/seveup_logo.jpg"
    },
]


# ─── Routes ─────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pass
    projets = load_projets()
    return render_template("index.html",
                           projets=projets,
                           certifications=CERTIFICATIONS)


@app.route("/cv")
def resume():
    current_skills = [
        {"name": "Python",     "logo": "python.png"},
        {"name": "SQL",        "logo": "sql.png"},
        {"name": "Power BI",   "logo": "powerbi.png"},
        {"name": "Looker",     "logo": "looker.png"},
        {"name": "Flask",      "logo": "flask.png"},
        {"name": "Postgres",   "logo": "postgres.png"},
        {"name": "Snowflake",  "logo": "snowflake.png"},
        {"name": "GCP",        "logo": "gcp.png"},
        {"name": "Git",        "logo": "git.png"},
    ]
    past_skills = [
        {"name": "Talend",     "logo": "talend.png"},
        {"name": "Docker",     "logo": "docker.png"},
        {"name": "Airflow",    "logo": "airflow.png"},
        {"name": "Oracle",     "logo": "oracle.png"},
        {"name": "Golang",     "logo": "golang.png"},
        {"name": "C",          "logo": "c.png"},
        {"name": "Luigi",      "logo": "luigi.png"},
        {"name": "R",          "logo": "r.png"},
        {"name": "JavaScript", "logo": "js.png"},
        {"name": "Java",       "logo": "java.png"},
        {"name": "PHP",        "logo": "php.png"},
    ]
    return render_template("resume.html",
                           current_skills=current_skills,
                           past_skills=past_skills,
                           certifications=CERTIFICATIONS)


# ─── AgriData Explorer ──────────────────────────────────────────────────────

DB_PATH = os.path.join(os.path.dirname(__file__), "static", "faostat.db")


@app.route("/projets/agridataexplorer")
def agridataexplorer():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT DISTINCT Country FROM observations ORDER BY Country")
    countries = [r["Country"] for r in cur.fetchall()]

    cur.execute("SELECT DISTINCT Item FROM observations ORDER BY Item")
    items = [r["Item"] for r in cur.fetchall()]

    cur.execute("SELECT MIN(Year) AS min_year, MAX(Year) AS max_year FROM observations")
    years_row = cur.fetchone()
    min_year, max_year = years_row["min_year"], years_row["max_year"]

    conn.close()

    return render_template(
        "agri_data.html",
        countries=countries,
        items=items,
        min_year=min_year,
        max_year=max_year,
        selected_country=countries[0],
        selected_item=items[0],
        start_year=min_year,
        end_year=max_year,
    )


@app.route("/get_data", methods=["POST"])
def get_data():
    req = request.get_json()
    country    = req.get("country")
    item       = req.get("item")
    start_year = req.get("start_year")
    end_year   = req.get("end_year")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT Year, SUM(Value) AS production
        FROM observations
        WHERE Country=? AND Item=? AND Element='Production' AND Value IS NOT NULL
          AND Year BETWEEN ? AND ?
        GROUP BY Year ORDER BY Year
    """, (country, item, start_year, end_year))
    prod_rows = cur.fetchall()

    cur.execute("""
        SELECT Year, SUM(Value)/COUNT(Value) AS yield
        FROM observations
        WHERE Country=? AND Item=? AND Element='Yield' AND Value IS NOT NULL
          AND Year BETWEEN ? AND ?
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


# ─── Entry point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))        
    
