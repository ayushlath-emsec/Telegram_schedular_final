from databaseConnection import *
import pandas as pd
from datetime import datetime , timezone ,date
from pymongo import MongoClient
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest , GetHistoryRequest ,GetDialogsRequest
from telethon.utils import get_input_peer
from telethon.tl.types import InputPeerEmpty
from bson.objectid import ObjectId
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from telethon.tl.types import InputPeerUser
import csv
import asyncio

def scrapSuccess(func):
    collection.update_one({"url":func},{'$set':{"isUrgent":False,"status":"done","time":datetime.now(),"failedCount" : 0}})
def scrapFailed(func , failedCount):
    collection.update_one({"url":func},{'$set':{"isUrgent":False,"status":"error","time":datetime.now(),"failedCount" : failedCount+1}})
def scrapRunning(func):
    collection.update_one({"url":func},{'$set':{"status":"running","time":datetime.now()}})

now=datetime.now()
CreatedDate = now.strftime("%d/%m/%y %H:%M:%S")
CreatedDate = datetime.strptime(CreatedDate,"%d/%m/%y %H:%M:%S")
CreatedDate = datetime.timestamp(CreatedDate)
# add your function here 

async def telegram_scrap_func(url,_id):
    api_id = 23638228
    api_hash = '80a5e4bfe054a1c735b1bf69b4205d27'
    phone = '+919369973479'
    name = "anshu"
    client = TelegramClient('anshu', api_id, api_hash)

    try:
        await client.start()
    except PhoneNumberInvalidError:
        print('Invalid phone number!')
        return

    channel = await client.get_entity(url)
    await client(JoinChannelRequest(channel))

    if channel.megagroup:
        chat_type = 'Group'
    else:
        chat_type = 'channel'
    print(chat_type)

    user_count=channel.participants_count
    print("Connected..")
    chat=[]
    media_link=[]
    media1_status=[]
    channel_id=[]
    channel_name=[]
    total_user_count=[]
    createdAt_date=[]
    chat_Date=[]
    chat_ID=[]
    user_Id=[]
    channel_creation_date=[]
    count=0
    doc = collection.find_one({'_id':ObjectId(_id)})
    try:
        from_id = int(doc['last_scrap_id'])
    except:
        from_id = 0
    msg = client.iter_messages(channel)
    async for message in msg:
        if message.id > from_id:   
            if message.id==1:
                # print(message.fwd_from.from_id)
                channel_creation_date.append(message.date.strftime('%d/%m/%Y %H:%M:%S'))
            else:
                channel_creation_date.append(None)
            if message.action is None: 
                try:
                    if message.message:
                        user_chat=message.message
                        try:
                            url_title=message.media.webpage.title
                            if url_title:
                                user_chat=f"{user_chat}\nTitle: {url_title}"
                        except:
                            pass 
                    else:
                        user_chat=None        
                except:
                        pass
                try:       
                    if message.photo:
                        user_media_link= f"image link( {url}/{message.id} )"
                    elif message.document:
                        if message.document.mime_type=='video/mp4':
                            user_media_link=f"video link( {url}/{message.id} )"
                        else:
                            user_media_link=f"file link( {url}/{message.id} )"
                            try:
                                file_name=message.document.attributes[-1].file_name
                                if file_name:
                                    user_media_link=f"{user_media_link}\nfile name: {file_name}"      
                            except:
                                pass 
                    else:
                        user_media_link=None                   
                except:
                    pass            
                if user_chat==None:
                    media1=True
                else:
                    media1=False
                try:
                    user_Id.append(message.from_id.user_id)
                except:
                    user_Id.append(None)
                    
                chat.append(user_chat)
                media_link.append(user_media_link)
                media1_status.append(media1)         
                channel_id.append(channel.id)
                channel_name.append(channel.title)
                chat_ID.append(message.id)
                chat_Date.append(message.date.strftime('%d/%m/%Y %H:%M:%S'))
                createdAt_date.append(CreatedDate)
                total_user_count.append(channel.participants_count)
                count+=1
        else:
            print("Channel already scrapped upto date")
            break
            return           
    # inserting
    print(count)
    await client.disconnect()
    data = {'channel_id':channel_id,'chat':chat,'user_id':user_Id,'media_link':media_link,"is_media":media1_status,'chat_ID': chat_ID,'chat_Date': chat_Date,'createdAt':int(createdAt_date)}
    df1 = pd.DataFrame(data)
    print(df1)
    docs = df1.to_dict('records')
    collection1.insert_many(docs)

    if len(chat_Date)>0 and channel_creation_date[0]!=None:
        collection.update_one({"_id":ObjectId(_id)},{ "$set": { 'channel_id':channel.id,'channel_name':channel.title,'total_user':channel.participants_count,'channel_username':channel.username,'is_group':channel.megagroup,'channel_creation_date':channel_creation_date[0],"last_scrap_id":chat_ID[0]}})
    elif channel_creation_date[0]==None:
        collection.update_one({"_id":ObjectId(_id)},{ "$set": { 'channel_id':channel.id,'channel_name':channel.title,'total_user':channel.participants_count,'channel_username':channel.username,'is_group':channel.megagroup,"last_scrap_id":chat_ID[0]}})
    print("Data Inserted!!")
