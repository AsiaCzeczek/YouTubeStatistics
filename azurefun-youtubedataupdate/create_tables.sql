BEGIN TRANSACTION;

CREATE TABLE Channel (
    Id bigint IDENTITY(1, 1) NOT NULL primary key,
    ChannelId varchar(255) NOT NULL UNIQUE,
    Title nvarchar(500) NOT NULL,
    CreatedDate datetime2 NOT NULL,
    DefaultLanguage varchar(50),
    Country varchar(50),
    IsForKids bit
);

CREATE TABLE ChannelStatistic (
    Id bigint IDENTITY(1, 1) NOT NULL primary key,
    ChannelId varchar(255) NOT NULL,
    Datetime datetime2 NOT NULL,
    ViewCount bigint,
    CommentCount bigint,
    SubscriberCount bigint,
    VideoCount int,
    CONSTRAINT FK_ChannelStatistic_Channel FOREIGN KEY (ChannelId) REFERENCES Channel (ChannelId)
)

CREATE TABLE Video (
    Id bigint IDENTITY(1, 1) NOT NULL primary key,
    VideoId varchar(255) NOT NULL UNIQUE,
    PublishDate datetime2 NOT NULL,
    ChannelId varchar(255),
    Title nvarchar(500) NOT NULL,
    Tags nvarchar(500),
    CategoryId varchar(255),
    DefaultLanguage varchar(50),
    DurationInMin smallint NOT NULL,
    HdOrSd varchar(2),
    HasCaption bit,
    IsLicensed bit,
    IsEmbeddable bit,
    IsForKids bit,
    CountryRank smallint,
    CONSTRAINT FK_Video_Channel FOREIGN KEY (ChannelId) REFERENCES Channel (ChannelId)
);

CREATE TABLE VideoStatistic (
    Id bigint IDENTITY(1, 1) NOT NULL primary key,
    VideoId varchar(255) NOT NULL,
    Datetime datetime2 NOT NULL,
    ViewCount bigint,
    LikeCount bigint,
    FavoriteCount bigint,
    CommentCount bigint,
    StatisticInCountry varchar(50) NOT NULL,
    CONSTRAINT FK_VideoStatistic_Video FOREIGN KEY (VideoId) REFERENCES Video (VideoId)
)

COMMIT;
