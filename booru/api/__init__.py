from logging import log
from booru.login import login_ro
from dotenv import dotenv_values


config = dotenv_values(".env")
CLIENT_ID = config["REDDIT_CLIENT_ID"]
CLIENT_SECRET = config["REDDIT_CLIENT_SECRET"]
USER_AGENT = config["REDDIT_USER_AGENT"]


reddit = login_ro(
    client_id=CLIENT_ID, 
    client_secret=CLIENT_SECRET, 
    user_agent=USER_AGENT
    )
