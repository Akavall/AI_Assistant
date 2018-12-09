from gtts import gTTS  
import json
import os
import requests
import random as rn
import pandas_datareader.data as web

from utils import get_artist_songs

class AI_Assistant(object):

    def __init__(self):
        
        self.config = self.get_config()

    def get_config(self):
        
        with open("config.json") as f:
            config = json.load(f) 

        return config
         

    def respond(self, text):

        tts = gTTS(text=text, lang='en') 
        tts.save("response.mp3")
        os.system("mplayer response.mp3")


    def handle_simple_response(self, content):

        with open("simple_responses.json") as f:
            simple_responses = json.load(f)

        for entry in simple_responses:
            if all(ele in content for ele in entry["keywords"]):
                self.respond(entry["answer"])
                return 
     

    def greeting(self):
        text = "Hi, I am Alice, I am listening"
        self.respond(text)
    
    def do_math(self, content):

        dont_know_text = """I don't think that I understood this question, 
                            could be math problem I am not familiar with"""

        d = {
             "plus": "+",
             "times": "*",
             "minus": "-",
             "divided by": "/",
            }

        try:
            
            if "what is" in content:            
                math_part = content.split("what is")[1]            
            if "what's" in content:
                math_part = content.split("what's")[1]
            if "whats" in content:
                math_part = content.split("what's")[1]
            
            original_math_part = math_part

            for k, v in d.items():
                math_part = math_part.replace(k, v)

            print("About to evaluate math_part: {}".format(math_part))
            result = round(eval(math_part), 3)
            print("Result: {}".format(result))

            self.respond(original_math_part + " is {}".format(result))

        except Exception as exc:

            if isinstance(exc, ZeroDivisionError):
                self.respond("Division by zero is not allowed by convention")
            else:
                print("Could not do math problem: {}".format(exc))
                self.respond(dont_know_text)

    def is_prime(self, content):
        
        num = ''.join(x for x in content if x.isdigit() or x == "-")
    
        print("checking if {} is prime".format(num))
        
        try:

            result = requests.get("http://34.208.248.130:8088/is_prime?num={}".format(num))
            if isinstance(result.content, bytes):
                self.respond(result.content.decode("utf-8"))
            else:
                # I don't know if this is actually being hit
                self.respond(result.content)
 
        except Exception as exc:
            print("Could not get get response from prime api: {}".format(exc))

    def get_weather(self, content):
        pass

    def play_music(self, content):
    
        if "bad" in content and "religion" in content:
            self.play_artist("BadReligion") 
        elif "emily" in content:
            self.play_artist("EmilyDavis")

    def play_artist(self, artist_name):

        print("Got request to play: {}".format(artist_name))
        
        artist_dir = self.config["music_dir"] + artist_name + "/"

        artist_songs = get_artist_songs(artist_dir)

        rn.shuffle(artist_songs) 

        n_songs_to_play = 1

        if len(artist_songs) >= n_songs_to_play:
            print("About to play: {}".format(artist_songs[:n_songs_to_play]))
            for i in range(n_songs_to_play):
                os.system('mplayer \"{}\"'.format(artist_songs[i]))
        else:   
            print("About to play: {}".format(artist_songs))
            for song in artist_songs:
                os.system('mplayer \"{}\"'.format(artist_songs[i]))

    def tell_a_joke(self):
        
        with open("jokes.json") as f:
            jokes = json.load(f)

        joke = rn.choice(jokes)
        print("About to tell joke: {}".format(joke))
        self.respond(joke)

    def tell_an_interesting_fact(self):
        
        with open("interesting_facts.json") as f:
            interesting_facts = json.load(f)

        fact = rn.choice(interesting_facts)
        print("About to tell fact: {}".format(fact))
        self.respond(fact)

    def get_stock_price(self, content):

        name_to_ticker = {"amazon": "amzn",
                          "google": "goog",
                          "chevron": "cvx",
                          "yahoo": "yhoo",
                          "walmart": "wal",
                        }

        s_content = content.split()
        
        ticker = s_content[-1]

        if ticker in ("ticker", "stock") and len(ticker) >= 2:
            ticker = s_content[-2]

        if ticker in name_to_ticker:
            ticker = name_to_ticker[ticker]

        try:
            price = web.get_last_iex(ticker).to_dict()[0]["price"]
            self.respond("{} is at {}, this information has 15 minute delay".format(ticker, price))    
        except Exception as exc:
            print("Could not get price for ticker: {}".format(ticker))

        
        


            
        
        
