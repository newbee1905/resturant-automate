import socket
import json
import threading
from dataclasses import dataclass, field

from command import CommandParser, UpdateCommand, ListOrdersCommand
from observer import Subject, Observer

def handle_client(parser, conn, addr):
	print(f"Connected by {addr}")
	with conn:
		while True:
			data = conn.recv(1024)
			if not data:
				break

			message = json.loads(data.decode())
			print(f"Received message from {addr}: {json.dumps(message, indent=2)}")

			command_data = parser.parse(message["command"])

			conn.sendall(json.dumps({"test": True}).encode())  # Echo back the received message

def start_server(host='127.0.0.1', port=8080):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((host, port))
		s.listen()
		print(f"Server listening on {host}:{port}...")

		command_parser = CommandParser({
			"update": UpdateCommand(),
			"list": ListOrdersCommand()
		})
		
		while True:
			conn, addr = s.accept()

			client_thread = threading.Thread(target=handle_client, args=(command_parser, conn, addr))
			client_thread.start()

@dataclass
class SubjectServer:
	host: str = '127.0.0.1'
	port: int = 8080
	subjects: dict = field(default_factory=dict)

	def __post_init__(self):
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.bind((self.host, self.port))
		self.server_socket.listen()
	
	def start(self):
		try:
			while True:
				client_socket, client_address = self.server_socket.accept()
				threading.Thread(target=self.handle_client, args=(client_socket,)).start()
		finally:
			self.server_socket.close()

	def handle_client(self, client_socket):
		with client_socket:
			try:
				data = client_socket.recv(1024)
				if not data:
					break

				message = json.loads(data.decode())
				print(f"Received message from {addr}: {json.dumps(message, indent=2)}")

				command_data = parser.parse(message["command"])
			except ConnectionResetError:
				pass
		print(f"Connected by {addr}")
		with conn:
			while True:
				data = conn.recv(1024)
				if not data:
					break

				message = json.loads(data.decode())
				print(f"Received message from {addr}: {json.dumps(message, indent=2)}")

				command_data = parser.parse(message["command"])

				conn.sendall(json.dumps({"test": True}).encode())  # Echo back the received message

if __name__ == "__main__":
	start_server()

