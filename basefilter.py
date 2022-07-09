import os
class BaseFilter:
    def get_verdict(self, email):
        pass
    def train(self, path):
        pass
    def test(self, path):
        emails = os.listdir(path)
        with open(os.path.join(path, "!prediction.txt"), "w", encoding="utf-8") as f:
            for email in emails:
                if (email[0] == "!"):
                    continue
                f.write(email + " " + self.get_verdict(email) + "\n")
        
    