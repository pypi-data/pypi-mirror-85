## tweepyAuth
have you ever wanted to easily get a tweepy api object without any hassle?
this is the project for you!
its this simple:
```py
import tweepyauth 
import tweepy
api = tweepyauth.auto_authenticate()
print(api.me())
```

you can install this great library using pip with `pip3 install tweepyauth` 
___
optional arguments for auto_authenticate() are as follows:

`tokenfile=` (string) the file to read from or write twitter tokens to [defaults to `'twitter_tokens.txt'`]  
`keyfile=` (string) the file to read from or write twitter (consumer) keys to [defaults to `'twitter_keys.txt'`]  
`silent=` (bool) determines if console output should be printed [defaults to `False`]