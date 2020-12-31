###**SPARKIFY**

####**Project Objectives**

The Objective of this project is to:
1. Perform data modeling with Postgres
2. Build an ETL pipeline using Python via Jupyther Notebook
3. Define fact and dimension tables for a star schema data model optimized for query on song play analysis.
4. Implement ETL pipeline that transfers data from files in JSON format into tables in Postgres using Python and SQL.

###**Project Description**
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.
    
###**Definition of Key Project Deliverables**

###**Datasets**
The Dataset is a collection of user activities/logs and songs played stored in two directories both in JSON format. Our focus is on the data collected and stored in two datasets:

1. `songs_data`
2. `log_data`

1. **Songs dataset**
The first dataset is a subset of real data from the <a href="http://millionsongdataset.com/" target="_blank">A Million Song Dataset</a>. Each file is in .JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset:

`song_data/A/B/C/TRABCEI128F424C983.json
 song_data/A/A/B/TRAABJL12903CDCF1A.json`
 
Below is a sample of a file stored on the path `data/song_data` in JSON format: 

```
{
     num_songs:1
     artist_id:"ARD7TVE1187B99BFB1"
     artist_latitude:null
     artist_longitude:null
     artist_location:"California - LA"
     artist_name:"Casual"
     song_id:"SOMZWCG12A8C13C480"
     title:"I Didn't Mean To"
     duration:218.93179
     year:0
 }
```

2. **Log dataset**
The second dataset consists of log files in JSON format generated by this <a href="https://github.com/Interana/eventsim" target="_blank">Event Simulator</a> based on the songs in the dataset above. These simulate activity logs from a music streaming app based on specified configurations.

The log files in the dataset are partitioned by year and month. For example, here are filepaths to two files in this dataset:

`log_data/2018/11/2018-11-12-events.json
 log_data/2018/11/2018-11-13-events.json`

Below is a sample of a file stored on the pat `data/log_data` in .JSON format:

```
{
    "artist": null,
    "auth": "Logged In",
    "firstName": "Walter",
    "gender": "M",
    "itemInSession": 0,
    "lastName": "Frye",
    "length": null,
    "level": "free",
    "location": "San Francisco-Oakland-Hayward, CA",
    "method": "GET",
    "page": "Home",
    "registration": 1540919166796.0,
    "sessionId": 38,
    "song": null,
    "status": 200,
    "ts": 1541105830796,
    "userAgent": "\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36\"",
    "userId": "39"
 }
```
 
 ###**Database Schema**
 
 The database star schema is used in this the data mainly for the benefits of fast aggregation and the simplicity of the queries. The star schema is used to optimize queries for songs played. There two main tables that are used in this table model are the fact table and dimension tables.
 
 ![Sparkify db Schema](https://user-images.githubusercontent.com/76578061/103400730-754e8f80-4b03-11eb-8688-98e723664a8c.png)

 
 1. **Fact Table**
 
  i. **songplays**- Consists of records in log data associated with song plays .i.e. records with the page `NextSong`
 Table Songplays:
 
 ```
 songplays (
	songplay_id SERIAL PRIMARY KEY,
	start_time timestamp NOT NULL,
	user_id varchar NOT NULL,
	level varchar NULL,
	song_id varchar NOT NULL,
	artist_id varchar NOT NULL,
	session_id int NOT NULL,
	location varchar NULL,
	user_agent varchar NULL
);
```

  2. **Dimension Tables**
  
   i. **User**- Users in the Sparkify app
  Table Users:
  
```
  users (
    user_id varchar PRIMARY KEY UNIQUE NOT NULL,
    first_name varchar NULL,
    last_name varchar NULL,
    gender varchar NULL,
    level varchar NULL
);
``` 

   ii. **song**- Songs in the music database
  Table Songs:
  
```
  songs (
    song_id PRIMARY KEY UNIQUE NOT NULL,
    title varchar NULL,
    artist_id varchar NULL,
    year int NULL,
    duration numeric NULL
);
```

   iii. **artists**- Artists in the music database
  Table Artists:
  
 ```
 artists (
	artist_id varchar PRIMARY KEY UNIQUE NOT NULL,
	name varchar NULL,
	location varchar NULL,
	latitude decimal NULL,
	longitude decimal NULL
);
 ```

   iv. **time**- Timestamps of records in `songplays` broken down into specific units
  Table Time
  
  ```
  time (
    start_time timestamp NOT NULL,
    hour int NULL,
    day int NULL,
    week int NULL,
    month int NULL,
    year int NULL,
    weekday int NULL
);
  ```

###**Environment**

Python 3.6 or above

PostgresSQL 9.5 or above

psycopg2 - PostgreSQL database adapter for Python

###**Project File**

`sql_queries.py`- Contains sql queries for:
- Creating fact and dimension tables
- Dropping tables 
- Inserting records/tuples

`create_table.py`- Contains code for
- Setting up database to create Sparkifydb
- Creating the fact table
- Creating dimension tables

`etl.ipynb`- A jupyter notebook used to:
- Create ETL process queries
- Analyse database prior to running

`etl.py`- Contains code to:
- Read `song_data` and `log_data`
- Process `song_data` and `log_data`
- Implement the ETL pipeline

`test.ipynb`- Jupyter notebook used to:
- Connect to postgres database
- Validate the data loaded

###**Project Processes**

 1. **Database**
 
 To create the database and tables we run the script `create_table.py` which contains the code that will import all queries stored in `sql_queries.py` and will execute them.
 
 First it will drop existing tables and databases, then it will go ahead to create the database and all its tables.
 
 Each table has a primary key which will be used to joined with other tables in the star schema database model.
 
 The `ON CONFLICT DO NOTHING` clause is used to write to tables on all the insert queries to avoid errors on conflicting data.
 
 2. **ETL**
 
 The `etl.py` script provides many functions to perform the ETL process:
 
 The function `process_song_file` will read each .JSON file located in the file path `data/song_data` to extract data and write into the `artists` and `songs` table.
 
 The function `get_files` gets a list of all log .JSON files in the file path `data/log_data`. By parsing each log file, the `time` and `users` dimensional tables are created together with the `songplays` fact table.
 
 In order to extract time, each record is filtered by the `NextSong!` action which extracts the timestamp, hour, day, week of year, year, month, and weekday from the ts column and set the time_data to a list of ordered values by converting ts timestamp column to datetime.
 
 The following methods are used to filter the records and decode the timestamp value:
 
    ```
    df = df[df.page == "NextSong"] 
    
     t = pd.to_datetime(df['ts'], unit='ms')
     time_data = (t, t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year,t.dt.weekday)
     ```
 
 In order to get the data for the `users` table, the script will: 
 - Read 'userId','firstName','lastName', 'gender', 'level';
 - Remove duplicates;
 - Insert unique user records into the users table.
 
 In order to get the data for the `songsplay` table, the script will:
 - Extract `song_id` and `artist_id` from the `log` .JSON file
 - Decode `ts` and extract the datetime value
 - Write the data into `songplays` table.
 
 ##**Project Instructions**
 
###**Create database and tables**
 - Run python3 `create_tables.py` to create the database and tables.
 - Run `test.ipynb!` Jupyter notebook to confirm the creation of the tables with the correct columns.

###**ETL Process**
After creating the database and tables we can start the ETL process:
 - Run python3 `etl.py` which will extract data from all the .json files located at the `data!` folder and store it on the Postgres database.
