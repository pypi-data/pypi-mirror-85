  # -*- coding: utf-8 -*-
 
"""
“Commons Clause” License Condition Copyright Pirxcy/Oli 2019-2020 / 2020-202
 
The Software is provided to you by the Licensor under the
License, as defined below, subject to the following condition.
 
Without limiting other conditions in the License, the grant
of rights under the License will not include, and the License
does not grant to you, the right to Sell the Software.
 
For purposes of the foregoing, “Sell” means practicing any or
all of the rights granted to you under the License to provide
to third parties, for a fee or other consideration (including
without limitation fees for hosting or consulting/ support
services related to the Software), a product or service whose
value derives, entirely or substantially, from the functionality
of the Software. Any license notice or attribution required by
the License must also include this Commons Clause License
Condition notice.
 
Software: AnimeBot (SevenBot)
 
License: Apache 2.0
"""
 
__name__ = "AnimeBot"
__author__ = "Pirxcy"
__version__ = "1.0.2"
 
import random
import asyncio
import time
import itertools
import unicodedata 
import ssl
import json
import time
import re
import aiohttp
import discord
import timeago
import sanic
import ssl
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
from discord.ext.commands import guild_only
from itertools import cycle
from sanic import Sanic
from sanic.response import text

print("Bot Logging In...")

with open('config.json') as f:
    data = json.load(f)

prefix1 =(data['prefix'])
TOKEN =(data['token'])
GAME_NAME = 'My Prefix is !\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n Enjoy'

status = cycle(['!help' 'with Hiro 💖' 'On {self.bot.servers}'])

app = Sanic(__name__)
bot = commands.Bot(command_prefix=prefix1)
client = commands.Bot(command_prefix=prefix1)
bot.remove_command('help')

kalib = "AnimeBot"

@app.route('/')
async def hello_world(request):
    return text('Bot Ready As {kalib}')

@bot.command()
async def ride(ctx):
  file = discord.File("daft.mp4")
  await ctx.send(file=file)
  

@bot.command()
async def lucidcry(ctx):
  file = discord.File("lucid.mp4")
  await ctx.send(file=file)

@bot.command()
async def Ride(ctx):
  file = discord.File("daft.mp4")
  await ctx.send(file=file)

@bot.command()
async def Darling(ctx):
  file = discord.File("darling.mp4")
  await ctx.send(file=file)

@bot.command()
async def darling(ctx):
  file = discord.File("darling.mp4")
  await ctx.send(file=file)

@bot.event
async def on_ready():
  ch_pr.start()
  print(f'Bot is ready! Logged in as {bot.user.name} [{bot.user.id}]')
  await app.create_server(host="0.0.0.0",port=8080, return_asyncio_server=True)

@tasks.loop(seconds=10)
async def ch_pr():
  statuses = ["!help", f"with {len(bot.guilds)} Servers | !help", "with Hiro 💖"]     
  status = random.choice(statuses)
  await bot.change_presence(activity=discord.Game(name=status))

@bot.command()
async def Help(ctx):
    url = "https://pastebin.com/raw/YsVc4nN6"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            text = await res.text(encoding="utf-8")
    embed = discord.Embed(
        title=f'All Commands And What They DO',
        description=text,
        color=0xff0000
    )
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    url = "https://pastebin.com/raw/YsVc4nN6"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            text = await res.text(encoding="utf-8")
    embed = discord.Embed(
        title=f'All Commands And What They DO',
        description=text,
        color=0xff0000
    )
    await ctx.send(embed=embed)

@bot.command()
async def Upcoming(ctx):
    url = "https://pastebin.com/raw/Ksrreu80"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            text = await res.text(encoding="utf-8")
    embed = discord.Embed(
        title=f'Upcoming Features',
        description=text,
        color=0xff0000
    )
    await ctx.send(embed=embed)

@bot.command()
async def upcoming(ctx):
    url = "https://pastebin.com/raw/Ksrreu80"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            text = await res.text(encoding="utf-8")
    embed = discord.Embed(
        title=f'Upcoming Features',
        description=text,
        color=0xff0000
    )
    await ctx.send(embed=embed)

@bot.command()
async def Whatsnew(ctx):
    url = "https://pastebin.com/raw/6zp34aK0"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            text = await res.text(encoding="utf-8")
    
    embed = discord.Embed(  
        title=f'Newest Features',
        description=text,
        color=0xff0000
    )
    embed.set_footer(text='AnimeBot By <@733302490753269852>')
    await ctx.send(embed=embed)

