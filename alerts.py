import urllib.request, urllib.parse

def send_telegram_alert(cfg, message):
    if not cfg.telegram_bot_token or not cfg.telegram_chat_id:
        return False
    url=f"https://api.telegram.org/bot{cfg.telegram_bot_token}/sendMessage"
    data=urllib.parse.urlencode({"chat_id":cfg.telegram_chat_id,"text":message}).encode()
    try:
        with urllib.request.urlopen(url,data=data,timeout=8):
            return True
    except Exception:
        return False
