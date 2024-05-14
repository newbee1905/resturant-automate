import jwt
from datetime import datetime, timedelta, timezone
import threading

payload_data = {
	# "exp": datetime.now(tz=timezone.utc),
	"exp": datetime.now(tz=timezone.utc) + timedelta(seconds=5),
	"name": "Jessica Temporal",
	"nickname": "Jess",
}

my_secret = 'my_super_secret'

token = jwt.encode(payload=payload_data,  key=my_secret, algorithm="HS256")

data = jwt.decode(token, key=my_secret, algorithms=["HS256"])

time_left = data["exp"] - datetime.now(tz=timezone.utc).timestamp()

print(time_left)
# print(time_left.days())
