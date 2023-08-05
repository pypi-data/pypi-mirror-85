# dlabs.py

A fully asynchronous wrapper for the Discord Labs API.

### Installation

Installing `dlabs.py` is easy, just run `pip install dlabs.py`!

### Usage 

Currently, as of Nov 10th 2020 the API provides 2 routes - this package makes use of them, and as soon as new ones are added, the wrapper will be updated simultaneously.

Below are some simple example cogs using the API wrapper to automatically post stats to Discord Labs posting manually, and fetching bots! (note that `bot` is expected to be your instance of discord.py's `commands.Bot` or `commands.AutoShardedBot`)

```py
import dlabs
from discord.ext import commands


class DiscordLabs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.discord_labs = dlabs.Client(bot, token="YOUR DISCORD LABS TOKEN", autopost=True)
        
    
def setup(bot):
    bot.add_cog(DiscordLabs(bot))
```

And that's it! It's that easy to automatically post stats with `dlabs.py`. However, if you don't want to autopost the statistics and call the function manually, there's a way too, here's an example - 

```py
import dlabs
from discord.ext import commands


class DiscordLabs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.discord_labs = dlabs.Client(bot, token="YOUR DISCORD LABS TOKEN")
        
        
     @commands.command()
     async def post_dlabs_stats(self, ctx):
        await self.discord_labs.post_stats()
        await ctx.send("Posted the stats to Discord Labs!")
        
    
def setup(bot):
    bot.add_cog(DiscordLabs(bot))
```

Now, there's one more thing you can do, and that is fetching Bot information straight from Discord Labs. Here's an example on how you could do that:


```py
import dlabs
from discord.ext import commands
from discord import Embed


class DiscordLabs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.discord_labs = dlabs.Client() # Doesn't require authorization!
        
        
     @commands.command()
     async def coolbot(self, ctx, id):
          cool_bot = await self.discord_labs.get_bot(id) 
          
          embed = Embed(
            color=0xefefef,
            title=f"{cool_bot.name} is a cool bot!",
            description=f"It's got {cool_bot.uptime} uptime!"
          )
          embed.set_thumbnail(url=cool_bot.avatar_url)
          
          await ctx.send(embed=embed)
          
    
def setup(bot):
    bot.add_cog(DiscordLabs(bot))
```

### Contributing 

This package is opensource so anyone with adequate python experience can contribute to this project!

### Report Issues
If you find any error/bug/mistake with the package or in the code feel free to create an issue and report it [here.](https://github.com/itsmewulf/dlabs.py/issues)

### Fix/Edit Content
If you want to contribute to this package, fork the repository, make your changes and then simply create a Pull Request!

### Contact
If you want to contact me -<br>
**Mail -** ```wulf.developer@gmail.com```<br>
**Discord -** ```wulf#9716```
