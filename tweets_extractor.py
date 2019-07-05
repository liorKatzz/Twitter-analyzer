import tweepy
import pandas as pd

"""
Here we are going to extract the following fields and export it to a csv:
date: datetime
text: str
num_of_likes: int
mun_of_comments: int
retweeted: bool
hashtags: list of hashtags
"""

# Authentication
auth = tweepy.OAuthHandler("", "")
auth.set_access_token("",
                      "")
api = tweepy.API(auth, wait_on_rate_limit=True)


def extract_data_to_df(user_name):
    """
    Given a user, returns the df with all the data
    :param user_name:
    :return:
    """
    df = pd.DataFrame(columns=['tweet_id', 'date', 'content', 'num_of_likes', 'retweeted', 'hashtags'])
    statuses = api.user_timeline(screen_name=user_name, count=200, include_rts=True)
    while statuses:
        df_length = len(df)
        for i in range(len(statuses)):
            status = statuses[i]
            df.loc[i+df_length] = [status.id, status.created_at, status.text, status.favorite_count, status.retweeted,
                                   status.entities['hashtags']]
        # Get the id that all of the already read statuses are greater than, and put it as the max_id to get
        # the next 200 statuses
        max_id = statuses.max_id
        statuses = api.user_timeline(screen_name=user_name, count=100, include_rts=True, max_id=max_id)
    df.to_csv(".../statuses_{}.csv".format(user_name))
    return df


extract_data_to_df("realDonaldTrump")

