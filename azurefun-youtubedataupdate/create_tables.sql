CREATE TABLE Video (
    Id bigint IDENTITY(1, 1) NOT NULL primary key,
    VideoId varchar(255) NOT NULL UNIQUE,
    PublishDate datetime2 NOT NULL,
    ChannelId varchar(255),
    Title nvarchar(100) NOT NULL,
    Tags nvarchar(500),
    CategoryId varchar(255),
    DefaultLanguage varchar(50),
    DurationInMin smallint,
    HdOrSd varchar(2),
    HasCaption bit,
    IsLicensed bit,
    IsEmbeddable bit,
    IsForKids bit,
);

CREATE TABLE VideoStatistic (
    Id bigint IDENTITY(1, 1) NOT NULL primary key,
    VideoId varchar(255) NOT NULL,
    Datetime datetime2 NOT NULL,
    ViewCount bigint NOT NULL,
    LikeCount bigint NOT NULL,
    FavoriteCount bigint NOT NULL,
    CommentCount bigint NOT NULL,
    CONSTRAINT FK_VideoStatistic_Video FOREIGN KEY (VideoId) REFERENCES Video (VideoId)
)