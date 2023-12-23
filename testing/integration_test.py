import pytest
from unittest.mock import AsyncMock
from DiscordBlogBot.main import blog_post_task, intents
from aioresponses import aioresponses
from discord.ext import commands
import aiohttp
import asyncio

# Sample blog post response from the WordPress API
SAMPLE_BLOG_POST = [
    {
        'id': 123,
        'title': {'rendered': 'Test Title'},
        'date': '2022-01-01T12:00:00',
        'link': 'https://example.com/test-post',
    }
]

# Sample WordPress blog information
WP_BLOG_INFO = {'author': 'Author1', 'url': 'https://wordpress-site-1.com'}

# Sample channel ID
CHANNEL_ID = 123456789012345678

@pytest.mark.asyncio
async def test_integration_wp_blog_and_bot():
    # Create a mock bot
    bot = commands.Bot(command_prefix="!", intents=intents)

    # Set the bot's session
    bot.http_session = aiohttp.ClientSession()

    # Set the bot's loop
    bot.loop = asyncio.get_event_loop()

    # Set the bot's token
    bot.token = "mock_bot_token"

    # Mock the bot's get_channel function for fetching the bot channel
    async def mock_get_channel(channel_id):
        assert channel_id == CHANNEL_ID
        return mock_channel

    # Set the bot's get_channel function
    bot.get_channel = AsyncMock(return_value=mock_get_channel(CHANNEL_ID))

    # Set the bot's channel
    mock_channel = bot.get_channel.return_value

    # Start the blog post task
    blog_post_task.start(bot.http_session, mock_channel)

    # Mock the aiohttp client session using aioresponses
    with aioresponses() as mock_session:
        # Mock the response for the WordPress blog API
        mock_session.get(
            f"{WP_BLOG_INFO['url']}/posts",
            payload=SAMPLE_BLOG_POST,
            status=200
        )

        # Wait for the loop to run
        await asyncio.sleep(0.5)

    # Stop the blog post task
    blog_post_task.stop()
