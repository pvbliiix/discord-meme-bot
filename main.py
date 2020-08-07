import discord
from PIL import Image
import requests
from io import BytesIO

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.content.find("!meme") != -1:
            pic_ext = ['.jpg', '.png', '.jpeg']
            for ext in pic_ext:
                if(message.attachments[0].url.endswith(ext)):
                    response = requests.get(message.attachments[0].url)
                    src = Image.open(BytesIO(response.content))
                    template = Image.open("template.png")
                    out = Image.open("template.png")
                    size_x = 275
                    size_y = 203

                    if src.size[0] > size_x or src.size[1] > size_y:
                        src.thumbnail((size_x, size_y), Image.LANCZOS)

                    top_left = (163, 91)

                    blank_x = size_x - src.size[0]
                    blank_y = size_y - src.size[1]
                    out.paste(src, (int(top_left[0] + blank_x / 2), int(top_left[1] + blank_y / 2)))

                    out.paste(template, (0, 0), template)
                    out.save("meme.png")
                    await message.channel.send(file=discord.File("meme.png"))

token = read_token()

client = MyClient()
client.run(token)