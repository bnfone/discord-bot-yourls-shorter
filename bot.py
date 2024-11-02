import os
import json
import requests
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

YOURLS_URL = os.getenv("YOURLS_URL")
YOURLS_SIGNATURE_TOKEN = os.getenv("YOURLS_SIGNATURE_TOKEN")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ENABLE_CUSTOM_URL = os.getenv("ENABLE_CUSTOM_URL", "false").lower() == "true"
ENABLE_INFO_COMMAND = os.getenv("ENABLE_INFO_COMMAND", "false").lower() == "true"
EPHEMERAL_RESPONSE = os.getenv("EPHEMERAL_RESPONSE", "false").lower() == "true"
GITHUB_LINK = os.getenv("GITHUB_LINK", "https://github.com/your-github-repo")
DONATION_LINK = os.getenv("DONATION_LINK", "https://your-donation-link.com")

# Persistent statistics file
STATS_FILE = "stats.json"

# Initialize statistics with default values if file does not exist or keys are missing
def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            stats = json.load(f)
    else:
        stats = {}

    # Ensure default structure
    stats.setdefault("total_links", 0)
    stats.setdefault("user_stats", {})
    stats.setdefault("domain_stats", {})
    return stats

# Load initial stats
stats = load_stats()

# Set up the bot with required intents
intents = discord.Intents.default()
intents.message_content = True

# Initialize bot
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Bot is logged in as {bot.user}')

def save_stats():
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=4)

def increment_stats(user_id, domain):
    """Update statistics with new link data."""
    stats["total_links"] += 1
    
    # Update user stats
    if str(user_id) in stats["user_stats"]:
        stats["user_stats"][str(user_id)] += 1
    else:
        stats["user_stats"][str(user_id)] = 1

    # Update domain stats
    if domain in stats["domain_stats"]:
        stats["domain_stats"][domain] += 1
    else:
        stats["domain_stats"][domain] = 1

    save_stats()

async def create_short_url(interaction: discord.Interaction, url: str, custom_keyword=None):
    """Helper function to create a short URL using the YOURLS API."""
    try:
        params = {
            "signature": YOURLS_SIGNATURE_TOKEN,
            "action": "shorturl",
            "format": "json",
            "url": url
        }
        if custom_keyword:
            params["keyword"] = custom_keyword

        response = requests.get(YOURLS_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                short_url = data["shorturl"]

                # Increment statistics
                domain = url.split("/")[2]
                increment_stats(interaction.user.id, domain)

                await interaction.response.send_message(
                    f"Here is your short link: {short_url}", 
                    ephemeral=EPHEMERAL_RESPONSE
                )
            else:
                error_message = data.get("message", "An unknown error occurred.")
                await interaction.response.send_message(
                    f"Failed to create short link: {error_message}", 
                    ephemeral=EPHEMERAL_RESPONSE
                )
        
        elif response.status_code == 503:
            await interaction.response.send_message(
                "The server is currently overloaded or undergoing maintenance. "
                "Please try again later.",
                ephemeral=EPHEMERAL_RESPONSE
            )
        
        else:
            error_details = response.json()
            error_message = error_details.get("message", "An error occurred.")
            await interaction.response.send_message(
                f"Error: {response.status_code} - {error_message}", 
                ephemeral=EPHEMERAL_RESPONSE
            )

    except requests.exceptions.RequestException:
        await interaction.response.send_message(
            "A network error occurred while connecting to the YOURLS service. "
            "Please check your connection and try again.",
            ephemeral=EPHEMERAL_RESPONSE
        )
    except Exception as e:
        await interaction.response.send_message(
            f"An unexpected error occurred: {e}",
            ephemeral=EPHEMERAL_RESPONSE
        )

@bot.tree.command(name="shorturl", description="Create a short URL using YOURLS")
async def shorturl(interaction: discord.Interaction, url: str):
    await create_short_url(interaction, url)

@bot.tree.command(name="shortlink", description="Create a short URL using YOURLS")
async def shortlink(interaction: discord.Interaction, url: str):
    await create_short_url(interaction, url)

if ENABLE_CUSTOM_URL:
    @bot.tree.command(name="customurl", description="Create a custom short URL using YOURLS")
    async def customurl(interaction: discord.Interaction, url: str, custom_keyword: str):
        await create_short_url(interaction, url, custom_keyword)

if ENABLE_INFO_COMMAND:
    @bot.tree.command(name="info", description="Information about this bot")
    async def info(interaction: discord.Interaction):
        embed = discord.Embed(
            title="YOURLS Shortener Bot",
            description="This bot allows you to create short URLs directly from Discord using YOURLS. "
                        "Built with love for easy URL sharing!",
            color=discord.Color.blue()
        )
        embed.add_field(name="GitHub", value=f"[Source Code]({GITHUB_LINK})", inline=False)
        embed.add_field(name="Support", value=f"Consider supporting the development: [Donate here]({DONATION_LINK})", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=EPHEMERAL_RESPONSE)

@bot.tree.command(name="stats", description="View bot statistics")
async def stats_command(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    user_count = stats["user_stats"].get(user_id, 0)
    top_domains = sorted(stats["domain_stats"].items(), key=lambda x: x[1], reverse=True)[:5]
    domain_stats = "\n".join([f"{domain}: {count}" for domain, count in top_domains])

    embed = discord.Embed(
        title="Bot Statistics",
        color=discord.Color.green()
    )
    embed.add_field(name="Total Links Shortened", value=str(stats["total_links"]), inline=False)
    embed.add_field(name="Your Links Shortened", value=str(user_count), inline=False)
    # embed.add_field(name="Top Domains", value=domain_stats or "No data", inline=False)

    # Add ping
    start_time = time.time()
    await interaction.response.send_message("Calculating ping...", ephemeral=True)
    end_time = time.time()
    ping = round((end_time - start_time) * 1000)
    embed.add_field(name="Bot Ping", value=f"{ping} ms", inline=False)

    await interaction.edit_original_response(content=None, embed=embed)

# Run the bot
bot.run(DISCORD_TOKEN)
