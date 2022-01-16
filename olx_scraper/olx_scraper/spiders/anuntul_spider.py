import scrapy
from ..items import ApartamentItem


# noinspection SpellCheckingInspection
class AnuntulSpider(scrapy.Spider):
    name = "anuntul_spider"
    start_urls = [
        "https://www.anuntul.ro/anunturi-imobiliare-vanzari/apartamente-2-camere/?search[sumar][rubricaId]=1&search[sumar][subrubricaId]=4&search[zona][]=Titan-Dristor&search[fields][0][fields][0][value][min]=&search[fields][0][fields][0][value][max]=&search[fields][0][fields][1][value][]=0&search[fields][0][fields][1][value][]=1&search[metrou]=&search[schita]=&search[cautareId]=&search[query]=&search[lat]=&search[lng]=&search[sortf]=valabilitate.sort&search[sorts]=-1&search[page]=&search[owner]="
    ]
    # counter = 0

    def parse(self, response):
        # get all divs which contain info
        divs = response.xpath("//div[@class='list-txt']")
        for div in divs:
            # make an item
            item = ApartamentItem()

            # apart id
            # item['apartment_id'] = self.counter
            # self.counter += 1

            # titlu_anunt + url_anunt
            titlu = div.xpath(".//div[@class='float-left title-anunt i-fl']/a/text()").get()
            url = div.xpath(".//div[@class='float-left title-anunt i-fl']/a/@href").get()
            if titlu:
                item['titlu_anunt'] = titlu.strip()
            if url:
                item['url_anunt'] = url.strip()

            # descriere
            descriere = div.xpath(".//p/text()").get()
            if descriere:
                item['descriere'] = descriere.strip()

            # pret + moneda
            pret_moneda = div.xpath(".//div[@class='float-right price-list i-fr']/text()").get()
            if pret_moneda:
                pret_moneda = pret_moneda.strip().split()
                pret = pret_moneda[0].replace(",", "").replace('.', '').strip()
                moneda = pret_moneda[-1].strip()
                item['pret'] = pret
                item['moneda'] = moneda

            # data_postare
            data_postare = div.xpath(".//div[@class='loc-data float-right']/text()").get()
            if data_postare:
                item['data_postare'] = " ".join(data_postare.split())

            # an_constructie_bloc, compartimentare, etaj, nr_total_etaje, suprafata_utila
            info_list = div.xpath(".//div[@class='label-listing']/ul/li/text()").getall()
            if info_list:
                for info in info_list:
                    if 'mp' in info:
                        item['suprafata_utila'] = info.strip()
                    elif 'An' in info:
                        item['an_constructie_bloc'] = info.strip()
                    elif 'comandat' in info:
                        item['compartimentare'] = info.strip()
                    elif 'Etaj' in info:
                        temp = info.split('din')
                        item['etaj'] = temp[0].strip()
                        item['nr_total_etaje'] = temp[-1].strip()

            yield item

        # next_page
        next_page = response.xpath('//a[@class="page-link" and text()="»"]/@href').get()
        if next_page:
            yield response.follow(next_page.strip(), self.parse)
