import json,asyncio,pprint

import requests
# from requests.exceptions import ConnectionError


class Xbet():
    def __init__(self):
        pass

    async def scan_live(self):
        while True:
            self.champs_id=set()
            responce=requests.get("https://api.melbet.ru/LiveFeed/Mb_GetChampsZip?sports=1&partner=195&country=1&gr=241&groupChamps=true").json()
            for champ in responce['Value'][0]['L']:
                if "CSC" not in champ:
                    self.champs_id.add(champ['LI'])
                else:
                    for sc in champ['SC']:
                        self.champs_id.add(sc['LI'])
            asyncio.create_task(self.corner_bet_chek())
            print("-------------------------------------------------------")
            await asyncio.sleep(60)

    async def corner_bet_chek(self):
        for id in (id for id in self.champs_id):
            responce=requests.get("https://api.melbet.ru/LiveFeed/Mb_GetGamesZip?champs={}&gr=241&partner=195&mode=2&withSubGames=true&grMode=2&groupEvents=true".format(id)).json()
            for item in(fn['I'] for item in responce['Value'][0]['G'] if "SG" in item
                        for fn in item['SG'] if 'Угловые. 1-й Тайм' in fn['FN']
                        if item['SC']['S'][0]['Value'] == '0' and item['SC']['S'][9]['Value'] == '0'):
                await self.total_find(item)

    async def total_find(self,item):
        responce = requests.get("https://api.melbet.ru/LiveFeed/Mb_GetEventsZip?id={}&partner=195&grMode=2&groupEvents=true&gr=241".format(item)).json()
        for total in (responce for total in responce['Value']['GE'][0]['E'][0]
                      if total['P'] == 0.5 and total['C'] >= float(1.5)):
            await self.message.answer(f"{total['Value']['L']} - {total['Value']['O1']} : {total['Value']['O2']}")
            # print(f"{total}")


async def main():
    bet=Xbet()
    await bet.scan_live()


if __name__ == "__main__":
    asyncio.run(main())
