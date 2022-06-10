import openrouteservice

token = None
with open("token.txt") as f:
    token = f.read().strip()
coords = (())
client = openrouteservice.Client(key=token)