# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ApartamentItem(scrapy.Item):
    # define the fields for your item here like:
    # apartment_id = scrapy.Field()
    titlu_anunt = scrapy.Field()
    url_anunt = scrapy.Field()
    descriere = scrapy.Field()
    proprietar_agentie = scrapy.Field()
    compartimentare = scrapy.Field()
    suprafata_utila = scrapy.Field()
    suprafata_construita = scrapy.Field()
    an_constructie_bloc = scrapy.Field()
    nr_total_etaje = scrapy.Field()
    etaj = scrapy.Field()
    data_postare = scrapy.Field()
    pret = scrapy.Field()
    moneda = scrapy.Field()
    negociabil = scrapy.Field()
    stare = scrapy.Field()
    adresa = scrapy.Field()
    numar_bai = scrapy.Field()
