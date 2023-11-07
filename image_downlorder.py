from threading import Thread
from multiprocessing import Process
import requests
import json
import time

class ImageDownloader(Process):

    def __init__(self, queries, images):
        super(ImageDownloader, self).__init__()
        self.queries = queries
        self.previous_query = None
    
        self.images = images
    def run(self):
        query = self.queries.get()
        print("Query", query)
        while query is  not None:
            # if self.previous_query == query:
            #     self.previous_query = query
            #     print("Same Query is requested. ")
            #     query = self.queries.get()
            #     continue

            url = f'https://unsplash.com/napi/search/photos?page=1&query={query}'

            r = requests.get(url)
             
            if r.status_code == 200:
                response_json = json.loads(r.content)
                results = response_json['results']
                for image in results:
                    self.__download_image(image)

            else:
                print('Image Couldn\'t be retrieved')

               
           
            self.previous_query =query

    def __download_image(self, image):
        urls = image['urls']
        raw = urls['raw']
        print(raw)

        res = requests.get(raw, stream=True)

        if res.status_code == 200:
            res.raw.decode_content = True

            #https://plus.unsplash.com/premium_photo-1663127705654-a28e2ddf4af6?

            x= raw.split('?')
           
            image_name = x[0].split('/')[-1]

            file_name = f'images/{image_name}.jpg'

            with open(file_name,'wb') as f:
                f.write(res.content)

            self.images.put(file_name)

            print('Image sucessfully Downloaded: ', file_name)
        else:
            print('Image Couldn\'t be retrieved')

