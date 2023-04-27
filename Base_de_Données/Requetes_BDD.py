import psycopg2 #Import des librairies nécessaires
import psycopg2.extras
import sys
import pandas as pd


USERNAME = "yguiberteau"
PASSWORD = "Ya&2l&BDD"
HOSTNAME = "pgsql" #Remplacer par "localhost" pour les connexions à distance 


def requete():
    '''Affiche dans le terminal la réponse à une requête passée en entrée par l'utilisateur. La sortie est auss enregistrée dans un fichier Excel.'''
    print('Trying to connect to the database')
    try:
        conn = psycopg2.connect(host=HOSTNAME,dbname=USERNAME,user=USERNAME,password=PASSWORD)
        print('Connected to the database')
        cur = conn.cursor()
    except Exception as e:
        exit("Can not connect to database: "+str(e))
    try:
        command=input("Veuillez saisir votre requête SQL :\n") #Requête SQL
        print("Trying to execute command: ",command)
        cur.execute(command)
        print("Execute OK")
        rows=cur.fetchall()
        if (not rows):
            exit("Il n'y a pas d'éléments correspondant à cette requête.")
        print("Voici les éléments correspondant à votre requête:")
        for i in range(0,len(rows)): #Affichage des résultats de la requête dans le terminal
            print(r[i])
        df=pd.DataFrame(columns=['NumDep','Département','Taux pauvreté 2018']) #Création d'une dataframe contenant les résultats de la requête
        i=0
        for r in rows:
            df.loc[i]=[r[0],r[1],r[2]]
            i+=1
        writer=pd.ExcelWriter('Requete_INSEE.xlsx',engine="xlsxwriter") #Sauvegarde de la dataframe dans un fichier Excel
        df.to_excel(writer,sheet_name='Requete') 
        writer.save()
        writer.close()
        print("Cette requête a été sauvegardée dans le fichier Requete_Mito.xlsx à l'onglet Requete\n")
        cur.close()
        conn.close()
        print("La connexion PostreSQL est fermée")
    except Exception as e:
        exit("Error when running command: "+command+" : "+str(e))
        

requete()