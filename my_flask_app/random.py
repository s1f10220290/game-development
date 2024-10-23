from pymongo import MongoClient
import random

# MongoDB Atlasに接続
client = MongoClient("mongodb+srv://<username>:<password>@cluster.mongodb.net/test")
db = client['user_database']  # データベース名
collection = db['questions']    # コレクション名

# ランダムに1つの問題を取得
random_problem = collection.aggregate([{"$sample": {"size": 1}}])

for problem in random_problem:
    print(problem["question"])  # 問題文を表示
