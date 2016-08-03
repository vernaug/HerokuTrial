#!/usr/bin/env python
import os
import csv
import json
import string
import urllib
from flask import Flask
from flask import request
#from random import randint
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)
#response = ""

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    #if req.get("result").get("action") == "yahooWeatherForecast":
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = makeYqlQuery(req)
    if yql_query is None:
        return {}
    yql_url = baseurl + urllib.urlencode({'q': yql_query}) + "&format=json"
    print(yql_url)

    result = urllib.urlopen(yql_url).read()
    print("yql result: ")
    print(result)

    data = json.loads(result)
    res = makeWebhookResult(data,req)
    return res

##################################################################################################
'''
    else if req.get("result").get("action") == "recommend.people":

        set_of_responses = [
        "Sorry.I searched far and wide but could'nt find any suitable recommendation",
        "Still learning. Nothing to show for this query",
        "Could you please rephrase the query? I am not sure I get you",
        "I could'nt make sense of the last part. Could you please repeat it?",
        "Sorry. No recommendations to offer"
        ]

        sample = open("data.csv","r")
        reader = csv.reader(sample)

        keyword = req.get("result").get("parameters").get("keyword")

        for line in reader:
            if keyword in line[0]:
                for a in range(1,len(line)):

                    name = line[a].replace("@tcs.com","")
                    name = name.replace("."," ")

                    if response == "":
                        response = "I think these people can help you with "+line[0]+":\n"
                        response = response + "\t\t:pencil2:\t" + name.title() + "     ---- " + line[a] + "\n"
                    else:
                        response = response + "\t\t:pencil2:\t" + name.title() + "     ---- " + line[a] + "\n"
                break 
        
        if not response:
            magic = randint(0,4)
            response = set_of_responses[magic]
'''
##################################################################################################

def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeWebhookResult(data,req):   
    
    if req.get("result").get("action") == "yahooWeatherForecast":
        query = data.get('query')
        if query is None:
            return {}
    
        result = query.get('results')
        if result is None:
            return {}
    
        channel = result.get('channel')
        if channel is None:
            return {}
    
        item = channel.get('item')
        location = channel.get('location')
        units = channel.get('units')
        if (location is None) or (item is None) or (units is None):
            return {}
    
        condition = item.get('condition')
        if condition is None:
            return {}
    
        print(json.dumps(item, indent=4))    
        
        speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
                 ", the temperature is " + condition.get('temp') + " " + units.get('temperature')

'''
    else if req.get("result").get("action") == "recommend.people":
        response = ""
        repository = [
        ["nadia architecture","c.anantaram@tcs.com","mahesh.psingh@tcs.com","lipika.dey@tcs.com","ishan.verma@tcs.com"],
        ["deep learning","puneet.agarwal@tcs.com","lovekesh.vig@tcs.com","sarmimala.saikia@tcs.com","m.nambiar@tcs.com"],
        ["nlu","gautam.shroff@tcs.com","patidar.mayur@tcs.com","shaurya.r@tcs.com","y.mohit@tcs.com"],
        ["sensor analytics","ehtesham.hassan@tcs.com","malhotra.pankaj@tcs.com","vishnu.tv@tcs.com","gaurangi.anand@tcs.com"],
        ["entity resolution","karamjit.singh@tcs.com","gupta.garima@tcs.com","rajgopal.srinivasan@tcs.com"],
        ["evangelise","cs.joshi@tcs.com","sandeep.saxena@tcs.com","t.chattopadhyay@tcs.com","rajgopal.srinivasan@tcs.com"]
        ]
        keyword1 = req.get("result").get("parameters").get("keyword")
        
        for am in range(len(repository)):
            if keyword1 in repository[am][0]:
                for you in range(1,len(repository[am])):
                    
                    name = repository[am][you].replace("@tcs.com","")
                    name = name.replace("."," ")
                    if response == "":
                        response = "I think these people can help you with "+repository[am][0]+":\n"
                        response = response + "\t\t:pencil2:\t" + name.title() + "     ---- " + repository[am][you] + "\n"
                    else:
                        response = response + "\t\t:pencil2:\t" + name.title() + "     ---- " + repository[am][you] + "\n"
                break 
        speech = response
    '''
    print("Response:")
    print(speech)

        slack_message = {
            "text": speech
        }
    
        print(json.dumps(slack_message))
    
        return {
            "speech": speech,
            "displayText": speech,
            "data": {"slack": slack_message},
            # "contextOut": [],
            "source": "apiai-weather-webhook-sample"
        }
'''
    else if req.get("result").get("action") == "recommend.people":

        set_of_responses = [
        "Sorry.I searched far and wide but could'nt find any suitable recommendation",
        "Still learning. Nothing to show for this query",
        "Could you please rephrase the query? I am not sure I get you",
        "I could'nt make sense of the last part. Could you please repeat it?",
        "Sorry. No recommendations to offer"
        ]

        response = ""
        sample = open("data.csv","r")
        reader = csv.reader(sample)

        keyword = req.get("result").get("parameters").get("keyword")

        for line in reader:
            if keyword in line[0]:
                for a in range(1,len(line)):

                    name = line[a].replace("@tcs.com","")
                    name = name.replace("."," ")

                    if response == "":
                        response = "I think these people can help you with "+line[0]+":\n"
                        response = response + "\t\t:pencil2:\t" + name.title() + "     ---- " + line[a] + "\n"
                    else:
                        response = response + "\t\t:pencil2:\t" + name.title() + "     ---- " + line[a] + "\n"
                break 
        
        if not response:
            magic = 1
            response = set_of_responses[magic]
        
        slack_message = {
            "text": response
        }

        print(json.dumps(slack_message))

        return {
            "speech": response,
            "displayText": response,
            "data": {"slack": slack_message},
            # "contextOut": [],
            "source": "custom-python-code"
        }
        
'''

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')

