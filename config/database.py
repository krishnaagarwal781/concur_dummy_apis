from pymongo import MongoClient

client = MongoClient(
    "mongodb://gewgawrav:catax1234@concur.cumulate.live"
)
db = client["concur-apis"]