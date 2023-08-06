## Useful functions to log efficiently into a log.txt file and send you logs by Telegram.

Using this logger will :
- Create a `log.txt` file and append it new errors, with date and time of happening ;
- Send you every info or error via Telegram.

To install, type `python3 -m pip install tglog`, or try with `py ` instead of `python3` if you get any error.

You need your telegram chat_id, usually a chain of integers and the token of the telegram bot you want to receive logs from.

If you don't know your telegram chat_id, just send `/my_id` to telegram bot `@get_id_bot`.

If you haven't created any telegram bot, just send `/newbot` to `@BotFather`.

How to use : 

## Initialization :
```
import tglog

my_chat_id = "12345"            # Your telegram chat_id
my_bot_token = "token123"       # The token of the telegram bot you want to receive logs from

# Initialize your logger :

tl = tglog.logger(my_chat_id, my_bot_token)
```

## Use any of those functions in your code :
### Useful for debugging ; Telegram bot won't send notification :
Receive message when checkpoint reached :
`tl.debug("info for debugging")`    
### Useful for logging some infos
 Receive some infos :
`tl.info("info to be logged")`     
### Useful for logging errors
Receive traceback of errors :
`tl.error(traceback.format_exc())`  


