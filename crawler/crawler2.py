from facebook_scraper import get_posts
from random import randint
import time, os, re
import pandas as pd




options={"comments": True}
df= pd.DataFrame()
posts= get_posts("WeiderTW", pages=30, cookies = "www.facebook.com_cookies.txt", options=options)
print(posts)
for i,post in enumerate(posts):
    # print("post: ",post)
    if int(post['time'].strftime("%Y")) <= 2019: break # 2019之前的資料不要
    df = pd.concat([df, pd.Series({
            # 'user_id': str(post['user_id']),
            'username': str(post['username']),
            'time': post['time'],
            # 'post_url': post['post_url'],
            # 'post_id': str(post['post_id']),
            'post_text': post['post_text'].strip().replace("\n", ""),
            # 'like_count': post ['reactions']['讚']   if '讚' in post['reactions'].keys() else 0,
            # 'love_count'     : post ['reactions']['大心']  if '大心' in post['reactions'].keys() else 0,
            # 'go_count'       : post ['reactions']['加油'] if '加油' in post['reactions'].keys() else 0,
            # 'wow_count'      : post ['reactions']['哇']   if '哇' in post['reactions'].keys() else 0,
            # 'haha_count'     : post ['reactions']['哈']   if '哈' in post['reactions'].keys() else 0,
            # 'sad_count'      : post ['reactions']['嗚']   if '嗚' in post['reactions'].keys() else 0,
            # 'angry_count'    : post ['reactions']['怒']   if '怒' in post['reactions'].keys() else 0,
            'share_count'    : post['comments'],
            'comment_count'  : post['shares'],
        })],
        ignore_index=True)
    # warnings.filterwarnings( "ignore" )
    # i = i + 1
    # print("\n\t>>>>> DONE{}.....POST_ID: {}  {}\n\t>>>>> {}\n\n".format(i, str(post['post_id']), str(post['time']), str(post['post_url'])))
    print(post.keys())
    print("username: ", post['username'], "\ttext:", post['text'], "\tlike:", (post.get('reactions') or {}).get("讚"), post.get("likes"))
    print("----")
    time.sleep(randint(1,5)) # 睡1-5秒，官方文件的討論區有些建議能睡大約一分鐘左右

print(df)