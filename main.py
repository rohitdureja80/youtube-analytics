import Services.YouTubeApi as y
import Database.Postgres as database
from pandas import json_normalize
import json
import datetime
from loguru import logger
import urllib.request 
import urllib.error 

def main():
    try: 
        logger.info("Starting process...")
        youtube = y.YouTubeApi()
        response = youtube.GetVideoCategories()
        logger.info("Retrieved video categories from YouTube api")
        now = datetime.datetime.now()
        df = json_normalize(response["items"])
        df.insert(0, "insertDate", now)
        db = database.Postgres()
        db.LoadDataFrame(data=df, tableName="VideoCategoriesRaw", boolReplace=True)
        logger.info("Video categories saved to database")
        for item in response["items"]:
            try:
                categoryId = item["id"]
                logger.debug("Category ID: " + categoryId)
                videos = youtube.GetMostPopularVideos(categoryId=categoryId, numResults=25)
                logger.debug("Retrieved most popular videos for video category " + categoryId)
                json_string = json.dumps(videos, indent=2) 
                #print(json_string)
                df = json_normalize(videos["items"])
                df.insert(0, 'videoCategoryId', categoryId)
                df.insert(0, "insertDate", now)
                #print(df)
                db.LoadDataFrame(data=df, tableName="MostPopularVideosRaw", boolReplace=False)
                logger.info("Most popular videos for video category " + categoryId + " saved to database")
            except Exception as e:
                logger.debug(e)
                continue
        query = 'select distinct b."snippet.title" as "Category", a."snippet.channelId" as "ChannelId",  a."snippet.channelTitle" as "ChannelTitle" from public."MostPopularVideosRaw" a inner join public."VideoCategoriesRaw" b on (a."videoCategoryId" = b."id")'
        logger.debug(query)
        records = db.GetData(query)
        print(type(records))
        logger.debug(">> Printing records...")
        logger.success("...Ending process")
    except Exception as err:
        logger.warning(err)

if __name__ == "__main__":
   main()