import urllib
import bs4 as bs4

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pymongo

client = pymongo.MongoClient("")
for name in client.list_database_names():
    print(name)
db = client['crypto-database']
cryptos = db['cryptos']

my_url = "https://finance.yahoo.com/cryptocurrencies?offset=0&count=60"

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# HTML parsing
page_soup = soup(page_html, "html.parser")

# Grabs each row
containers = page_soup.findAll("tr", {"class": "simpTblRow Bgc($hoverBgColor):h BdB Bdbc($seperatorColor) Bdbc($tableBorderBlue):h H(32px) Bgc($lv2BgColor)"})
containers2 = page_soup.findAll("tr", {"class":"simpTblRow Bgc($hoverBgColor):h BdB Bdbc($seperatorColor) Bdbc($tableBorderBlue):h H(32px) Bgc($lv1BgColor)"})

for container in containers:
    name = container.td.a["title"]
    name = name.replace("USD", "").lower()
    price = container.span.text
    price = price.replace(',', '')
    change_container = container.findAll("td", {"class", "Va(m) Ta(end) Pstart(20px) Fw(600) Fz(s)"})
    change = change_container[1].text
    change_percent = change_container[2].text
    market_container = container.findAll("td", {"class", "Va(m) Ta(end) Pstart(20px) Fz(s)"})
    market_cap = market_container[0].text
    abbrContainer = container.findAll("a", {"class", "Fw(600) C($linkColor)"})
    abbr = abbrContainer[0].text.replace("-USD", "")
    try:
        logo_container = container.findAll("img", {"class":"W(20px) H(20px) Mend(5px)"})
        logo = logo_container[0].get('src')
    except:
        continue

    crypto1 = {
        'name': name.replace("USD", "").lower().rstrip(),
        'abbr': abbr,
        'change': change,
        'change_percent': change_percent,
        'market_cap': market_cap,
        'price': float(price),
        'logo': logo
    }

    # doc = cryptos.find_one_and_update(
    #     {"name": crypto1["name"]},
    #     {"$set":
    #          {"price": crypto1["price"],
    #           "change": crypto1["change"],
    #           "change_percent": crypto1["change_percent"],
    #           "market_cap": crypto1["market_cap"]
    #           }
    #      }, upsert=True
    # )
    #cryptos.insert_one(crypto1)
    print(crypto1)

for container in containers2:
    name = container.td.a["title"]
    name = name.replace("USD", "").lower()
    price = container.span.text
    price = price.replace(',', '')
    change_container = container.findAll("td", {"class", "Va(m) Ta(end) Pstart(20px) Fw(600) Fz(s)"})
    change = change_container[1].text
    change_percent = change_container[2].text
    market_container = container.findAll("td", {"class", "Va(m) Ta(end) Pstart(20px) Fz(s)"})
    market_cap = market_container[0].text
    abbrContainer = container.findAll("a", {"class", "Fw(600) C($linkColor)"})
    abbr = abbrContainer[0].text.replace("-USD", "")
    try:
        logo_container = container.findAll("img", {"class": "W(20px) H(20px) Mend(5px)"})
        logo = logo_container[0].get('src')
    except:
        continue

    crypto2 = {
        'name': name.replace("USD", "").lower().strip(),
        'abbr': abbr,
        'change': change,
        'change_percent': change_percent,
        'market_cap': market_cap,
        'price': float(price),
        'logo': logo
    }

    # doc = cryptos.find_one_and_update(
    #     {"name": crypto2["name"]},
    #     {"$set":
    #          {"price": crypto2["price"],
    #           "change": crypto2["change"],
    #           "change_percent": crypto2["change_percent"],
    #           "market_cap": crypto2["market_cap"]
    #           }
    #      }, upsert=True
    # )

    print(crypto2)

    #cryptos.insert_one(crypto2)
