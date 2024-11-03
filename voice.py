import asyncio
import edge_tts
def saythis(initial,final):
    text = f"Move {initial} to {final}"

    # Text to be converted into speech
    output_file = "voice/voiceoutput.mp3"

    # Choose a male American voice
    voice = "en-GB-RyanNeural"  # Example of a male American voice

    async def mainye():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        #print(f"Audio content saved to {output_file}")

    # Run the async function
    asyncio.run(mainye())

    # Play the audio file
    import os
    os.system("open voice/voiceoutput.mp3")  # Use 'start' for Windows, 'open' for macOS, 'xdg-open' for Linux

def winrun():
    text = "You did well. for a human"

    # Text to be converted into speech
    output_file = "voice/win.mp3"

    # Choose a male American voice
    voice = "en-GB-RyanNeural"  # Example of a male American voice

    async def mainye():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        #print(f"Audio content saved to {output_file}")

    # Run the async function
    asyncio.run(mainye())

    # Play the audio file
    import os
    os.system("open voice/win.mp3")  # Use 'start' for Windows, 'open' for macOS, 'xdg-open' for Linux

def ignorethisrun(): 
    for i in ["wow","lol"]:
        text = i
        # Text to be converted into speech
        output_file = f"voice/{i}.mp3"

        # Choose a male American voice
        voice = "en-GB-RyanNeural"  # Example of a male American voice

        async def mainye():
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_file)
            #print(f"Audio content saved to {output_file}")

        # Run the async function
        asyncio.run(mainye())

        # Play the audio file
        import os
        os.system(f"open voice/{i}.mp3")  # Use 'start' for Windows, 'open' for macOS, 'xdg-open' for Linux


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

win()
