import os
DOMINO_API_KEY=os.environ['DOMINO_USER_API_KEY']
DOMINO_URL=os.environ['DOMINO_API_HOST']

def get_domino_url():
    return DOMINO_URL+'/'

def get_domino_api_key():
    return DOMINO_API_KEY
