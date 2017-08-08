import logging

import tweepy

from twitter_settings import *
import time


def get_api():
    """
    APIの認証
    """
    auth = tweepy.OAuthHandler(P_CONSUMER_KEY, P_CONSUMER_SECRET)
    auth.set_access_token(P_ACCESS_TOKEN, P_ACCESS_TOKEN_SECRET)

    return tweepy.API(auth_handler=auth, wait_on_rate_limit=True)


def get_all_my_friends(api):
    """
    全相互フォローユーザーのオブジェクトを取得
    """
    all_sougos = list()
    for friend in tweepy.Cursor(api.friends).items():
        # logger.warning('Retrieving data from Twitter.')
        all_sougos.append(friend)
    return all_sougos


def get_all_my_followers(api):
    """
    全フォロワーのオブジェクトを取得
    """
    all_followers = list()
    for follower in tweepy.Cursor(api.followers).items():
        # logger.warning('Retrieving data from Twitter.')
        all_followers.append(follower)
    return all_followers


def follow_user_with_conditions(target_user, upper_limit_of_friends=2000, upper_limit_of_crazy=50):
    """
    条件を指定してフォロバする
    """
    # そのユーザーのツイッター開始からの期間
    # twitter_experience_days = (datetime.datetime.now() - target_user.created_at).days
    # そのユーザーの平均ツイート数
    # crazy = target_user.statuses_count * 1. / twitter_experience_days
    # if target_user.friends_count < upper_limit_of_friends and crazy < upper_limit_of_crazy:
    #     # そのユーザーをフォローする
    #     target_user.follow()
    #     print(u"ユーザ名:{0:15}  ツイート数:{1:<9d}  廃人度(tweets/a day):{2:.2f}".format
    #     (target_user.screen_name, target_user.statuses_count, crazy))
    #     return True

    target_user.follow()
    print('フォロバ。')
    return True


if __name__ == "__main__":

    while True:

        FORMAT = '%(asctime)s - %(name)s - %(message)s'
        logging.basicConfig(format=FORMAT)
        logger = logging.getLogger('twitter_api')

        api = get_api()

        # 全相互フォロワー
        all_my_friends = get_all_my_friends(api)

        # 全フォロワー
        all_my_followers = get_all_my_followers(api)

        follow_count = 0
        # フォロワーで相互フォローしていないユーザをフォローする
        for unknown_follower in all_my_followers:
            # 相互でない人を条件に基づいてフォロバする
            if unknown_follower not in all_my_friends:
                if follow_user_with_conditions(unknown_follower) is True:
                    follow_count += 1
                    # フォローは14人まで
                    if follow_count >= 14:
                        print('14人フォロバした。')
                        break

        print('15分間休む。')
        for i in range(15):
            print('.')
            time.sleep(60)
