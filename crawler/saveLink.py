import os, sqlite3



base_path= os.path.abspath(os.path.dirname(__file__))


createTableText= {
    "youtube":'''CREATE TABLE IF NOT EXISTS youtube(
        ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        link TEXT,
        company TEXT,
        videoContent TEXT
    );'''
}


def getData(tableName, commamd):
    conn = sqlite3.connect(base_path+"/data/data.db")
    cursor= conn.cursor()
    cursor.execute(createTableText[tableName])
    result= cursor.execute(commamd)
    # conn.close()
    return result.fetchall()


def insertData(tableName, data:dict):
    conn = sqlite3.connect(base_path+"/data/data.db")
    
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