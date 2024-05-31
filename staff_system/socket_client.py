import socket
import json

def send_messages(staff_type, host='127.0.0.1', port=8080):
	global command_parser

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((host, port))

		while True:
			try:
				message = input("> ")
				if message.lower() == 'exit':
					print("Exiting...")
					break

				full_message = f"{staff_type}: {message}"

				command_data = { "staff_type": staff_type, "command": message }
				s.sendall(json.dumps(command_data).encode())

				data = s.recv(1024)
				res = json.loads(data.decode())
				print(f"Received back from server: {json.dumps(res, indent=2)}")
			except Exception as e:
				print(e)

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(
		prog="Staff Client Application",
		description="Demo TUI for staffs",
	)

	parser.add_argument("staff_type", choices=["kitchenstaff", "waitstaff"])
	args = parser.parse_args()

	send_messages(args.staff_type)
