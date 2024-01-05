# Base imports
import html
import os
import re
from hashlib import md5
from typing import Tuple, Union

# Installed Imports
import aiohttp
import discord
from discord.abc import GuildChannel
from discord.ext import commands, tasks
from dotenv import load_dotenv

# Local Imports
from DiscordBlogBot.blog_list import BLOGS, NON_WP_BLOGS

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

LOOP_SPEED = 5


# printing hashes of secrets instead of secrets
def print_secret(secret_to_hash: Union[int, str]) -> str:
    """Returns MD5 hash of an input.
    Parameters:
    secret_to_hash (Union[int, str]) a secret whose hash should be printed

    Returns:
    hexdigest (str) hexdigest of md5 of initial secret
    """
    try:
        encoded_string = str(secret_to_hash).encode("utf-8")
        hash_object = md5(encoded_string, usedforsecurity=False)
    except TypeError as e:
        print(f"Trouble with encoding, generating rando instead. Error:{e}")
        from random import SystemRandom
        return SystemRandom().random()
    return hash_object.hexdigest()


# Defining Discord bot
# TODO why prefix = "!" ?
# TODO maybe fewer intents are required than used.
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


async def fetch_latest_wp_blog_post(
    session: aiohttp.ClientSession, blog_dict: dict
) -> Tuple[int, str]:
    """ Gets the most recent blog post from a Wordpress blog.
    Parameters:
    session (aiohttp.ClientSession): client session to make GET request
    blog_dict (dict): dict containing info needed to fetch blog and make string

    Returns: blog_id (int), print_string
    """
    blog_api = blog_dict["url"]
    # asynch context manager (!)
    async with session.get(
        blog_api + "/posts", params={"per_page": 1, "orderby": "date"}
    ) as response:
        response.raise_for_status()
        try:
            latest_post = await response.json()
            post_id = latest_post[0]["id"]
            title = html.unescape(latest_post[0]["title"]["rendered"])
            # TODO different encoding for posting time, date is fine,
            # time not really helpful.
            posting_time = latest_post[0]["date"]
            post_url = latest_post[0]["link"]
            author = blog_dict["author"]
            post_print_string = (
                "HEY, LISTEN! \nNew Blog post from "
                + f"{author}! Released on {posting_time}!\nTitle: {title} "
                + f"\nLink:{post_url}"
            )
            return post_id, post_print_string
        except (IndexError, KeyError) as e:
            print(f"Error parsing JSON: {e}")
            return None, None


async def fetch_latest_non_wp_blog_post(
    session: aiohttp.ClientSession, blog_dict: dict
) -> Tuple[str, str]:
    """ Gets the most recent blog post from a Non-Wordpress blog.
    Parameters:
    session (aiohttp.ClientSession): client session to make GET request
    blog_dict (dict): dict containing info needed to fetch blog and make string

    Returns: blog_slug (str), print_string (str)
    """
    update_url = blog_dict["url"] + blog_dict["update_route"]
    async with session.get(update_url) as response:
        response.raise_for_status()

        script_content = re.search(r" /blog/slug/[^;]+", await response.text())
        if script_content:
            lastest_post_route = script_content.group().strip()
            author = blog_dict["author"]
            post_print_string = (
                "HEY, LISTEN! \nNew Blog post from "
                + f"{author}! \n Link:{blog_dict['url'] + lastest_post_route}"
            )
            return lastest_post_route, post_print_string
        else:
            print("Failed to find blog post at URL")
            return None, None


async def send_latest_blog_post(
    channel: GuildChannel,
    blog_info_to_be_printed: str
) -> None:
    """ Sends the printstring to the discord channel.
    Parameters:
    channel (GuildChannel): GuildChannel object to send post to
    blog_info_to_be_printed (str): pre-generated string to send to channel

    Raises (Exception): if channel not found
    """
    # TODO replace with logger
    print(blog_info_to_be_printed)
    if channel:
        await channel.send(blog_info_to_be_printed)
    else:
        raise Exception(f"Channel {channel} not found! GO FIX!")


# Event decorator for discord bot to loop
@tasks.loop(seconds=LOOP_SPEED)
async def blog_post_task(
    session: aiohttp.ClientSession,
    channel: GuildChannel
) -> None:
    """ Loops and calls fetchers and sender.
    Parameters:
    channel (GuildChannel): GuildChannel object to send post to
    session (aiohttp.ClientSession): client session to make GET request
    """
    # TODO check session is alive at beginning of each loop

    # Iterate through Wordpress blogs
    for blog_dict in BLOGS:
        post_id, blog_info_to_be_printed = await fetch_latest_wp_blog_post(
            session, blog_dict
        )
        if post_id not in blog_dict["buffer"]:
            # if it's a new post, add it to the buffer
            blog_dict["buffer"].add(post_id)
            await send_latest_blog_post(channel, blog_info_to_be_printed)

    # Iterate through other blogs
    for blog_dict in NON_WP_BLOGS:
        (
            id_surrogate_route,
            blog_info_to_be_printed,
        ) = await fetch_latest_non_wp_blog_post(session, blog_dict)
        if id_surrogate_route not in blog_dict["buffer"]:
            # if it's a new post, add it to the buffer
            blog_dict["buffer"].add(id_surrogate_route)
            await send_latest_blog_post(channel, blog_info_to_be_printed)


# Event decorator for discord bots
@bot.event
async def on_ready():
    """ Startup configurations.Gets session and channel object,
        Populates the buffers.
    """
    # Called once when the bot is initialized
    print(
        f"Logged in as {bot.user.name} with ID ({print_secret(bot.user.id)})"
    )

    # Initialize aiohttp session
    session = aiohttp.ClientSession()
    # Get Discord Channel object
    channel = bot.get_channel(CHANNEL_ID)
    for blog_dict in BLOGS:
        blog_dict["buffer"] = set()
        post_id, _ = await fetch_latest_wp_blog_post(session, blog_dict)
        blog_dict["buffer"].add(post_id)
    for blog_dict in NON_WP_BLOGS:
        blog_dict["buffer"] = set()
        id_surrogate_route, _ = await fetch_latest_non_wp_blog_post(
            session,
            blog_dict
        )
        blog_dict["buffer"].add(id_surrogate_route)

    blog_post_task.start(session, channel)


# so the file doesn't run when imported
if __name__ == "__main__":
    # But when the file is run, run the bot with its token.
    bot.run(BOT_TOKEN)
