import edge_tts
import asyncio

async def list_voices():
    voices = await edge_tts.list_voices()
    for voice in voices:
        print(f"Name: {voice['Name']}, Gender: {voice['Gender']}, Locale: {voice['Locale']}")

# Run the async function
asyncio.run(list_voices())
