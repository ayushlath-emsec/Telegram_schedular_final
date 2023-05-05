from flask import Flask
from databaseConnection import *
from mainScrap import *
from datetime import date,datetime,timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from flag import *
import asyncio

# Flask..
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Telegram'
def telegram_scrapping():
    print(datetime.now())
    if (isNodeBusy!=True):
        if collection.count_documents({'isUrgent':True})>0:
            print(f"No of urgent Channel :{collection.count_documents({'isUrgent':True})}")
            _urgent = collection.find({"isUrgent":True,"status":{"$ne":"running"}})
            try:
                getfunction(_urgent[0])
            except:
                pass 
        else:  
            d = datetime.today() - timedelta(hours=0, minutes=30)
            if collection.count_documents({"status":{"$ne":"running"},"time":{"$lte":d}})>0:
                _not_urgent =collection.find({"status":{"$ne":"running"},"time":{"$lte":d}})           
                getfunction(_not_urgent[0])    
            else:
                print("Every Channel Scrapped!!") 
    else:
        print("Schedular is Busy!!")


telegram_scrapping()
# Scheduler..
async def main():
    sched = BackgroundScheduler(daemon = True)
    sched.add_job(telegram_scrapping,'interval',minutes=20)
    sched.start()

@app.route('/')
def hello_world():
	return 'Hello Telegram!!'
       
# main flask function
if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    loop.close()     
    app.run(debug=True)