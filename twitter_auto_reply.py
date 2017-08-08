import tweepy
import datetime
from twitter_settings import *

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

print("API完了")


class Listener(tweepy.StreamListener):
    def on_status(self, status):
        status.created_at += datetime.timedelta(hours=9)

        # リプライが来たら返信
        if str(status.in_reply_to_screen_name) == "recatem" and str(status.user.screen_name) == "takashaaark":
            tweet = "@" + str(status.user.screen_name) + " " + "リプどうも\n" \
                    + str(datetime.datetime.today())
            api.update_status(status=tweet)
        return True

    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True

    def on_timeout(self):
        print('Timeout...')
        return True


# Twitterオブジェクトの生成
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

listener = Listener()
stream = tweepy.Stream(auth, listener)
stream.userstream()
print("終了")