@bot.command()
async def whatsnew(ctx):
    url = "https://pastebin.com/raw/6zp34aK0"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            text = await res.text(encoding="utf-8")
    embed = discord.Embed(
        title=f'Newest Features',
        description=text,
        color=0xff0000
    )
    embed.set_footer(text='AnimeBot By <@733302490753269852>')
    await ctx.send(embed=embed)

@bot.command()
async def nuke(ctx, amount=9999):
  await ctx.channel.purge(limit=amount)
  time.sleep(0.5)
  responses_list = ['***Nuked*** __this channel__ :white_check_mark:\n"You are now...my darling!"\n「あなたは今...私の最愛の人です！」\nZero Two (Japanese: ゼロツー, Hepburn: Zero Tsū)\nhttps://i.kym-cdn.com/photos/images/original/001/332/861/61b.gif', '***Nuked*** __this channel__ :white_check_mark:\n"I feel the same! Zero Two, I love you too!"\n-Hiro\n https://imgur.com/nL0CSWm', '***Nuked*** __this channel__ :white_check_mark:\n“ Im not gonna run away, I never go back on my word! That’s my nindo: my ninja way.”\n-Naruto\nhttps://i.pinimg.com/originals/d8/7e/17/d87e1799ab54d12da50ebff62b6f584b.gif', '***Nuked*** __this channel__ :white_check_mark:\n“Pika, pika chu”\nhttps://i.giphy.com/media/h3XmHtJQLEMyk/giphy.webp', '***Nuked*** __this channel__ :white_check_mark:\n“ My friends were the first to accept me for who I am.”\n Naruto.\n https://i.pinimg.com/originals/04/c7/89/04c7897eaac3a6cc37aa9989366b9c18.gif', '***Nuked*** __this channel__ :white_check_mark:\nhttps://i.kym-cdn.com/photos/images/newsfeed/001/334/590/96c.gif', '***Nuked*** __this channel__ :white_check_mark:\nhttps://imgur.com/a/86qKhoz']
  choice = random.choice(responses_list)
  await ctx.send(f"{choice}")
  if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("You don't have permission")

@bot.command()
async def Nuke(ctx, amount=9999):
  await ctx.channel.purge(limit=amount)
  time.sleep(0.5)
  responses_list = ['***Nuked*** __this channel__ :white_check_mark:\n"You are now...my darling!"\n「あなたは今...私の最愛の人です！」\nZero Two (Japanese: ゼロツー, Hepburn: Zero Tsū)\nhttps://i.kym-cdn.com/photos/images/original/001/332/861/61b.gif', '***Nuked*** __this channel__ :white_check_mark:\n"I feel the same! Zero Two, I love you too!"\n-Hiro\n https://imgur.com/nL0CSWm', '***Nuked*** __this channel__ :white_check_mark:\n“ Im not gonna run away, I never go back on my word! That’s my nindo: my ninja way.”\n-Naruto\nhttps://i.pinimg.com/originals/d8/7e/17/d87e1799ab54d12da50ebff62b6f584b.gif', '***Nuked*** __this channel__ :white_check_mark:\n“Pika, pika chu”\nhttps://i.giphy.com/media/h3XmHtJQLEMyk/giphy.webp', '***Nuked*** __this channel__ :white_check_mark:\n“ My friends were the first to accept me for who I am.”\n Naruto.\n https://i.pinimg.com/originals/04/c7/89/04c7897eaac3a6cc37aa9989366b9c18.gif', '***Nuked*** __this channel__ :white_check_mark:\nhttps://i.kym-cdn.com/photos/images/newsfeed/001/334/590/96c.gif', '***Nuked*** __this channel__ :white_check_mark:\nhttps://imgur.com/a/86qKhoz']
  choice = random.choice(responses_list)
  await ctx.send(f"{choice}")
  if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("You don't have permission")

@bot.command()
async def fotd(ctx):
    url = "https://pastebin.com/raw/AycH0XVP"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            text = await res.text(encoding="utf-8")
    embed = discord.Embed(
        title=f'Your Fact of The Day is',
        description=text,
        color=0xff0000
    )
    embed.set_footer(text='AnimeBot By <@733302490753269852>')
    await ctx.send(embed=embed)

