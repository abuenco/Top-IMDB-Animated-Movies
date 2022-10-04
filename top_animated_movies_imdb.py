"""
Top Animated Movies on IMDB
"""

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Load CSV and connect to database
CSV_FILE = 'TopAnimatedImDb.csv'
DB_NAME = 'top_animated_movies_imdb.db'

movie_data = pd.read_csv(CSV_FILE)

con = sqlite3.connect(DB_NAME)
cur = con.cursor()

# If database doesn't exist, create one
movie_db_check = cur.execute('SELECT name FROM sqlite_master')

if not movie_db_check.fetchone():
    movie_table = '''
        CREATE TABLE animated_movies (
            Title VARCHAR NOT NULL,
            Rating NUMERIC(2, 1), 
            Votes FLOAT,
            Gross VARCHAR,
            Genre VARCHAR NOT NULL,
            Metascore INT,
            Certificate CHAR,
            Director VARCHAR NOT NULL,
            Year INT NOT NULL,
            Description VARCHAR,
            Runtime VARCHAR
            );
        '''

    cur.execute(movie_table)
    movie_data.to_sql('animated_movies', con, if_exists='append', index=False)
    con.commit()

# What are the top 10 animated movies rated on IMDB?
top_ten_command = '''
    SELECT Title, Rating, Year FROM animated_movies
    ORDER BY Rating DESC
    LIMIT 10;
    '''

top_ten = pd.read_sql(top_ten_command, con)
print("The Top 10 animated movies on IMDB are: ")
print(top_ten)


# How many Hayao Miyazaki directed films are in the top 85?
hayao_count_command = '''
    SELECT COUNT(Title) as "No. of Hayao Miyazaki Films"
    FROM animated_movies WHERE Director="Hayao Miyazaki";
    '''

hayao_count = pd.read_sql(hayao_count_command, con)
print(hayao_count)


# What movies directed by Hayao Miyazaki are in the top 85 of IMDB?
hayao_movies_command = '''
    SELECT Title as "Hayao Miyazaki Films", Rating, Year
    FROM animated_movies
    WHERE Director="Hayao Miyazaki"
    ORDER BY Rating DESC;
    '''

hayao_movies = pd.read_sql(hayao_movies_command, con)
print(hayao_movies)


# How many adventure films are in the top 85 animated movies on IMDB?
adventure_count_command = '''
    SELECT COUNT(*) as "No. of Adventure Animated Films"
    FROM animated_movies
    WHERE Genre LIKE "%Adventure%";
    '''

adventure_count = pd.read_sql(adventure_count_command, con)
print(adventure_count)


# How many adventure films in the top 85 animated movies on IMDB
# are produced by Brad Bird?
bradBird_adventure_command = '''
    SELECT Title as "Brad Bird Adventure Film", Rating, Year
    FROM animated_movies
    WHERE Genre LIKE "%Adventure" AND
    DIRECTOR="Brad Bird";
    '''
    
bradBird_adventure = pd.read_sql(bradBird_adventure_command, con)
print(bradBird_adventure)


# Who are the directors who produced films in the top 85 animated movies 
# on IMDB, and how many of those films did they produce?
directors_command = '''
    SELECT Director, COUNT(*) as Frequency 
    FROM animated_movies 
    GROUP BY Director;
    '''

directors = pd.read_sql(directors_command, con)

# Plot a histogram
plt.bar(directors.Director, directors.Frequency)
plt.xlabel('Directors', fontsize=16)
plt.ylabel('Number of animated movies in Top 85 of IMDB', fontsize=16)
plt.xticks(rotation='vertical')
plt.title('Directors in the Top 85 Animated Films of IMDB', fontsize=20)
plt.tight_layout()
plt.show()

con.close()