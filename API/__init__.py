import asyncio
from postgrest_py import PostgrestClient
from os import getcwd
from config import conf
import json

CONFIG_PATH = f"{getcwd()}/config/config.ini"

async def access():
    async with PostgrestClient("http://localhost:3000/rpc") as client:
        param = conf.get_token(filename=CONFIG_PATH)
        try:
            client.auth(token=param['access_token'])
        except Exception as e:
            print("login fallido")
            print(f'Error!: {e}')
        try:
            response = await client.from_("access").insert({}).execute()
            print(f"La respuesta es:{response}")
            return True
        except Exception as e:
            print(e)
            return False

async def obtain_range_data(data,symbol):
    async with PostgrestClient("http://localhost:3000/rpc") as client:
        param = conf.get_token(filename=CONFIG_PATH)
        try:
            client.auth(token=param['access_token'])
        except Exception as e:
            print("Petición fallida")
            print(f'Error!: {e}')
        try:
            response = await client.from_("obtain_analysis").insert({"data":data, "symbol":symbol}).execute()
            return json.loads(response.json())['data']
        except Exception as e:
            return None

async def get_sentiment_analysis(function:str):
    async with PostgrestClient("http://localhost:3000/rpc") as client:
        param = conf.get_token(filename=CONFIG_PATH)
        try:
            client.auth(token=param['access_token'])
        except Exception as e:
            print("Petición fallida")
            print(f'Error!: {e}')
        try:
            response = await client.from_(function).insert({}).execute()
            return json.loads(response.json())['data']
        except Exception as e:
            return None