@bot.command()
async def Fotd(ctx):
    url = "https://pastebin.com/raw/AycH0XVP"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            text = await res.text(encoding="utf-8")
    embed = discord.Embed(
        title=f'Your Fact of The Day is',
        description=text,
        color=0xff0000
    )
    embed.set_footer(text='AnimeBot By <@733302490753269852>')
    await ctx.send(embed=embed)


@bot.command()
async def qotd(ctx):
    url = "https://pastebin.com/raw/Bgi68c8d"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            text = await res.text(encoding="utf-8")
    embed = discord.Embed(
        title=f'Your Question of The Day is',
        description=text,
        color=0xff0000
    )
    embed.set_footer(text='AnimeBot By <@733302490753269852>')
    await ctx.send(embed=embed)

@bot.command()
async def Qotd(ctx):
    url = "https://pastebin.com/raw/Bgi68c8d"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            text = await res.text(encoding="utf-8")
    embed = discord.Embed(
        title=f'Your Question of The Day is',
        description=text,
        color=0xff0000
    )
    embed.set_footer(text='AnimeBot By <@733302490753269852>')
    await ctx.send(embed=embed)

@bot.command()
async def crash(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://pastebin.com/raw/6k6dgRTq") as res:
            text = await res.text(encoding="utf-8")
            embed = discord.Embed(color=0xff0000)
            embed.set_footer(text='AnimeBot By <@733302490753269852>')
    await ctx.send(text)


@bot.command()
async def status(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://pastebin.com/raw/0ze8ad4V") as res:
            text = await res.text(encoding="utf-8")
            embed = discord.Embed(color=0xff0000)
            embed.set_footer(text='AnimeBot By <@733302490753269852>')
    await ctx.send(text)

@bot.command()
async def ping(ctx):
    t_1 = time.perf_counter()
    await ctx.trigger_typing()
    t_2 = time.perf_counter()
    ms = round((t_2-t_1)*1000)
    embed = discord.Embed(color=0xff0000)
    embed.add_field(name=":ping_pong: Pong!", value = f"{ms}ms")
    embed.set_footer(text='AnimeBot By <@733302490753269852>')
    await ctx.send(embed=embed)    


@bot.command()
async def Ping(ctx):
    t_1 = time.perf_counter()
    await ctx.trigger_typing()
    t_2 = time.perf_counter()
    ms = round((t_2-t_1)*1000)
    embed = discord.Embed(color=0xff0000)
    embed.add_field(name=":ping_pong: Pong!", value = f"{ms}ms")
    embed.set_footer(text='AnimeBot By <@733302490753269852>')
    await ctx.send(embed=embed)

@bot.command()
async def invite(ctx):
    await ctx.send(f"{ctx.author.mention} Add This To Your Server For an Awesome Anime Experience https://discord.com/api/oauth2/authorize?client_id=770030131418234892&permissions=8&scope=bot")

@bot.command()
async def commands(ctx):
    embed = discord.Embed(color=0x00ffff)
    embed.add_field(name=f"{bot.user.name}'s Commands List", value = "`ping` `help` `invite` `ban` `kick` `choose` `jointime` `nuke` `whatsnew` `upcoming` `crash`  `qotd` `fotd` `commands` `ride`")
    embed.set_footer(text='AnimeBot By <@733302490753269852>')
    await ctx.send(embed=embed)

@bot.command()
async def Commands(ctx):
    embed = discord.Embed(color=0x00ffff)
    embed.add_field(name=f"{bot.user.name}'s Commands List", value = "`ping` `help` `invite` `ban` `kick` `choose` `jointime` `nuke` `whatsnew` `upcoming` `crash`  `qotd` `fotd` `commands` `ride`")
    embed.set_footer(text='AnimeBot By <@733302490753269852>')
    await ctx.send(embed=embed)

@bot.command()
async def credit(ctx):
    embed = discord.Embed(color=0x00ffff)
    embed.add_field(name=f"{bot.user.name} was Coded/Made By", value = "Pirxcy and Gomashio")
    embed.set_thumbnail(url='https://i.imgur.com/c1bumIE.gif')
    embed.set_image(url='https://cdn.discordapp.com/attachments/769636434264850433/771057317529518100/tenor.gif')
    embed.set_footer(text='Support Him By Joining The Discord Server - https://discord.gg/xHHv8aJ')
    await ctx.send(embed=embed)

@bot.command()
async def credits(ctx):
    embed = discord.Embed(color=0x00ffff)
    embed.add_field(name=f"{bot.user.name} was Coded/Made By", value = "<@733302490753269852> and Gomashio")
    embed.set_thumbnail(url='https://i.imgur.com/c1bumIE.gif')
    embed.set_image(url='https://i.imgur.com/c1bumIE.gif')
    embed.set_footer(text='Support Him By Joining The Discord Server - https://discord.gg/xHHv8aJ')
    await ctx.send(embed=embed)

@bot.command()
async def Credit(ctx):
    embed = discord.Embed(color=0x00ffff)
    embed.add_field(name=f"{bot.user.name} was Coded/Made By", value = "<@733302490753269852>")
    embed.set_thumbnail(url='https://i.imgur.com/c1bumIE.gif')
    embed.set_author(name='Pirxcy')
    embed.set_image(url='https://i.imgur.com/c1bumIE.gif')
    embed.set_footer(text='Support Him By Joining The Discord Server - https://discord.gg/xHHv8aJ')
    await ctx.send(embed=embed)

@bot.command()
async def Credits(ctx):
    embed = discord.Embed(color=0x00ffff)
    embed.add_field(name=f"{bot.user.name} was Coded/Made By", value = "<@733302490753269852>")
    embed.set_thumbnail(url='https://i.imgur.com/c1bumIE.gif')
    embed.set_author(name='Pirxcy')
    embed.set_image(url='https://i.imgur.com/c1bumIE.gif')
    embed.set_footer(text='Support Him By Joining The Discord Server - https://discord.gg/xHHv8aJ')
    await ctx.send(embed=embed)


@bot.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason: str = None):
    if reason == None:
        reason = 'No Reason Provided'
    await member.kick(reason=reason)
    embed = discord.Embed(color=0x0000ff)
    embed.add_field(name=f"{user} has been banned by {ctx.message.author}", value = f"`{reason}`")
    embed.set_footer(text='AnimeBot By <@733302490753269852>')
    await ctx.send(embed=embed)
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("You don't have permission")

@bot.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason: str = None):
    if reason == None:
        reason = 'No Reason Provided'
    await member.kick(reason=reason)
    embed = discord.Embed(color=0x0000ff)
    embed.add_field(name=f"{user} has been kicked by {ctx.message.author}", value = f"`{reason}`")
    embed.set_footer(text='AnimeBot By <@733302490753269852>')
    await ctx.send(embed=embed)
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("You don't have permission")

