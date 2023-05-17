#Ce code permet de faire l'annotation de variants par vep pour des variants connu et inconnu puis par mitomaster pour les variants déjà connu

import subprocess
import os
import csv

#Annotation par VEP

def annotate_vcf(vcf_file):
    output_path = os.path.join(os.path.dirname(__file__), 'output_vep.csv')
    print(f"Le fichier output sera créé à l'emplacement : {output_path}")
    vep_command = f'/home/escros/project_prog/demo-app/anno/annotation/ensembl-vep/vep -i {vcf_file} --cache --dir_cache /home/escros/.vep --fasta /home/escros/project_prog/demo-app/anno/annotation/REF.fasta --assembly GRCh38 --format vcf --vcf --pick --force_overwrite --no_escape --everything --output_file {output_path}' 
    subprocess.call(vep_command, shell=True)
    if os.path.exists(output_path):
        print("Le fichier output a été créé avec succès!")
    else:
        print("Erreur : le fichier output n'a pas été créé.")

annotate_vcf('/home/escros/project_prog/demo-app/anno/annotation/TSVC_variants_IonXpress_011.vcf')
#Fichier annoté se nomme output_vep.csv

import re

def process_line(line):
    term_matches = re.findall(r'(\w+)=([^=]+)', line)
    print('term_matches',term_matches)
    
    terms = [(term[1].split(',')) for term in term_matches]
    print('terms',terms)
    """
    result = []
    num_elements = max(len(term[1]) for term in terms)

    for i in range(num_elements):
        new_line = []
        for term in terms:
            term_key = term[0]
            term_values = term[1]
            if i < len(term_values):
                new_line.append(term_values[i])
        result.append(new_line)
    return result
    """

# Annotation avec fichier de MitoMap

