#!/bin/bash

if command -v gatk &> /dev/null
then
    echo "GATK est déjà installé"
else 
    echo "Installation de GATK"
    wget https://github.com/broadinstitute/gatk/releases/download/4.2.0.0/gatk-4.2.0.0.zip -O gatk-4.2.0.0.zip
    unzip gatk-4.2.0.0.zip
    rm gatk-4.2.0.0.zip
fi


if command -v samtools &> /dev/null
then
    echo "samtools est déjà installé"
else 
    echo "Installation de samtools"
    wget https://github.com/samtools/samtools/releases/download/1.12/samtools-1.12.tar.bz2 -O samtools-1.12.tar.bz2

    tar xjf samtools-1.12.tar.bz2
    cd samtools-1.12
    ./configure --prefix=`pwd`
    make
    make install
    cd ..
    rm -rf samtools-1.12 samtools-1.12.tar.bz2
fi


if command -v java &> /dev/null
then
    echo "Java est déjà installé"
else 
    sudo apt-get update
    sudo apt-get install -y default-jre default-jdk
fi


if ! file "$(command -v java)" | grep "64-bit"
then
    sudo apt-get install -y default-jre default-jdk
fi



