#appel de gatk
export PATH="/net/cremi/mallecorre/Bureau/projetProgrammation/gatk-4.2.0.0/:$PATH"
gatk Mutect2 \
-R "/net/cremi/mallecorre/Bureau/projetProgrammation/IonXpress_011.fasta" \
-I "/net/cremi/mallecorre/Bureau/projetProgrammation/IonXpress_011.bam" \
-O "/Users/mallorylecorre/Desktop/Projet/fichier.vcf" \
--mitochondria-mode
