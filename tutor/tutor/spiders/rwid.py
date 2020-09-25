import scrapy


class RwidSpider(scrapy.Spider):
    name = 'rwid'
    login_url = 'http://localhost:5000/login'


    start_urls = ['http://localhost:5000/']

    def parse(self, response):
        print("Get Response.... !")
        self.logger.info(response.headers.getlist("Set-Cookie"))
        url = 'http://localhost:5000/login'
        data = {
            "username": "user",
            "password": "user12345"
        }
        yield scrapy.FormRequest(url, formdata=data,
                                 meta={'dont_redirect': True, 'handle_httpstatus_list': [302]},
                                 callback=self.afterlogin)
        self.logger.info(response.headers.getlist("Set-Cookie"))

    def afterlogin(self, response):
        print("Logged in..")
        yield scrapy.Request('http://localhost:5000', callback=self.startparse)

    def startparse(self, response):
        # Login check
        # yield {"title": response.css("title::text").get()}

        """
        1. Ambil semua data barang yang ada di halaman hasil -> akan menuju detail (parsing detail) 
        2. Ambil semua link next page (balik ke startparse)

        """

        # Get Detail Product
        title_page_links = response.css('.card-title a')
        yield from response.follow_all(title_page_links, self.parse_detail)

        pagination_links = response.css('.pagination a.page-link')
        yield from response.follow_all(pagination_links, self.startparse)

    def parse_detail(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        image = '.card-img-top::attr(src)'
        title = '.card-title::text'
        stock = '.card-stock::text'
        description = '.card-text::text'

        return {
            'image': extract_with_css(image),
            'title': extract_with_css(title),
            'stock': extract_with_css(stock),
            'desc': extract_with_css(description)

        }







