#!/usr/bin/env python3
import os

GATK = "/gatk/gatk-4.2.0.0/gatk"

FichierBam = "/data/sorted.bam"

fichierFastaReference = "/data/REF.fasta"

outputFichierVcf = "/data/output.vcf"

cmd = f"{GATK} Mutect2 " \
      f"-R {fichierFastaReference} " \
      "--mitochondria " \
      f"-I {FichierBam} " \
      f"-O {outputFichierVcf}.gz"

os.system(cmd)
