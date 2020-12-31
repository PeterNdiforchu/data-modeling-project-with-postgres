import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    -Opens and reads song_data file
    -Inserts both song and artist records into songs table and artists table respectively.
    Parameters:
        cur (cursor): psycopg2 connection to postgres db
        filepath (string): song_data filepath
    
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data =  df[['artist_id', 'artist_name','artist_location','artist_longitude','artist_latitude']].values[0].tolist() 
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    -Opens and reads the log_data file 
    -Insert records into the artists, users and songsplay table based on variable constrainsts in sql_queries.py
    Parameters:
        cur (cursor): psycopg2 connection to postgres db
        filepath (string): log_data filepath
    """
    # open log file
    df = pd.read_json(filepath, lines=True) 

    # filter by NextSong action
    df[df['page']=='NextSong'] 

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = [t, \
             t.dt.hour, \
             t.dt.day, \
             t.dt.week, \
             t.dt.month, \
             t.dt.year, \
             t.dt.dayofweek]
    column_labels = ['ts', 'hour', 'day', 'week', 'month', 'year', 'dayofweek']
    time_df = pd.DataFrame({c: d for c,d in zip (column_labels, time_data)}).dropna()

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]
    user_not_null_df=user_df[user_df["userId"].notnull()]
    user_drop_dup_df = user_not_null_df.drop_duplicates('userId',keep='first')

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts, unit='ms'), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)
        

def process_data(cur, conn, filepath, func):
    """
    -Execute the ETL pipeline process by processing all data files and storing to the sparkify db
    -Get filepath and files necessary for executing ETL pipeline
    -Process functions to execute datafiles and ETL processes.
    Parameters:
        cur: psycopg2 cursor
        conn: psycopg2 connection object
        filepath (string): location of the datafiles
        func (function): function to execute datafiles (log_data and song_data)
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
