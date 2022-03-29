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
from mutagen.mp3 import MP3


bot = commands.Bot(command_prefix='!')
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
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
em_help_music = discord.Embed(title="", colour=0x87CEEB)
url = ''
sp_music = []
all_roles = []


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
    em_help.add_field(name="Команды", value="!музыка", inline=False)
    em_help_music.set_author(name="Raxun", icon_url="https://avatars.githubusercontent.com/u/94015674?s=400&u=7d739"
                                              "fe0e1593df54e804fb6e097f597a3a838d7&v=4")
    em_help_music.add_field(name="Команды", value="!плейлист (ссылка на трек Spotify) !стоп !музыка", inline=False)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    else:
        if message.channel.id not in sp:
            print(message.content, message.author)
            '''if message.attachments:
                photo_url = message.attachments[0].url
                chan = bot.get_channel(935793713748262923)
                await chan.send(photo_url)
            else:
                chan = bot.get_channel(935793713748262923)
                await chan.send(message.content)'''
    await bot.process_commands(message)


@bot.command('помощь')
async def help(ctx):
    await ctx.message.channel.send(embed=em_help)


@bot.command('музыка')
async def music(ctx):
    await ctx.message.channel.send(embed=em_help_music)


@bot.command('плейлист')
async def playlist(ctx):
    global vc
    if len(ctx.message.content) > 10:
        url = ctx.message.content[9:-1]
        result = spotify.track(url)
        performers = ""
        music = result['name']
        for names in result["artists"]:
            performers = performers + names["name"] + ", "
        performers = performers.rstrip(", ")
        name = f"{performers} - {music}"
        ydl_opts = {'format': 'bestaudio/best',
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3',
                                        'preferredquality': '192'}],
                    'outtmpl': f'./{name}.webm'}

        videosSearch = VideosSearch(f'{performers} - {music}', limit=1)
        videoresult = videosSearch.result()["result"][0]["link"]
        sp_files = os.listdir()
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(videoresult, download=False)
        url_misic = info['formats'][0]['url']
        add_music = {name: url_misic}
        sp_music.append(add_music)
    em_playlist = discord.Embed(title="Плейлист", colour=0x87CEEB)
    em_playlist.set_author(name="Raxun", icon_url="https://avatars.githubusercontent.com/u/94015674?s=400&u=7d739"
                                                  "fe0e1593df54e804fb6e097f597a3a838d7&v=4")
    for i, elem in enumerate(sp_music):
        name = elem.key()
        em_playlist.add_field(name=str(i + 1), value=name, inline=False)
    await ctx.message.channel.send(embed=em_playlist)


@bot.command('старт')
async def start_music(ctx):
    for element in sp_music:
        url_music = element.value()
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
        await asyncio.sleep(1)
        vc.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=url_misic, **FFMPEG_OPTIONS))


@bot.command('стоп')
async def stop_music(ctx):
    global sp_music, vs
    sp_music = []
    await ctx.voice_client.disconnect()


@bot.command('роль')
async def role(ctx, role):
    all_roles = []
    for role in bot.get_guild(ctx.channel).roles:
        all_roles.append(role.id)
    all_roles.reverse()  # to make it higher first
    all_roles = ['<@&' + str(all_roles[i]) + '>' for i in range(len(all_roles)) if all_roles[i] not in prohibited_roles]
    em_roles.set_author(name="Raxun", icon_url="https://avatars.githubusercontent.com/u/94015674?s=400&u=7d739"
                                               "fe0e1593df54e804fb6e097f597a3a838d7&v=4")
    em_roles.add_field(name="Команды", value='!роль (тег роли)', inline=False)
    em_roles.add_field(name="Роли", value=' | '.join(all_roles), inline=True)
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
