import pymongo

# MongoDb Connection...
client =pymongo.MongoClient("mongodb+srv://emseccomandcenter:TUXnEN09VNM1drh3@cluster0.psiqanw.mongodb.net/?retryWrites=true&w=majority")
db =client['Telegram_Server']
collection =db['channel_info']
collection1 = db['Data']
print ("total channel in collection:", collection.count_documents( {} ))