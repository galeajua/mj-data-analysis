import scrapy

class GameLogsSpider(scrapy.Spider):
    name = "game_logs"
    start_urls = [
        'https://www.michaeljordansworld.com/game_by_game.htm',
    ]

    def parse(self, response):
        target_strings = ["completegamelog19971998.htm",
                          "completegamelog19961997.htm", 
                          "completegamelog19951996.htm",
                          "completegamelog19941995.htm", 
                          "completegamelog19921993.htm"]

        season_href = [href for href in response.css('a::attr(href)').extract() if any(href.endswith(string) for string in target_strings)]

        for link in season_href:
            yield response.follow(link, self.parse_game_log)


    def parse_game_log(self, response):
        for tr in response.css('tr.a-top:not(.color-2)'):
            date_value = tr.css('td:nth-child(3)::text').get()
            fg_value_1 = tr.css('td:nth-child(4)::text').get()
            fg_value_2 = tr.css('td:nth-child(5)::text').get()

            item = {
                'MJ career game': tr.css('td:nth-child(1)::text').get(),
                'Team game this season': tr.css('td:nth-child(2)::text').get(),
                'Date': date_value,
                'Opponent': f"{fg_value_1} {fg_value_2}",
                'Result': tr.css('td:nth-child(6)::text').get(),
                'Minutes played': tr.css('td:nth-child(7)::text').get(),
                'Field goal made': tr.css('td:nth-child(8)::text').get(),
                '3-Pointers made': tr.css('td:nth-child(10)::text').get(),
                'Free throws made': tr.css('td:nth-child(12)::text').get(),
                'Total rebounds': tr.css('td:nth-child(16)::text').get(),
                'Assists': tr.css('td:nth-child(17)::text').get(),
                'Steals': tr.css('td:nth-child(18)::text').get(),
                'Blocks': tr.css('td:nth-child(19)::text').get(),
                'Personal fouls': tr.css('td:nth-child(21)::text').get(),
                'Points': tr.css('td:nth-child(22)::text').get()
                }
             
            if not any(value == "None" or value is None for value in item.values()):
                yield item