# Log Analysis project for Udacity

## Introduction
This project sets up a mock PostgreSQL database for a fictional news website. The provided Python script uses the psycopg2 library to query the database and produce a report that answers the following three questions:
### Questions
    1. What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.

    2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.

    3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser.

## Requirements
- Python3
- Vagrant / Virtual Box (config: https://github.com/udacity/fullstack-nanodegree-vm)
- PostgreSQL
- psycopg2

## How to run

- After setting up Vagrant and install all requisites, load the data into psql from [this file | https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip]
- Make sure you have access to the table and rows from the above sql file
- Using python3 execute command `python3 solution.py`, this will answer the 3 questions asked above

## Sample Output

```
What are the most popular three articles of all time?:
"Candidate is jerk, alleges rival" -- 338647 views
"Bears love berries, alleges bear" -- 253801 views
"Bad things gone, say good people" -- 170098 views

Who are the most popular article authors of all time?:
Ursula La Multa -- 507594 views
Rudolf von Treppenwitz -- 423457 views
Anonymous Contributor -- 170098 views
Markoff Chaney -- 84557 views

On which days did more than 1% of requests lead to errors?:
July 17, 2016 -- 2.3% errors
```

