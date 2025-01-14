import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class LocantoOtherSpider(CrawlSpider):
    name = "locanto_other_pages"  # unique identifier for the spider
    # allowed_domains = ["www.locanto.ie"]  # limits the crawl to this domain list
    # start_urls = ["https://www.locanto.ie/Other-Jobs/615/"]  # first url to crawl
    start_urls = ["https://www.locanto.ie/Hospitality-Tourism-Travel/622/"]  # testing url to see limits

    rules = (
        # use the parse() function on pages whose links match ".../ID_(number)/..." within the "entries" cs class
        # e.g. https://dublin.locanto.ie/ID_4964952094/Window-blinds-installer.html
        #       will match if it's in the list of entries on the page
        # Rule(LinkExtractor(allow="Other-Jobs")),
        # restricting the pages it can move to, along with how it calls back
        Rule(LinkExtractor(allow="Hospitality-Tourism-Travel")),
        Rule(LinkExtractor(allow="ID_", restrict_css=".entries"), callback="parse"),
    )

    def parse(self, response):
        title = response.css(".header-text::text").get()  # extract the title
        ad_id = response.css(".vap_ad_id::text").get()  # extract the ad id
        # format ad id
        ad_id = ad_id.replace("Ad ID: ", "")
        ad_id = ad_id.replace("\n", "")
        desc = response.css("#js-user_content::text").get()  # extract the description
        # NOTE: some ad descriptions are more complex and can't be extracted with this method
        #       for example: ads with "About this position" header, in the description.

        # username = response.css(".vap_sidebox_username::text").get()  # extract the username
        # username = username.replace("\n", "")  # format username
        # NOT ALL ADS HAVE A USERNAME

        # extract the location
        city = response.xpath("//div[@itemprop='address']/span[@itemprop='addressLocality']/text()").get()
        country = response.xpath("//div[@itemprop='address']/span[@itemprop='addressCountry']/text()").get()

        # PHONE NUMBER REQUIRES A LOGGED IN ACCOUNT
        yield {
            "title": title,
            "ad_id": ad_id,
            "desc": desc,
            # "username": username,
            "city": city,
            "country": country,
        }
