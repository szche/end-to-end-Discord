import discord
from discord.ext import commands

from diffie_hellman import DiffieHellman
from aes import AESCipher

database = {
        "token": None,
        "keys": {},
        "chats": {},
} 

bot = commands.Bot(command_prefix="")
keybase = {}

def start_bot():
    global bot
    with open("dcToken.txt", "r") as f:
        token = ''.join(f.readlines()) 
    database['token'] = token
    bot.run(token, bot=False)

@bot.event
async def on_ready():
    print("-" * 40)
    print('Started the bot as:', bot.user)
    print("BOT:", database)
    users = bot.users
    for user in users:
        database['chats'][str(user.id)] = []
        database['keys'][str(user.id)] = None
    print("-" * 40)

@bot.event
async def on_message(message):
    #Ignore MSGs if they're not DMs
    #TODO implement end-to-end group chatting
    print(database)
    if message.author == bot.user or not isinstance(message.channel, discord.DMChannel):
        return

    #print(message.author)
    #print(message.content)
    database['chats'][str(message.author.id)].append(message.content)

    if message.content.startswith("===KEYEXCH==="):
        # Perform a Diffie-Hellman key exchange
        print(f"Key exchange started with {message.author.name}")
        value = message.content.find("value:")
        k2 = int(message.content[value+6:])
        df = DiffieHellman(k2)
        k1 = df.generate_k()
        key = df.generate_full_key()
        
        keybase[message.author.id] = key 

        print("Key with user: ", message.author.name, " is ", keybase[message.author.id] )
        await message.author.send(f"===KEYACK===\nvalue:{k1}")

    elif message.content.startswith("====KEYACK==="):
        value = message.content.find("value:")
        key = message.content[value+6:]
        keybase[message.author.id] *= int(key) 

    elif message.content.startswith("===MSG==="):
        # Recieve a message:
        content = message.content[9:]
        aes = AESCipher( keybase[message.author.id] ) 
        decrypted = aes.decrypt(content)
        print(content)
        print(decrypted)
        await message.author.send("Roger that")

if __name__ == "__main__":
    start_bot()


