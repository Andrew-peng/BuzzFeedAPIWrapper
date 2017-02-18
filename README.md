# BuzzFeedAPIWrapper
A simple wrapper class for [BuzzFeed's public API](https://gist.github.com/chezclem/c98b5170971c94dd1015)

---

Clone the repository using `git clone`
Run setup.py `python setup.py`

Heres an example of getting Tasty articles from Feb 2nd to Feb 4th that have over 10 comments.

```python
from pythonbuzzfeed import BuzzFeedAPI
buzzes = self.API.get_popular(feed, "2017-02-02 00:00:00", "2017-02-04 00:00:00", 10)
for buzz in buzzes:
    #do something
```

I wrote some unit tests in tests.py. The code is not very efficient. I have to loop through all the buzzes for one feed because the buzzfeed API does not allow queries for certain timeranges and are not sorted by time. As far as I can tell, the only parameters able to be passed in are feed/comment and page number. I used the python requests package to receive the JSON data and datetime to get all the buzzes within a certain time frame. 