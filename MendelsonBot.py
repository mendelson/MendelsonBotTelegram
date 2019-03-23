import time
import json
import requests
import telepot

TOKEN = "401969059:AAGKDJu6eWzuFXfAYdkvOQDDDShZBMeZmhQ"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
bot = telepot.Bot(TOKEN)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def correct_spelling(chat, message_id, text):
    words = text.split()
    for word in words:
        reply = word
        if "mara" in word:
            reply = reply.replace("mara", "dara")
            #send_message(reply, chat, "reply_to_message_id")
        if "mente" in word:
            reply = reply.replace("mente", "mendi")
            #send_message(reply, chat)
        # Sending message if there is a reason
        if reply != word:
            reply += '*'
            bot.sendMessage(chat_id=chat, text=reply, reply_to_message_id=message_id)

def text_replies(chat, message_id, text):
    if "tchau" in text or "até mais" in text:
        reply = "Valeu valeu valeu"
        bot.sendMessage(chat_id=chat, text=reply, reply_to_message_id=message_id)
    if "boa noite" in text:
        reply = "Mas já vai tão cedo?"
        bot.sendMessage(chat_id=chat, text=reply, reply_to_message_id=message_id)
    if "bom dia" in text:
        reply = "Ninguém liga!"
        bot.sendMessage(chat_id=chat, text=reply, reply_to_message_id=message_id)
    if "te amo" in text:
        reply = "Eu sei"
        bot.sendMessage(chat_id=chat, text=reply, reply_to_message_id=message_id)
    if "nervoso" in text:
        reply = "Nervoso? Que tal pescar?"
        bot.sendMessage(chat_id=chat, text=reply, reply_to_message_id=message_id)

def file_replies(chat, message_id, text):
    if "ata" in text or "ah tá" in text or "ah ta" in text:
        audio_id = "CQADAQADEgADpGnRR7iiZrR0nD4_Ag"
        bot.sendAudio(chat_id=chat, audio=audio_id, reply_to_message_id=message_id)
    if "saco" in text or "af" in text or "raiva" in text or "droga" in text or "bobo" in text or "bobão" in text:
        gif = "https://media.tenor.com/images/030501f2391081f75bce12b26bfe83b6/tenor.gif"
        """mimimi = "https://api.telegram.org/bot{0}/sendDocument?chat_id={1}&document={2}".format(TOKEN, chat, gif)
        requests.get(mimimi)"""
        bot.sendDocument(chat_id=chat, document=gif, reply_to_message_id=message_id)
        #sendDocument(chat, "https://media.tenor.com/images/030501f2391081f75bce12b26bfe83b6/tenor.gif")
    if "banana" in text:
        gif = "http://data.photofunky.net/output/image/0/b/9/c/0b9c5f/photofunky.gif"
        """banana = "https://api.telegram.org/bot{0}/sendDocument?chat_id={1}&document={2}".format(TOKEN, chat, gif)
        requests.get(banana)"""
        bot.sendDocument(chat_id=chat, document=gif, reply_to_message_id=message_id)

def treat_all(updates):
    for update in updates["result"]:
        chat = update["message"]["chat"]["id"]
        message_id = update["message"]["message_id"]
        text = update["message"]["text"].lower()

        # Correções de palavras
        correct_spelling(chat, message_id, text)
        # Respostas textuais
        text_replies(chat, message_id, text)
        # Respostas com arquivos
        file_replies(chat, message_id, text)

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            treat_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()