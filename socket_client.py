import asyncio
import socket

# Define message sending function
async def send_message(reader, writer, username):
	while True:
		message = input()
		writer.write(f"{message}\n".encode())
		await writer.drain()

# Define connection establishment function
async def connect_to_server(host, port):
	try:
		reader, writer = await asyncio.open_connection(host, port)
		username = input("Enter your username: ")
		writer.write(username.encode())
		await writer.drain()
		print(f"Connected to server as {username}")
		asyncio.create_task(send_message(reader, writer, username))
		while True:
			data = await reader.read(1024)
			if not data:
				break
			print(data.decode())
	except ConnectionRefusedError:
		print("Connection failed!")
	finally:
		writer.close()
		await writer.wait_closed()

# Client configuration
HOST = "localhost"
PORT = 8080

async def main():
	await connect_to_server(HOST, PORT)

asyncio.run(main())

