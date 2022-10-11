# Log librairy
from configparser import ConfigParser
from python_tracer.Logger import VerboseLevel,Logger

# project import
from src.scrapper import getSniffer

# global import 
from os import listdir, remove, rename
from shutil import rmtree
from json import load
from requests import get
from tarfile import open as open_tar

# Librairie global variable
_GITHUB_URL = "https://github.com/manami-project/anime-offline-database/tags"
_DOWNLOAD_URL = "https://github.com/manami-project/anime-offline-database/archive/refs/tags/%(tag_)s.tar.gz"

# Log variable initialisation
config = ConfigParser()
config.read("hisa.ini")
log_level   = int(config.get("log", "prod_env"))
log_path    = config.get("log", "path")
extension   = config.get("log", "extension")

log = Logger(log_path,log_level,service_name="anime", log_extension=extension)

def get_anime_offline():
    """
        Function that load the last anime offline database from an open-source project

        (param) None

        (return) anime_offline_db [json] : the anime offline database in an json object
    """
    all_aodb = listdir("./input/")
    all_json_file = []

    # D
    for _file in all_aodb:
        if ".json" in _file:
            all_json_file.append(_file)

    if len(all_json_file) == 0:
        log.warning("No anime offline database found")

    is_ok, _status, github_page = getSniffer(_GITHUB_URL)

    # Testing in request was successfull
    if not is_ok:
        log.error("Request responde with status %(status)s" % {"status" : _status})
        log.debug(github_page)
    
    # If no json file and no file in offline then program panic
    if not is_ok and len(all_json_file) == 0:
        log.fatal("Can not continue this program")
        exit(-1)

    # If at least one json and resquest fail then we load the lastest json file downloaded
    if not is_ok and len(all_json_file) > 0:
        log.info("We found at least one json file so we can continue the program")
        json_path ="./input/"+ str(sorted(all_json_file)[-1])
        return load(open(json_path,"r"))

    # Else, request sucess so we need to know if we have downloaded the lastest anime offline
    # database from the open source project
    last_tags_div = github_page.find("div", class_="commit js-details-container Details")
    _last_realese_links = last_tags_div.find("a",class_="Link--primary",href=True)
    _tags = _last_realese_links.text
    
    for _file in all_aodb:
        if _tags in _file and ".json" in _file:
            log.info("We allready have the last version")
            return load(open("./input/%(tags)s.json" % {"tags" : _tags}, "r" ))
    
    ## We need to download the file and 
    log.info("[1/6] Downloading last release")
    response = get(_DOWNLOAD_URL % {"tag_" : _tags})
    tar_file = open("./input/tmp.tar.gz", "wb")
    tar_file.write(response.content)
    log.info("[2/6] Extract data")
    extractor = open_tar("./input/tmp.tar.gz")
    extractor.extract("anime-offline-database-%(version)s/anime-offline-database-minified.json" % {"version" : _tags},"./input/")
    log.info("[3/6] Remove original file")
    remove("./input/tmp.tar.gz")
    log.info("[4/6] Rename mimified JSON file")
    _input_aodbm = "./input/anime-offline-database-%(version)s/anime-offline-database-minified.json" % {"version" : _tags}
    _output_aodbm = "./input/%(version)s.json" % {"version" : _tags}
    rename(_input_aodbm, _output_aodbm)
    log.info("[5/6] Remove unwanted folder")
    rmtree( "./input/anime-offline-database-%(version)s/" % {"version" : _tags})
    log.done("[6/6] Operation completed")
    return load(open("./input/%(tags)s.json" % {"tags" : _tags}, "r" ))