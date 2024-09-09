import scrapy
import schedule
import time
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from time import sleep
import smtplib
from email.message import EmailMessage
import imghdr
EMAIL_ADDRESS = 'rgebarinha@gmail.com'
EMAIL_PASSWORD = 'thujijxvfskzprgw'


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


def enviar_email():
    mail = EmailMessage()
    mail['Subject'] = 'Previsão do Tempo'
    mensagem = '''
    Baixe este arquivo com a previsão do tempo de hoje e para os próximos 3 dias
    '''
    mail['From'] = EMAIL_ADDRESS
    mail['To'] = 'tomwelling2311@gmail.com'
    mail.add_header('Content-Type', 'text/html')
    mail.set_payload(mensagem.encode('utf-8'))
    # Anexar qualquer tipo de arquivo(que não seja imagem)
    arquivos = ['C:\\Users\\rgeba\\OneDrive\\Documentos\\CURSO DEV APRENDER\\Proejto Destrava Web\\Projeto#1 - Web Scraper para Previsão do Tempo\\weatherscraping\\output.csv']

    for arquivo in arquivos:
        with open(arquivo, 'rb') as arquivo:
            dados = arquivo.read()
            nome_arquivo = arquivo.name
            mail.add_attachment(dados, maintype='application',
                                subtype='octet-stream', filename=nome_arquivo)

    # Enviar o email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as email:
        email.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        email.send_message(mail)


def run_spider():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(WeatherspiderSpider)
    process.start()


schedule.every().day.at('12:08').do(run_spider)
schedule.every().day.at('12:09').do(enviar_email)


while True:
    schedule.run_pending()
    sleep(1)
