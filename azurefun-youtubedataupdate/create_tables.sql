CREATE TABLE Channel (
    Id bigint IDENTITY(1, 1) NOT NULL primary key,
    ChannelId varchar(255) NOT NULL UNIQUE,
    Title nvarchar(100) NOT NULL,
    CreatedDate datetime2 NOT NULL,
    DefaultLanguage varchar(50),
    Country varchar(50),
    IsForKids bit
);

CREATE TABLE ChannelStatistic (
    Id bigint IDENTITY(1, 1) NOT NULL primary key,
    ChannelId varchar(255) NOT NULL,
    Datetime datetime2 NOT NULL,
    ViewCount bigint NOT NULL,
    CommentCount bigint,
    SubscriberCount bigint NOT NULL,
    VideoCount int NOT NULL,
    CONSTRAINT FK_ChannelStatistic_Channel FOREIGN KEY (ChannelId) REFERENCES Chanel (ChannelId)
)

CREATE TABLE Video (
    Id bigint IDENTITY(1, 1) NOT NULL primary key,
    VideoId varchar(255) NOT NULL UNIQUE,
    PublishDate datetime2 NOT NULL,
    ChannelId varchar(255),
    Title nvarchar(100) NOT NULL,
    Tags nvarchar(500),
    CategoryId varchar(255),
    DefaultLanguage varchar(50),
    DurationInMin smallint NOT NULL,
    HdOrSd varchar(2) NOT NULL,
    HasCaption bit NOT NULL,
    IsLicensed bit NOT NULL,
    IsEmbeddable bit NOT NULL,
    IsForKids bit,
    CONSTRAINT FK_Video_Channel FOREIGN KEY (ChannelId) REFERENCES Chanel (ChannelId)
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