from neomodel import config
import os
from dotenv import load_dotenv

load_dotenv()

# initiliaze neomodel config
NEO4J_URI= os.getenv('NEO4J_CONNECTION_URI')
NEO4J_USERNAME= os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD= os.getenv('NEO4J_PASSWORD')

NEO4J_DATABASE = {
    'default': {
        'HOST': NEO4J_URI,  
        'PORT': 7687, 
        'USER': 'neo4j',  
        'PASSWORD': NEO4J_PASSWORD,
        'SCHEME': 'neo4j+s', 
    }
}

config.DATABASE_URL = f"{NEO4J_DATABASE['default']['SCHEME']}://{NEO4J_DATABASE['default']['USER']}:{NEO4J_DATABASE['default']['PASSWORD']}@{NEO4J_DATABASE['default']['HOST']}:{NEO4J_DATABASE['default']['PORT']}"

