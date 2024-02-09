import discord
from discord.commands import Option
import json
import os
import aiosqlite
from dotenv import load_dotenv

load_dotenv()
with open("./data.json") as dataFile:
    data = json.load(dataFile)
intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

con = None


@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(f"Doing Something")
    )
    global con
    con = await aiosqlite.connect("Main.db")
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    if message.content.startswith(data['prefix']):
        msg = message.content.replace(data['prefix'], '', 1)

        if msg.startswith('roll'):
            lmsg = msg.split(' ')
            try:
                rollNo = int(lmsg[1])
                rmmsg = " ".join(lmsg[2:])
            except:
                await message.reply(f"Incorrect Format: {msg}")
            else:
                await message.channel.send(f"Roll No: {rollNo} {rmmsg}")


@bot.slash_command(name="hello", description="dasdasdas")
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond("Hey!")


@bot.slash_command(name="set-id", description="dasdasdas")
async def setId(ctx: discord.ApplicationContext, roll: Option(str, description="Enter your Roll Number"), user: Option(discord.user.User, description="Mention Member")):
    await con.execute("UPDATE users SET userid = ? WHERE rollno = ?", (user.id, roll))
    await con.commit()
    await ctx.respond(f"<@{user.id}> is Roll: {roll}")


@bot.slash_command(name="roll-message", description="dasdasdas")
async def rollMessage(ctx: discord.ApplicationContext, roll: Option(str, description="Enter your Roll Number"), message: Option(str, description="Enter Message", required=False, default="")):
    rolls = []

    # Split input by spaces to handle individual rolls or ranges
    roll_parts = roll.split(" ")

    for part in roll_parts:
        if '-' not in part:
            try:
                rolls.append(int(part))
            except ValueError:
                pass
        else:
            range_parts = part.split("-")
            try:
                start_roll = min(int(range_parts[0]), int(range_parts[1]))
                end_roll = max(int(range_parts[0]), int(range_parts[1]))
                rolls.extend(range(start_roll, end_roll + 1))
            except ValueError:
                pass

    # Using a parameterized query to prevent SQL injection
    query = f"SELECT rollno, username, userid FROM users WHERE rollno IN {tuple(rolls)}"
    result = await con.execute(query)
    results = await result.fetchall()

    msg = ""
    for row in results:
        try:
            roll = row[0]
            name = row[1]
            id = row[2]
            msg += f"{roll}) {name}, {message}\n" if id is None else f"{roll}) <@{id}>, {message}\n"
        except IndexError:
            msg += f"{roll}) Unknown, {message}\n"
    if msg == "":
        msg = f"{message}\n"
    await con.commit()
    await ctx.respond(msg)


bot.run(str(os.getenv("TOKEN")))
