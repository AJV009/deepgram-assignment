from deepgram import Deepgram
import asyncio

# will expire in 1 hour
DEEPGRAM_API_KEY = '2054a76e22d1d9f294df6f90dfb454ac9983401c' 

PATH_TO_FILE = 'Bueller-Life-moves-pretty-fast.wav'

async def main():
    dg_client = Deepgram(DEEPGRAM_API_KEY)
    socket = await dg_client.transcription.live({'punctuate': True})
    async def process_audio(connection):
        with open(PATH_TO_FILE, 'rb') as audio:
            CHUNK_SIZE_BYTES = 8192
            CHUNK_RATE_SEC = 0.001
            chunk = audio.read(CHUNK_SIZE_BYTES)
            while chunk:
                connection.send(chunk)
                await asyncio.sleep(CHUNK_RATE_SEC)
                chunk = audio.read(CHUNK_SIZE_BYTES)
            await connection.finish()
    socket.register_handler(socket.event.CLOSE, lambda _: print('Connection closed.'))
    socket.register_handler(socket.event.TRANSCRIPT_RECEIVED, print)
    await process_audio(socket)

asyncio.run(main())