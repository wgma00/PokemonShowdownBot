from cleverbot import Cleverbot


class Clever(object):

    def __init__(self):
        self.bot = Cleverbot()
        self.last = ""

    def update(self, last_msg):
        self.last = last_msg

    def reply(self):
        return self.bot.ask(self.last)


if __name__ == "__main__":
    c = Clever()
    c.update("hello")
    print(c.reply())
