from flask import Flask, render_template, request
import psycopg2
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')
    
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
    for i in regions:
        page = page + i[0] + '<br>'
    return page

@app.route("/liste_departements_region_request")
def liste_departements_region_request():
    regions = query_db_local(DATABASE, 'select * from regions')
    return render_template('liste_departements_region_form.html', regions=regions)
    
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
    annees = query_db_local(DATABASE, 'select distinct annee from nb_diplomes_dept order by annee asc')
    diplomes = query_db_local(DATABASE, 'select * from niveaux_diplomes')
    return render_template("liste_departements_annee_diplome_form.html", annees=annees, diplomes=diplomes)

@app.route("/liste_departements_annee_diplome", methods=['POST'])
def liste_departements_annee_diplome():
    page=""
    annee = request.form["annee"]
    niveau = request.form["diplome"]
    depts = query_db_local(DATABASE, 'select distinct nom from departements dp, nb_diplomes_dept nb where dp.num=nb.dept and nb.annee={} and nb.niveau={} and (select count(*) from nb_diplomes_dept where annee={} and niveau={} and sexe=\'H\')>(select count(*) from nb_diplomes_dept where annee={} and niveau={} and sexe=\'F\')'.format(annee,niveau,annee,niveau,annee,niveau))
    
    if depts:
        for dept in depts:
            page += dept[0] + '<br>'
    else:
        page='Il n\'existe aucun departement dans lequel il y a plus de femmes diplomees que d\'hommes a cette annee et a ce niveau de diplome.'
    return page

##########################################################################################

def get_db_local(dbname):
    try:
        print("Trying to connect to database {}...".format(dbname))
        db = psycopg2.connect(dbname=dbname)
        print("Connected to database {}!".format(dbname))
        return db
    except Exception as e:
        return "Error when connecting to {}: {}".format(dbname, str(e))

def query_db_local(database, command):
    cur = get_db_local(database).cursor()
    print('Trying to execute command "{}" on database {}...'.format(command, database))
    try:
        cur.execute(command)
        rv = cur.fetchall()
        cur.close()
        print("Command executed successfully!")
        return rv
    except Exception as e:
        return 'Error when running command "{}": {}'.format(command, str(e))


def get_db(host, dbname, user):
    print("Trying to connect to database {} with user {} and host {}...".format(dbname, user, host))
    try:
        db = psycopg2.connect(host=host, dbname=dbname, user=user)
        print("Connected to database {}!".format(dbname))
        return db
    except Exception as e:
        return "Error when connecting to {}: {}".format(dbname, str(e))

def query_db(host, dbname, user, command):
    cur = get_db(host, dbname, user)
    print('Trying to execute command "{}" on database {} with user {} and host {}...'.format(command, dbname, user, host))
    try:
        cur.execute(command)
        rv = cur.fetchall()
        cur.close()
        print("Command executed successfully!")
        return rv
    except Exception as e:
        return 'Error when running command "{}": {}'.format(command, str(e))

    

	

#NE SURTOUT PAS MODIFIER     
if __name__ == "__main__":
    app.run(debug=True)
    
   
