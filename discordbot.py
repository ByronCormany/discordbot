import os
import discord
from discord.ext import commands, tasks
from flask import Flask, request, jsonify
from threading import Thread
import psycopg2
import asyncio
import time
from datetime import datetime

# Initialize Flask app for receiving stock updates
app = Flask(__name__)



intents = discord.Intents.default()  # Make sure the bot can read messages
intents.messages = True  # Enable the "messages" intent
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)

"""
# Set up the Discord bot
intents = discord.Intents.default()
intents.messages = True  # Ensure bot can read messages
bot = commands.Bot(command_prefix="!", intents=intents)
client = discord.Client(intents=intents)

# Discord channel ID where the messages will be sent
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")


@app.route('/update_stock', methods=['POST'])
def update_stock():
    # Get stock update data from the stock-checking program
    try:
        # Get stock update data from the stock-checking program
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        product_id = data.get("product_id")
        stock_status = data.get("stock_status")
        price = data.get("price")
        url = data.get("url")

        # Send a message to the Discord channel
        send_stock_update_to_discord(product_id, stock_status, price, url)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == "Hello":
        await message.channel.send("Squeak")
# Run Flask app in the background (useful for development or in environments like AWS Lambda)
# Database function to fetch the first row from stock_availability

def get_first_row():
    try:
        # Connect to the database
        DB_HOST = "pokemonstock.cx2iykw6mfl0.us-west-1.rds.amazonaws.com"
        DB_NAME = "postgres"
        DB_USER = "postgres"
        DB_PASS = "Pokepass123##"
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        cursor = conn.cursor()

        # Execute the query to get the first row
        cursor.execute("SELECT * FROM stock_availability LIMIT 1;")
        row = cursor.fetchone()

        # Close the connection
        cursor.close()
        conn.close()

        return row
    except Exception as e:
        return str(e)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# Command to fetch the first row from the database
@bot.command(name="getfirst")
async def get_first(ctx):
    row = get_first_row()

    if row:
        # Format the message with the first row's details
        product_id, stock_status, price, url, last_updated, last_notified = row
        message = f"First Product in DB:\nID: {product_id}\nStock Status: {'In stock' if stock_status else 'Out of stock'}\nPrice: ${price}\nURL: {url}\nLast Updated: {last_updated}"
    else:
        message = "Error retrieving data from the database."

    # Send the message to the Discord channel
    await ctx.send(message)


# Set up the Discord bot event
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@client.event
async def on_message(message):
    print(f"Received message: {message.content}")
    if message.author == client.user:
        print("author == client")
        return

    if message.content.lower() == "Hello":
        print("trying to squeak")
        await message.channel.send("Squeak")

    await bot.process_commands(message)

def run_flask():
    print("run flask")
    app.run(host='0.0.0.0', port=5000)

# Start the Flask app and the Discord bot
if __name__ == "__main__":
    from threading import Thread
    # Run Flask API in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    print("main")
    # Run Discord bot
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))
    
"""

"""
# Command to fetch the first row from the database
@client.event
async def get_first(message):
    print("triggered")
    clean_message = message.content.replace("<@1336020067678158920> ", "")
    if clean_message.lower() == "getdata":
        print("triggered")  # Debugging line

        row = get_first_row()

        if row:
            # Format the message with the first row's details
            product_id, stock_status, price, url, last_updated, last_notified = row
            mes = f"First Product in DB:\nID: {product_id}\nStock Status: {'In stock' if stock_status else 'Out of stock'}\nPrice: ${price}\nURL: {url}\nLast Updated: {last_updated}"
        else:
            mes = "Error retrieving data from the database."

        # Send the message to the Discord channel
        await message.channel.send(mes)
"""

DB_HOST = "pokemonstock.cx2iykw6mfl0.us-west-1.rds.amazonaws.com"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "Pokepass123##"
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")
# Set up the Discord bot event

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    print("Bot is ready and running!")  # Debugging line
    Thread(target=poll_database, daemon=True).start()


@client.event
async def on_message(message):
    print(f"Received message: {message.content}")  # Debugging line
    clean_message = message.content.replace("<@1336020067678158920> ", "")
    if message.author == client.user:
        return

    if clean_message.lower() == "lilcho":
        await message.channel.send("You'd wish the world you know to end!!!! >:)")

    if clean_message.lower() == "hello":
        await message.channel.send("Squeak")

    if clean_message.lower() == "getdata":
        print("triggered")  # Debugging line

        row = get_first_row()
        print(row)
        if row:
            # Format the message with the first row's details
            sid, product_id, stock_status, price, url, last_updated, last_notified = row
            mes = f"First Product in DB:\nStorage ID: {sid}\nID: {product_id}\nStock Status: {'In stock' if stock_status else 'Out of stock'}\nPrice: ${price}\nURL: {url}\nLast Updated: {last_updated}"
        else:
            mes = "Error retrieving data from the database."

        # Send the message to the Discord channel
        await message.channel.send(mes)
        #print("Squeak triggered")  # Debugging line
        #await message.channel.send("Squeak")


def get_first_row():
    try:
        # Connect to the database
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        cursor = conn.cursor()

        # Execute the query to get the first row
        cursor.execute("SELECT * FROM stock_availability LIMIT 1;")
        row = cursor.fetchone()

        # Close the connection
        cursor.close()
        conn.close()

        return row
    except Exception as e:
        return str(e)


def get_latest_stock_data():
    """Fetch all products and their last notified timestamps."""
    try:
        connection = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
        )
        cursor = connection.cursor()

        # Select products that have a different last_updated and last_notified
        cursor.execute("""
            SELECT product_id, stock_status, price, url, last_updated, last_notified
            FROM stock_table
            WHERE last_notified IS NULL OR last_updated > last_notified;
        """)

        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        return rows  # List of tuples with product details
    except Exception as e:
        print(f"❌ Database error: {e}")
        return []

def send_stock_update_to_discord(product_id, stock_status, price, url):
    """Send a Discord notification."""
    channel = bot.get_channel(int(DISCORD_CHANNEL_ID))
    if not channel:
        print("❌ Could not find Discord channel.")
        return

    # Format the message
    message = f"**Product in Stock!**: {url} - Price: ${price}" if stock_status else f"**Product out of stock**: {url} - Price: ${price}"

    # Use asyncio to send the message safely
    asyncio.run_coroutine_threadsafe(channel.send(message), bot.loop)

    # Update last_notified timestamp in the database
    try:
        connection = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
        )
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE stock_table 
            SET last_notified = %s 
            WHERE product_id = %s;
        """, (datetime.utcnow(), product_id))

        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"❌ Error updating last_notified timestamp: {e}")

def poll_database():
    """Continuously check for stock updates."""
    while True:
        print("🔍 Checking for stock changes...")
        rows = get_latest_stock_data()

        for row in rows:
            product_id, stock_status, price, url, last_updated, last_notified = row
            send_stock_update_to_discord(product_id, stock_status, price, url)

        time.sleep(30)  # Check every 30 seconds


if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))
