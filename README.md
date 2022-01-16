# upb-clco-proiect

## Diagrama proiect
![diagram](images/clco_diagrama_proiect.jpg)


## Utilizare
1. kubectl create namespace kafka
2. kubectl apply -k . -n kafka
3. cd olx_scraper
4. scrapyd-deploy
5. 
    a. scrapyd-client schedule anuntul_spider -p olx_scraper
    b. scrapyd-client schedule imobiliare_spider -p olx_scraper