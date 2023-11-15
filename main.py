import Services.YouTubeApi as y
import Database.Postgres as database
from pandas import json_normalize
import json

def main():
    youtube = y.YouTubeApi()
    response = youtube.GetVideoCategories()
    df = json_normalize(response["items"])
    db = database.Postgres()
    db.LoadDataFrame(data=df, tableName="VideoCategoriesRaw", boolReplace=True)
    for item in response["items"]:
        categoryId = item["id"]
        print("Category ID: " + categoryId)
        videos = youtube.GetMostPopularVideos(categoryId=categoryId, numResults=25)
        json_string = json.dumps(videos, indent=2) 
        #print(json_string)
        df["videoCategoryId"] = categoryId
        df = json_normalize(videos["items"])
        #print(df)
        db.LoadDataFrame(data=df, tableName="MostPopularVideosRaw", boolReplace=False)

if __name__ == "__main__":
   main()