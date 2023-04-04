import pandas as pd #Import des librairies nécessaires
import psycopg2
import psycopg2.extras


USERNAME = "yguiberteau"
PASSWORD = "Ya&2l&BDD"
HOSTNAME = "pgsql" #Remplacer par "localhost" pour les connexions à distance 


#Insertion des données issues des fichiers .xlsx dans des dataframes pandas
df_variants = pd.read_excel("BDD_ADNmt.xlsx",sheet_name="Variants") #usecols='A:L',skiprows=[0,1,17,22,23,24] ou skiprows=[i for i in range(0,30)] + [i for i in range(133,139)]
df_variants.fillna(value="NULL",inplace=True) #Remplacement des cases vides de la dataframe par la valeur 'NULL'
df_annotations = pd.read_csv("annotations.csv",sep=",") #sep à voir avec le fichier de sortie d'Esther
df_nomenclature = pd.read_csv("nomenclature.csv",sep=",") #à voir pour une insertion manuelle dans la dataframe plutot qu'à partir d'un csv


try:
    print("Connexion à la base de données...") #Connexion à la base de données
    conn = psycopg2.connect(host=HOSTNAME,dbname=USERNAME,user=USERNAME,password=PASSWORD)
except Exception as e :
    exit("Connexion impossible à la base de données: " + str(e))
print("Connecté à la base de données")

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


print("Insertion des données dans la table Variants") 
try:
    for i in range (1,df_variants.shape[0]):
        value=list(df_variants.iloc[i])
        command="INSERT INTO Variants VALUES ({},'{}',{},{},{},{},{},{},{},{},{},{});".format(*value) #Formatage des chaînes grâce aux accolades et à la fonction format
        cur.execute(command)
    print("Importation des données dans la table Variants réussie.")
except Exception as e:
    cur.close()
    conn.close()
    exit("Error when running: ",command," : ",str(e))


print("Insertion des données dans la table Annotations")
try:
    for i in range (df_annotations.shape[0]):
        value=list(df_annotations.iloc[i])
        command="INSERT INTO Annotations VALUES ({},'{}',{},'{}','{}','{}');".format(*value) #Formatage des chaînes grâce aux accolades et à la fonction format
        cur.execute(command)
    print("Importation des données dans la table Annotations réussie.")
except Exception as e:
    cur.close()
    conn.close()
    exit("Error when running: ",command," : ",str(e))


print("Insertion des données dans la table Nomenclature")
try:
    for i in range (df_nomenclature.shape[0]):
        value=list(df_nomenclature.iloc[i])
        command="INSERT INTO Nomenclature VALUES ({},'{}',{},'{}','{}','{}');".format(*value) #Formatage des chaînes grâce aux accolades et à la fonction format
        cur.execute(command)
    print("Importation des données dans la table Nomenclature réussie.")
except Exception as e:
    cur.close()
    conn.close()
    exit("Error when running: ",command," : ",str(e))


conn.commit() #Fermeture de la connexion à la base de données
cur.close()
conn.close()

print("La connexion PostgreSQL est fermée.")