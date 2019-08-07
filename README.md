# WikimediaDumpDownload

This code offers the possibility to download dumps from Wikidata, Wikipedia, Wiktionary and Wikisource by language (in the futur, it could also download the history of those projets).

Before anything, choose yourself a folder in which to load all wikimedia projects.

Once downloaded, the dump of a wikimedia project gets stored in :

	/wiki***/langue/[history_vs_normal]/$DUMP$

(except for wikidata project which already is multilingual)

on top of those 4 projects is a hidden folder : .temp which is created in that root to temporarily contain the index html files which list the dumps for each projects.

This code can either be run as command line or refered to as a library

1) Command line usage is :

	\-r <...> specify root folder to store dumps (compulsory parameter when allready has been specified : gets stored in the .config)
	 -p <...> wikimedia projet to download
	 -l <...> language
	 -d delete mode (alternative mode : delete dump and path specific to it)
	 -u update-index (updates the html index pointing to dumps, use this argument alone when you want to refresh the indexes to dumps available to download)

*usage*:

	#create a source folder for the project
	python3 WikimediaDumpsBuilder.py -r ~/Documents/

	#update indexes
	python3 WikimediaDumpsBuilder.py -u

	#download projects
	python3 WikimediaDumpsBuilder.py -p wikidata
	python3 WikimediaDumpsBuilder.py -p wiktionary -l fr
...

	#delete projects
	python3 WikimediaDumpsBuilder.py -r -p wikidata -d
	python3 WikimediaDumpsBuilder.py -p wiktionary -l fr -d
...


2) as a library

*usage*:

	import WikimediaDumpsBuilder

	#create a source folder for the project
	wb = WikimediaDumpsBuilder(<path_root_project>)

	#update indexes
	wb.update_index()

	#download projects
	wb.download_dump("wikidata") #download wikidata into it
	wb.download_dump("wikipedia", "fr") #download wikipedia into it

	#delete projects
	wb.delete_dump("wikidata")
	wb.delete_dump("wikipedia", "fr") 
