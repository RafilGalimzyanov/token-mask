# OpenAI - proxy 
build docker-containers 
```angular2html
docker-compose build
```
run docker-containers
```angular2html
docker-compose up
```
## Requirements
Example of `.env`:
```angular2html
ADMIN_TOKEN=test
OPENAI_BASE_URL=https://your_proxy_bla.bla.com

DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=postgres
DB_PORT=5432
DB_NAME=postgres
```

## Usage example
```jupyter
import os

from openai import OpenAI


os.environ['OPENAI_BASE_URL'] = "https://token-mask.com"
os.environ['OPENAI_API_KEY'] = "token-mask-user-token"

client = OpenAI(base_url=os.getenv("OPENAI_API_BASE"))

message = [
      {
        "role": "system",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": "Hello!"
      }
    ]
response = client.chat.completions.create(model="gpt-3.5-turbo", messages=message, max_tokens=10)
print(response)
```
