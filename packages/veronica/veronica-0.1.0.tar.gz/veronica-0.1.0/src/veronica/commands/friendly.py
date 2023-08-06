from cmd import Cmd
import os
import random
import getpass

class Friendly(Cmd):
    def do_intro(self,args):
        username = getpass.getuser().capitalize()
        response = [
            "I'm Veronica, your personal Linux assistant.",
            "Heya "+username+", I'm Veronica, your Linux assistant.",
            "I'm your personal Linux assistant Veronica. To know more about what I can do, please type 'help'."
        ]
        print(response[random.randint(0,len(response)-1)])

    def do_hi(self,args):
        username = getpass.getuser().capitalize()
        response = ["Hey wassup!",
            "Wasabi!",
            "Konnichiwa "+username,
            "Greetings "+username+", how can I help you?",
            "Good Morning "+username+", what can I do for you today?",
            "Veronica at your service, sir. What shall I do today?"
        ]
        print(response[random.randint(0,len(response)-1)])
    
    def do_joke(self,args):
        print("This is a joke: HAHAHA")