# Telegram Auto Forward Bot

This makes a user send all messages from one/many chat(s) to another chat(s).

## Setting up 
* First:
- `APP_ID` and `API_HASH` - Get it from my.telegram.org   
- `SESSION` - A telethon session string, get it from [here](https://replit.com/@TeamUltroid/UltroidStringSession)
- `FROM_CHANNEL` - Channel ID(s) split by space or just one channel ID
- `TO_CHANNEL` - Channel ID(s) split by space or just one channel ID
- `BLOCKED_TEXTS` - To block any specific text in message. ( If that text is found inside the text, then that message will not get forward)
- `MEDIA_FORWARD_RESPONSE` - To manage media forward. ( To allow media forward - yes or no)
- `REPLACE_DICT` - To replace text in messages. (word:replacement) seperated by comma

* Deployment:

- Clone the repo:   <code>git clone https://github.com/dhruvknsr/Telegram-AutoForwardBot</code></br>
- Make a <code>.env</code> file in the root of the repo, like <a href="https://github.com/dhruvknsr/telegram-auto_forwarder/blob/main/.env.sample">.env.sample</a> and fill in the values.</br>
- Use <code>python3 bot.py</code> to start the bot.</br>  
</details>

## Usage
All new messages will be auto-posted!!
Join the channel from you want the posts to be taken.
Join as admin in the channel where you want the posts to be sent to.

## Credits
> [Ayush7445](https://github.com/Ayush7445) for the original script [telegram-forwarder_auto]
