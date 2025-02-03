import os
import discord
from discord.ext import commands, tasks
from flask import Flask, request, jsonify

# Initialize Flask app for receiving stock updates
app = Flask(__name__)

# Set up the Discord bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Discord channel ID where the messages will be sent
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")

@app.route('/update_stock', methods=['POST'])
def update_stock():
    # Get stock update data from the stock-checking program
    data = request.get_json()
    product_id = data.get("product_id")
    stock_status = data.get("stock_status")
    price = data.get("price")
    url = data.get("url")

    # Send a message to the Discord channel
    send_stock_update_to_discord(product_id, stock_status, price, url)
    return jsonify({"status": "success"}), 200

def send_stock_update_to_discord(product_id, stock_status, price, url):
    # Create the message based on the stock status
    if stock_status:
        message = f"**Product in Stock!**: {url} - Price: ${price}"
    else:
        message = f"**Product out of stock**: {url} - Price: ${price}"

    # Send the message to the specified Discord channel
    channel = bot.get_channel(int(DISCORD_CHANNEL_ID))
    bot.loop.create_task(channel.send(message))

# Set up the Discord bot event
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Run Flask app in the background (useful for development or in environments like AWS Lambda)
def run_flask():
    app.run(host='0.0.0.0', port=5000)

# Start the Flask app and the Discord bot
if __name__ == "__main__":
    from threading import Thread
    # Run Flask API in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Run Discord bot
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))