from time import sleep
from threading import Thread, RLock
from queue import Queue
from collections import defaultdict

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from game_logic import COLUMN_COUNT

class Event():
    def __init__(self, bot, column):
        self.bot = bot
        self.column = column

class DemocracyMode():
    def __init__(self, bot):
        self.bot = bot
        self.queue_in = Queue()

        self.votes_lock = RLock()
        self.reset_votes()

    def reset_votes(self):
        with self.votes_lock:
            self.votes = defaultdict(int)

    def get_vote(self, valid_locations, reset=False):
        with self.votes_lock:
            filtered_votes = {
                key: value
                for key, value in self.votes.items()
                if key in valid_locations
            }
            if len(filtered_votes) == 0:
                if reset:
                    print(f'No valid votes from "{self.bot.name}" yet!')
                vote = None
            elif len(filtered_votes) == 1:
                vote = list(filtered_votes.keys())[0]
            else:
                vote = max(*filtered_votes, key=lambda column: filtered_votes[column])

            if reset:
                self.reset_votes()

            return vote

    def start(self):
        self.bot.queue = self.queue_in
        self.bot.start_polling()
        thread = Thread(target=self.run, args=())
        thread.daemon = True
        print(f'Starting democracy thread for bot "{self.bot.name}"...')
        thread.start()

    def run(self):
        while True:
            batch = self.queue_in.get()
            with self.votes_lock:
                for event in batch:
                    print(f'"{self.bot.name}" voting for {event.column}')
                    self.votes[event.column] += 1


class Bot():
    def __init__(self, name, config, queue=None):
        self.name = name
        self.youtube = build('youtube', 'v3', developerKey=config['api_key'])
        self.video_id = config['video_id']
        self.queue = queue

    def start_polling(self):
        thread = Thread(target=self.run, args=())
        thread.daemon = True
        print(f'Starting polling thread for bot "{self.name}"...')
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
                print(f'Polling-Error in bot "{self.name}":', e)
                sleep(10)
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

            polling_interval = response['pollingIntervalMillis'] / 1000
            print(f'Bot "{self.name}" sleeping {round(polling_interval, 2)}s')
            sleep(polling_interval)

if __name__ == '__main__':
    import json

    with open('config.json', 'r') as fp:
        bot_config = json.load(fp)['left_player']

    video_id = input('Enter Video ID: ')

    bot = Bot('testbot', bot_config, None)

    for message in bot.messages():
        print(message)
