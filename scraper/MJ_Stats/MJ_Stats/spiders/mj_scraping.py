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
                          "completegamelog19921993.htm", 
                          "completegamelog19911992.htm", 
                          "completegamelog19901991.htm", 
                          "completegamelog19891990.htm", 
                          "completegamelog19881989.htm", 
                          "completegamelog19871988.htm", 
                          "completegamelog19861987.htm"]

        gpx_href = [href for href in response.css('a::attr(href)').extract() if any(href.endswith(string) for string in target_strings)]

        for link in gpx_href:
            yield response.follow(link, self.parse_game_log)


    def parse_game_log(self, response):
        for tr in response.css('tr.a-top:not(.color-2)'):
            date_value = tr.css('td:nth-child(3)::text').get()
            fg_value_1 = tr.css('td:nth-child(4)::text').get()
            fg_value_2 = tr.css('td:nth-child(5)::text').get()

            item = { 
                'MJG': tr.css('td:nth-child(1)::text').get(),
                'TmG': tr.css('td:nth-child(2)::text').get(),
                'Date': date_value,
                'Opponent': f"{fg_value_1} {fg_value_2}",
                'Result': tr.css('td:nth-child(6)::text').get(),
                'MP': tr.css('td:nth-child(7)::text').get(),
                'FG': tr.css('td:nth-child(8)::text').get(),
                'FGA': tr.css('td:nth-child(9)::text').get(),
                '3P': tr.css('td:nth-child(10)::text').get(),
                '3PA': tr.css('td:nth-child(11)::text').get(),
                'FT': tr.css('td:nth-child(12)::text').get(),
                'FTA': tr.css('td:nth-child(13)::text').get(),
                'ORB': tr.css('td:nth-child(14)::text').get(),
                'DRB': tr.css('td:nth-child(15)::text').get(),
                'TRB': tr.css('td:nth-child(16)::text').get(),
                'AST': tr.css('td:nth-child(17)::text').get(),
                'STL': tr.css('td:nth-child(18)::text').get(),
                'BLK': tr.css('td:nth-child(19)::text').get(),
                'TO': tr.css('td:nth-child(20)::text').get(),
                'PF': tr.css('td:nth-child(21)::text').get(),
                'PTS': tr.css('td:nth-child(22)::text').get()
                }
             
            if not any(value == "None" or value is None for value in item.values()):
                yield item