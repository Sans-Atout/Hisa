from urllib3 import PoolManager
from time import sleep
from random import randint
from bs4 import BeautifulSoup

# the PoolManager for the request
HTTP_REQUESTER = PoolManager()

#the defaut header use for making website request
HEADERS =   { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

def getSniffer(url:str,minWait:int=10,maxWait:int=20,t:int=10,p= None):
    """
        Function that executes a GET request and outputs the corresponding
        sniffing tool.

        (param) url     : [str] the get request url
        (param) minWait : [int] the minimum time to wait before making the request
                          (in second) the default value is 30s
        (param) maxWait : [int] the maximum time to wait before making the request
                          (in second) the default value is 60s
        (param) t       : [int] the timeout time (in second). the default value is 10s
        (param) p       : the body param of the request. the default value is None

        (return) tupple of value compose of :
                        [boolean]   : does the request succed or not
                        [int]       : the response status (if time the response
                                      status is 0)
                        [bs4]       : the bs4 object
    """
    sleep_random = randint(minWait,maxWait)
    sleep(sleep_random)
    try:
        response = HTTP_REQUESTER.request("GET",url,p,HEADERS,timeout=t)
        if response.status != 200:
            return False, response.status, response.data
        return True, response.status, BeautifulSoup(response.data, features="lxml")
    except Exception as e:
        return False, 0 , e
