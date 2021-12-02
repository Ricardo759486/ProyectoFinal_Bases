from dotenv import load_dotenv
import os

load_dotenv()

userdb = os.environ['MYSQL_USER']
passworddb = os.environ['MYSQL_PASSWORD']
hostdb = os.environ['MYSQL_HOST']
portdb = os.environ['MYSQL_PORT']
databasedb = os.environ['MYSQL_DATABASE']


DATABASE_CONNECTION_URI = f'mysql://{userdb}:{passworddb}@{hostdb}/{databasedb}'
DATABASE_CONNECTION_QUERY =f"host={hostdb},user={userdb}, passwd={passworddb},db={databasedb}"