import os
import urllib.parse as up
import psycopg2


def executeQuery(queryString):
    up.uses_netloc.append("postgres")
    url = up.urlparse(os.environ["DATABASE_URL"])
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

    cursor = conn.cursor()
    cursor.execute(queryString)
    conn.commit()

    results = None
    try:
        results = cursor.fetchall()
    except psycopg2.ProgrammingError:
        results = "error"
    return results

