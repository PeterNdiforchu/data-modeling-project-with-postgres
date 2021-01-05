# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = ("""
    create table if not exists songplays (songplay_id serial primary key, \
                                          start_time timestamp NOT NULL, \
                                          user_id varchar, \
                                          level varchar, \
                                          song_id varchar, \
                                          artist_id varchar, \
                                          session_id int, \
                                          location varchar, \
                                          user_agent varchar);
 """)

user_table_create = ("""
    create table if not exists users (user_id varchar primary key, \
                                      first_name varchar, \
                                      last_name varchar, \
                                      gender varchar, \
                                      level varchar);
 """)

song_table_create = ("""
    create table if not exists songs (song_id varchar primary key, \
                                      title varchar NOT NULL, \
                                      artist_id varchar NOT NULL, \
                                      year varchar NOT NULL, \
                                      duration float NOT NULL);
""")

artist_table_create = ("""
    create table if not exists artists (artist_id varchar primary key, \
                                        name varchar NOT NULL, \
                                        location varchar NOT NULL, \
                                        latitude float NOT NULL, \
                                        longitude float NOT NULL);
""")

time_table_create = ("""
    create table if not exists time (start_time timestamp primary key, \
                                     hour int NOT NULL, \
                                     day int NOT NULL, \
                                     week int NOT NULL, \
                                     month int NOT NULL, \
                                     year int NOT NULL, \
                                     weekday int NOT NULL);
""")

# INSERT RECORDS

songplay_table_insert = ("""
    INSERT INTO songplays (
                             start_time, \
                             user_id, \
                             level, \
                             song_id, \
                             artist_id, \
                             session_id, \
                             location, \
                             user_agent)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT
    DO NOTHING;
""")

user_table_insert = ("""
    INSERT INTO users (
                        user_id, \
                        first_name, \
                        last_name, \
                        gender, \
                        level)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (user_id) DO UPDATE \
        SET level=excluded.level || 'free';
""")

song_table_insert = ("""
    INSERT INTO songs (
                        song_id, \
                        title, \
                        artist_id, \
                        year, \
                        duration)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT
    DO NOTHING;
""")

artist_table_insert = ("""
    insert into artists (
                          artist_id, \
                          name, \
                          location, \
                          latitude, \
                          longitude)
    VALUES(%s, %s, %s, %s, %s)
    ON CONFLICT
    DO NOTHING;
""")


time_table_insert = ("""
    INSERT into time ( 
                       start_time, \
                       hour, \
                       day, \
                       week, \
                       month, \
                       year, \
                       weekday)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT
    DO NOTHING;
""")

# FIND SONGS

song_select = ("""
    SELECT songs.song_id, artists.artist_id
                   FROM songs
                   JOIN artists
                   ON songs.artist_id = artists.artist_id
                   WHERE songs.title = %s
                   AND artists.name = %s
                   AND songs.duration = %s;
""")

# QUERY LISTS-  WHERE songs.title = %s AND artists.name = %s             AND songs.duration = %s

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
