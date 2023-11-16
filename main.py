import Services.YouTubeApi as y
import Database.Postgres as database
from pandas import json_normalize
import json
import datetime
from loguru import logger

def main():
    logger.info("Starting process...")
    youtube = y.YouTubeApi()
    response = youtube.GetVideoCategories()
    now = datetime.datetime.now()
    df = json_normalize(response["items"])
    df.insert(0, "insertDate", now)
    db = database.Postgres()
    db.LoadDataFrame(data=df, tableName="VideoCategoriesRaw", boolReplace=True)
    for item in response["items"]:
        categoryId = item["id"]
        #print("Category ID: " + categoryId)
        videos = youtube.GetMostPopularVideos(categoryId=categoryId, numResults=25)
        json_string = json.dumps(videos, indent=2) 
        #print(json_string)
        df = json_normalize(videos["items"])
        df.insert(0, 'videoCategoryId', categoryId)
        df.insert(0, "insertDate", now)
        #print(df)
        db.LoadDataFrame(data=df, tableName="MostPopularVideosRaw", boolReplace=False)
    
    query = 'select distinct b."snippet.title" as "Category", a."snippet.channelId" as "ChannelId",  a."snippet.channelTitle" as "ChannelTitle" from public."MostPopularVideosRaw" a inner join public."VideoCategoriesRaw" b on (a."videoCategoryId" = b."id")'
    records = db.GetData(query)
    logger.trace(">> Printing records...")
    print(records)
    logger.info("...Ending process")

if __name__ == "__main__":
   main()