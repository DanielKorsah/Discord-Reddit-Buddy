import praw


def get_nonsticky_submissions(subreddit, sort_type, num=5):

    start_list = get_submissions(subreddit, sort_type, num)

    # add extra submissions num for each sticky stickes
    for submission in start_list:
        if submission.stickied:
            num += 1

    # regenerate list with new num
    out_list = get_submissions(subreddit, sort_type, num)
    out_list = strip_stickies(out_list)
    return out_list


def get_submissions(subreddit, sort_type, num):
    if sort_type == "hot":
        out_list = subreddit.hot(limit=num)
    elif sort_type == "new":
        out_list = subreddit.new(limit=num)
    elif sort_type == "rising":
        out_list = subreddit.rising(limit=num)
    elif sort_type == "controversial":
        out_list = subreddit.controversial(limit=num)
    elif sort_type == "top":
        out_list = subreddit.top(limit=num)
    return out_list


def strip_stickies(submissions):
    return filter(lambda x: not x.stickied, submissions)


def get_links(submissions):
    # lambda to  return the same list but their urls using map and a lambda function
    links = map(lambda x: x.url, submissions)
    return links


def get_titles(submissions):
    titles = map(lambda x: x.title, submissions)
    return titles
