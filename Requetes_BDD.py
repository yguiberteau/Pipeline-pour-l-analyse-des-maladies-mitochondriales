import psycopg2 #Import des librairies nécessaires
import psycopg2.extras
import sys
import pandas as pd


USERNAME = "yguiberteau"
PASSWORD = "Ya&2l&BDD"
HOSTNAME = "pgsql" #Remplacer par "localhost" pour les connexions à distance 


def taux_pauvrete_2018():
    '''Affiche la liste des départements où le taux de pauvreté en 2018 était compris entre 15% et 20%, classés du plus fort taux au plus faible.'''
    print('Trying to connect to the database')
    try:
        conn = psycopg2.connect(host=HOSTNAME,dbname=USERNAME,user=USERNAME,password=PASSWORD)
        print('Connected to the database')
        cur = conn.cursor()
    except Exception as e:
        exit("Can not connect to database: "+str(e))
    try:
        command='''SELECT numdep,nccenrdep,tx_pauv_2018 
            FROM socialdepartement
            WHERE tx_pauv_2018 >= 15 AND tx_pauv_2018 <=20
            ORDER BY tx_pauv_2018 DESC;''' #Requête SQL
        print("Trying to execute command: ",command)
        cur.execute(command)
        print("Execute OK")
        rows=cur.fetchall()
        if (not rows):
            exit("Il n'y a pas d'éléments correspondant à cette requête.")
        print("Voici les départements correspondant à la requête:")
        for r in rows: #Affichage des résultats de la requête dans le terminal
            print("Département :",r[1],"("+r[0]+")")
            print("Taux de pauvreté en 2018 :",r[2],"%\n")
#        book=load_workbook('Requete_INSEE.xlsx')    
        df=pd.DataFrame(columns=['NumDep','Département','Taux pauvreté 2018']) #Création d'une dataframe contenant les résultats de la requête
        i=0
        for r in rows:
            df.loc[i]=[r[0],r[1],r[2]]
            i+=1
        writer=pd.ExcelWriter('Requete_INSEE.xlsx',engine="xlsxwriter") #Sauvegarde de la dataframe dans un fichier Excel
#        writer.book=book
        df.to_excel(writer,sheet_name='Requete1') 
        writer.save()
        writer.close()
        print("Cette requête a été sauvegardée dans le fichier Requete_INSEE.xlsx à l'onglet Requête1\n")
        cur.close()
        conn.close()
        print("La connexion PostreSQL est fermée")
    except Exception as e:
        exit("Error when running command: "+command+" : "+str(e))