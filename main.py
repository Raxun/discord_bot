from __future__ import unicode_literals
import discord
import requests
import asyncio
from discord.ext import commands
from discord_webhook import DiscordWebhook
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch
import youtube_dl
import os


bot = commands.Bot(command_prefix='!')
TOKEN = "OTQ5OTYxODU1NDQ5ODQ5ODc2.YiR-6w.azhDOCmYS-sngzTHtHI7sqrZPnM"
webhook = DiscordWebhook(url='https://discord.com/api/webhooks/951126186422050847/wmtZcrOElwCDwcKfICqFhOY644q-'
                             '8uMiaDn55GgZ0Mqelj3HuDfMtU4c2hGp83IjbPSG')
all_roles = []
em_help = discord.Embed(title="", colour=0x87CEEB)
sp = [777095890920800278, 777095890920800279, 777095891374571520, 916333647722856508, 916334058135490600,
      916334138108301383, 916334302688595999, 916334961819262976, 916335148876853258, 916335433334521897,
      916337519069626380, 916337618495623198, 916347339009044511, 916349370499207189, 916366928006742087,
      916366983270920233, 916402152174391357, 916561765234520086, 916775540822790164, 924331753831817257,
      926095511302324264, 935793713748262923, 936678560444350544, 940183407466512435, 945749710256341002]
prohibited_roles = [777095890920800277, 950084976106434603, 916336276377067550, 951123097556242462,
                    922929900896260197, 916349586807857253, 931265070380490783, 916347414347149363, 916404928178708530,
                    916346185516720190, 921662122570690580, 916335782237724702]

client_id = "78a7bbd4b14d44f089471f96cff65c7f"  # Сюда вводим полученные данные из панели спотифая
secret = "a9052a01b1a94306851d93742998921d"  # Сюда вводим полученные данные из панели спотифая

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=secret)
spotify = spotipy.Spotify(auth_manager=auth_manager)
em_roles = discord.Embed(title="", colour=0x87CEEB)
url = ''
sp_music = []


@bot.event
async def on_ready():
    global all_roles
    print(f'{bot.user} has connected to Discord!')
    for guild in bot.guilds:
        print(
            f'{bot.user} подключились к чату:\n'
            f'{guild.name}(id: {guild.id})')
        # print(client.get_channel(935793713748262923)) basar
        # print(client.get_channel(916349370499207189)) music
        # print(client.get_channel(916402152174391357)) real man
        # print(client.get_channel(916775540822790164)) test-bot
    em_help.set_author(name="Raxun", icon_url="https://avatars.githubusercontent.com/u/94015674?s=400&u=7d739"
                                              "fe0e1593df54e804fb6e097f597a3a838d7&v=4")
    em_help.add_field(name="Команды", value="!котики !собачка !роли !таймер", inline=False)
    em_help.add_field(name="Особенности", value="все личные сообщения бота анонимно отправляются "
                                                "в :book:базар:book:", inline=False)

    for role in bot.get_guild(777095890920800277).roles:
        all_roles.append(role.id)
    all_roles.reverse()  # to make it higher first
    all_roles = ['<@&' + str(all_roles[i]) + '>' for i in range(len(all_roles)) if all_roles[i] not in prohibited_roles]
    em_roles.set_author(name="Raxun", icon_url="https://avatars.githubusercontent.com/u/94015674?s=400&u=7d739"
                                               "fe0e1593df54e804fb6e097f597a3a838d7&v=4")
    em_roles.add_field(name="Команды", value='!роль (тег роли)', inline=False)
    em_roles.add_field(name="Роли", value=' | '.join(all_roles), inline=True)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    else:
        if message.channel.id not in sp:
            if message.attachments:
                photo_url = message.attachments[0].url
                chan = bot.get_channel(935793713748262923)
                await chan.send(photo_url)
            else:
                chan = bot.get_channel(935793713748262923)
                await chan.send(message.content)
        if "аче" == message.content.lower() or "ачу" == message.content.lower():
            await message.channel.send('а ничe на, нормально общайся')
    await bot.process_commands(message)


@bot.command('помощь')
async def cat(ctx):
    await ctx.message.channel.send(embed=em_help)


@bot.command('роли')
async def cat(ctx):
    await ctx.message.channel.send(embed=em_roles)


@bot.command('котики')
async def cat(ctx):
    res = requests.get('https://api.thecatapi.com/v1/images/search').json()
    await ctx.message.channel.send(res[0]['url'])


@bot.command('собачка')
async def cat(ctx):
    res = requests.get('https://dog.ceo/api/breeds/image/random').json()
    await ctx.message.channel.send(res[0]['url'])


@bot.command('таймер')
async def cat(ctx):
    try:
        mes = ctx.message.content.lower().split()
        time = (int(mes[mes.index('часов') - 1]) * 3600) + (int(mes[mes.index('минут') - 1]) * 60) + \
               (int(mes[mes.index('секунд') - 1]))
        await ctx.message.channel.send(f'таймер поставлен на {" ".join(mes[2:4])} '
                                   f'{" ".join(mes[4:6])} и {" ".join(mes[6:8])}')
        await asyncio.sleep(time)
        await ctx.message.channel.send(':alarm_clock:Время пришло ебан!')
    except ValueError:
        await ctx.message.channel.send('Неверный формат. Чтобы поставить таймер введите - '
                                   '!таймер n часов n минут n секунд')


@bot.command('плейлист')
async def playlist(ctx):
    if len(ctx.message.content) > 10:
        url = ctx.message.content[9:-1]
        result = spotify.track(url)
        performers = ""
        music = result['name']
        for names in result["artists"]:
            performers = performers + names["name"] + ", "
        performers = performers.rstrip(", ")
        name = f"{performers} - {music}"
        print(name)
        ydl_opts = {'format': 'bestaudio/best',
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3',
                                        'preferredquality': '192'}],
                    'outtmpl': f'./{name}.webm'}

        videosSearch = VideosSearch(f'{performers} - {music}', limit=1)
        videoresult = videosSearch.result()["result"][0]["link"]
        name = name + '.mp3'
        sp_files = os.listdir()
        if name not in sp_files:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([videoresult])
        sp_music.append(name)
    em_playlist = discord.Embed(title="Плейлист", colour=0x87CEEB)
    for i, name in enumerate(sp_music):
        em_playlist.add_field(name=str(i + 1), value=name[:-4], inline=False)
    await ctx.message.channel.send(embed=em_playlist)


@bot.command('музыка')
async def music(ctx):
    for musics in sp_music:
        channel = ctx.message.author.voice.channel
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(musics), after=lambda e: music(ctx))
        del sp_music[sp_music.index(musics)]
        asyncio.run_coroutine_threadsafe(ctx.send("No more songs in queue."))


@bot.command('стоп')
async def stop_music(ctx):
    global sp_music
    global em_playlist
    channel = ctx.message.author.voice.channel
    await channel.disconnect()
    sp_music = []


@bot.command('роль')
async def role(ctx, role):
    print(role)
    flag = False
    role = role[3:-1]
    for elem in bot.get_guild(777095890920800277).roles:
        if int(role) == elem.id and elem.id not in prohibited_roles:
            role = elem
            await ctx.author.add_roles(role)
            await ctx.channel.send('Роль добавлена')
            flag = True
    if not flag:
        await ctx.channel.send('Ошибка, пошел кабанчиком отсюдова')


bot.run(TOKEN)
