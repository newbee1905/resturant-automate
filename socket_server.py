import asyncio
import socket

# Define message handling function
async def handle_message(reader, writer, username):
	while True:
		data = await reader.read(1024)
		if not data:
			break
		message = f"{username}: {data.decode()}"
		# Broadcast message to all connected clients (excluding sender)
		for client in connected_clients:
			if client != (reader, writer):
				client[1].write(message.encode())
		print(message)

# Define connection handler (async)
async def handle_connection(server_socket):
	reader, writer = await server_socket.accept()
	print("Client connected!")
	username = await reader.read(1024).decode()
	connected_clients.append((reader, writer))
	# Send welcome message
	writer.write(f"Welcome, {username}!\n".encode())
	await writer.drain()
	asyncio.create_task(handle_message(reader, writer, username))

# Server configuration
HOST = "localhost"
PORT = 8080
connected_clients = []

async def main():
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((HOST, PORT))
	server_socket.listen()
	print(f"Server listening on {HOST}:{PORT}")

	# Accept connections concurrently
	while True:
		asyncio.create_task(handle_connection(server_socket))
	await server_socket.close()

asyncio.run(main())

