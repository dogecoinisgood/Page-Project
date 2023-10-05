import os, sqlite3, json
from threading import Thread


base_path= os.path.abspath(os.path.dirname(__file__))
db_path= os.path.abspath(os.path.join(base_path, "crawler/data/data.db"))


# -------------------------  資料庫部分  -------------------------
createTableText= {
    "youtube":'''CREATE TABLE IF NOT EXISTS youtube(
        ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        link TEXT,
        videoContent TEXT,
        channel_name TEXT,
        channel_ID TEXT,
        subscribers INTEGER,
        views INTEGER,
        likes INTEGER,
        dislikes INTEGER,
        category TEXT
    );''',
    "keywords":'''CREATE TABLE IF NOT EXISTS youtube(
        ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        keywords TEXT
    );'''
}

def getCols(tableName):
    conn= sqlite3.connect(db_path)
    cursor= conn.cursor()
    cursor.execute(createTableText[tableName])
    cursor.execute(f"PRAGMA TABLE_INFO({tableName})")
    return [col[1] for col in cursor.fetchall()]


# cols= {"ID":"INTEGER", "link":"TEXT", ...}
def updateCols(tableName, newCols):
    conn= sqlite3.connect(db_path)
    cursor= conn.cursor()
    cursor.execute(createTableText[tableName])
    cursor.execute(f"PRAGMA TABLE_INFO({tableName})")
    cols= [col[1] for col in cursor.fetchall()]
    for col in newCols:
        if col not in cols:
            cursor.execute(f"ALTER TABLE {tableName} ADD COLUMN {col} {newCols[col]} DEFAULT '';")


def getData(tableName, commamd):
    conn = sqlite3.connect(db_path)
    cursor= conn.cursor()
    cursor.execute(createTableText[tableName])
    result= cursor.execute(commamd)
    # conn.close()
    return result.fetchall()


def insertData(tableName, data:dict):
    conn = sqlite3.connect(db_path)
    
    cursor= conn.cursor()
    cursor.execute(createTableText[tableName])
    
    values= list(data.values())
    for i,value in enumerate(values):
        if type(value)==str:
            values[i]= "'"+ value.replace("'","''")+ "'"
        elif type(value)==int:
            values[i]= str(value)
    cursor.execute(f"INSERT INTO {tableName} ({','.join(data.keys())}) VALUES ({','.join(values)});")
    new_data_id= cursor.lastrowid
    conn.commit()
    # conn.close()
    return new_data_id


def updateData(tableName, data:dict, id):
    conn = sqlite3.connect(db_path)
    
    cursor= conn.cursor()
    cursor.execute(createTableText[tableName])
    
    for col in data:
        if type(data[col])==str:
            data[col]= "'"+ data[col].replace("'","''")+ "'"
        elif type(data[col])==int:
            data[col]= str(data[col])
    values= [f"{col} = {data[col]}" for col in data]
    cursor.execute(f"UPDATE {tableName} SET {','.join(values)} WHERE id={id};")
    conn.commit()
    # conn.close()


def dbExec(*args):
    conn = sqlite3.connect(db_path)
    cursor= conn.cursor()
    cursor.execute(*args)
    conn.commit()
    return cursor.fetchall()


# 更新欄位，並在新的category欄位填上"美妝"
updateCols("youtube", {"channel_name":"TEXT", "channel_ID":"TEXT", "subscribers":"INTEGER", "views":"INTEGER", "likes":"INTEGER", "dislikes":"INTEGER", "category":"TEXT"})
for row in getData("youtube", "SELECT id,category FROM youtube"):
    if not row[1]:
        updateData("youtube", {"category":"美妝"}, row[0])


# -------------------------  程式設定部分  -------------------------
def getCategory():
    return ["美妝", "球鞋"]
    return [value[0] for value in dbExec("SELECT DISTINCT category FROM youtube;")]


def getKeywords(category):
    return {
        "美妝": ["產品", "品牌", "唇膏", "色號", "質地", "光澤", "漂亮", "推薦", "嘴唇", "霧面", "包裝", "不錯", "保濕", "彩妝", "訂閱", "膚色", "好用", "皮膚", "好看", "特別", "自然", "系列", "搭配", "上妝", "底妝", "腮紅", "眼妝", "眼影"],
        "球鞋": ["籃球", "休閒", "合腳", "磨腳", "顯瘦", "增高", "推薦", "品牌", "好用", "防水", "設計", "產品", "聯名", "搭配", "長腿", "防滑", "山系", "慢跑", "好看", "舒適", "健走", "運動", "柔軟", "真皮", "刺繡", "鞋帶", "橡膠", "鞋底"]
    }[category]
    result= getData("category", f"SELECT keywords FROM category WHERE category='{category}';")
    if result:
        return json.loads(result[0])
    else:
        return []





# -------------------------  文章比對部分  -------------------------
model_name= "distiluse-base-multilingual-cased-v2"
model_path= os.path.abspath(os.path.join(base_path, "crawler/data/sentence-transformers", model_name))




def loadModel2():
    global model, util
    try:
        from sentence_transformers import SentenceTransformer, util
        if os.path.exists(model_path):
            model = SentenceTransformer(model_path)
        else:
            model = SentenceTransformer(model_name)
            model.save(model_path)
    except:
        print("error: model未載入完畢")
loadModelThread= Thread(target=loadModel2)
def loadModel():
    global loadModelThread
    loadModelThread.start()

def compare(category, artical):
    # 等到載入model再執行
    loadModelThread.join()
    
    data= getData("youtube", f"SELECT videoContent,views,likes,dislikes FROM youtube WHERE category='{category}';")
    data= sorted(data, key=lambda x:(x[2]-x[3])/x[1], reverse=True)
    
    dataBad= data[-int(len(data)*0.1):]
    # 取前10%(約30筆)文章做比對
    data= data[:int(len(data)*0.1)]
    embeddings = model.encode([row[0] or '' for row in data]+[artical])
    diss= [float(util.pytorch_cos_sim(embeddings[i], embeddings[-1])) for i,row in enumerate(data)]
    # 取前10%中，相似性最高的前10筆文章，做相似度的平均
    diss= sorted(diss, reverse=True)
    if len(diss)>=10: diss= diss[:10]
    # 後10%的不取10篇，而是和全部的文章做相似度的平均
    diss2= [float(util.pytorch_cos_sim(embeddings[i], embeddings[-1])) for i,row in enumerate(data)]
    
    return f"相似度: {sum(diss)/len(diss)*100 :.2f} % "+ ('good' if sum(diss)/len(diss)>=sum(diss2)/len(diss2) else 'bad')


