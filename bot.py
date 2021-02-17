import discord
from discord.ext import commands

from diffie_hellman import DiffieHellman
from aes import AESCipher

database = {
        "token": None,
        "users": {},
        "chats": {},
} 

bot = commands.Bot(command_prefix="")

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
        print(user)
        df = DiffieHellman()
        k1 = df.generate_k()
        database['chats'][str(user.id)] = []
        database['users'][str(user.id)] = { 
                    'name': user.name, 
                    'key': df 
                } 
        print("Sending to:", user)
        u = await bot.fetch_user(user.id)
        try:
            await u.send(f'===KEYEXCH===\nvalue:{k1}')
        except:
            print("Erorr sending key-exchange to:", user)
        print("-" * 40)

@bot.event
async def on_message(message):
    #Ignore MSGs if they're not DMs
    #TODO implement end-to-end group chatting
    if message.author == bot.user or not isinstance(message.channel, discord.DMChannel):
        return

    database['chats'][str(message.author.id)].append(message.content)

    if message.content.startswith("===KEYEXCH==="):
        # Perform a Diffie-Hellman key exchange
        print(f"Key exchange started with {message.author.name}")
        k2 = message.content.find("value:")
        df = DiffieHellman()
        k1 = df.generate_k()
        key = df.generate_full_key(k2)
        database['users'][str(message.author.id)]['key'] = df
        print("Key with user: ", message.author.name, " is ", database['users'][str(message.author.id)]['key'].key)
        await message.author.send(f"===KEYACK===\nvalue:{k1}")

    elif message.content.startswith("===KEYACK==="):
        value = message.content.find("value:")
        k2 = message.content[value+6:]
        df = database['users'][str(message.author.id)]['key']
        df.generate_full_key(k2)
        database['users'][str(message.author.id)]['key'] = df
        print("Key with user: ", message.author.name, " is ", database['users'][str(message.author.id)]['key'].key)

    elif message.content.startswith("===MSG==="):
        # Recieve a message:
        content = message.content[9:]
        key = database['users'][str(message.author.id)]['key'].key
        aes = AESCipher( key ) 
        try:
            decrypted = aes.decrypt(content)
        except:
            print("Error while decrypting message")
            return
        print(content)
        print(decrypted)
        await message.author.send("Roger that")

if __name__ == "__main__":
    start_bot()


