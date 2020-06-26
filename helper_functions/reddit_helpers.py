import praw


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
    return list(filter(lambda x: not x.stickied, submissions))


def get_links(submissions):
    # lambda to  return the same list but their urls using map and a lambda function
    links = list(map(lambda x: x.url, submissions))
    return links


def get_titles(submissions):
    titles = list(map(lambda x: x.title, submissions))
    return titles
