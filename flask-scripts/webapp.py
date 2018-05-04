from flask import Flask, render_template, request
import psycopg2
    
#NE PAS MODIFIER LA LIGNE SUIVANTE
app = Flask(__name__)
DATABASE = 'miniproj'
HOST = 'dbserver'
DATABASE_SERVER = 'bpinaud'
USER = 'lgoudin'
            
@app.route("/")
def hello():
    return render_template('accueil_template.html')

@app.route("/liste_regions", methods=['GET'])
def liste_regions():
    regions = query_db(HOST, DATABASE_SERVER, USER, 'select nom from regions order by nom asc')
    return render_template('liste_regions.html', regions=regions)

@app.route("/liste_departements_region_request")
def liste_departements_region_request():
    regions = query_db(HOST, DATABASE_SERVER, USER, 'select * from regions order by nom asc')
    return render_template('liste_departements_region_form.html', regions=regions)
    
@app.route("/liste_departements_region", methods=['POST'])
def liste_departements_region():
    region = request.form["region"]
    departements = query_db('dbserver', 'bpinaud', 'lgoudin', 'select d.nom, d.num from regions r, departements d where r.num=d.region and r.nom=\'{}\' order by d.nom asc'.format(region))
    return render_template('liste_departements.html', depts=departements, region=region)

@app.route("/liste_departements_annee_diplome_request")
def liste_departements_annee_diplome_request():
    annees = query_db(HOST, DATABASE_SERVER, USER, 'select distinct annee from nb_diplomes_dept order by annee asc')
    diplomes = query_db(HOST, DATABASE_SERVER, USER, 'select * from niveaux_diplomes') 
    return render_template("liste_departements_annee_diplome_form.html", annees=annees, diplomes=diplomes)

@app.route("/liste_departements_annee_diplome", methods=['POST'])
def liste_departements_annee_diplome():
    annee = request.form["annee"]
    niveau = request.form["diplome"]
    depts = query_db(HOST, DATABASE_SERVER, USER, 'select distinct d.nom from departements d,nb_diplomes_dept nb where nb.dept=d.num and ((select sum(num) from nb_diplomes_dept where annee={} and niveau={} and sexe=\'H\')<(select sum(num) from nb_diplomes_dept where annee={} and niveau={} and sexe=\'F\')) order by d.nom asc'.format(annee,niveau,annee,niveau))
    diplome_name = query_db(HOST, DATABASE_SERVER, USER, 'select label from niveaux_diplomes where id={}'.format(niveau))
    return render_template('liste_departements_annee_diplome.html', annee=annee, depts=depts, diplome_name=diplome_name)

@app.route("/liste_num_request")
def liste_num_request():
    diplomes = query_db(HOST, DATABASE_SERVER, USER, 'select * from niveaux_diplomes') 
    annees = query_db(HOST, DATABASE_SERVER, USER, 'select distinct annee from nb_diplomes_dept order by annee asc')
    depts = query_db(HOST, DATABASE_SERVER, USER, 'select * from departements order by nom asc')
    ages = query_db(HOST, DATABASE_SERVER, USER, 'select * from tranches_ages')
    return render_template('liste_num_form.html', diplomes=diplomes, annees=annees, depts=depts, ages=ages)

@app.route("/liste_num", methods=['POST'])
def liste_num():
    diplome = request.form["diplome"]
    annee = request.form["annee"]
    dept = request.form["dept"]
    age = request.form["age"]
    
    nums = query_db(HOST, DATABASE_SERVER, USER, 'select sum(num) from nb_diplomes_dept where niveau={} and annee={} and dept=\'{}\' and age={}'.format(diplome,annee,dept,age))
    age_name = query_db(HOST, DATABASE_SERVER, USER, 'select label from tranches_ages where id={}'.format(age))
    diplome_name = query_db(HOST, DATABASE_SERVER, USER, 'select label from niveaux_diplomes where id={}'.format(diplome))
    dept_name = query_db(HOST, DATABASE_SERVER, USER, 'select nom from departements where num=\'{}\''.format(dept))
    return render_template('liste_num.html', nums=nums, diplome_name=diplome_name, annee=annee, age_name=age_name, dept_name=dept_name)

@app.route("/wiki_dept")
def wiki_dept():
    depts = query_db(HOST, DATABASE_SERVER, USER, 'select * from departements order by nom asc')
    return render_template('wiki_dept.html', depts=depts)

@app.route("/moyenne_request")
def moyenne_request():
    niveaux = query_db(HOST,DATABASE_SERVER,USER, 'select * from niveaux_diplomes')
    return render_template('moyenne_request.html', niveaux=niveaux)

@app.route("/moyenne", methods=['POST'])
def moyenne():
    niveau = request.form["diplome"]
    diplome = query_db(HOST, DATABASE_SERVER, USER, 'select label from niveaux_diplomes where id={}'.format(niveau))
    moyenne = query_db(HOST,DATABASE_SERVER,USER, 'select round(avg(num)) from nb_diplomes_dept where niveau={}'.format(niveau))
    return render_template("moyenne.html", moyenne=moyenne, diplome=diplome)

#############################################################################################################################################################################


def get_db(host, dbname, user):
    print("Trying to connect to database {} with user {} and host {}...".format(dbname, user, host))
    try:
        db = psycopg2.connect(host=host, dbname=dbname, user=user)
        print("Connected to database {}!".format(dbname))
        return db
    except Exception as e:
        print("Error when connecting to {}: {}".format(dbname, str(e)))

def query_db(host, dbname, user, command):
    cur = get_db(host, dbname, user).cursor()
    print('Trying to execute command "{}" on database {} with user {} and host {}...'.format(command, dbname, user, host))
    try:
        cur.execute(command)
        rv = cur.fetchall()
        cur.close()
        print("Command executed successfully!")
        return rv
    except Exception as e:
        return('Error when running command "{}": {}'.format(command, str(e)))

    

	

#NE SURTOUT PAS MODIFIER     
if __name__ == "__main__":
    app.run(debug=True)
    
   
