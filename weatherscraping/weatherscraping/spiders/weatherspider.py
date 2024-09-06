import scrapy


class WeatherspiderSpider(scrapy.Spider):
    name = "weatherspider"

    def start_requests(self):
        urls = [
            "https://www.climatempo.com.br/previsao-do-tempo/15-dias/cidade/313/niteroi-rj"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        contador = 0
        for elemento in response.xpath("//section[@class='accordion-card -daily-infos _border-bl-light-1']"):
            contador += 1
            if contador == 5:
                break
            yield {
                'Data': elemento.xpath("./div[1]/span/text()").get(),
                'Temperatura Máxima': elemento.xpath(".//div[@class='_flex']/span[@class='-gray']/text()").get(),
                'Temperatura Mínima': elemento.xpath(".//div[@class='_flex _margin-b-10']/span[@class='-gray']/text()").get(),
                'Condição do Tempo': elemento.xpath(".//p[@class='-gray -line-height-22 _margin-t-sm-20']/text()").get()
            }
