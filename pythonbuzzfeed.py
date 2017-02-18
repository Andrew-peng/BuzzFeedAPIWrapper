import requests
from datetime import datetime

class BuzzFeedAPI(object):
    def __init__(self):
        self.prefix = "http://www.buzzfeed.com/api/v2/feeds/"
        self.comments = "http://www.buzzfeed.com/api/v2/comments/"
    def request(self, path, params={}):
        try:
            return requests.get(path, params=params)
        except requests.exceptions.RequestException:
            raise BuzzFeedException("Invalid API response")

    def get_feed_page(self, feed, pagenum):
        d = {}
        d['p'] = pagenum
        r = self.request(self.prefix + feed, d)
        return r.json()['buzzes']

    def get_comments_page(self, buzz_id, pagenum):
        d = {}
        d['p'] = pagenum
        r = self.request(self.comments + buzz_id, d)
        return r.json()['comments']

    def get_num_comments(self, buzz_id):
        d={}
        d['p'] = 1
        total = 0
        while True:
            r = self.request(self.comments + buzz_id, d)
            if r.status_code != 200:
                break
            else:
                comments = r.json()['comments']
                if len(comments) > 0:
                    total += len(comments)
                else:
                    return total
            d['p'] += 1
        return total

    def get_timerange(self, feed, start, end):
        #initialize page number
        d = {}
        d['p'] = 1
        #convert to datetime
        start_date = None
        end_date = None
        try:
            start_date = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
            end_date = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise BuzzFeedException("Invalid time. Format expected: %Y-%m-%d %H:%M:%S")
        inrange = []

        #loop over all buzzes to get ones in a certain time range
        while True:
            r = self.request(self.prefix + feed, d)
            if r.status_code != 200:
                break
            else:
                buzzes = r.json()['buzzes']
                if buzzes is not None and len(buzzes) > 0:
                    for buzz in buzzes:
                        date = datetime.strptime(buzz['published_date'], '%Y-%m-%d %H:%M:%S')
                        if date > start_date and date < end_date:
                            inrange.append(buzz)
                else:
                    break
                d['p'] += 1
        return inrange

    def get_popular(self, feed, start_date, end_date, threshold = 0):
        buzzes = self.get_timerange(feed, start_date, end_date)
        d = {}
        abovethreshold = []
        for buzz in buzzes:
            total = 0
            d['p'] = 1
            while True:
                r = self.request(self.comments + buzz['id'], d)
                if r.status_code !=  200:
                    break
                else:
                    comments = r.json()['comments']
                    if comments is not None and len(comments) > 0:
                        total += len(comments)
                    else:
                        break
                    d['p'] += 1
            if total >= threshold:
                abovethreshold.append(buzz)
        return abovethreshold

class BuzzFeedException(Exception):
    def __init__(self, arg):
        self.arg = arg
    def __str__(self):
        return self.arg
