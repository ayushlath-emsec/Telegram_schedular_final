from scrapTelegram import *
from databaseConnection import collection , collection1
from flag import *
import asyncio
# Scrapping...

def getfunction(func):
    print("Scrapping in progress...")
    _url = func['url']
    failedCount = func['failedCount']
    _id = func['_id']
    isNodeBusy = True
    try:    
        print(_url + " is scrapping now")
        scrapRunning(_url)
        asyncio.run(telegram_scrap_func(_url,ObjectId(_id)))
        scrapSuccess(_url)
        print(_url + " Scrapped Succesfully")
    except:
        print(_url + " Scrapping Failed")
        print("FailedCount of Telegram Channel : " , (failedCount+1) )
        scrapFailed(_url , failedCount)       
        
    isNodeBusy = False