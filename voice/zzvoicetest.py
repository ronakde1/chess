import asyncio
import edge_tts

voices=["AU-WilliamNeural","CA-LiamNeural","HK-SamNeural","IN-PrabhatNeural","IE-ConnorNeural","KE-ChilembaNeural","NZ-MitchellNeural","NG-AbeoNeural","PH-JamesNeural","SG-WayneNeural","ZA-LukeNeural","TZ-ElimuNeural"]
for voicetype in voices:
    # Text to be converted into speech
    text = f"Hello, this is the voice {voicetype}."
    output_file = f"voice/{voicetype}.mp3"

    # Choose a male American voice
    voice = f"en-{voicetype}"  # Example of a male American voice

    async def main():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        print(f"Audio content saved to {output_file}")

    # Run the async function
    asyncio.run(main())

    # Play the audio file
    import os
    os.system(f"open voice/{voicetype}.mp3")  # Use 'start' for Windows, 'open' for macOS, 'xdg-open' for Linux
    
