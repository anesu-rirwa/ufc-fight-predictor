import scrapy
import string #which is later used to generate a list of lowercase letters
from scrapy import Selector
from scrapy.crawler import CrawlerProcess

class FightersSpider(scrapy.Spider):
    name = "fighters"
    start_urls = ["http://www.ufcstats.com/statistics/fighters"]
    
    def parse(self, response):
        # extracting fighter links from the main page
        fighter_links = response.xpath('//tbody//a[@class="b-link b-link_style_black"]/@href').extract() #Uses XPath to extract the links to individual fighter pages from the list of fighters on the current page.

        # iterate through each fighter link and send a request to their details page
        for link in fighter_links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_fighter)

        # follow pagination link
        next_page = response.xpath('//li[@class="b-statistics__paginate-item"]/a[@class="b-statistics__paginate-link"]').extract_first()

        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)


    def parse_fighter(self, response):
        sel = Selector(response)

        # extracting fighter details
        fighter_name = sel.xpath('//span[@class="b-content__title-highlight"]/text()').get()
        fighter_nickname = sel.xpath('//p[@class="b-content__Nickname"]/text()').get()
        height = sel.xpath('//i[contains(text(), "Height")]/following-sibling::text()[1]').get()
        weight = sel.xpath('//i[contains(text(), "Weight")]/following-sibling::text()[1]').get()
        reach = sel.xpath('//i[contains(text(), "Reach")]/following-sibling::text()[1]').get()
        stance = sel.xpath('//i[contains(text(), "STANCE")]/following-sibling::text()[1]').get()
        date_of_birth = sel.xpath('//i[contains(text(), "DOB")]/following-sibling::text()[1]').get()

        slpm = sel.xpath('//i[contains(text(), "SLpM")]/following-sibling::text()[1]').get() # strikes landed per minute
        ssa = sel.xpath('//i[contains(text(), "Str. Acc.")]/following-sibling::text()[1]').get() # significant strike accuracy
        samp = sel.xpath('//i[contains(text(), "SApM")]/following-sibling::text()[1]').get() # stikes absorbed per minute
        ssd = sel.xpath('//i[contains(text(), "Str. Def.")]/following-sibling::text()[1]').get() # significant strike defence

        td_avg = sel.xpath('//i[contains(text(), "TD Avg.")]/following-sibling::text()[1]').get() # takedown_average
        td_acc = sel.xpath('//i[contains(text(), "TD Acc.")]/following-sibling::text()[1]').get() # takedown_ accuracy
        td_def = sel.xpath('//i[contains(text(), "TD Def.")]/following-sibling::text()[1]').get() # takedown_defense

        sub_avg = sel.xpath('//i[contains(text(), "Sub. Avg.")]/following-sibling::text()[1]').get() # takedown_defense# submission_average

        # Output scraped data
        yield {
            'fighter_name': fighter_name,
            'figter_nickname': fighter_nickname, 
            'height': height,
            'weight': weight,
            'reach': reach,
            'stance': stance,
            'date_of_birth': date_of_birth,
            'slpm': slpm,
            'ssa': ssa,
            'samp': samp,
            'ssd': ssd,
            'td_avg': td_avg,
            'td_acc': td_acc,
            'td_def': td_def,
            'sub_avg': sub_avg
        }

if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    # Iterate through the alphabet and generate start URLs
    for letter in string.ascii_uppercase:
        start_url = f'http://www.ufcstats.com/statistics/fighters?char={letter}'
        process.crawl(FightersSpider, start_urls=[start_url])

    process.start() 