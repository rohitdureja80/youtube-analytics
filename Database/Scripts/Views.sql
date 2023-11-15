-- View: public.vwMostPopularVideos
-- DROP VIEW public."vwMostPopularVideos";

CREATE OR REPLACE VIEW public."vwMostPopularVideos"
 AS
 SELECT b."snippet.title" AS "Category",
    a."snippet.title" AS "VideoTitle",
    a."snippet.publishedAt" AS "PublishedAt",
    a."snippet.channelId" AS "ChannelId",
    a."snippet.channelTitle" AS "ChannelTitle",
    a."statistics.viewCount" AS "ViewCount",
    a."statistics.likeCount" AS "LikeCount",
    a."statistics.favoriteCount" AS "FavoriteCount",
    a."statistics.commentCount" AS "CommentCount",
    a."snippet.defaultLanguage" AS "DefaultLanguage",
    a."insertDate" AS "InsertDate"
   FROM "MostPopularVideosRaw" a
     JOIN "VideoCategoriesRaw" b ON a."videoCategoryId" = b.id;

ALTER TABLE public."vwMostPopularVideos"
    OWNER TO postgres;


-- View: public.vwPopularChannels
-- DROP VIEW public."vwPopularChannels";

CREATE OR REPLACE VIEW public."vwPopularChannels"
 AS
 SELECT DISTINCT b."snippet.title" AS "Category",
    a."snippet.channelId" AS "ChannelId",
    a."snippet.channelTitle" AS "ChannelTitle"
   FROM "MostPopularVideosRaw" a
     JOIN "VideoCategoriesRaw" b ON a."videoCategoryId" = b.id;

ALTER TABLE public."vwPopularChannels"
    OWNER TO postgres;

