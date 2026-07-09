import anthropic, os

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

message = client.messages.create(
    max_tokens=2000,
    model="claude-haiku-4-5",
    messages=[
        {
            "role":"user",
            "content":"Hello Claude, tell me how to use your API using the Python language"
        }
    ]
)

print(message.content[0].text)