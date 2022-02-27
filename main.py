import argparse
from driver import CustomBrowserManager
import Post_getter

brows_manage = CustomBrowserManager()
reader_manager = Post_getter.PostReader()
reader = reader_manager.create_reader()

c = 1
for post in reader:
    url = f'https://vk.com/wall{post[3]}_{post[2]}'
    count = int(post[6])
    comments = brows_manage.comments(url, count)
    for comment in comments:
        print(f'{c}: ', comment)
    c += 1

