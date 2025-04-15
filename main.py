import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

TOKEN = os.getenv("DISCORD-KA-RAAZ")
GEMINI_API_KEY = os.getenv("AI_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="~", intents=intents)

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

@bot.event
async def on_ready():
    print(f'🔥 Bot online as {bot.user}! Time to destroy some egos 😈')

@bot.command()
async def roast(ctx, member: discord.Member = None):
    """Brutal roast jo mention wale bande ki zindagi hila de 😂🔥"""

    if member is None:
        await ctx.send("Bhai kisi ko tag toh kar! ~roast @username 🔥")
        return
    
    if member == bot.user:
        await ctx.send("Abe main AI hoon, tere words mere CPU tak nahi pahunchte! 😂🤖")
        return
    
    # Get last 5 messages from the mentioned user
    messages = []
    async for message in ctx.channel.history(limit=200):
        if message.author == member and message.author != bot.user:
            messages.append(f"{message.author.name}: {message.content}")
        if len(messages) >= 5:
            break

    if len(messages) < 2:
        await ctx.send(f"{member.mention} Bhai thoda aur likh le, tabhi roast kar paunga! 😂🔥")
        return

    history = "\n".join(messages[::-1])  # Reverse to maintain order
    prompt = f"""
    Neeche di gayi chat history padhkar **{member.name} ka ek next-level, savage roast** likho.  
    Sirf **Hinglish (English letters only)** mein likhna.  
    **Roast aisa ho jo banda zindagi bhar yaad rakhe, full sarcasm aur meme-wale vibes ho.**  
    **Thodi personal touches daalo taki aur relatable lage, but limit cross mat karna.**  
    **Galiyan allowed hai, full burn hone chahiye. do it in about 60 words**  

    Chat history:
    {history}

    Ab full power mein roast likho:
    """

    # Generate Roast
    response = model.generate_content(prompt)
    
    # Send Roast
    await ctx.send(f"🔥 **{member.mention}, bhai teri aukaat ka poora analysis:**\n\n{response.text}")

bot.run(TOKEN)