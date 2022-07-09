from basefilter import BaseFilter
from collections import Counter
from corpus import Corpus
from trainingcorpus import TrainingCorpus
import os
import math
class MyFilter(BaseFilter):
    def __init__(self):
        self.totalSpamCounter = Counter()
        self.totalHamCounter = Counter()
        self.numberOfHams = 0
        self.numberOfSpams = 0

        #List of common stopwords taken from: https://xpo6.com/list-of-english-stop-words/
        self.stopwords = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thick", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]

        self.suffixes = [":", ";", "<", "ing", "ed", "ies", "es", "s", "ion", "able", "ship", "er", "ive", "in", "ment", "ely", "ess", "ee", "e"]
        self.prefixes = [">","un"]
        self.vowels = ["a", "e", "i", "o", "u", "y"]

    def stem(self, string):
        if string in self.stopwords or len(string) < 4:
            return ""
       
        for suffix in self.suffixes:
            if string.endswith(suffix):
                if suffix == "ed" and string[len(string) - 2] == string[len(string) - 3] and string[len(string) - 2] == 'e':
                    string = string[0:(len(string) - len(suffix) + 1)]
                    return string
                string = string[0:(len(string) - len(suffix))]
                #Filters double consonant endings
                if len(string) > 2:
                    if string[len(string)-1] == string[len(string) - 2] and  not string[len(string) - 1] in self.vowels:
                        string = string[0:len(string) - 2]
                        
            
        for prefix in self.prefixes:
            if string.startswith(prefix):
                string = string[len(prefix):len(string)]
        
        return string

    def train(self, path):
        trainingCorp = TrainingCorpus(path)

        for title, body in trainingCorp.spams():
            spamWords = []
            wholeText = title + " " + body
            words = wholeText.lower().replace('.', ' ').replace(',', ' ').replace('/', ' ').split()

            for word in words:
                word = self.stem(word)
                if word == "":
                    continue
                else:
                    spamWords.append(word)
            
            self.totalSpamCounter += Counter(spamWords)
            self.numberOfSpams += 1


        for title, body in trainingCorp.hams():
            hamWords = []

            wholeText = title + " " + body
            words = wholeText.lower().replace('.', ' ').replace(',', ' ').replace('/', ' ').split()
            for word in words:
                word = self.stem(word)
                if word == "":
                    continue
                else:
                    hamWords.append(word)

            
            self.totalHamCounter += Counter(hamWords)
            self.numberOfHams += 1


        
        
    def test(self, path):
        corpus = Corpus(path)
        #If no emails have been trained on, load default dicts
        if self.numberOfHams == 0 and self.numberOfSpams == 0:
            self.numberOfSpams = 461
            self.numberOfHams = 153
            with open("defaultSpamCounter", 'r', encoding="utf-8") as f:
                body = f.readlines()
                for line in body:
                    parts = line.split()
                    self.totalSpamCounter[parts[0]] = int(parts[1])
            with open("defaultHamCounter", "r", encoding="utf-8") as g:
                body = g.readlines()
                for line in body:
                    parts = line.split()
                    self.totalHamCounter[parts[0]] = int(parts[1])
        
        for title, body in corpus.emails():
            spamicity = 0.0
            bayesianCoefficient = 0.0
            wholeText = title + " " + body
            words = wholeText.lower().replace('.', ' ').replace(',', ' ').replace('/', ' ').split()

            for word in words:
                rateInSpams = 0.0
                rateInHams = 0.0
                word = self.stem(word)
                if word == "":
                    continue
                else:
                    #Only words that show up in spam mails 10+ should be counted, discarding outliers
                    if self.totalSpamCounter[word] > 10:
                        rateInSpams = self.totalSpamCounter[word] / self.numberOfSpams
                        rateInHams = self.totalHamCounter[word] / self.numberOfHams
                        spamicityOfWord = rateInSpams / (rateInSpams + rateInHams)
                        #Words that have a spamicity of 1 did not appear in ham mails and are ignored
                        if spamicityOfWord == 1:
                            spamicityOfWord = 0.99

                        bayesianCoefficient += (math.log(1 - spamicityOfWord) - math.log(spamicityOfWord) )

            #Limiting bayesianCoefficient to avoid OverflowErrors
            if bayesianCoefficient > 500:
                bayesianCoefficient = 500
            elif bayesianCoefficient < -500:
                bayesianCoefficient = -500
            
            eToTheBayesianCoefficient = (math.e ** bayesianCoefficient)
            spamicity = 1/(1 + eToTheBayesianCoefficient)
            

            with open(os.path.join(path, "!prediction.txt"), "a", encoding="utf-8") as f:
                if spamicity > 0.95:
                    verdict = "SPAM"
                else:
                    verdict = "OK"
                f.write(title + " " + verdict + "\n")

        return 