@bot.command()
async def choose(ctx, *choice: str):
    await ctx.send(f"{ctx.message.author} - I choose **{choice}**!")

@bot.command()
@guild_only()
async def jointime(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.message.author
    await ctx.send(f'{member.name} joined at `{member.joined_at}`')

@bot.command(aliases=["8ball"])
async def eightball(ctx):
    responses_list = ['Yes.', 'No.', 'Maybe.', 'Definitely', 'Not at all.', 'Ask me another time.']
    choice = random.choice(responses_list)
    embed = discord.Embed(color=0xFFFFFF)
    embed.add_field(name=":8ball: 8Ball Says...", value=f'`{choice}`')
    embed.set_footer(text='AnimeBot By <@733302490753269852>')
    await ctx.send(embed=embed)

@bot.command(aliases=["anime?"])
async def howanime(ctx):
    responses_list = ['5% Anime (╯°□°）╯︵ ┻━┻', '50% Anime', '69% Anime', 'Your Fulltime Anime God ¯\_(ツ)_/¯', 'Not at all Anime...', '75% Anime']
    choice = random.choice(responses_list)
    embed = discord.Embed(color=0xFFFFFF)
    embed.add_field(name="You Are...", value=f'`{choice}`')
    embed.set_footer(text='AnimeBot By <@733302490753269852>')
    await ctx.send(embed=embed)

@bot.command(aliases=["howbig"])
async def pp(ctx):
    responses_list = ['8=D', '8==D', '8===D', '8====D', '8=====D', '8=========D']
    choice = random.choice(responses_list)
    embed = discord.Embed(color=0xFFFFFF)
    embed.add_field(name="Ur Size is... ", value=f'`{choice}`')
    embed.set_footer(text='AnimeBot By <@733302490753269852>')
    await ctx.send(embed=embed)

bot.run(TOKEN)