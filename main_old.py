import discord
from discord.commands import Option
import json
import os
from dotenv import load_dotenv

load_dotenv()
with open("./data.json") as dataFile:
    data = json.load(dataFile)

intents = discord.Intents.all()


bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
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


@bot.slash_command(name="roll-message", description="dasdasdas")
async def roll(ctx: discord.ApplicationContext, roll: Option(int, description="Enter your Roll Number"), message: Option(str, description="Enter Message", required=False, default="")):
    response = f"Roll No: {roll} \nName: {data['names'][roll-1]}"
    if (message != ""):
        response += f"\nMessage: {message}"
    await ctx.respond(response)


@bot.slash_command(name="bulk-roll-message", description="dasdasdas")
async def bulkRoll(ctx: discord.ApplicationContext, roll: Option(str, description="Enter your Roll Number"), message: Option(str, description="Enter Message", required=False, default="")):
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
                start_roll = int(range_parts[0])
                end_roll = int(range_parts[1])
                rolls.extend(range(start_roll, end_roll + 1))
            except ValueError:
                pass

    msg = ""
    for roll_number in rolls:
        try:
            name = data['names'][roll_number-1]
            msg += f"{roll_number}) {name}, {message}\n"
        except IndexError:
            msg += f"{roll_number}) Unknown, {message}\n"

    await ctx.respond(msg)


bot.run(str(os.getenv("TOKEN")))
