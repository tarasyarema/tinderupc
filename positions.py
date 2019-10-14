import json
import requests
from random import shuffle

ROLES = [
        ("CEO", "the Dreamer"),
        ("CPO", "the Visionary"),
        ("CTO", "the Doer"),
        ("CSO", "the Hustler"),
        ("CMO", "the Architect"),
        ("PR guy", "the Connector")
    ]

with open(".creds") as f:
    data = json.load(f)

URL = data["slack"]
MEM = data["members"]

for i in range(len(ROLES), len(MEM)):
    ROLES.append(("CFO", "the Fapper"))

shuffle(MEM)

text = ""
for m, r in zip(MEM, ROLES):
    text += f"- *{r[0]}*: {m}, _{r[1]}_\n"

requests.post(
        URL, 
        data=json.dumps({"text": text}), 
        headers={"Content-Type": "application/json"})