#Creation et ouverture du fichier csv en mode écriture
#Mettre chemin d'accès, de préférence avec dexu barres obliques pour éviter les problèmes
with open('/home/escros/project_prog/demo-app/anno/annotation/variants_annotation.csv.csv','w',newline='') as csv_file :
    #Ouverture du fichier VCF en mode lecture
    with open('/home/escros/project_prog/demo-app/anno/annotation/TSVC_variants_IonXpress_011.vcf','r') as vcf_file:

        #Création d'un objet writer pour écrire dans un fichier CSV
        writer = csv.writer(csv_file)
        
        #Ecrire l'en-tête CSV
        writer.writerow(['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL','FILTER','INFO1','INFO2','AF', 'AO', 'DP', 'FAO', 'FDP', 'FDVR', 'FR', 'FRO', 'FSAF', 'FSAR', 'FSRF', 'FSRR', 'FWDB', 'FXX', 'HRUN', 'HS_ONLY', 'LEN', 'MLLD', 'OALT', 'OID', 'OMAPALT', 'OPOS', 'OREF', 'PB', 'PBP', 'QD', 'RBI', 'REFB', 'REVB', 'RO', 'SAF', 'SAR', 'SRF', 'SRR', 'SSEN', 'SSEP', 'SSSB', 'STB', 'STBP', 'TYPE', 'VARB','AC_disease','AF_disease','aachange_disease','homoplasmy','heteroplasmy','PubMedIDs','Disease','Disease_status','HGFL'])

        data_col_total=[]
        #Parcourir le fichier VCF ligne par ligne
        for line in vcf_file : 
            data_col = []
            #Ignorer les lignes commentées
            if line.startswith('#'):
                continue
            #print(line)
            #Diviser les lignes en colonnes en fonction des tabulations
            cols=line.strip().split('\t')
            if len(cols) < 8:  # vérifier que la ligne contient au moins 8 colonnes
                continue
            # Extraire les informations nécéssaires
            cols[0]='M'
            #print('cols',cols)
            for i in range(len(cols)):
                #print('i',i)
                if i ==7 : 
                    cols70 = cols[7].strip().split(';')
                    cols = cols[0:7]+cols[8:]+cols70
                    if (len(cols[4])>1):
                        for alt in cols[4] :
                            line = cols[0:4]+[alt]+cols[5:]
                    else:
                        line = cols
                    for i in range(9,len(line)):
                        line[i] = line[i].split("=")[1]
                        data_col.append(line[i])  
            data_col_total.append(cols)  
        #print('TSVC',data_col_total[0]) 

    '''           if i != 7:
                    data_col.append(cols[i])
                    #print('data_col',data_col)
            informations = cols[7].strip().split(';')
            #print('info',informations)
            for i in range(len(informations)):
                #print('ii',i)
                data_col.append(informations[i].split("=")[1])
                #print('data_col',data_col)
            data_col_total.append(data_col)
    '''
          
            
           #print(data_col)
            #writer.writerow(data_col)

    #On extrait les informations du fichier disease
    with open('/home/escros/project_prog/demo-app/anno/annotation/Mitomap/disease.vcf','r') as disease:
        data_col_disease_total=[] 
        for line2 in disease : 
            data_col_disease=[]
            if line2.startswith('#'):
                continue
            cols2=line2.strip().split('\t')
            if len(cols2) < 8: 
                continue
            cols2[0]='M'
            for j in range(len(cols2)):
                if j == 7 :
                    cols7 = cols2[7].strip().split(';')
                    cols2 = cols2[0:7]+cols7+cols2[8:]
                    if (len(cols2[4])>1):
                        for alt in cols2[4] :
                            line = cols2[0:4]+[alt]+cols2[5:]
                    else:
                        line = cols2
                    for i in range(7,len(line)):
                        line[i] = line[i].split("=")[1]
                        data_col_disease.append(line[i])  
            data_col_disease_total.append(cols2)  
        #print("disease",data_col_disease_total[1])

    with open('/home/escros/project_prog/demo-app/anno/annotation/output_vep.csv') as vep_file :
        data_col_vep_total=[]
        for lineVEP in vep_file :
            print(f"LINE VEP: {lineVEP}")
            data_col_vep=[]
            if lineVEP.startswith('#'):
                continue
            colsVEP=lineVEP.strip().split('\t')
            if len(colsVEP) < 8: 
                continue
            colsVEP[0]='M'
            for j in range(len(colsVEP)):
                if j == 7 :
                    cols7VEP = colsVEP[7].strip().split(';')
                    colsVEP = colsVEP[0:7]+colsVEP[8:]+cols7VEP
                    if (len(colsVEP[4])>1):
                        for alt in colsVEP[4] :
                            lineVEP = colsVEP[0:4]+[alt]+colsVEP[5:]
                    else:
                        lineVEP = colsVEP
                    #print("line",lineVEP[9:len(lineVEP)])  
                    #print(lineVEP)             
                    for i in range(9,len(lineVEP)):
                        #print("i",lineVEP[i])
                       
                       
                       
                        
                        #result = process_line(lineVEP[i])
                        #for row in result:
                            #print(row)
                            #pass
                            #concat = [' '.join(row) for row in result]
                            #print(concat)



                            #data_col_vep.append(' '.join(row))
                            #print("dt",data_col_vep)


                        lineVEP[i] = lineVEP[i].split("=")[1]
                        data_col_vep.append(lineVEP[i])  
                        print("dt",data_col_vep)
            data_col_vep_total.append(colsVEP)  
        #print("VEP",data_col_vep_total)
        
    #On compare les informations de data_col et data_col_disease : 
    data_anno = []
    #lignes=line2.strip().split('\t')
    for ligne1 in data_col_total :
        #print('ligne1',ligne1) 
        elem1=ligne1[0:2]+ligne1[3:5]
        #print('elem1',elem1)
        for ligne2 in data_col_disease_total : 
            #print('ligne2', ligne2)
            elem2=ligne2[0:2]+ligne2[3:5]
            #print('elem2',elem2)
            if elem1==elem2:
                #print(ligne2[7:])
                #print(elem1)
                data_ligne=ligne1+ligne2[7:]
                #print('data_ligne',data_ligne)
                data_anno.append(data_ligne)
    #print('data_anno',data_anno)

    # Faire gaffe a la concordance des colonnes, ce ne sont pas les mêmes pour data_anno et vep
    # Voir quelle colonne correspond a laquelle

    # On inclut dans data_anno les variants annotés pas encore présents
    for ligne1 in data_col_vep_total:
        #print(ligne1)
        elem1 = ligne1[0:2] + ligne1[3:5]
        #print('elem1',elem1)
        found = False
        for ligne2 in data_anno:
            elem2 = ligne2[0:2] + ligne2[3:5]
            #print('elem2',elem2)
            if elem2 == elem1:
                found = True
                break
        if not found:
            data_anno.append(ligne1)
    #print(data_anno)
    
    #Creation du fichier de sortie regroupant les variants non annoté et annoté grace à vep et les variants déjà connu dans la littérature (avec Mitomap)
    writer.writerows(data_anno)
    #Fichier en sortie s'appelle variants_annotation.csv