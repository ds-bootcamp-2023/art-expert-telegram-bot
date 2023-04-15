# Telegram bot

## To run locally

1. Create .env file with secrets and environment variables
```sh
TELEGRAM_TOKEN=<YOUR_TELEGRAM_TOKEN>
HUGGING_FACE_API_TOKEN=<YOUR_HUGGING_FACE_TOKEN>
MODEL_API_URL=<YOUR_MODEL_API_URL>
HUGGING_FACE_API_URL="https://api-inference.huggingface.co"
```

2. Install dependencies

```sh
$ poetry install
```

3. Run bot

```sh
$ poetry run python run_bot.py
```

You can also build and run bot in Dockerfile provided you pass all the required env variables.


## To deploy on fly.io:

1. Set telegram token

```sh
$ flyctl secrets set TELEGRAM_TOKEN=<YOUR_TELEGRAM_TOKEN>
```

2. Set https://huggingface.co/ API token

```sh
$ flyctl secrets set HUGGING_FACE_API_TOKEN=<YOUR_HUGGING_FACE_TOKEN>
```

3. Set URL of your model API in fly.toml

```toml
[env]
  MODEL_API_URL = "<YOUR_MODEL_API_URL>"
```

4. Change appname in fly.toml to your app name (will be created automatically)

```toml
app = "<YOUR_APP_NAME>"
```

5. Deploy

```sh
$ flyctl deploy
```
