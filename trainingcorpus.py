from corpus import Corpus
import os
class TrainingCorpus(Corpus):
    def get_class(self, email):
        with open(os.path.join(self.path, "!truth.txt"), "r", encoding="utf-8") as f:
            for line in f:
                if email in line:
                    words = line.split()
                    return words[1]

    def is_ham(self, email):
        if self.get_class(email) == "OK":
            return True
        else:
            return False

    def is_spam(self, email):
        if self.get_class(email) == "SPAM":
            return True
        else:
            return False
    def hams(self):
        for email in os.listdir(self.path):
                if email[0] == '!':
                    continue
                if self.is_ham(email):
                    with open(os.path.join(self.path, email), 'r', encoding='utf-8') as g:
                        body = g.read()
                        yield (email, body)

    def spams(self):
        for email in os.listdir(self.path):
                if email[0] == '!':
                    continue
                if self.is_spam(email):
                    with open(os.path.join(self.path, email), 'r', encoding='utf-8') as g:
                        body = g.read()
                        yield (email, body)


