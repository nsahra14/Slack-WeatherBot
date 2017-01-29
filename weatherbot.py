import pyowm
import time
from slackclient import SlackClient
from tokens import owmtoken
from tokens import slacktoken

owm = pyowm.OWM(owmtoken)

BOT_ID = 'U3VR1T7TM'
AT_BOT = "<@" + BOT_ID + ">"
PROMPT = 'weather'
SLACK_BOT_TOKEN = slacktoken

slack_client = SlackClient(SLACK_BOT_TOKEN)
print(slack_client)


def handle_command(command, channel):
    """
        Receives commands directed at the bot and extracts locations
        for weather. If not not valid weather request, responds with clarification.
    """
    response = "Ask me what the weather is somewhere!"
    if PROMPT in command.lower():
        city = command.split('in')[1].split('?')[0]
        obs = owm.weather_at_place(city)
        weather = obs.get_weather()
        status = weather.get_detailed_status()
        temp = weather.get_temperature(unit='fahrenheit')['temp']
        wind = weather.get_wind()['speed'] #mph
        clouds = weather.get_clouds() #int percentage
        if weather.get_rain():
        	rain = 'There is rain in the 3-hour forecast'
        else:
        	rain = 'There is no rain in the 3-hour forecast'
        if weather.get_snow():
        	snow = 'There is snow in the 3-hour forecast'
        else:
        	snow = 'There is no snow in the 3-hour forecast'
        
        # print(weather.to_JSON())

        response = 'Weather in {}: \n\
        {}F degrees \n\
        windspeed is {}mph \n\
        {}% cloud cover \n\
        {} \n\
        {}'.format(city, temp, wind, clouds, rain, snow)
    
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)




def parse_slack_output(slack_rtm_output):
    """
       	Returns None unless a message is directed at the Bot, based on its ID.
       	If directed at bot, returns what is after @botid, and the channel.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                print(output['text'])
                return output['text'].split(AT_BOT)[1], output['channel']

    return None, None




if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading events
    if slack_client.rtm_connect():
        print("weatherbot connected and running")
        while True: #reads as long as connected
        	command, channel = parse_slack_output(slack_client.rtm_read())
        	if command and channel:
        		handle_command(command, channel)
        	time.sleep(READ_WEBSOCKET_DELAY)
    else:
    	print("Connection failed. Invalid Slack token or bot ID?")


