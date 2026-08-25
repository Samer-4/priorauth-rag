import os
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

resp = client.messages.create(
    model = "claude-sonnet-5",
    max_tokens = 100,
    messages = [{"role": "user", "content": "Reply with the single word: ready"}],
)
print(resp.content[0].text) 