# Configuration

The `config.ini` file controls all aspects of Moodle Mate. Here are the key sections:

## Moodle Settings

```ini
[moodle]
url = https://your.moodle.instance
username = your_username
password = your_password
```

## AI Settings

```ini
[ai]
enabled = 1
api_key = your_api_key
model = gpt-4o-mini
temperature = 0.7
max_tokens = 150
system_prompt = Summarize the message concisely with appropriate emojis, excluding links.
endpoint = https://api.openai.com/v1/chat/completions
```

## Notification Settings

```ini
[notification]
max_retries = 5
fetch_interval = 60  # seconds
```

## Pushbullet Settings

```ini
[pushbullet]
enabled = 0
api_key = your_pushbullet_key  # Required if enabled
```

## Discord Settings

```ini
[discord]
enabled = 1
webhook_url = your_webhook_url
bot_name = MoodleMate
thumbnail_url = your_thumbnail_url  # Optional thumbnail URL for webhook
```

You can generate a new configuration file using the `--gen-config` flag when running MoodleMate:
```bash
python main.py --gen-config
```
