# DiscordBlogBot
Bot that posts new blog post announcements in given discord channel

## General Setup
TODO Finish writing instructions
TODO format this file

Create Discord bot in Discord Dev Portal
Get Token from Bot
Make sure to activate permissions for all (3) intents.

## repo_secrets.py

The file 'repo_secrets.py' should contain the following information: Blogdata, ChannelID, Bot Token.
Add them as follows:
```python
BOT_TOKEN='INSERT BOT TOKEN HERE'
CHANNEL_ID=INSERT CHANNEL ID HERE
BLOGS=[{
'author':'Blog_Author', 'url':'wordpress URL',
}]
NON_WP_BLOGS=[{
'author':'Blog_Author', 'url':'wordpress URL', 'update_route':'/route'
}]
```
such that:
The bot token contains a string of the bot token from Discord (see discord bot dev portal)
the Channel ID is the id of the channel you want the bot to post the messages in (see LINK on how to make channel ID visible)
BLOGS is a list containing dicts of entires, one for each blog. The author is self-explanatory,
the url should point to the blog base API. So if your blog is "https://mysuperblog.com", then the url you need is:
'https://public-api.wordpress.com/wp/v2/sites/mysuperblog.com'
NON_WP_BLOGS is a similar list of blogs with author such that url points to the base website, and update_route is such that the concantenation of url and update_route always points to the newest blog article.
if the website does NOT have such a thing, good luck.

