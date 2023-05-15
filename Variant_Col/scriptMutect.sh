#!/usr/bin/env python3
import os

GATK = "/gatk/gatk-4.2.0.0/gatk"

FichierBam = "/data/input.bam"

fichierFastaReference = "/Users/mallorylecorre/Desktop/ProjetProg/REF.fasta"

# Chemin de sortie pour le fichier VCF
outputFichierVcf = "/data/output.vcf"

cmd = f"{GATK} HaplotypeCaller " \
      f"-R {fichierFastaReference} " \
      f"-I {FichierBam} " \
      f"-O {outputFichierVcf} " \
      "--emit-ref-confidence GVCF " \
      "--stand-call-conf 20 " \
      "--read-filter MappingQualityReadFilter " \
      "--filter-mapping-quality 30 " \
      "--filter-expression \"QUAL < 30.0\" " \
      "--filter-name \"LowQual\" " \
      "--dbsnp /path/to/dbSNP.vcf " \
      "--mitochondria-mode " \
      "--interval-padding 100"

os.system(cmd)
