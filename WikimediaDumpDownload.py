import argparse
import os
import re
import subprocess

#a class interface to donwload amongst wikimedia's following dumps : wikidata, wikipedia, wikisource and wiktionary.
#This class is meant to be a library or executed through bash with valid parameters.
#Because of the structure of wikimedia's projects, wikidata is internally handeled separatly than other projects.
#When implemented, historical queries will only allow to sum-up downloads for past n days version and never to target only specificaly one. We will consider wikimedia project as oriented to present.
class WikimediaDumpDownloader():

    #Crée un dossier au niveau de path_root_project si celui-ci n'existe pas déjà
    def __init__(self, path_root_project):

        if path_root_project ==  None:
            raise Exception("Specify path to root of dumps.")

        #url vers le json wikidata
        self.url_wikidata_dump = "https://dumps.wikimedia.org/wikidatawiki/entities/"
        #url vers les projets wikimedia à l'exclusion de wikidata
        self.url_wiki_dumps = "https://dumps.wikimedia.org/backup-index.html"
        self.prefix_url_wiki_dumps = "https://dumps.wikimedia.org/"
        #chemin local vers la racine du projet
        self.path_root_project = None

        if path_root_project[:-1]=="/":
            path_root_project=path_root_project[:-1]
        #On regarde si un tel dossier WikimediaDumps existe déjà
        bool_root_exists_allready = False
        for dirname in os.listdir(path_root_project):
            if dirname == 'WikimediaDumps':
                bool_root_exists_allready = True
        #si non on le crée
        self.path_root_project = path_root_project+"WikimediaDumps/"
        if not bool_root_exists_allready:
            os.mkdir(self.path_root_project)

        ##projets

        #si n'ont pas été crée les sous-dossiers par project + temp
        bool_exists_allready = False
        bool_exists_allready2 = False
        bool_exists_allready3 = False
        bool_exists_allready4 = False
        bool_exists_allready5 = False
        for dirname in os.listdir(self.path_root_project):
            if dirname == "wikidata":
                bool_exists_allready = True
            if dirname == "wikipedia":
                bool_exists_allready2 = True
            if dirname == "wikisource":
                bool_exists_allready3 = True
            if dirname == "wiktionary":
                bool_exists_allready4 = True
            if dirname == ".temp":
                bool_exists_allready5 = True

        #si non on les crée
        if not bool_exists_allready:
            os.mkdir(self.path_root_project+"wikidata")
        if not bool_exists_allready2:
            os.mkdir(self.path_root_project+"wikipedia")
        if not bool_exists_allready3:
            os.mkdir(self.path_root_project+"wikisource")
        if not bool_exists_allready4:
            os.mkdir(self.path_root_project+"wiktionary")
        if not bool_exists_allready5:
            os.mkdir(self.path_root_project+".temp")

        ##INDEX HTML
        #on verifie si n'ont pas été crée les sous-dossiers index_wikidata et index_wikis
        bool_exists_allready = False
        bool_exists_allready2 = False
        for dirname in os.listdir(self.path_root_project+".temp/"):
            if dirname == "index_wikidata":
                bool_exists_allready = True
            if dirname == "index_wikis":
                bool_exists_allready2 = True

        #si effectivement non on les crée
        if not bool_exists_allready:
            os.mkdir(self.path_root_project+"/.temp/index_wikidata")
        if not bool_exists_allready2:
            os.mkdir(self.path_root_project+"/.temp/index_wikis")


    #saves the path to index created in self.path_index_wikidata_dumps which is of html index page for download page for the dumps for wikidata
    def wget_url_wikidata_dump(self):
        #delete all previous files downloaded in the same emplacement
        for root, dirs, files in os.walk(self.path_root_project+"/.temp/index_wikidata"):
            for filename in files:
                os.remove(self.path_root_project+"/.temp/index_wikidata/"+filename)
        subprocess.run(["wget", self.url_wikidata_dump, "--directory-prefix="+self.path_root_project+"/.temp/index_wikidata"])

        #searching for the file name
        file_downloaded = ""
        for root, dirs, files in os.walk(self.path_root_project+"/.temp/index_wikidata"):
            for filename in files:
                file_downloaded =  filename
        self.path_index_wikidata_dumps = self.path_root_project+"/.temp/index_wikidata/"+file_downloaded

    #saves the path to index created in self.path_index_wikis_dumps which is of html index page for download page for the dumps
    def wget_url_wiki_dumps(self):
        #delete all previous files downloaded in the same emplacement
        for root, dirs, files in os.walk(self.path_root_project+"/.temp/index_wikis"):
            for filename in files:
                os.remove(self.path_root_project+"/.temp/index_wikis/"+filename)
        subprocess.run(["wget", self.url_wiki_dumps, "--directory-prefix="+self.path_root_project+"/.temp/index_wikis"])

        #searching for the file name
        file_downloaded = ""
        for root, dirs, files in os.walk(self.path_root_project+"/.temp/index_wikis"):
            for filename in files:
                file_downloaded =  filename
        self.path_index_wikis_dumps = self.path_root_project+"/.temp/index_wikis/"+file_downloaded


    def update_index(self):
        self.wget_url_wikidata_dump()
        self.wget_url_wiki_dumps()


    '''#from html index file we extract the table : date - url ; keeping for further wikidata's dumps per date
    ##but for now just the url of latest json
    def get_table_wikidata(self):
        reg_extr_url = re.compile("^<a href=([^>]+)>([^>]+)</a>")
        with open(self.path_index_wikidata_dumps) as fp:
            for line in fp:
                matcher_reg_extr = reg_extr_url.search(line)
                if not matcher_reg_extr == None:
                    value_href = matcher_reg_extr.group(1)
                    print(value_href)
        #delete all previous files downloaded in the same emplacement
        for root, dirs, files in os.walk(self.path_root_project+"wikidata"):
            for filename in files:
                os.remove(self.path_root_project+"wikidata/"+filename)
        subprocess.run(["wget", self.url_wikidata_dump+"/latest-all.json.bz2", "--directory-prefix="+self.path_root_project+"wikidata"])
    '''

    #from html index file we extract a list : (project - langue - date - url) ; for other wikimedia projects
    def get_table_wikis(self, path_index_wikis_dumps):
        reg_extr_url = re.compile("^<li>[0-9 :\-]{20}<a href=\"([^\"]+)\"")
        list_href = []
        with open(self.path_index_wikis_dumps) as fp:
            for line in fp:
                matcher_reg_extr = reg_extr_url.search(line)
                if not matcher_reg_extr == None:
                    value_href = matcher_reg_extr.group(1)
                    list_href.append(value_href)
        return list_href

    #verifies if path exists else creates a path to it,
    #wget --directory-prefix=self.path_root_project/project/langue/date
    def download_dump(self, project, langue=None):#, date):
        #contiendra le path du fichier téléchargé
        retour = ""
        #téléchargement du latest wikidata
        if project=="wikidata":
            if not langue=="None":
                raise Exception("Wikidata is multilingual, should not target a language while extracting wikidata.")
            else:
                #effacer la version précédente
                for root, dirs, files in os.walk(self.path_root_project+"wikidata"):
                    for filename in files:
                        os.remove(self.path_root_project+"wikidata/"+filename)
                subprocess.run(["wget", self.url_wikidata_dump+"/latest-all.json.bz2", "--directory-prefix="+self.path_root_project+"wikidata"])
                zip=""
                for root, dirs, files in os.walk(self.path_root_project+"wikidata"):
                    for f in files:
                        zip = f
                subprocess.run(["bzip2", "-d", self.path_root_project+"wikidata/"+zip])
                #return the file's path
                filename = zip[:-4]
                retour = self.path_root_project+"wikidata/"+filename

        #téléchargement du latest wikipedia pour la langue ciblée
        else:
            if langue=="None":
                raise Exception("Specify language")
            #instanciation de la structure project 2 langue 2 date  2 url
            table_wiki = self.get_table_wikis(self.path_index_wikis_dumps)
            project2prefix_suffixe_reg = {"wikipedia": re.compile("^(.+)(wiki)$"),"wikisource":re.compile("^(.+)(wikisource)$"),"wiktionary":re.compile("^(.+)(wiktionary)$")}
            #recherche de l'url de la page contenant le lien de téléchargement
            target_url = ""
            link_date = ""
            link_langue = ""
            link_project = ""
            #the final dump to download if a wiki is the first href of this form
            reg_page_dump_extractor = re.compile("<li class='file'><a href=\"([^\"]+)\">")
            for link in table_wiki:
                splitted=link.split('/')
                link_date = splitted[1]
                link_lg_project = splitted[0]
                #print(link_lg_project)
                for key in project2prefix_suffixe_reg.keys():
                    #print("\t"+key, project2prefix_suffixe_reg)
                    matcher_reg_extr = project2prefix_suffixe_reg[key].search(link_lg_project)
                    if not matcher_reg_extr == None:
                        langue_read = matcher_reg_extr.group(1)
                        project_read = key #extracted "wiki" but wants "wikipedia"
                        #print(langue_read, langue, project_read, project)
                        if langue_read == langue and project_read == project:
                            link_langue = langue
                            link_project = matcher_reg_extr.group(2)#extracted "wiki"
                            target_url = self.prefix_url_wiki_dumps+link_langue+link_project+"/"+link_date
                            #effacer les fichiers temps précédentes
                            for root, dirs, files in os.walk(self.path_root_project+".temp/"):
                                for f in files:
                                    try:
                                        os.remove(self.path_root_project+".temp/"+f)
                                    except(FileNotFoundError):
                                        pass
                            #wget ther target_url in temp folder
                            subprocess.run(["wget", target_url, "--directory-prefix="+self.path_root_project+".temp"])

                            #TODO : wget final download and erease target_url
                            for root, dirs, files in os.walk(self.path_root_project+".temp"):
                                for filename in files:
                                    with open(self.path_root_project+".temp/"+filename) as fp:
                                        for line in fp:
                                            matcher_url_dump = reg_page_dump_extractor.search(line)
                                            #breaks file reading at first match
                                            if not matcher_url_dump == None:
                                                href = "https://dumps.wikimedia.org"+matcher_url_dump.group(1)
                                                bool_exists_allready = False
                                                for dirname in os.listdir(self.path_root_project+project):
                                                    if dirname == langue:
                                                        bool_exists_allready = True

                                                #si non on les crée
                                                if not bool_exists_allready:
                                                    os.mkdir(self.path_root_project+project+"/"+langue)
                                                else:#on supprime les anciens fichiers s'y trouvant
                                                    for root, dirs, files in os.walk(self.path_root_project+project+"/"+langue):
                                                        #only one file so safe to break
                                                        for f in files:
                                                            filename = f
                                                            os.remove(self.path_root_project+project+"/"+langue+"/"+f)


                                                #print("href", href)
                                                #print("path", self.path_root_project+project+"/"+langue)

                                                #y télécharger le dump final
                                                subprocess.run(["wget", href, "--directory-prefix="+self.path_root_project+project+"/"+langue])
                                                #le decompresser
                                                zip = ""
                                                for root, dirs, files in os.walk(self.path_root_project+project+"/"+langue):
                                                    #only one file so safe to break
                                                    for f in files:
                                                        zip = f
                                                        subprocess.run(["bzip2", "-d", self.path_root_project+project+"/"+langue+"/"+filename])
                                                        break
                                                #return the file's path
                                                filename = zip[:-4] #taking ".bz2 away"
                                                retour = self.path_root_project+project+"/"+langue+"/"+filename
                                                break

                                #effacer fichier du temp
                                for root, dirs, files in os.walk(self.path_root_project+".temp"):
                                    #only one file so safe to break
                                    for f in files:
                                        filename = f
                                        os.remove(self.path_root_project+".temp/"+f)
                            #effacer le dossier temps
                            for root, dirs, files in os.walk(self.path_root_project+".temp"):
                                for filename in files:
                                    os.remove(self.path_root_project+".temp/"+filename)
                            os.rmdir(self.path_root_project+".temp")
        return retour

    #effacer le dossier langue s'il existe
    def delete_dump(self, project, langue=None):
        if project=="wikidata":
            if not langue=="None":
                raise Exception("Wikidata is multilingual, should not target a language while extracting wikidata.")
            else:
                for root, dirs, files in os.walk(self.path_root_project+project):
                    for file in files:
                        os.remove(self.path_root_project+project+"/"+file)
        else:
            for root, dirs, files in os.walk(self.path_root_project+project):
                for dir in dirs:
                    if dir == langue:
                        for root, dirs, files in os.walk(self.path_root_project+project+"/"+langue):
                            for file in files:
                                os.remove(self.path_root_project+project+"/"+langue+"/"+file)
                        os.rmdir(self.path_root_project+project+"/"+langue)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='A partir de la racine donné en paramètre, permet de télécharger/supprimer un dump voulu')

    #root folder to main folder containing the dumps to be downloaded
    parser.add_argument("-r", "--root", help="Root for storing dumps. Compulsory parameter when allready has been specified", default="None")
    #one of wikidata, wikipedia, wikisource and wiktionary
    parser.add_argument("-p", "--project", help="Project targeted", default="None")    #if project is wikidata, this argument can be skipped
    parser.add_argument("-l", "--langue", help="Language targeted.", default="None")
    #if d request deletion of language in project
    parser.add_argument("-d", "--delete", help="Request deletion of given language in given project. (no argument)", action='store_true', default="None")
    #use this arument to update index files pointing to dumps
    parser.add_argument("-u", "--update_index", help="Update html index files. Use it when you want to update the date of the dumps, don't if you want to keep the same date as previous session. (no argument)", action='store_true', default="None")

    '''#on ignorera cette possibilité pour le moment il faut donc le laisser à son default "latest"
    parser.add_argument("-t", "--time", help="télécharger les dumps des d derniers jours (default = latest).",  default='latest')
    '''
    args = parser.parse_args()

    update_index=args.update_index
    path_root_project = args.root
    project = args.project
    langue = args.langue
    delete = args.delete

    #try to upload from file if none in cmd line arguments
    if path_root_project == "None":
        try:
            with open("config") as fp:
                for line in fp:
                    path_root_project = line
        except(FileNotFoundError):
            raise ValueError("Please specify a path to command line arguments (-r)")

    #throw error if still no path
    if path_root_project == "None":
        raise ValueError("Please specify a path to command line arguments (-r)")

    wikimedia_dumps = WikimediaDumpDownloader(path_root_project)
    config_file = open("config", "w")
    config_file.write(path_root_project)
    config_file.close()

    #throw error if update-index is used uncorrectly
    if not update_index == "None":
        if not project == "None":
            raise ValueError("Do not specify project if updating indexes.")
        elif not langue == "None":
            raise ValueError("Do not specify languages if updating indexes.")
        elif not delete == "None":
            raise ValueError("Do not specify deletion if updating indexes.")
        else:
            wikimedia_dumps.update_index()
    else:
        if delete == "None":
            path = wikimedia_dumps.download_dump(project, langue)
        else:
            wikimedia_dumps.delete_dump(project, langue)
        #date = args.date
