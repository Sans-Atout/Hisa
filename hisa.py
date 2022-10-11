#!/bin/python
# Log librairy
from configparser import ConfigParser
from python_tracer.Logger import VerboseLevel,Logger

# Log variable initialisation
config = ConfigParser()
config.read("hisa.ini")
log_level   = int(config.get("log", "prod_env"))
log_path    = config.get("log", "path")
extension   = config.get("log", "extension")

log = Logger(log_path,log_level,service_name="hisa", log_extension=extension)
log.info("The goal of this programm is to extract and format our database")
log.debug("Loading librairies")
from src.get_offline_db import get_anime_offline
log.done("[1/2] Project librairies")

log.done("[2/2] Global librairies")

_aodb = get_anime_offline()