########This python file contain teh function to read teh text from different social platform 
########(Twitter, Iinstagram, Tumblr, Youtube, Reddit)

'''
Twitter function
'''

def get_twitter_text(data):
    if 'retweeted_status'in data:
        try:
            text = data['retweeted_status']['extended_tweet']['full_text']
        except:
            text = data['retweeted_status']['text']
    else:
        try:
            text = data['extended_tweet']['full_text']
        except:
            if 'full_text' in data:
                text = data['full_text']
            else:
                text = data['text']
    return text

'''
Tumblr function
'''

def get_tumblr_comments_text(data):
    comment_list = []

    if 'comment_result' in data: ###this tumblr json data has already been cleaned
        return [data['comment_result']['reply_text']]

    for comment in data['comments']:
        try:
            comment_list.append(comment['reply_text'])
        except:
            continue
    return comment_list

def get_tumblr_text(data):
    d_list = data['text']
    return d_list

'''
Instagram function
'''

############get the comments from instagram 
def get_instagram_comments_text(data):
    c_list = []

    if 'comment_result' in data: ###this instagram json data has already been cleaned
        return [data['comment_result']['text']]

    try:
        comments_list = data['edge_media_to_comment']['edges']
    except:
        preview_num = 0
        parent_num = 0
        if 'edge_media_to_parent_comment' in data:
            parent_num = len(data['edge_media_to_parent_comment']['edges'])
        
        if 'edge_media_preview_comment' in data:
            preview_num = len(data['edge_media_preview_comment']['edges'])
        
        print(parent_num,preview_num)
        if parent_num >= preview_num:
            comments_list = data['edge_media_to_parent_comment']['edges']
        else:
            comments_list = data['edge_media_preview_comment']['edges']
        
    for comment in comments_list:
        c_list.append(comment['node']['text'])
    return c_list

def get_instagram_post_text(data):
    try:
        text = data['edge_media_to_caption']['edges'][0]['node']['text']
    except:
        text = ''
    return text

'''
Youtube function
'''

def get_youtube_description_text(data):
    return data['description']

def get_youtube_title_text(data):
    return data['title']


def get_youtube_comments_text(data):
    data_list = []

    if 'comment_result' in data: ###this youtube json data has already been cleaned
        return data['comment_result']['comment_text']


    if len(data['comments']) != 0:
        for comment in data['comments']:
            data_list.append(comment['comment_text'])
    return data_list


'''
Reddit function
'''

def get_reddit_title_text(data):
    reddit_title = ''
    for p_key in data['post']:
        reddit_title = data['post'][p_key]['title']
        break
    return reddit_title

def get_reddit_description_text(data):
    reddit_des = ''
    for p_key in data['post']:
        reddit_des = get_reddit_text(data['post'][p_key])
        break
    return reddit_des

#######return a list of comment text
def get_reddit_comments_text(data):
    data_list = []
    
    if 'comment_result' in data: ###this reddit json data has already been cleaned
        return [get_reddit_text(data['comment_result'])]

    for com_key in data['comments']:
        data_list.append(get_reddit_text(data['comments'][com_key]))
    return data_list

def get_reddit_text(data):
    text = ''
    for content in data['media']['richtextContent']['document']:
        try:
            ###############fetch last layer
            con = dict(content)
            for c in con:
                if 'c' in con:
                    con = con['c'][0]
                else:
                    break
            ################

            if con['e'] == 'link':
                text = text + con['u'] + ' '
            else:
                text = text + con['t'] + ' '
        except Exception as e:
            continue
    return text
