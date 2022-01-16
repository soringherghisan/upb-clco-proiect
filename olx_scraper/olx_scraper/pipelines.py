# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
# import psycopg2  # lib to talk to postgres dbs
import pymongo  # lib to talk to mongodb
from kafka import KafkaProducer
import json

"""
class OlxScraperPipelinePostgres:

    # in this example, my postgres db is inside a container with it's port
    # mapped to the docker host's port

    # Define function to configure the connection to the database & connect to it
    def open_spider(self, spider):
        hostname = 'localhost'  # sau ip docker ? sau port forward ? -> a mers portforward ; ip docker nu raspunde
        username = 'postgres'
        password = 'postgres'
        database = 'postgres'
        self.connection = psycopg2.connect(
            host=hostname,
            port="10432",
            user=username,
            password=password,
            dbname=database
        )
        self.cursor = self.connection.cursor()

    # Define function to disconnect from database
    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()

    # Define function to process each scraped item and insert it into    PostgreSQL table
    def process_item(self, item, spider):
        try:
            # Execute SQL command on database to insert data in table
            self.cursor.execute(
                "insert into anuntul_apartments(apartment_id, titlu_anunt, url_anunt, descriere, proprietar_agentie,"
                "compartimentare, suprafata_utila) values(%s,%s,%s,%s,%s,%s,%s)",
                (item['apartment_id'], item['titlu_anunt'], item['url_anunt'], item['descriere'],
                 item.get('proprietar_agentie'), item['compartimentare'], item['suprafata_utila'])
            )
            self.connection.commit()
        except Exception as e:
            print(e)
            self.connection.rollback()
            raise

        return item
"""


class OlxScraperPipelineMongo:
    spider_to_collection_map = {
        "anuntul_spider": "anuntul.ro",
        "imobiliare_spider": "imobiliare.ro"
    }

    def open_spider(self, spider):
        # kafka
        self.producer = KafkaProducer(bootstrap_servers=['my-cluster-kafka-bootstrap:9092'],
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'))

        # mongodb
        username = "root"
        password = "example"
        hostname = "mongo"
        port = 27017
        db = "apartments"
        collection = self.spider_to_collection_map[spider.name]

        self.connection = pymongo.MongoClient(
            host=hostname,
            port=port,
            username=username,
            password=password
        )
        self.db = self.connection[db]
        self.collection = self.db[collection]

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        # insert item into collection -
        self.collection.insert_one(dict(item))

        self.producer.send('jci-test-topic', dict(item))

        return item
