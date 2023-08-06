from cmd import Cmd
import os
import geocoder
import requests
import urllib.parse
import json
from veronica.common import checkAPIActive,api_key
def f_to_c(far):
    return str(round((far-32)*5/9,2))

class Information(Cmd):

    def do_weather(self,args):
        locError = False
        if (args != ""):
            print("Retreiving weather for "+args.capitalize()+" ... ")
            g = geocoder.arcgis(args)
            print(g)
            coord = g.latlng
        elif (args == "" or locError):
            print("Retrieving weather for your current location ... ")
            g = geocoder.ip('me')
            coord = g.latlng
        if(checkAPIActive('darksky')):
            response = requests.get('https://api.darksky.net/forecast/'+api_key['darksky']+'/'+str(coord[0])+','+str(coord[1]))
            if(response.status_code == 200):
                data = response.json()
                res = data['currently']['summary']+" today with "+f_to_c(data['currently']['temperature'])+"° C."
                if(data['currently']['precipProbability']>0.5):
                    res += " Expect a "+str(data['currently']['precipProbability']*100)+"% chance of "+data['currently']['precipType']+"."
                print("")
                print(res)
                print("")
            else:
                print("Error: "+response.status_code)
    def do_calc(self,args):
        inpstr = args.split(' ')[0]
        for x in inpstr:
            if(x.isalpha() and x!='e'):
                print("Sorry incorrect");
                return
        print("Your result is",eval(inpstr))

    def do_pomodoro(self,args):
        print(args) 

    def do_info(self,args):
        print("Retreiving information for your query ... ")
        try:
            query,limit = args.split(':')
            limit = int(limit)
        except ValueError:
            query = args
            limit = 1
        service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
        if(checkAPIActive('knowledge_graph')):
            parameters = {
                'query': query,
                'limit': limit,
                'indent': True,
                'key': api_key['knowledge_graph'],
            }
            response = requests.get(service_url,params=parameters)
            if(response.status_code == 200):
                data = response.json()
                for i in range(limit):
                    try:
                        res = data['itemListElement'][i]['result']
                        print("")
                        try:
                            print(res['name'])
                        except KeyError:
                            pass
                        try:
                            print(res['description'])
                        except KeyError:
                            pass
                        try:    
                            print(res['detailedDescription']['articleBody'])
                        except KeyError:
                            pass
                        print("")
                    except IndexError:
                        print("Sorry, no data available!")
            else:
                print("Error: "+response.status_code)
