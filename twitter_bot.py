import tweepy
import time


CONSUMER_KEY = #This is where the personal Consumer Key, obtained from Twitter's Developer website, goes
CONSUMER_SECRET = #This is where the Consumer Secret Key, obtained from Twitter's Developer website, goes
ACCESS_KEY = #This is where the Access Key, obtained from Twitter's Developer website, goes
ACCESS_SECRET = #This is where the Acccess Secret Key, obtained from Twitter's Developer website, goes

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


def open_file(file_name):
    """
    This function opens a file, reads the first line, and returns that line as an integer

    :param file_name: name of file to open, type str
    :return: since_id, which is id of last tweet the program interacted with, type int
    """
    file_read = open(file_name, 'r')
    since_id = int(file_read.read().strip())
    file_read.close()
    return since_id


def update_file(since_id, file_name):
    """
    This function updates the information of the file it opens, which will be the since_id

    :param since_id: id of last tweet program interacted with, type int
    :param file_name: name of file to open, type str
    :return: None
    """
    file_write = open(file_name, 'w')
    file_write.write(str(since_id))
    file_write.close()
    return


def respond_to_user(file_name):
    """
    uses Tweepy functions to look at mentions that account has received, and properly respond to user

    :param file_name: name of file to open that contains the id of the last tweet the program interacted with, since_id
    :return: None
    """
    since_id = open_file(file_name)
    # USE 1178169900591992832 AS since_id FOR TESTING
    mentions = api.mentions_timeline(since_id)
    for mention in reversed(mentions):  # for loop to iterate through mentions, starting from oldest to newest
        update_file(mention.id, file_name)
        if str(mention.in_reply_to_status_id) == "None":  # checks whether account was mentioned under a tweet or not
            # replies to user under the same tweet they mentioned the account in informing them on how to use the bot
            api.update_status('@' + mention.user.screen_name +
                              " Please @ this account under a tweet you would like to see the Quoted Retweets for :)",
                              mention.id)
            print("Telling user instructions...", end="\n")
        else:
            # replies to user under the same tweet they mentioned the account with a link to what they requested
            api.update_status('@' + mention.user.screen_name +
                              " https://twitter.com/search?q=https%3A%2F%2Ftwitter.com%2F"
                              + str(mention.in_reply_to_screen_name) + "%2Fstatus%2F"
                              + str(mention.in_reply_to_status_id), mention.id)
            print("Sending user link...", end="\n")


def main():
    """
    This is the main function which puts to use all of the previous functions so that they can run properly

    :return: None
    """
    file_name = "since_id"
    respond_to_user(file_name)


while True:
    main()
    time.sleep(15)  # reruns the program every 15 seconds so that Twitter's API limit is not reached

