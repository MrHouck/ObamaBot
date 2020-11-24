import discord, requests, asyncio, http.client,random,os
from discord.ext import commands, tasks

bot = commands.Bot(case_insensitive=True, command_prefix="obama ")
bot.link_cache = {}
def urlExists(url):
    r=requests.get(url.replace("obama.mp4", "video_created.txt"))

    return r.status_code != 404

@bot.event
async def on_ready():
    clear_cache.start()
    print("OBAMAFYING EVERYTHING........")

@bot.command()
async def say(ctx, *, text):
    """
    obama says something funny yes
    """
    if text == None or text.startswith("http"):
        return
    if ctx.author.id == 471389057184694273:
        await ctx.message.delete()
        await ctx.send("blacklisted kid die")
        return
    if text in bot.link_cache.keys():
        await ctx.message.delete()
        return await ctx.send(f"{ctx.author.mention} says: \n{bot.link_cache[text]}")
    res=requests.post("http://talkobamato.me/synthesize.py", data={"input_text":text})
    headers=res.headers
    video_url="http://talkobamato.me/synth/output/{}/obama.mp4"
    url = video_url.format(res.url.split('/')[3].replace("?speech_key=","").replace("synthesize.py",""))
    msg = await ctx.channel.send("Processing...")

    if urlExists(url) == False:
        while urlExists(url) == False:
            await asyncio.sleep(2)
    bot.link_cache[text] = url 
    await msg.edit(content=f"{ctx.author.mention} says: \n"+url)

@bot.command()
async def picture(ctx):
    """
        get this: a picture of barrack obama OR!!! michelle obama
    """
    if random.randint(0, 1) == 0:
        files = os.listdir("./pictures")
        r= random.choice(files)
        await ctx.send(file=discord.File(f"./pictures/{r}"))
    else:
        files = os.listdir("./michelle")
        r= random.choice(files)
        await ctx.send(file=discord.File(f"./michelle/{r}"))

@bot.command()
async def barrack(ctx):
    """
    picture of barrack obama
    """
    files = os.listdir("./pictures")
    r= random.choice(files)
    await ctx.send(file=discord.File(f"./pictures/{r}"))

@bot.command()
async def michelle(ctx):
    """
    picture of michelle obama
    """
    files = os.listdir("./michelle")
    r= random.choice(files)
    await ctx.send(file=discord.File(f"./michelle/{r}"))

@bot.command()
@commands.cooldown(3, 10, commands.BucketType.user)
async def ping(ctx):
    """
    ping pong mf
    """
    return await ctx.send(str(round(bot.latency*1000,3)) + "ms")

@ping.error
async def ping_e(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        return await ctx.send("cooldown smh")

@bot.event
async def on_message(message):
    print(bot.link_cache)
    if message.author != bot.user and (message.channel.id == 778299733902622730 or message.channel.id == 778376412724985866):
        if message.content == None or message.content.startswith("http"):
            return
        if message.author.id == 471389057184694273:
            await message.delete()
            return
        text = message.clean_content
        if text in bot.link_cache.keys():
            await message.delete()
            return await message.channel.send(f"{message.author.mention} says: \n{bot.link_cache[text]}")
        print('post')
        res=requests.post("http://talkobamato.me/synthesize.py", data={"input_text":text})
        print('ha')
        headers=res.headers
        video_url="http://talkobamato.me/synth/output/{}/obama.mp4"
        await message.delete()
        url = video_url.format(res.url.split('/')[3].replace("?speech_key=","").replace("synthesize.py",""))
        msg = await message.channel.send("Processing...")

        if urlExists(url) == False:
            while urlExists(url) == False:
                await asyncio.sleep(2)
        bot.link_cache[text] = url
        await msg.edit(content=f"{message.author.mention} says: \n"+url)

        
    else:
        await bot.process_commands(message)


@tasks.loop(minutes=20)
async def clear_cache():
    bot.link_cache = {}
    print("Cleared cache")
bot.run("Nzc4Mjk3MTkxNzY0NDU5NTYw.X7P7vg.hTFGavdrm2Io3_scCLVP1qEgF6I")
