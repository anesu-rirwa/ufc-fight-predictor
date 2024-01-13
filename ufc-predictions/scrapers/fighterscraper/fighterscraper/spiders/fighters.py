import scrapy
import string #which is later used to generate a list of lowercase letters
from scrapy import Selector
from scrapy.crawler import CrawlerProcess

class FightersSpider(scrapy.Spider):
    name = "fighters"
    start_urls = ["http://www.ufcstats.com/statistics/fighters"]
    
    # http://www.ufcstats.com/fighter-details/1338e2c7480bdf9e
    def parse(self, response):
        # extracting fighter links from the main page
        fighter_links = response.xpath('//tbody//a[@class="b-link b-link_style_black"]/@href').extract() #Uses XPath to extract the links to individual fighter pages from the list of fighters on the current page.

        # iterate through each fighter link and send a request to their details page
        for link in fighter_links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_fighter)

    def parse_fighter(self, response):
        sel = Selector(response)

        # extracting fighter details
        fighter_name = sel.xpath('//span[@class="b-content__title-highlight"]/text()').get()
        fighter_record = sel.xpath('//span[@class="b-content__title-record"/text()]').get()
        fighter_nickname = sel.xpath('//span[@class="b-content__Nickname"/text()]').get()

        height = sel.xpath('//li[contains(i[@class="b-list__box-item-title"], "Height")]/text()')

        reach = sel.xpath()
        stance = sel.xpath()
        date_of_birth = sel.xpath()



# height
# weight
# reach
# stance
# dob

# slpm (strikes landed per minute)
# ssa (significant strike accuracy)
# sapm (stikes absorbed per minute)
# striking_defense

# takedown_average
# takedown_ accuracy
# takedown_defense

# submission_average