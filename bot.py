from time import sleep
from threading import Thread, RLock
from queue import Queue
from collections import defaultdict

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from game_logic import COLUMN_COUNT
from config import config

class Event():
    def __init__(self, bot, column, voter=None):
        self.bot = bot
        self.column = column
        self.voter = voter

class DemocracyMode():
    def __init__(self, bot):
        self.bot = bot
        self.queue_in = Queue()

        self.one_vote_per_person = config['app'].get('one_vote_per_person', True)
        self.prevent_switching_sides = config['app'].get('prevent_switching_sides', False)

        self.opponent = None

        self.votes_lock = RLock()
        self.reset_votes()

        self.new_game()

    def new_game(self):
        with self.votes_lock:
            self.voters_this_game = set()

    def has_voted_this_game(self, voter):
        return voter in self.voters_this_game

    def reset_votes(self):
        with self.votes_lock:
            self.voters = dict()
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
                    print(f'No valid votes from "{self.bot.player}" yet!')
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
        print(f'Starting democracy thread for bot "{self.bot.player}"...')
        thread.start()

    def run(self):
        while True:
            batch = self.queue_in.get()
            with self.votes_lock:
                for event in batch:
                    print(f'"{self.bot.player}" voting for {event.column + 1}')

                    # Prevent switching sides
                    if self.prevent_switching_sides and self.opponent.has_voted_this_game(event.voter):
                        print(f'Ignoring vote for {self.bot.player} from opponent player {event.voter}')
                        continue

                    self.voters_this_game.add(event.voter)

                    # Clear previous vote
                    if self.one_vote_per_person and event.voter in self.voters:
                        print(f'Reverting previous vote for {self.bot.player} from player {event.voter}')
                        vote = self.voters[event.voter]
                        self.votes[vote] -= 1

                    self.votes[event.column] += 1
                    self.voters[event.voter] = event.column


class Bot():
    def __init__(self, player, queue=None):
        self.player = player
        self.player_config = config['players'][player]
        self.youtube = build('youtube', 'v3', developerKey=config['app']['api_key'])
        self.queue = queue

    def start_polling(self):
        thread = Thread(target=self.run, args=())
        thread.daemon = True
        print(f'Starting polling thread for bot "{self.player}"...')
        thread.start()

    def run(self):
        for batch in self.messages():
            events = []
            for message in batch:
                text = message['text']
                author = message['author']

                try:
                    column = int(text)
                except ValueError:
                    # ignore messages that aren't numbers
                    continue

                if not 1 <= column <= COLUMN_COUNT:
                    # ignore numbers that don't correspond to a column
                    continue

                events.append(Event(self, column - 1, voter=author))

            self.queue.put(events)

    def messages(self):
        request = self.youtube.videos().list(part='liveStreamingDetails', id=self.player_config['video_id'])
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
                print(f'Polling-Error in bot "{self.player}":', e)
                sleep(10)
                continue

            page_token = response['nextPageToken']

            if first_run:
                first_run = False
                sleep(response['pollingIntervalMillis'] / 1000)
                continue

            items = response['items']

            yield [
                {
                    'author': item['snippet']['authorChannelId'],
                    'text': item['snippet']['textMessageDetails']['messageText'],
                }
                for item in items
            ]

            polling_interval = response['pollingIntervalMillis'] / 1000
            print(f'Bot "{self.player}" sleeping {round(polling_interval, 2)}s')
            sleep(polling_interval)

if __name__ == '__main__':
    bot = Bot('left_player')

    for message in bot.messages():
        print(message)
