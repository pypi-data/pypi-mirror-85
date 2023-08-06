# Basic Web Scraper

## Project Description
This package can be used for simple automated web surfing / scraping.

Create classes inheriting the included BasicSpider class to create custom behavior to suit your requirements.

---

### Usage Example
```python
from basic_web_scraper.BasicSpider import BasicSpider

class CustomSpider(BasicSpider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def custom_operation(self, threshold):
        """
        Scroll to predefined threshold.
        If past threshold, scroll back up.
        """
        if self.get_page_y_offset() < threshold:
            self.mousewheel_vscroll(number_of_scrolls=2)

        else:
            y_difference = self.get_page_y_offset() - threshold
            self.smooth_vscroll_up_by(y_difference)


```

---

## More Description

### Driver
In order for the package to work, you must include a __```geckodriver.exe```__ in your local project directory. Otherwise a __```GeckoNotFoundException```__ will be raised

Note: This package currently only supports working with The Firefox geckodriver, which can be downloaded from [here](https://github.com/mozilla/geckodriver/releases)

### [__BasicSpider.py__](https://github.com/aziznal/basic-web-scraper/blob/master/BasicSpider.py)

Use this as the superclass for your own project's spider

This Spider allows you to do basic things like goto a url, scroll down the page in different ways, refresh the page, etc..

It acts as an interface to _**selenium.webdriver**_ to make setting up a project easier

More docs will be added in the future.
