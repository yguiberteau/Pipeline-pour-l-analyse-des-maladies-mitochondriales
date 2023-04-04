# Pipeline-pour-l-analyse-des-maladies-mitochondriales


#Execution haplogrep

sudo apt install openjdk-11-jre-headless  #install java

wget https://github.com/genepi/haplogrep3/releases/download/v3.2.1/haplogrep3-3.2.1-linux.zip

sudo apt install unzip #installe la fonction unzip

unzip haplogrep3-3.2.1-linux.zip  #unzip le zip

./haplogrep3 #execute haplogrep3 et affiche toutes les commandes

./haplogrep3 classify




#Execution eKLIPse

sudo apt install python2

pip install biopython #install biopython

pip install tqdm #install tqdm

wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.7.1/ncbi-blast-2.7.1+-x64-linux.tar.gz #install blast

tar -xvzf ncbi-blast-2.7.1+-x64-linux.tar.gz #decompresse

wget https://github.com/dooguypapua/eKLIPse/blob/master/eKLIPse_v2-1.zip #attention fichier erroné

unzip eKLIPse_v2-1.zip 

cd eKLIPse_v2-1 #se mettre dans le reportoire du fichier dezipé

python eKLIPse.py

