# Etape de construction : Clone du referentiel GitHub
FROM alpine/git as clone
WORKDIR /app
RUN git clone https://github.com/yguiberteau/Pipeline-pour-l-analyse-des-maladies-mitochondriales.git

# Utilisez l'image de base Ubuntu 18.04
FROM ubuntu:18.04

####Annotation####

# Mise a jour des paquets et installation des dependances necessaires
RUN apt-get update && apt-get -y install \
    build-essential \
    git \
    libpng-dev \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev \
    perl \
    perl-base \
    unzip \
    wget \
    python \
    python-pip \
    && rm -rf /var/lib/apt/lists/*

# Copie des fichiers de configuration VEP dans le conteneur
COPY vep.ini /opt/vep/.vep/vep.ini

# Installation de VEP et des dependances Perl
RUN wget https://github.com/Ensembl/ensembl-vep/archive/RELEASE_109.zip && \
    unzip RELEASE_109.zip && \
    rm RELEASE_109.zip && \
    mv ensembl-vep-RELEASE_109 /opt/vep && \
    cd /opt/vep && \
    perl INSTALL.pl -a a -n -s homo_sapiens -y GRCh37 && \
    cd -

# Installation des dependances et copie du script Python
COPY --from=clone /app/Pipeline-pour-l-analyse-des-maladies-mitochondriales/Annotation/anno_panda.py /app/anno_panda.py
WORKDIR /app
RUN pip install pandas

# Definition de la commande d'execution du conteneur
CMD ["python", "/app/anno_panda.py"]
