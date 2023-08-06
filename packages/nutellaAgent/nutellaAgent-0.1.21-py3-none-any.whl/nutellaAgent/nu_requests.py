import threading
import aiohttp
import json

class Requests(threading.Thread):

    # 받은 request_datas를 json형태로 해당 url에 post
    async def post_action(self, request_datas, url):
        json_string = json.dumps(request_datas)
        headers = {'Content-Type': 'application/json; charset = utf-8'}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers = headers, data = json_string) as resp:
                data = await resp.text()
 
    # 받은 parameter(apiKey 값)을 해당 url로 넘겨서 projectId 값 받아오기. 리턴값은 list
    async def get_action(self, parameter1, parameter2, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params = {'id': parameter1, 'name': parameter2}) as resp:
                data = await resp.text()
                return json.loads(data)
    
