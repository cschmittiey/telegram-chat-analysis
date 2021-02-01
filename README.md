# telegram-chat-analysis
Analyze your telegram chats! 

Right now, here's what this tool does
- hackily gets chat messages into postgres by importing a single exported chat history JSON file, which you can get by using Telegram Desktop

Here's what I'd like to do with it in the future
- output pretty graphs of stats from your chat
- random quotes?
- markov chains?
- sentiment analysis by user?
- actually upsert instead of just ignoring messages that were already added

## Instructions for use:
pip install psycopg2 dateutil

connect to your postgres database, and create a table for your messages to be stored in:
```sql
create table <tablename>
(
    id                   bigint not null
        constraint <tablename>_pkey
            primary key,
    type                 text,
    date                 timestamp,
    actor                text,
    actor_id             bigint,
    action               text,
    title                text,
    members              text,
    text                 text,
    width                integer,
    height               integer,
    "from"               text,
    from_id              bigint,
    media_type           text,
    reply_to_message_id  bigint,
    sticker_emoji        text,
    edited               text,
    message_id           bigint,
    mime_type            text,
    duration_seconds     bigint,
    forwarded_from       bigint,
    location_information point,
    via_bot              text,
    poll                 boolean,
    duration             bigint
);

```

edit config.ini to reflect your database connection settings, place the result.json from telegram in the same directory, and then fire up the script!