import urllib.request
import urllib.parse
import json

class TelegramBotService:
    global base_url
    global chat_id

    def __init__(self, token, chat_id):
        self.base_url = 'https://api.telegram.org/bot' + token + '/'
        self.chat_id = chat_id
        return

    def send_message(self, text, custom_keyboard):
        url = self.base_url + 'sendMessage'

        values = {
            'chat_id': str(self.chat_id),
            'text': text.encode('utf-8')
        }
        reply_markup = json.dumps({
            'keyboard': custom_keyboard,
            'resize_keyboard': True,
            'one_time_keyboard': True,
            #    'selective': (reply_to != None),
        })
        values['reply_markup'] = reply_markup

        data = urllib.parse.urlencode(values)
        data = data.encode('utf-8')  # data should be bytes
        req = urllib.request.Request(url, data)
        with urllib.request.urlopen(req) as response:
            the_page = response.read()
        print(the_page)
        return

    """
    def get_updates(self, baseUrl):

        url = baseUrl + 'getUpdates'

        data = urllib.parse.urlencode(values)
        data = data.encode('utf-8')  # data should be bytes
        req = urllib.request.Request(url, data)
        with urllib.request.urlopen(req) as response:
            the_page = response.read()
        print(the_page)
        return
    """