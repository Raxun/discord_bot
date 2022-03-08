import discord
import requests
import asyncio


# config/environments/production.rb
config.assets.compile = true # setting to true makes your app vulnerable

TOKEN = "OTQ5OTYxODU1NDQ5ODQ5ODc2.YiR-6w.azhDOCmYS-sngzTHtHI7sqrZPnM"

# люблю нюхать лютую бебру
sp = [777095890920800278, 777095890920800279, 777095891374571520, 916333647722856508, 916334058135490600,
      916334138108301383, 916334302688595999, 916334961819262976, 916335148876853258, 916335433334521897,
      916337519069626380, 916337618495623198, 916347339009044511, 916349370499207189, 916366928006742087,
      916366983270920233, 916402152174391357, 916561765234520086, 916775540822790164, 924331753831817257,
      926095511302324264, 935793713748262923, 936678560444350544, 940183407466512435, 945749710256341002]


class YLBotClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            print(
                f'{self.user} подключились к чату:\n'
                f'{guild.name}(id: {guild.id})')
        # print(client.get_channel(935793713748262923)) basar
        # print(client.get_channel(916349370499207189)) music
        # print(client.get_channel(916402152174391357)) real man
        # print(client.get_channel(916775540822790164)) test-bot

    async def on_message(self, message):
        if message.author == self.user:
            return
        else:
            print(message.author, message.content)
            if message.channel.id not in sp:
                chan = client.get_channel(935793713748262923)
                await chan.send(message.content)
            if "аче" in message.content.lower() or "ачу" in message.content.lower():
                await message.channel.send('а ничe на, нормально общайся')
            if "котики!" in message.content.lower():
                res = requests.get('https://api.thecatapi.com/v1/images/search').json()
                await message.channel.send(res[0]['url'])
            if 'собачка!' in message.content.lower():
                res = requests.get('https://dog.ceo/api/breeds/image/random').json()
                await message.channel.send(res['message'])
            if 'set_timer in' in message.content.lower():
                try:
                    mes = message.content.lower().split()
                    time = (int(mes[mes.index('hours') - 1]) * 3600) + (int(mes[mes.index('minutes') - 1]) * 60) + \
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
