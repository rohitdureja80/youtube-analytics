import psycopg2
import pandas as pd
from sqlalchemy import create_engine 
from Services.ConfigParser import ConfigParser

class Postgres:
    def __init__(self):
        config = ConfigParser()
        db_config = config.DbConfigSettings()
        self.connection_string = "postgresql://" + db_config["username"] + ":" + db_config["password"] + "@" + db_config["host"] + "/" + db_config["databaseName"]
    
    def LoadDataFrame(self, data, tableName, boolReplace):
        if (boolReplace):
            exists = 'replace'
        else:
            exists = 'append'    
        db = create_engine(self.connection_string)
        conn = db.connect()
        df = pd.DataFrame(data)
        df.to_sql(tableName, con=conn, if_exists=exists, index=False)
        conn = psycopg2.connect(self.connection_string)
        conn.autocommit = True
        conn.close()
    
    def GetData(self, query):
        conn = psycopg2.connect(self.connection_string)
        cur = conn.cursor()
        cur.execute(query)
        records = cur.fetchall()
        conn.commit()
        conn.close()
        return records

        
