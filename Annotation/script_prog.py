import subprocess
import os

#Annoter le fichier VCF
def annotate_vcf(vcf_file):
    output_path = os.path.join(os.path.dirname(__file__), 'output.csv')
    print(f"Le fichier output sera créé à l'emplacement : {output_path}")
    vep_command = f'/home/escros/project_prog/demo-app/anno/annotation/ensembl-vep/vep -i {vcf_file} --cache --dir_cache /home/escros/.vep --fasta /home/escros/.vep/homo_sapiens/109_GRCh38 --assembly GRCh38 --format vcf --vcf --pick --force_overwrite --no_escape --everything --output_file {output_path}' 
    subprocess.call(vep_command, shell=True)
    if os.path.exists(output_path):
        print("Le fichier output a été créé avec succès!")
    else:
        print("Erreur : le fichier output n'a pas été créé.")

# Annoter le fichier VCF
annotate_vcf('/home/escros/project_prog/demo-app/anno/annotation/TSVC_variants_IonXpress_011.vcf')

# /home/escros/project_prog/demo-app/anno/annotation/ensembl-vep/vep -i /home/escros/project_prog/demo-app/anno/annotation/TSVC_variants_IonXpress_011.vcf --cache --dir_cache /home/escros/project_prog/demo-app/anno/annotation/vep_cache --fasta /home/escros/project_prog/demo-app/anno/annotation/vep_cache/homo_sapiens/109_GRCh38 --assembly GRCh38 --format vcf --vcf --pick --force_overwrite --no_escape --everything --output_file output.csv