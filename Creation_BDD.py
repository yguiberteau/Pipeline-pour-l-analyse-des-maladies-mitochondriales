import pandas as pd #Import des librairies nécessaires
import psycopg2
import psycopg2.extras


USERNAME = "yguiberteau"
PASSWORD = "Ya&2l&BDD"
HOSTNAME = "pgsql" #Remplacer par "localhost" pour les connexions à distance 


try:
    print("Connexion à la base de données...") #Connexion à la base de données
    conn = psycopg2.connect(host=HOSTNAME,dbname=USERNAME,user=USERNAME,password=PASSWORD)
except Exception as e :
    exit("Connexion impossible à la base de données: " + str(e))
print("Connecté à la base de données")

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


#cur.execute("DROP TABLE Variants CASCADE")
#conn.commit()


try:
    print("Création de la table Variants") 
    cur.execute("""CREATE TABLE public.Variants(NumPatient int primary key not null,
                                            Variant text primary key not null,
                                            Heteroplasmie text not null,
                                            OccCohorte int not null);""")
    print("Table Variants créée avec succès")
except Exception as e:
    exit("Impossible de créer la table Variants"+str(e))
    
    
#cur.execute("DROP TABLE Annotations")
#conn.commit()


try:
    print("Création de la table Annotations") #Voir intitulés des colonnes avec Esther et types des variables
    cur.execute("""CREATE TABLE public.Annotations(Variant text primary key not null,
                                            Chrom text not null,
                                            Pos int not null,
                                            Id text not null,
                                            Ref char(1) not null,
                                            Alt char(1) not null
                                            Qual float not null
                                            Filters text not null
                                            Info text not null);""")
    print("Table Annotations créée avec succès")
except Exception as e:
    exit("Impossible de créer la table Annotations"+str(e))
    

#cur.execute("DROP TABLE Annotations")
#conn.commit()


try:
    print("Création de la table Nomenclature")
    cur.execute("""CREATE TABLE public.Nomenclature(Variant text primary key not null,
                                            Pos text not null,
                                            Type int not null);""")
    print("Table Nomenclature créée avec succès")
except Exception as e:
    exit("Impossible de créer la table Nomenclature"+str(e))


conn.commit() #Fermeture de la connexion à la base de données
cur.close()
conn.close()

print("La connexion PostgreSQL est fermée.")