# PostFinder Bot

**PostFinder Bot** helps streamline your content management by searching for specific posts based on keywords. Here's how it works:

1. **Search:** Enter keywords, and the bot will find relevant posts.
2. **Forward to Admin:** The bot sends these posts to the admin for review.
3. **Approval:** If the admin approves, the bot automatically posts the content to the admin's channel.

Simplify your workflow and ensure quality content with PostFinder Bot!


## Run Locally

Clone the project

```bash
  git clone https://github.com/aabduvak/PostFinder.git
```

Go to the project directory

```bash
  cd PostFinder
```

Install dependencies

```bash
  pip install -r requirements.txt
```


You need to create .env file:
```bash
BOT_TOKEN = "${BOT_TOKEN}"
CHANNEL_ID = "${YOUR_CHANNEL_ID}"
ADMIN_ID = "${YOUR_CHAT_ID}" # run "chat_id" command on the bot or use "https://t.me/JsonDumpBot" to get ids
```


Start the server

```bash
  sudo docker-compose up --build
```

On the browser navigate to url below

```bash
  http://172.21.0.3:8501 # password is on docker-compose.yml file
```

