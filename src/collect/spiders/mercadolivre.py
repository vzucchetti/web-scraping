import scrapy


class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"] #request 
    page_count = 1
    max_page = 20

    def parse(self, response): # function to parse considering the request
        products = response.css('div.ui-search-result__content') #html block with the information desired

        for product in products: #loop to curse the block and extract the each information needed for all itens

            #price of itens are splited in main value and the cents, but original and descounted prices are grouped
            #created a new variable to get each of these values, and able to isolate original and descounted
            prices = product.css('span.andes-money-amount__fraction::text').getall()
            cents = product.css('span.andes-money-amount__cents::text').getall()
            
            yield{
                'brand': product.css('span.ui-search-item__brand-discoverability.ui-search-item__group__element::text').get(),
                'name': product.css('h2.ui-search-item__title::text').get(),
                'old_price_reais': prices[0] if len(prices) > 0 else None, #getting the 1st value of the list (original price) with validation to be greater than 0
                'old_price_cents': cents[0] if len(cents) > 0 else None, #same thing than above for cents with validation to be greater than 1
                'new_price_reais': prices[1] if len(prices) > 1 else None, #same thing than old price but getting the 2nd value (new price with descount)
                'new_price_cents': cents[1] if len(cents) > 1 else None, 
                'reviews_rating_number': product.css('span.ui-search-reviews__rating-number::text').get(),
                'reviews_amount': product.css('span.ui-search-reviews__amount::text').get(),
            }

        if self.page_count < self.max_page:
            #jumping for the next page
            next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                #counting the number of pages to get until the max page defined
                self.page_count += 1
                #avancing to the next page, and with the command call this page and repeting the parse funcion for this page
                yield scrapy.Request(url=next_page, callback=self.parse)