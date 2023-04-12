import csv

#Creation et ouverture du fichier csv en mode écriture
#Mettre chemin d'accès, de préférence avec dexu barres obliques pour éviter les porblèmes
with open('/media/estcros/EMTEC B110/Année scolaire 2022-2023/M1/S2/PROJET/output_csv.csv','w',newline='') as csv_file :
    #Ouverture du fichier VCF en mode lecture
    with open('/media/estcros/EMTEC B110/Année scolaire 2022-2023/M1/S2/PROJET/TSVC_variants_IonXpress_011.vcf','r') as vcf_file:

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
                if i != 7:
                    data_col.append(cols[i])
                    #print('data_col',data_col)
            informations = cols[7].strip().split(';')
            #print('info',informations)
            for i in range(len(informations)):
                #print('ii',i)
                data_col.append(informations[i].split("=")[1])
                #print('data_col',data_col)
            data_col_total.append(data_col)
        #print(data_col_total[0])   
            
           #print(data_col)
            #writer.writerow(data_col)

    #On extrait les informations du fichier disease
    with open('/media/estcros/EMTEC B110/Année scolaire 2022-2023/M1/S2/PROJET/Mitomap/disease.vcf','r') as disease:
        data_col_disease_total=[] 
        for line2 in disease : 
            #print(line2)
            data_col_disease=[]
            if line2.startswith('#'):
                continue
            cols2=line2.strip().split('\t')
            #print("wtf",cols2)
            if len(cols) < 8: 
                continue
            cols2[0]='M'

            for j in range(len(cols2)):
                if j == 7 :
                    cols7 = cols2[7].strip().split(';')
                    cols = cols2[0:7]+cols7+cols2[8:]

                    if (len(cols[4])>1):
                        for alt in cols[4] :
                            line = cols[0:4]+[alt]+cols[5:]
                    else:
                        line = cols
                    #print("ligne",line)
                    for i in range(7,len(line)):
                        line[i] = line[i].split("=")[1]
                        #print("lin",line[i])
                        data_col_disease.append(line[i])  
                    #print("dt",data_col_disease)
            data_col_disease_total.append(cols[0:7]+data_col_disease)  
        #print("dt",data_col_disease_total)

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
    #print(data_anno)
    writer.writerows(data_anno)
