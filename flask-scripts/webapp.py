# coding=utf-8

import time
from flask import *
import sys
import random as r
import psycopg2
    
#NE PAS MODIFIER LA LIGNE SUIVANTE
app = Flask(__name__)
DATABASE = 'miniproj'
            
@app.route("/")
def hello():
    return render_template('accueil_template.html')


@app.route("/liste_regions", methods=['GET'])
def liste_regions():
    page = '<h2>Liste des regions Francaises :</h2>'
    regions = query_db_local(DATABASE, 'select nom from regions')
    #regions = query_db('dbserver', 'bpinaud', 'lgoudin', 'select nom from regions')
    print(regions)
    for i in regions:
        page = page + i[0] + '<br>'
    return page

@app.route("/liste_departements_region_request")
def liste_departements_region_request():
    return app.send_static_file("liste_departements_region_form.html")
    
@app.route("/liste_departements_region", methods=['POST'])
def liste_departements_region():
    region = request.form["region"].upper().strip()
    page="<h2>Liste des departements de " + request.form["region"].strip().capitalize() + " : </h2>"
    departements = query_db_local(DATABASE, 'select d.nom, d.num from regions r, departements d where r.num=d.region and r.nommaj=\'{}\' order by d.nom asc'.format(region))
    #departements = query_db('dbserver', 'bpinaud', 'lgoudin', 'select d.nom, d.num from regions r, departements d where r.num=d.region and r.nommaj=\'{}\' order by d.nom asc'.format(region))
    for i in departements:
        page = page + i[1] + "  " + i[0] + "<br/>"
    return page

@app.route("/liste_departements_annee_diplome_request")
def liste_departements_annee_diplome_request():
    return app.send_static_file("liste_departements_annee_diplome_form.html")

@app.route("/liste_departements_annee_diplome", methods=['POST'])
def liste_departements_annee_diplome():
    page=""
    return page

def get_db_local(db_name):
    print("Connecting to database {}...".format(db_name))
    db = psycopg2.connect(dbname=db_name)
    return db

def query_db_local(database, command):
    cur = get_db_local(database).cursor()
    print("Executing command {} on database {}...".format(command, database))
    cur.execute(command)
    rv = cur.fetchall()
    cur.close()
    return rv

def get_db(host, dbname, user):
    print("Trying to connect to database {} with user {} and host {}...".format(dbname, user, host))
    try:
        db = psycopg2.connect(host=host, dbname=dbname, user=user)
        return db
    except Exception as e:
        return "Error when connecting to {}: {}".format(dbname, str(e))

def query_db(host, dbname, user, command):
    cur = get_db(host, dbname, user)
    print("Trying to execute command: {}; on database {} with user {} and host {}...".format(command, dbname, user, host))
    try:
        cur.execute(command)
        rv = cur.fetchall()
        cur.close()
        return rv
    except Exception as e:
        return "Error when running command: {}: {}".format(command, str(e))

    

	

#NE SURTOUT PAS MODIFIER     
if __name__ == "__main__":
    app.run(debug=True)
    
   
# def liste_regions():
#     page='<h2>Liste des regions Francaises :</h2>'
#     print("Trying to connect to the database")
#     try:
#         #conn = psycopg2.connect(host='dbserver', dbname='bpinaud', user='lgoudin')
#         conn = psycopg2.connect(dbname='miniproj', user='lucas')
#         print("Connected to the database")
#         cur = conn.cursor()
#         command = "select nom from regions order by nom asc"
#         print("Trying to execute command: " + command)
#         try:
#             cur.execute(command)
#             print("Execute OK")
#             rows = cur.fetchall()
#             print("Fetchall OK")
#             regions = rows

#             for i in regions:
#                 page = page + i[0] + "<br/>"
            

#         except Exception as e:
#             return "Error when running command: " + command + " : " + str(e)
        
#     except Exception as e:
#         return "Cannot connect to database: " + str(e)
    
#     return page



# def liste_departements_region():
#     region = request.form["region"].upper().strip()
#     page="<h2>Liste des departements de " + request.form["region"].strip().capitalize() + " : </h2>"
#     print("Trying to connect to the database")
#     try:
#         #conn = psycopg2.connect(host='dbserver', dbname='bpinaud', user='lgoudin')
#         conn = psycopg2.connect(dbname='miniproj')
#         print("Connected to the database")
#         cur = conn.cursor()
#         command = "select d.nom, d.num from regions r, departements d where r.num=d.region and r.nommaj=\'" + region + "\' order by d.nom asc"
#         print("Trying to execute command: " + command)
#         try:
#             cur.execute(command)
#             print("Execute OK")
#             rows = cur.fetchall()
#             print("Fetchall OK")
#             for i in rows:
#                 page = page + i[1] + "  " + i[0] + "<br/>"

#         except Exception as e:
#             return "Error when running command: " + command + " : " + str(e)

#     except Exception as e:
#         return "Cannot connect to database: " + str(e)
        
#     return page