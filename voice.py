import asyncio
import edge_tts
def saythis(initial,final):
    text = f"Move {initial} to {final}"
    output_file = "voice/voiceoutput.mp3"
    voice = "en-GB-RyanNeural"
    async def mainye():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
    asyncio.run(mainye())
    import os
    os.system("open voice/voiceoutput.mp3")

def winrun():
    text = "You did well. for a human"
    output_file = "voice/win.mp3"
    voice = "en-GB-RyanNeural"
    async def mainye():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
    asyncio.run(mainye())
    import os
    os.system("open voice/win.mp3")

def sleekrun():
    for i in ["wow","lol"]:
        text = i
        output_file = f"voice/{i}.mp3"
        voice = "en-GB-RyanNeural"
        async def mainye():
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_file)
        asyncio.run(mainye())
        import os
        os.system(f"open voice/{i}.mp3")


def ignorethisrun(): 
    for i in ["wow","lol"]:
        text = i
        output_file = f"voice/{i}.mp3"
        voice = "en-GB-RyanNeural" 
        async def mainye():
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_file)
        asyncio.run(mainye())
        import os
        os.system(f"open voice/{i}.mp3") 


def win():
    import os
    os.system("open voice/win.mp3")

def ignorethis():
    import random
    import os
    chance = random.randint(0,3)
    if chance == 0:
        i=random.randint(0,1)
        os.system(f"open voice/{i}.mp3")

def say(stringyeye):
    text = f"{stringyeye}"
    output_file = "voice/voiceoutput.mp3"
    voice = "en-GB-RyanNeural"
    async def mainye():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
    asyncio.run(mainye())
    import os
    os.system("open voice/voiceoutput.mp3")