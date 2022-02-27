from typing import List, Optional, Dict, Iterator
import datetime
from base import BaseItem, CommentItem


from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

class CustomBrowserManager:
    '''Класс браузера'''

    def __init__(self, chrome=False, web_driver=None) -> None:
        self.broswer = webdriver.Chrome('/home/danil/Documents/Doploma/Panin/SelenuimVKParser/chromedriver')

    def load_items(self, item_container, args_find: dict, count: int):
        '''Генератор для получаения элементов с загрузкой их по Ajax'''
        items = item_container.find_elements(*args_find)
        downloaded_comments = len(items)
        N = -1
        while True:
            N += 1

            if N == count:
                break

            #Если номер элемента для отдачи больше, чем сейчас загружено, то загружаем еще элементы
            if N == downloaded_comments:


                start = datetime.datetime.now()
                while datetime.datetime.now() - start < datetime.timedelta(seconds=1) and len(item_container.find_elements(*args_find)) == downloaded_comments:
                    self.broswer.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    print(f'Time: {datetime.datetime.now() - start}. Items: {downloaded_comments}. Count {count}')

                    #При большом количестве комментариев требует регистрации, кликаем 'not now'
                    try:
                        if self.broswer.find_element(By.CLASS_NAME, 'JoinForm__notNowLink'):
                            self.broswer.find_element(By.CLASS_NAME, 'JoinForm__notNowLink').click()
                            self.broswer.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    except NoSuchElementException:
                        continue


                    #Проверяем что мы загрузили новые элементы, иначе элементы закончились и мы заканчиваем работу
                    new_items = item_container.find_elements(*args_find)
                    downloaded_comments = len(new_items)
                    if downloaded_comments == count:
                        break
                    
                items = new_items
            #Количество может не совпадать по причине показа только первых 20 комментариев в треде
            #В таком случае если данные не загрузились - прекращаем итерации
            if N == len(items):
                return

            yield items[N]

    def _generator(self, item: BaseItem, url: str, count: int = None):
        '''Базовая логика генератора для получаения элемента'''

        #Создаем новую вкладку, запоминаем и переключается на ее 
        # self.broswer.execute_script(f"window.open('', '{url}');")
        # generator_handler = self.broswer.window_handles[-1]
        # self.broswer.switch_to.window(generator_handler)

        #Загружаем страницу
        print(url)
        self.broswer.get(url)
        
        time_start = datetime.datetime.now()
        while True:
            #Находим контейнер постов
            try:
                posts_container = self.broswer.find_element(By.CLASS_NAME, item.container_tag)
            except NoSuchElementException:
                posts_container = None
            
            if posts_container or datetime.datetime.now() - time_start > datetime.timedelta(seconds=3):
                break
        print(datetime.datetime.now() - time_start, '!!!!')
        
        if not posts_container:
            return None

        #Создаем генератор для получения обьектов
        post_generator = self.load_items(posts_container, (By.CLASS_NAME, item.item_tag), count)
        while True:
            try:
                new_item = next(post_generator)
            except StopIteration:
                break
            yield item(new_item, url)
        
        # self.broswer.close()
    
    def comments(self, post_url: str, count: int = None) -> Iterator[CommentItem]:
        '''Генератор, который возвращяет коментарии как словари'''
        return self._generator(CommentItem, post_url, count)
