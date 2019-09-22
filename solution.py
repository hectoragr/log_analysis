#!/usr/bin/env python3

import psycopg2, bleach

def main():
  db = psycopg2.connect(database="news")
  c = db.cursor()
  c.execute("Select * from authors")
  print(c.fetchall())
  db.close()

if __name__ == '__main__':
  main()

