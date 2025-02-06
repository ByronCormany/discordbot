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
intents.message_content = True
#client = discord.Client(intents=intents)
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
DISCORD_CHANNEL_ID = "1336024591667298326"
# Set up the Discord bot event

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print("Bot is ready and running!")  # Debugging line
    Thread(target=poll_database, daemon=True).start()


@bot.event
async def on_message(message):
    print(f"Received message: {message.content}")  # Debugging line
    clean_message = message.content.replace("<@1336020067678158920> ", "")
    if message.author == bot.user:
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

"""
def get_latest_stock_data():
    Fetch all products and their last notified timestamps.
    try:
        connection = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
        )
        cursor = connection.cursor()

        # Select products that have a different last_updated and last_notified
        cursor.execute(
            SELECT product_id, stock_status, price, url, last_updated, last_notified
            FROM stock_availability
            WHERE last_notified IS NULL 
            OR (last_updated > last_notified AND stock_status <> (
                SELECT stock_status FROM stock_availability AS prev 
                WHERE prev.product_id = stock_availability.product_id 
                ORDER BY last_notified DESC LIMIT 1
            ));
        )

        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        return rows  # List of tuples with product details
    except Exception as e:
        print(f"❌ Database error: {e}")
        return []
"""

def get_latest_stock_data():
    """Fetch products where stock status has changed since last notification."""
    try:
        connection = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
        )
        cursor = connection.cursor()

        # Select products where stock status changed compared to the last notification
        cursor.execute("""
            SELECT product_id, stock_status, price, url, last_updated, last_notified
            FROM stock_availability
            WHERE (last_notified IS NULL OR last_updated > last_notified)
            AND stock_status IS DISTINCT FROM (
                SELECT stock_status FROM stock_availability WHERE product_id = stock_availability.product_id LIMIT 1);
        """)

        rows = cursor.fetchall()

        # Debugging: Print fetched rows
        print(f"🔍 Found {len(rows)} stock updates that require notification.")

        cursor.close()
        connection.close()

        return rows  # List of tuples with product details
    except Exception as e:
        print(f"❌ Database error: {e}")
        return []

def update_last_notified(product_id):
    """Update last_notified timestamp after sending a Discord notification."""
    try:
        # Establish database connection
        connection = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
        )
        cursor = connection.cursor()

        # Get current UTC time
        current_time = datetime.utcnow()
        print(f"🔍 Attempting to update last_notified for product_id: {product_id} at {current_time}")

        # Check if the product_id exists in the table
        cursor.execute("SELECT last_notified FROM stock_availability WHERE product_id = %s", (product_id,))
        result = cursor.fetchone()
        print(result)
        if result is None:
            print(f"❌ No matching product found for product_id: {product_id}")
        else:
            print(f"✅ Product found! Previous last_notified: {result[0]}")

            # Update last_notified field
            cursor.execute("""
                UPDATE stock_availability 
                SET last_notified = %s 
                WHERE product_id = %s;
            """, (current_time, product_id))

            # Commit the transaction
            connection.commit()
            print(f"✅ Successfully updated last_notified for product_id: {product_id} at {current_time}")

        # Close database connection
        cursor.close()
        connection.close()

    except Exception as e:
        print(f"❌ Error updating last_notified timestamp: {e}")

def send_stock_update_to_discord(product_id, stock_status, price, url):
    """Send a Discord notification."""
    channel = bot.get_channel(int(DISCORD_CHANNEL_ID))
    if not channel:
        print("❌ Could not find Discord channel.")
        return

    # Format the message
    #f"Product Stock Update!\nUPC: {product_id}\nStock Status: {'In stock' if stock_status else 'Out of stock'}\nPrice: ${price}\nURL: {url}\nLast Updated: {last_updated}"
    message = f"Product Stock Update!\nUPC: {product_id}\nStock Status: {'In stock' if stock_status else 'Out of stock'}\nPrice: ${price}\nURL: {url}"

    # Use asyncio to send the message safely
    asyncio.run_coroutine_threadsafe(channel.send(message), bot.loop)

    # Update last_notified timestamp in the database
    update_last_notified(product_id)

def poll_database():
    """Continuously check for stock updates and notify if changes occur."""
    while True:
        try:
            print("🔍 Checking for stock changes...")
            rows = get_latest_stock_data()
            print(rows)
            if rows:
                print(f"✅ Found {len(rows)} stock updates.")

                for row in rows:
                    product_id, stock_status, price, url, last_updated, last_notified = row
                    product_id = product_id.strip()
                    # Send notification
                    send_stock_update_to_discord(product_id, stock_status, price, url)

                    # Update last_notified timestamp in the database
                    update_last_notified('820650413186')
            else:
                print("📭 No stock changes detected.")

        except Exception as e:
            print(f"❌ Error polling database: {e}")

        time.sleep(30)  # Wait 30 seconds before checking again


if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))
