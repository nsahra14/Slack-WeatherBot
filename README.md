# Slack WeatherBot
Custom Bot created for a Slack team to ask the weather in a specific city.

###Usage
Get the bot's attention by sending a message with `@[weatherbot's name]`, and ask it for the `"weather in [some place]"`. 

###Files
`print_bot_id.py` fetches the user ID of the bot from the team it's a part of. 
`weatherbot.py` contains the script for the bot to listen for all events in the Slack team, parses the messages that are directed to the bot, 
and fetches the weather for the city requested using the pyOWM API. `weatheroutput.txt` contains the JSON format of example `Weather` objects returned by the 
pyOWM API's request for the weather at some place.

####Resources
[Slack API](https://api.slack.com/)

[pyOWM API](https://github.com/csparpa/pyowm)

Code used in part from [this](https://www.fullstackpython.com/blog/build-first-slack-bot-python.html) tutorial.
