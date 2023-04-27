import pandas as pd #Import des librairies nécessaires
import psycopg2
import psycopg2.extras
import sys


USERNAME = "yguiberteau"
PASSWORD = "Ya&2l&BDD"
HOSTNAME = "pgsql" #Remplacer par "localhost" pour les connexions à distance 


def remise_en_forme(df):
    Patients = []
    Variants = []
    OccCohorte = []

    for i in range (0,df.shape[1],2):
        for j in range (0,df.shape[0]):
            pat = df.columns[i]
            var = df.loc[j,pat] 
            if var != "NaN":
                Variants.append(var)
                Patients.append(int(pat[8:]))

    for i in range (1,df.shape[1],2):
        for j in range (0,df.shape[0]):
            col = df.columns[i]
            occ = df.loc[j,col] 
            if occ != "NaN":
                OccCohorte.append(int(occ))
            
    df_variants = pd.DataFrame({"NumPatient":Patients,
                "Variant":Variants,
                "OccCohorte":OccCohorte})
    return df_variants
  

def insert_Excel(path_excel):
    df_chargement = pd.read_excel(path_excel) #Insertion des données issues des fichiers .xlsx dans des dataframes pandas
    df_chargement.fillna(value="NaN",inplace=True) #Remplacement des cases vides de la dataframe par la valeur 'NaN'
    df_variants = remise_en_forme(df_chargement)

    try:
        print("Connexion à la base de données...")
        conn = psycopg2.connect(host=HOSTNAME,dbname=USERNAME,user=USERNAME,password=PASSWORD)
    except Exception as e :
        exit("Connexion impossible à la base de données: " + str(e))
    print("Connecté à la base de données")

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    print("Insertion des données dans la table Variants") 
    try:
        for i in range (1,df_variants.shape[0]):
            value=list(df_variants.iloc[i])
            command="INSERT INTO Variants VALUES ({},'{}',{});".format(*value) #Formatage des chaînes grâce aux accolades et à la fonction format
            print(command)
            cur.execute(command)
        print("Importation des données dans la table Variants réussie.")
    except Exception as e:
        cur.close()
        conn.close()
        exit("Error when running: ",command," : ",str(e))

    conn.commit() #Fermeture de la connexion à la base de données
    cur.close()
    conn.close()
    print("La connexion PostgreSQL est fermée.\n")


def insert_manuel():
    pat = int(input("Quel est le numéro du patient ?\n"))
    var = input("Quel est le variant ?\n")
    occ = int(input("Quel est l'occurence du variant dans la cohorte ?\n"))

    try:
        print("Connexion à la base de données...")
        conn = psycopg2.connect(host=HOSTNAME,dbname=USERNAME,user=USERNAME,password=PASSWORD)
    except Exception as e :
        exit("Connexion impossible à la base de données: " + str(e))
    print("Connecté à la base de données")

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    print("Insertion des données dans la table Variants") 
    try:
        value=[pat,var,occ]
        command="INSERT INTO Variants VALUES ({},'{}',{});".format(*value) #Formatage des chaînes grâce aux accolades et à la fonction format
        print(command)
        cur.execute(command)
        print("Importation des données dans la table Variants réussie.")
    except Exception as e:
        cur.close()
        conn.close()
        exit("Error when running: ",command," : ",str(e))

    conn.commit() #Fermeture de la connexion à la base de données
    cur.close()
    conn.close()
    print("La connexion PostgreSQL est fermée.\n")


def insertion_variants():
    rep = 0
    while rep == 0:
        print("Comment souhaitez-vous insérer les variants ?")
        print("1\tA partir d'un fichier Excel")
        print("2\tManuellement")
        rep=int(input())
        if rep==1:
            path = input("Entrez le path de votre fichier Excel.\n")
            insert_Excel(path)
        elif rep==2:
            insert_manuel()
        else:
            print("Choix incorrect. Veuillez recommencer")


def insertion_nomenclature():
    var = input("Quel est le variant ?\n")
    pos = int(input("Quelle est la position du variant ?\n"))
    type_var = input("Quelle est le type de la variation ?\n")

    try:
        print("Connexion à la base de données...")
        conn = psycopg2.connect(host=HOSTNAME,dbname=USERNAME,user=USERNAME,password=PASSWORD)
    except Exception as e :
        exit("Connexion impossible à la base de données: " + str(e))
    print("Connecté à la base de données")

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    print("Insertion des données dans la table Nomenclature")
    try:
        value=[var,pos,type_var]
        command="INSERT INTO Nomenclature VALUES ('{}',{},'{}');".format(*value) #Formatage des chaînes grâce aux accolades et à la fonction format
        cur.execute(command)
        print("Importation des données dans la table Nomenclature réussie.")
    except Exception as e:
        cur.close()
        conn.close()
        exit("Error when running: ",command," : ",str(e))

    conn.commit() #Fermeture de la connexion à la base de données
    cur.close()
    conn.close()
    print("La connexion PostgreSQL est fermée.\n")


def insertion_annotations(path_csv):
    df_annotations = pd.read_csv(path_csv,sep=",") #sep à voir avec le fichier de sortie d'Esther

    try:
        print("Connexion à la base de données...")
        conn = psycopg2.connect(host=HOSTNAME,dbname=USERNAME,user=USERNAME,password=PASSWORD)
    except Exception as e :
        exit("Connexion impossible à la base de données: " + str(e))
    print("Connecté à la base de données")

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    print("Insertion des données dans la table Annotations")
    try:
        for i in range (df_annotations.shape[0]):
            value=list(df_annotations.iloc[i])
            command="INSERT INTO Annotations VALUES ({},{},{},{},{},{});".format(*value) #Formatage des chaînes grâce aux accolades et à la fonction format
            cur.execute(command)
        print("Importation des données dans la table Annotations réussie.")
    except Exception as e:
        cur.close()
        conn.close()
        exit("Error when running: ",command," : ",str(e))   

    conn.commit() #Fermeture de la connexion à la base de données
    cur.close()
    conn.close()
    print("La connexion PostgreSQL est fermée.\n")


def menu():
    rep = 1
    while rep in range (1,6):
        print("Dans quelle table souhaitez-vous insérer des données ?")
        print("1\tTable Variants")
        print("2\tTable Nomenclature")
        print("3\tTable Annotations")
        print("0\tQuitter le programme")
        rep=int(input())
        if rep==1:
            insertion_variants()
        elif rep==2:
            insertion_nomenclature()
        elif rep==3:
            insertion_annotations()
        elif rep==0:
            print("Au revoir")
            sys.exit()
        else:
            print("Choix incorrect. Veuillez recommencer")
            

menu()