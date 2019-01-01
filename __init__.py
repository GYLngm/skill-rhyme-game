from mycroft import MycroftSkill, intent_file_handler


class RhymeGame(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('game.rhyme.intent')
    def handle_game_rhyme(self, message):
        self.speak_dialog('game.rhyme')


def create_skill():
    return RhymeGame()

