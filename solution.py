#!/usr/bin/env python3

import psycopg2, bleach

class DBC:
  def __init__(self):
    self.dbname = "news"
    self.db = psycopg2.connect(database=self.dbname)
    self.cur = self.db.cursor()
  
  def execute(self, statement):
    self.cur.execute(statement)

  def getAll(self):
    return self.cur.fetchall()
  
  def close(self):
    self.db.close()

def main():
  print()
  print("What are the most popular three articles of all time?:")
  for a in get_most_popular_articles():
    print('\"{}\" -- {} views'.format(a[0], a[1]))
  print()
  print("Who are the most popular article authors of all time?:")
  for a in get_most_popular_authors():
    print('{} -- {} views'.format(a[0], a[1]))
  print()
  print("On which days did more than 1% of requests lead to errors?:")
  for e in get_most_errors():
    print('{} -- {}% errors'.format(e[0].strftime('%B %d, %Y'), round(e[1]*100, 1)))

def get_most_popular_articles():
  dbc = DBC()
  stmt = """SELECT ar.title, count(*) AS views FROM articles ar
	    INNER JOIN log l ON l.path = CONCAT('/article/', ar.slug)
	    GROUP BY l.path, ar.title 
            ORDER BY views DESC 
            LIMIT 3"""
  dbc.execute(stmt)
  articles = dbc.getAll()
  dbc.close()
  return articles

def get_most_popular_authors():
  dbc = DBC()
  stmt = """SELECT au.name, count(*) AS views FROM articles ar
	    INNER JOIN authors au ON au.id=ar.author 
	    INNER JOIN log l on l.path = CONCAT('/article/', ar.slug)
	    GROUP BY au.name 
            ORDER BY views DESC"""
  dbc.execute(stmt)
  authors = dbc.getAll()
  dbc.close()
  return authors

def get_most_errors():
  dbc = DBC()
  stmt = """SELECT t.day, ROUND(((err.n_found*1.0) / t.requests), 3) AS percent
            FROM (SELECT date_trunc('day', time) "day", count(*) AS n_found
                  FROM log l
                  WHERE status = '404 NOT FOUND'
                  GROUP BY day) AS err
            INNER JOIN (SELECT date_trunc('day', time) "day", count(*) AS requests
                        FROM log l
                        GROUP BY day) AS t
            ON t.day = err.day
            WHERE (ROUND(((err.n_found*1.0) / t.requests), 3) > 0.01)
            ORDER BY percent DESC"""
  dbc.execute(stmt)
  errors = dbc.getAll()
  dbc.close()
  return errors 

if __name__ == "__main__":
  main()
