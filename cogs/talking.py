import asyncio
from discord.ext import commands
import string

from utils.talking_utils import get_response


class talkingfunctions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.author == self.bot.user:  # If message is from itself, do nothing
                return
            if message.author.bot:  # If message is a bot, do nothing
                return

            if message.mentions:
                tagged = message.mentions
                if tagged[0].id == self.bot.user.id:
                    await process(message, self.bot)
            if "botname" in message.content.lower():
                await process_name(message, self.bot)
        except Exception as e:
            print(f"speech function: {e}")


async def process(message, bot):
    try:
        msg = message.content.lower().translate(str.maketrans('', '', string.punctuation)).replace(
            str(bot.user.id), "").split(" ")
        while "" in msg:
            msg.remove("")
        msg = " ".join(msg)
        response = await get_response(msg)
        if response:
            await message.reply(response)
        return
    except Exception as e:
        print(f"speech function process: {e}")


async def process_name(message, bot):
    try:
        msg = message.content.lower().translate(str.maketrans('', '', string.punctuation)).replace(
            str(bot.user.id), "").replace("botname", "").split(" ")
        while "" in msg:
            msg.remove("")
        msg = " ".join(msg)
        response = await get_response(msg)
        if response:
            await message.reply(response)
        return
    except Exception as e:
        print(f"speech function process: {e}")


async def setup(bot):
    await bot.add_cog(talkingfunctions(bot))