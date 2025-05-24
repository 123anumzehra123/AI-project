import psycopg2
import urllib.parse as urlparse

class Config:


    DATABASE_URL = "postgresql://neondb_owner:npg_XibBn1K8PhZV@ep-black-bush-a5i7t6bx-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"

@staticmethod
def get_connection():
    
    result = urlparse.urlparse(Config.DATABASE_URL)

    username = result.username
    password = result.password
    database = result.path[1:] # remove leading /
    hostname = result.hostname
    port = result.port
    sslmode = 'require' # Important for Neon!

    conn = psycopg2.connect(
    dbname=database,
    user=username,
    password=password,
    host=hostname,
    port=port,
    sslmode=sslmode,
    )
    return conn