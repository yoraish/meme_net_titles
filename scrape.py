# script for scraping
import praw
import json
import numpy as np

my_client_secret = 'OaANBYgl4H6ye_tYV1PW_IvoagA'
my_user_agent = 'yoraish'
my_client_id = 'j1AQxvMldaBhWQ'
reddit = praw.Reddit(client_id=my_client_id, client_secret=my_client_secret, user_agent=my_user_agent)


def title_to_freq(title, word_to_ix):
    # takes in a title string, returns a frequency list that has frequency in ix that corresponds to word.
    words = title.split()
    out = np.array([0]*len(word_to_ix))
    for word in words:
        if word in word_to_ix:
            out[word_to_ix[word]] += 1
    else:
        # print(word, "not in dict")
        pass
    res = np.float32(out/out.max())
    if np.isnan(res[0]):
        return None
    return out/out.max()



if __name__ == "__main__":



    # load the word-to-ix dictionary
    with open("word_to_ix.json") as word_to_ix_db:
        # create a dict to map ids to class
        word_to_ix = json.load(word_to_ix_db)
    

    # get 10000 hot posts from the MachineLearning subreddit
    hot_posts = reddit.subreddit('all').hot(limit=500)
    # posts = [i for i in hot_posts]
    # print(len(posts))


    counter = 0
    x_train_scrape = {}
    y_train_scrape = {}
    x_test_scrape = {}
    y_test_scrape = {}

    freq_to_score = {}
    for post in hot_posts:
        up = post.ups
        title = ''.join([i for i in post.title if i.isalpha() or i == ' '])

        freq_lst = title_to_freq(title, word_to_ix)
        if type(freq_lst) != type(None):
            freq_to_score[str(tuple(freq_lst))] = up


    with open('all_scrape_data.json', 'w') as f:
        json.dump(freq_to_score, f)


    # convert the word to 