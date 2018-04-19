import time
from flask import *
import sys
import random as r
import psycopg2
    
#NE PAS MODIFIER LA LIGNE SUIVANTE
app = Flask(__name__)
number = 0
attempts = 0
            
@app.route("/")
def hello():
    return render_template('accueil_template.html')


@app.route("/liste_regions", methods=['GET'])
def liste_regions():
    page="<h2>Liste des régions Françaises :</h2>"
    print("Trying to connect to the database")
    try:
        conn = psycopg2.connect(host='dbserver', dbname='bpinaud', user='lgoudin')
        print("Connected to the database")
        cur = conn.cursor()
        command = "select nom from regions order by nom asc"
        print("Trying to execute command: " + command)
        try:
            cur.execute(command)
            print("Execute OK")
            rows = cur.fetchall()
            print("Fetchall OK")
            regions = rows

            for i in regions:
                page = page + i[0] + "<br/>"
            

        except Exception as e:
            return "Error when running command: " + command + " : " + str(e)
        
    except Exception as e:
        return "Cannot connect to database: " + str(e)
    
    return page

@app.route("/liste_departements_region_request")
def liste_departements_region_request():
    return app.send_static_file("liste_departements_region_form.html")
    
@app.route("/liste_departements_region", methods=['POST'])
def liste_departements_region():
    region = request.form["region"].upper().strip()
    page="<h2>Liste des départements de " + request.form["region"].strip().capitalize() + " : </h2>"
    print("Trying to connect to the database")
    try:
        conn = psycopg2.connect(host='dbserver', dbname='bpinaud', user='lgoudin')
        print("Connected to the database")
        cur = conn.cursor()
        command = "select d.nom, d.num from regions r, departements d where r.num=d.region and r.nommaj=\'" + region + "\' order by d.nom asc"
        print("Trying to execute command: " + command)
        try:
            cur.execute(command)
            print("Execute OK")
            rows = cur.fetchall()
            print("Fetchall OK")
            for i in rows:
                page = page + i[1] + "  " + i[0] + "<br/>"

        except Exception as e:
            return "Error when running command: " + command + " : " + str(e)

    except Exception as e:
        return "Cannot connect to database: " + str(e)
        
    return page

@app.route("/liste_departements_annee_diplome_request")
def liste_departements_annee_diplome_request():
    return app.send_static_file("liste_departements_annee_diplome_form.html")

@app.route("/liste_departements_annee_diplome", methods=['POST'])
def liste_departements_annee_diplome():
    page=""
    return page

#NE SURTOUT PAS MODIFIER     
if __name__ == "__main__":
    app.run(debug=True)
    
   
