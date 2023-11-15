import Services.YouTubeApi as y
import Database.Postgres as database
from pandas import json_normalize
import json
import datetime

def main():
    youtube = y.YouTubeApi()
    response = youtube.GetVideoCategories()
    now = datetime.datetime.now()
    df = json_normalize(response["items"])
    df.insert(0, "insertDate", now)
    db = database.Postgres()
    db.LoadDataFrame(data=df, tableName="VideoCategoriesRaw", boolReplace=True)
    for item in response["items"]:
        categoryId = item["id"]
        print("Category ID: " + categoryId)
        videos = youtube.GetMostPopularVideos(categoryId=categoryId, numResults=25)
        json_string = json.dumps(videos, indent=2) 
        #print(json_string)
        df = json_normalize(videos["items"])
        df.insert(0, 'videoCategoryId', categoryId)
        df.insert(0, "insertDate", now)
        #print(df)
        db.LoadDataFrame(data=df, tableName="MostPopularVideosRaw", boolReplace=False)

if __name__ == "__main__":
   main()