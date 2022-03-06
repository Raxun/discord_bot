import discord
import requests
import asyncio

TOKEN = "OTQ5OTYxODU1NDQ5ODQ5ODc2.YiR-6w.eyh_Hm7ExIthEtmExeUX_46e-4Y"


class YLBotClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            print(
                f'{self.user} подключились к чату:\n'
                f'{guild.name}(id: {guild.id})')

    async def on_message(self, message):
        if message.author == self.user:
            return
        else:
            if "котики!" in message.content.lower():
                res = requests.get('https://api.thecatapi.com/v1/images/search').json()
                await message.channel.send(res[0]['url'])
            if 'собачка!' in message.content.lower():
                res = requests.get('https://dog.ceo/api/breeds/image/random').json()
                await message.channel.send(res['message'])
            if 'set_timer in' in message.content.lower():
                try:
                    mes = message.content.lower().split()
                    time = (int(mes[mes.index('hours') - 1]) * 3600) + \
                           (int(mes[mes.index('minutes') - 1]) * 60) + \
                           (int(mes[mes.index('seconds') - 1]))
                    await message.channel.send(f'The timer should star in {" ".join(mes[2:4])} '
                                               f'{" ".join(mes[4:6])} and {" ".join(mes[6:8])}')
                    await asyncio.sleep(time)
                    await message.channel.send(':alarm_clock:Time Х has come!')
                except ValueError:
                    await message.channel.send('Неверный формат. Чтобы поставить таймер введите - '
                                               'set_timer in n hours n minutes n seconds')


client = YLBotClient()
client.run(TOKEN)
