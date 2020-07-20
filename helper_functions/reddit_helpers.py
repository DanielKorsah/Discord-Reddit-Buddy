import praw
from prawcore import NotFound


def reddit_auth():
    # get reddit credentials
    reddit_token_file = open("redditSecrets.txt", "r")
    r_id = reddit_token_file.readline().rstrip()
    r_secret = reddit_token_file.readline().rstrip()
    r_usersubreddit_name = reddit_token_file.readline().rstrip()
    r_password = reddit_token_file.readline().rstrip()
    reddit_token_file.close()

    # reddit authentication
    reddit = praw.Reddit(client_id=r_id, client_secret=r_secret,
                         password=r_password, user_agent='USERAGENT',
                         usersubreddit_name=r_usersubreddit_name)
    return reddit


def get_nonsticky_submissions(subreddit, sort_type, num):
    start_list = get_submissions(subreddit, sort_type, num)

    # add extra submissions num for each sticky stickes
    for submission in start_list:
        if submission.stickied:
            num += 1

    # regenerate list with new num
    out_list = get_submissions(subreddit, sort_type, num)
    out_list = strip_stickies(out_list)

    # if num was 1 and there were 2 stickes, makes sure that the second stick is accounted for
    if len(out_list) == 0:
        num += 1
        out_list = get_submissions(subreddit, sort_type, num)
        out_list = strip_stickies(out_list)

    return out_list


def get_submissions(subreddit, sort_type, num):
    # gettatr dynamically switches the function name out for sort_type
    out_list = getattr(subreddit, sort_type)(limit=num)
    return out_list


def strip_stickies(submissions):
    # lambda to return list of submission where each submission is not stickied
    return list(filter(lambda x: not x.stickied, submissions))


def get_links(submissions):
    # lambda to  return the same list but their urls using map and a lambda function
    links = list(map(lambda x: x.url, submissions))
    return links


def get_titles(submissions):
    # lambda to return a list of each submission's title
    titles = list(map(lambda x: x.title, submissions))
    return titles


def check_exists(subreddit_name):
    exists = True
    try:
        reddit_auth().subreddits.search_by_name(subreddit_name, exact=True)
    except NotFound:
        exists = False
    return exists


def subreddit_accessible(subreddit):
    # bypass quarantines or notify about bans
    try:
        # this make a request that wil either be an exception or false, i'm just care if there is an exception
        workaround = subreddit.quarantine
        # this is to make the warning about not using a variable go away
        x = workaround
        workaround = x
        return {True, ""}
    except Exception as e:
        if str(e) == "received 403 HTTP response":
            subreddit.quaran.opt_in()
            print(
                f"Opting in to quarantined subreddit: /r/{subreddit.display_name}")
            return {True, ""}

        elif str(e) == "received 404 HTTP response":
            return {False, f"Subreddit [/r/{subreddit.display_name}] is banned or private."}
