# Log librairy
from configparser import ConfigParser
from python_tracer.Logger import VerboseLevel,Logger

# project import
from src.scrapper import getSniffer

# global import 
from os import listdir
from json import load

# Librairie global variable
_GITHUB_URL = "https://github.com/manami-project/anime-offline-database/tags"

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
        if ".json" in _file[len(_file)-4:]:
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
