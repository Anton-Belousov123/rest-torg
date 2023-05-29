import requests
from bs4 import BeautifulSoup
import dataclasses


@dataclasses.dataclass
class Card:
    name: str
    url: str
    price: float
    photo: str


def scrape_card(card_block):
    url = 'https://rest-torg.ru' + card_block.find('a').get('href')
    price = float(card_block.find('span', {'class': 'product-preview__price-cur'}).text.split()[0].strip())
    photo = card_block.find('picture').find('img').get('data-src')
    return Card(
        url=url,
        price=price,
        photo=photo
    )

def scrape_cards(text: str):
    soup = BeautifulSoup(text, features='html.parser')
    items = soup.find_all('form', {'action': '/cart_items'})
    return items


def scrape_category(category_link: str):
    page_number = 0
    print(category_link)
    cards = []
    while True:
        page_number += 1
        request_url = category_link + f'?page={page_number}'
        response = requests.get(url=request_url)
        if 'По вашему запросу ничего не найдено' in response.text:
            break
        cards_blocks = scrape_cards(response.text)
        for card_block in cards_blocks:
            card = scrape_card(card_block)
            cards.append(card)
    print(len(cards))
categories = [
    'https://rest-torg.ru/collection/barnye-prinadlezhnosti',
    'https://rest-torg.ru/collection/kancelyarskie-tovary',
    'https://rest-torg.ru/collection/bytovaya-himiya',
    'https://rest-torg.ru/collection/konteynery-i-korobki',
    'https://rest-torg.ru/collection/krasota-i-zdorove',
    'https://rest-torg.ru/collection/odnorazovaya-odezhda',
    'https://rest-torg.ru/collection/odnorazovaya-posuda',
    'https://rest-torg.ru/collection/pakety',
    'https://rest-torg.ru/collection/spetsodezhda',
    'https://rest-torg.ru/collection/upakovochnye-materialy',
    'https://rest-torg.ru/collection/hozyajstvennye-tovary'
]

for category in categories:
    scrape_category(category_link=category)
