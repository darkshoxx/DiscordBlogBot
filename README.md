# DiscordBlogBot

Bot that posts new blog post announcements in given discord channel.
Written by darkshoxx. Equipped with an MIT license, so enjoy distribution.

## Requirements

- Server or PC running python 3.7+
- Discord server where you are owner

## General Setup

### Make Bot

Create Discord application/bot in Discord Dev Portal  
https://discord.com/developers/applications  
Give it a name  
Get Token from Bot:  
navigate  
![image1](/images_for_readme/image1.png)  
it will either display a token, or you'll need to reset the current token.  
![image2](/images_for_readme/image2.png)  
It will only be displayed once, so copy that immediately, it's one of the secrets
that goes into the environment variables (see below).
Make sure to activate permissions for all (3) intents.  
![image3](/images_for_readme/image3.png)  
Navigate to OAuth2 -> URL Generator  
Select "bot"  
Select permissions, "Send Message" and "View Channels" (TODO: Is View Channels Required?)  
Copy the link on the bottom into a browser, follow instructions to invite bot to channel.  
![image4](/images_for_readme/image4.png)  
The bot should now appear in your channel.

### Get your Channel Id:

#### Make sure you have Developer Mode enabled:

In discord, go to your user settings (cog at the bottom) navigate to  
App-Settings -> Advanced  
and make sure Developer mode is checked.  
![image5](/images_for_readme/image5.png)

#### Get Id:

Right-click the channel you want the updates to be posted in  
![image6](/images_for_readme/image6.png)  
Copy the ID and paste it in the environment variables, see below.  
Create a file ".env" in the same folder as main.py, and follow the instructions below on how to fill it.

## Environment variables

The file '.env' should contain the following information:  
ChannelID, Bot Token.  
Add them as follows:

```t
BOT_TOKEN='INSERT BOT TOKEN HERE'
CHANNEL_ID=INSERT CHANNEL ID HERE
```

such that:  
The bot token contains a string of the bot token from Discord  
(see above on how to get the token)  
The Channel ID is the id of the channel you want the bot to post the messages in
(see above on how to get the channel ID)

## Blog List

Replace the blogs in the `blog_list.py` file with your own list of blogs, using the following format

```t
BLOGS=[{
'author':'Blog_Author', 'url':'wordpress URL',
}]
NON_WP_BLOGS=[{
'author':'Blog_Author', 'url':'wordpress URL', 'update_route':'/route'
}]
```

BLOGS is a list containing dicts of entires, one for each blog.  
The author is self-explanatory,  
the url should point to the blog base API.
So if your blog is "https://mysuperblog.com", then the url you need is:  
'https://public-api.wordpress.com/wp/v2/sites/mysuperblog.com'  
NON_WP_BLOGS is a similar list of blogs with author such that url points to
the base website, and update_route is such that the concantenation of url and
update_route always points to the newest blog article.  
if the website does NOT have such a thing, I'm always open to pull requests.

## Install and launch

Make sure you have python (I recommend a virtual environment of at least 3.7) and
pip install the requirements:

```python
pip install -r requirements.txt
```

finally, run main.py  
Tested on Windows and Linux Ubuntu

## Errors, problems

Please raise an issue in this repo if the bot breaks or you have troubles with
installing or setup. I'm happy to help.
