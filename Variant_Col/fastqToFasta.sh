#!/bin/bash

seqtk seq -a IonXpress_011.fastq > IonXpress_011.fasta
samtools faidx IonXpress_011.fasta
