from dataclasses import dataclass
import re

@dataclass
class CommandParser:
	commands: dict

	def parse(self, command_str):
		match = re.match(r'^(\w+)(?:\s+(\w+)(?:\s+(\w+))?)?$', command_str.strip())
		if match:
			command_name, *args = match.groups()
			if command_name in self.commands:
				self.commands[command_name].execute(*args)
			else:
				print("Command not found")
		else:
			print("Invalid command format")

class Command:
	def execute(self, *args):
		raise NotImplementedError()

@dataclass
class UpdateCommand(Command):
	types = ["orders", "items"]

	def execute(self, staff: str, type_: str, id_: str):
		if not type_ or not id_:
			print("Error: 'update' command requires a type and an ID")
			return
		if type_ not in self.types:
			print("Error: type must be either `orders` or `items`")
			return

		if staff == "kitchenstaff" and type_ == "order":
			print("Error: Only Wait Staff can update order items")

		print(f"Updating {type_} with ID {id_}")

@dataclass
class ListOrdersCommand(Command):
	types = ["orders", "items"]

	def execute(self, type_: str, id_=None):
		if type_ not in self.types:
			print("Error: type must be either `orders` or `items`")
			return

		if type_ == "item":
			if id_:
				print(f"Listing order items for order with ID {id_}")
			else:
				print("Listing all order items")
		else:
			print(f"Listing orders of type {type_}")

if __name__ == "__main__":
	parser = CommandParser({
		"update": UpdateCommand(),
		"list": ListOrdersCommand()
		"observe": ObserveOrdersCommand()
	})

	while True:
		command = input("Enter command: ")
		if command.lower() == "exit":
			break
		parser.parse(command)

