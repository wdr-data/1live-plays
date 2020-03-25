from time import sleep
from threading import Thread

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from game_logic import COLUMN_COUNT

class Event():
    def __init__(self, bot, column):
        self.bot = bot
        self.column = column

class Bot():
    def __init__(self, name, config, video_id, queue):
        self.name = name
        self.youtube = build('youtube', 'v3', developerKey=config['api_key'])
        self.video_id = video_id
        self.queue = queue

    def start_polling(self):
        thread = Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        for batch in self.messages():
            events = []
            for message in batch:
                try:
                    column = int(message)
                except ValueError:
                    # ignore messages that aren't numbers
                    continue

                if not 1 <= column <= COLUMN_COUNT:
                    # ignore numbers that don't correspond to a column
                    continue

                events.append(Event(self, column - 1))

            self.queue.put(events)

    def messages(self):
        request = self.youtube.videos().list(part='liveStreamingDetails', id=self.video_id)
        response = request.execute()

        live_chat_id = response['items'][0]['liveStreamingDetails']['activeLiveChatId']
        page_token = None
        first_run = True

        while True:
            request = self.youtube.liveChatMessages().list(
                liveChatId=live_chat_id,
                part="id,snippet",
                pageToken=page_token,
                maxResults=2000,
            )

            try:
                response = request.execute()
            except HttpError as e:
                sleep(response['pollingIntervalMillis'] / 1000)
                continue

            page_token = response['nextPageToken']

            if first_run:
                first_run = False
                sleep(response['pollingIntervalMillis'] / 1000)
                continue

            items = response['items']

            yield [
                item['snippet']['textMessageDetails']['messageText']
                for item in items
            ]

            sleep(response['pollingIntervalMillis'] / 1000)

if __name__ == '__main__':
    import json

    with open('config.json', 'r') as fp:
        bot_config = json.load(fp)['pink']

    video_id = input('Enter Video ID: ')

    bot = Bot('testbot', bot_config, video_id, None)

    for message in bot.messages():
        print(message)
