#!/usr/bin/env python3

import psycopg2


class DBC:
    """A Class for creating the connection and cursor to the defined DB"""
    def __init__(self):
        self.dbname = "news"
        self.db = psycopg2.connect(database=self.dbname)
        self.cur = self.db.cursor()

    def execute(self, statement):
        self.cur.execute(statement)

    def getAll(self, stmt):
        self.cur.execute(stmt)
        return self.cur.fetchall()

    def close(self):
        self.db.close()


def main():
    dbc = DBC()
    print("\nWhat are the most popular three articles of all time?:")
    for a in get_most_popular_articles(dbc):
        print('\"{}\" -- {} views'.format(a[0], a[1]))
    print("\nWho are the most popular article authors of all time?:")
    for a in get_most_popular_authors(dbc):
        print('{} -- {} views'.format(a[0], a[1]))
    print("\nOn which days did more than 1% of requests lead to errors?:")
    for e in get_most_errors(dbc):
        print('{:%B %d, %Y} -- {:.1%} errors'.format(e[0], e[1]))
    dbc.close()


def get_most_popular_articles(dbc):
    """
    Given a db connection
    When executing the below statement
    It returns the top 3 articles of all time
    """
    stmt = """SELECT ar.title, count(*) AS views FROM articles ar
            INNER JOIN log l ON l.path = CONCAT('/article/', ar.slug)
            GROUP BY l.path, ar.title
            ORDER BY views DESC
            LIMIT 3"""
    articles = dbc.getAll(stmt)
    return articles


def get_most_popular_authors(dbc):
    """
    Given a db connection
    When executing the below statement
    It returns most read authors in descending order
    """
    stmt = """SELECT au.name, count(*) AS views FROM articles ar
            INNER JOIN authors au ON au.id=ar.author
            INNER JOIN log l on l.path = CONCAT('/article/', ar.slug)
            GROUP BY au.name
            ORDER BY views DESC"""
    authors = dbc.getAll(stmt)
    return authors


def get_most_errors(dbc):
    """
    Given a db connection
    When executing below statment
    It returns days with more than 1% 404s hits
    """
    stmt = """SELECT t.day, (err.n_found*1.0 / t.reqs) AS percent
            FROM (SELECT date_trunc('day', time) "day", count(*) AS n_found
                  FROM log l
                  WHERE status = '404 NOT FOUND'
                  GROUP BY day) AS err
            INNER JOIN (SELECT date_trunc('day', time) "day", count(*) AS reqs
                        FROM log l
                        GROUP BY day) AS t
            ON t.day = err.day
            WHERE (ROUND(((err.n_found*1.0) / t.reqs), 3) > 0.01)
            ORDER BY percent DESC"""
    errors = dbc.getAll(stmt)
    return errors


if __name__ == "__main__":
    main()
