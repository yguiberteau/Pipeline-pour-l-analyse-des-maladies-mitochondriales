import pandas as pd
import subprocess
import os

#Annotation par VEP
def annotate_vcf(vcf_file):
    output_path = os.path.join(os.path.dirname(__file__), 'output_vep.csv')
    print(f"Le fichier output sera créé à l'emplacement : {output_path}")
    vep_command = f'/home/escros/project_prog/demo-app/anno/annotation/ensembl-vep/vep -i {vcf_file} --cache --dir_cache /home/escros/.vep --offline --fasta /home/escros/project_prog/demo-app/anno/annotation/REF.fasta --assembly GRCh38 --format vcf --vcf --pick --force_overwrite --no_escape --everything --output_file {output_path}' 
    subprocess.call(vep_command, shell=True)
    if os.path.exists(output_path):
        print("Le fichier output a été créé avec succès!")
    else:
        print("Erreur : le fichier output n'a pas été créé.")
    return output_path


def load_vcf(file_variant):
    headers = []  # Variable pour stocker les en-têtes
    data = []  # Variable pour stocker les données du fichier
    with open(file_variant, 'r') as f:
        for line in f:
            if not line.startswith('#'):  # Sortir de la boucle lorsqu'on atteint la ligne non commentée
                data.append(line.strip().split('\t'))  # Ajouter les données à la liste
            if line.startswith('#CHROM'):  # Identifier la ligne des en-têtes
                headers = line.strip().split('\t')  # Extraire les en-têtes (à partir de la colonne 2)
    
    df = pd.DataFrame(data, columns=headers)
    return df

def parse_info_column(df):
    parsed_info = []  # Liste de dictionnaires pour stocker les informations analysées
    for index, row in df.iterrows():
        info = row['INFO']
        pairs = info.split(';')
        parsed_info_row = {}  # Dictionnaire pour stocker les informations de la ligne actuelle
        for pair in pairs:
            if '=' in pair:
                split_pair = pair.split('=')
                if len(split_pair) == 2:
                    key, value = split_pair
                    parsed_info_row[key] = value
        parsed_info.append(parsed_info_row)
    parsed_info_df = pd.DataFrame(parsed_info)
    merged_df = pd.concat([df.drop('INFO', axis=1), parsed_info_df], axis=1)
    return merged_df

def load_and_parse_vcf(file_path):
    vcf_data = load_vcf(file_path)
    vcf_data.rename(columns={'#CHROM': 'CHROM'}, inplace=True)
    # Permet d'homogénéisé les dataframes, dans toutes les situations le chromosome sera nommé "M"
    vcf_data['CHROM'] = 'M'
    return parse_info_column(vcf_data)

# Appel à la fonction annotate_vcf, sortie : Variants annotés par VEP
output_path_vep = annotate_vcf('/home/escros/project_prog/demo-app/anno/annotation/TSVC_variants_IonXpress_011.vcf')
csv_variant_VEP=load_and_parse_vcf(output_path_vep)

# Chargement et fusion des données Mitomap
vcf_variant_TSCV=load_and_parse_vcf('/home/escros/project_prog/demo-app/anno/annotation/TSVC_variants_IonXpress_011.vcf')
vcf_variant_disease=load_and_parse_vcf('/home/escros/project_prog/demo-app/anno/annotation/Mitomap/disease.vcf')
merged_data_Mitomap = pd.merge(vcf_variant_TSCV, vcf_variant_disease, on=['CHROM', 'POS', 'REF', 'ALT'], how='inner')

# Sortie : Variants déjà annotés dans la littérature
#output_file = '/home/escros/project_prog/demo-app/anno/annotation/output_mito.csv'
#merged_data_Mitomap.to_csv(output_file, index=False)

# Fusion des données Mitomap et VEP
merged_data_anno = merged_data_Mitomap.set_index(['CHROM', 'POS', 'REF', 'ALT']).combine_first(csv_variant_VEP.set_index(['CHROM', 'POS', 'REF', 'ALT'])).reset_index()

# Réorganisation des colonnes dans l'ordre souhaité
ordering_columns = ['CHROM', 'POS', 'ID','REF', 'ALT','QUAL','FILTER','FORMAT','TYPE','Disease','DiseaseStatus']
desired_order =  ordering_columns + list(merged_data_anno.columns.drop(ordering_columns))
merged_data_anno=merged_data_anno.reindex(columns=desired_order)

# Sortie : Variants annotés par Mitomap et VEP
output_file = '/home/escros/project_prog/demo-app/anno/annotation/annotation_VEP_Mitomap.csv'
merged_data_anno.to_csv(output_file, index=False)