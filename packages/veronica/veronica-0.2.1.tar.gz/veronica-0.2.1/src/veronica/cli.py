"""Console script for veronica."""
import argparse
import sys
from pip._vendor.colorama import init
from pip._vendor.colorama import Fore
from cmd import Cmd
import getpass
from .commands.friendly import Friendly
from .commands.information import Information
import pkg_resources
import sentry_sdk
from sentry_sdk import capture_message
from .commands.pomo import Pomodoro

class Veronica(Friendly,Information,Pomodoro):
    def do_EOF(self, args):
        print("")
        raise SystemExit

    def emptyline(self):
        return True
        
    def do_version(self,args):
        message=["Veronica v"+pkg_resources.require("veronica")[0].version,
        "Inspired from Tony Stark and built by Nirmal Khedkar",
        "Check out:",
        "   www.github.com/nirmalhk7/veronica-cli",             # TODO Display this as clickable link
        "   nirmallhk7.tech",                                   # TODO Display this as clickable link
        ""
        "Always #TeamIronMan. Love you 3000!"]
        xlen = 0
        for msg in message:
            if(xlen<len(msg)):
                xlen = len(msg)
        print("")
        print(Cmd.ruler*xlen)
        print("")
        for msg in message:
            print(msg)
        print("")
        print(Cmd.ruler*xlen)
    
    def onecmd(self, line):
       # print("Middleware To Be Inserted")
        super().onecmd(line)

def argParse(argx):
    commArg = argx[0]
    remArgs = ""
    print(commArg)

def main():
    """Console script for veronica."""
    # sentry_sdk.init("https://3ac0bcf6b7c94dceba16841163e807d0@o410546.ingest.sentry.io/5299322")

    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    args = parser.parse_args()

    init(autoreset=True)
    prompt = Veronica()
    prompt.prompt = 'veronica> '
    prompt.ruler = '-'
    if(len(args._)): argParse(args._)
    prompt.cmdloop(Fore.YELLOW+'Welcome '+getpass.getuser().capitalize()+"! Veronica at your service ...")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
