import os
import subprocess
import tarfile
import platform
import wget
import sys
import ctypes

#import urllib.request
#url = "https://www.perl.org/get.html"
#html = urllib.request.urlopen(url).read()
#perl_download_url = "https://www.activestate.com/products/perl/downloads/thank-you?dl=http%3A%2F%2Fdownloads.activestate.com%2FActivePerl%2Fwindows%2F64%2F5.32%2FActivePerl-5.32.1.001-MSWin32-x64-404865.exe"
#urllib.request.urlretrieve(perl_download_url, "ActivePerl-5.32.1.001-MSWin32-x64-404865.exe")

# fonction pour obtenir le chemin vers le répertoire où stocker les données VEP
def get_vep_cache_dir():
    # vérifier si le répertoire existe dans le dossier utilisateur
    home_dir = os.path.expanduser("~")
    cache_dir = os.path.join(home_dir, ".vep")
    if not os.path.exists(cache_dir):
        # si le répertoire n'existe pas, le créer
        os.makedirs(cache_dir)
    return cache_dir

# Vérifier si Perl est installé
def is_perl_installed():
    try:
        subprocess.check_output(['perl', '-v'])
        return True
    except:
        return False
    
# Installer les dépendances sous Linux
def install_dependencies_linux():
    if not is_perl_installed():
        subprocess.call(['sudo', 'apt-get', 'update'])
        subprocess.call(['sudo', 'apt-get', 'install', '-y', 'perl', 'cpanminus', 'htslib-tools', 'libssl-dev', 'liblzma-dev'])
        subprocess.call(['sudo', 'cpanm', 'DBI'])
        subprocess.call(['sudo', 'cpanm', 'DBD::mysql', 'Archive::Zip', 'Config::IniFiles', 'Module::Build', 'Bio::DB::HTS', 'IO::Socket::SSL'])

# Installer les dépendances sous Windows
#Spécifier chemin
def install_dependencies_windows():
    #subprocess.call(['C:\\Program Files\\Git\\usr\\bin\\perl.exe', '-MCPAN', '-e', 'install', 'DBI', 'DBD::mysql', 'Archive::Zip', 'Config::IniFiles', 'Module::Build', 'Bio::DB::HTS', 'IO::Socket::SSL'],stderr=subprocess.STDOUT)
    if not is_perl_installed():
        subprocess.call(['choco', 'install', 'strawberryperl', '-y'])
        subprocess.call(['C:\\Program Files\\Git\\usr\\bin\\perl.exe', '-MCPAN', '-e', 'install', 'DBI'], stderr=subprocess.STDOUT)
    subprocess.call(['C:\\Program Files\\Git\\usr\\bin\\perl.exe', 'vep/INSTALL.pl', '--NO_TEST', '--AUTO', 'all'])

# Installer les dépendances sous Macos   
def install_dependencies_macos():
    if not is_perl_installed():
        subprocess.call(['brew', 'install', 'perl'])

# fonction pour télécharger et extraire les données VEP
def download_vep():
    cache_dir = get_vep_cache_dir()
    url = "http://ftp.ensembl.org/pub/release-104/variation/indexed_vep_cache/homo_sapiens_vep_104_GRCh38.tar.gz"
    file_name = os.path.basename(url)
    file_path = os.path.join(cache_dir, file_name)

    if not os.path.exists(file_path):
        # télécharger le fichier depuis le lien URL
        print("Téléchargement de VEP ...")
        wget.download(url, file_path)
        print("\nTéléchargement terminé !")

    # extraire le fichier tar.gz téléchargé
    print("Extraction de VEP ...")
    with tarfile.open(file_path, "r:gz") as tar:
        tar.extractall(path=cache_dir)
    print("Extraction terminée !")

# Télécharger la base de données de référence
def download_reference():
    subprocess.call(['perl', 'vep/INSTALL.pl', '--NO_TEST', '--AUTO', 'all'])

#Ne fonctionne que sous windows
def run_as_admin():
    if os.name == 'nt':
        # Check if the current user has administrative privileges
        try:
            isAdmin = ctypes.windll.shell32.IsUserAnAdmin()
        except:
            isAdmin = False

        # If the current user is not an administrator, prompt for elevation
        if not isAdmin:
            params = ' '.join([sys.executable] + sys.argv)
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
            sys.exit(0)

# Annoter le fichier VCF
#def annotate_vcf(vcf_file):
#    vep_command = './vep/vep -i {} --cache --offline --dir_cache ~/.vep --fasta ~/.vep/homo_sapiens/103_GRCh38/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz --assembly GRCh38 --format vcf --vcf --fields "Uploaded_variation,Location,Allele,Gene,SYMBOL,Feature_type,Consequence" --pick --force_overwrite --no_stats --no_escape --everything --fork 8 --output_file output.csv'.format(vcf_file)
#    subprocess.call(vep_command, shell=True)

cache_dir = get_vep_cache_dir()

# Télécharger VEP
download_vep()

# vérifier la présence des données VEP
vep_cache_dir = get_vep_cache_dir()
if len(os.listdir(vep_cache_dir)) == 0:
    # télécharger les données VEP si elles ne sont pas déjà présentes
    download_vep()
    print("Téléchargement et extraction de VEP terminés !")
else:
    print("Les données VEP sont déjà présentes dans le répertoire :", vep_cache_dir)

# Installer les dépendances en fonction de l'OS
os_type = platform.system()
if os_type == 'Linux':
    install_dependencies_linux()
elif os_type == 'Windows':
    #S'assurer que le fichier est en admin pour pouvoir installer les packages comme il faut
    run_as_admin()
    install_dependencies_windows()
elif os_type == 'Darwin':
    install_dependencies_macos()
else:
    print("Sorry, this script does not support your operating system")

# Télécharger la base de données de référence
download_reference()

# Annoter le fichier VCF
#annotate_vcf('input.vcf')