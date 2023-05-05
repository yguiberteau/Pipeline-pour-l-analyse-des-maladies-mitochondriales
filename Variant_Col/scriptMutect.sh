#!/bin/bash


export PATH="/home/parallels/Desktop/ProjetProgrammation/gatk-4.2.0.0:$PATH"

gatk Mutect2 \

-R "/home/parallels/Desktop/ProjetProgrammation/IonXpress_011.fasta" \ \

--mitochondria \
-I "/home/parallels/Desktop/ProjetProgrammation/IonXpress_011.bam"\
-O mitochondria.vcf.gz
