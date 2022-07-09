import os
class Corpus:
    def __init__(self, path):
        self.path = path

    def emails(self):
            for email in os.listdir(self.path):
                if email[0] == '!':
                    continue
                with open(os.path.join(self.path, email), 'r', encoding='utf-8') as g:
                    body = g.read()
                    yield (email, body)
        
