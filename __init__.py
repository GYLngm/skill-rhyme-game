from mycroft import MycroftSkill, intent_file_handler

import requests
import random
import os

__author__ = 'sarathms'

class RhymeGameSkill(MycroftSkill):
    def __init__(self):
        super().__init__(name="RhymeGameSkill")

    @intent_file_handler('game.rhyme.intent')
    def handle_game_rhyme(self, message):
        self.speak_dialog('game.rhyme')

        game = RhymeGame()
        self.log.debug("Started game")

        while True:
            word = game.get_new_word()
            response = self.get_response('game.rhyme.question', {'word': word})
            self.log.debug(response)
            if game.answer(response):
                self.speak_dialog('game.rhyme.correct', {'word': word, 'response': response})
                # ready = self.get_response('game.rhyme.next')
                self.speak_dialog('game.rhyme.next')
            else:
                self.speak_dialog('game.rhyme.wrong', {'word': word, 'response': response})
                self.speak_dialog('game.rhyme.gameover', {'score': game.get_score()})
                break

def create_skill():
    return RhymeGameSkill()

# http://rhymebrain.com/talk?function=getRhymes&word=hello
rhyme_brain_url = "http://rhymebrain.com/talk"
word_list_path = os.path.join(os.path.dirname(__file__), "words.txt")

class RhymeGame:
    def __init__(self):
        self.gameover = False
        self.score = 0
        self.word = ''
        self.answers = []

        # Load word list from file
        # TODO: Find an API to get a simple word from
        word_list_file = open(word_list_path, "r")
        self.word_list = word_list_file.readlines()
        word_list_file.close()
        # self.turnHistory = []

    def start(self):
        pass

    def get_score(self):
        return self.score

    def _gen_new_set(self):
        # Get a random word
        # Get rhyming words in @answers
        self.word = random.choice(self.word_list)
        payload = {
            'function': 'getRhymes',
            'word': self.word
        }
        response = requests.get(rhyme_brain_url, params=payload)
        self.answers = [ x['word'] for x in response.json()]

    def get_new_word(self):
        self._gen_new_set()
        return self.get_word()

    def get_word(self):
        return self.word

    def answer(self, response):
        result = self.check_answer(response)
        if (result == True):
            self.score = self.score + 1
            self._gen_new_set()
        return result

    def check_answer(self, response):
        if response in self.answers:
            return True
        else:
            return False

    def end_game(self):
        self.gameover = True
        return self.score
