import datetime

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import aiohttp
import asyncio


async def collect_data():
    ua = UserAgent()

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': ua.random
    }
    async with aiohttp.ClientSession() as session:
        response = await session.get(url='https://www.belconsole.by/Karty_oplaty/xbox_live/game-pass-ultimate/',
                                     headers=headers)

        soup = BeautifulSoup(await response.text(), 'lxml')
        dict_xbox_card = {}

        xbox_pass = soup.find_all('div', class_="product-description")
        # print(xbox_pass)
        for i in xbox_pass:
            price_card = i.find('span', class_='old-price').text.strip()
            try:
                price_card_discount = i.find('span', class_='current-price').text.strip()
            except AttributeError:
                price_card_discount = 'No discount'
                continue
            # print(price_card)
            for name in i.find_all('a', class_='theme-link'):
                # print(p.text.strip())
                dict_xbox_card[name.text.strip()] = ['https://www.belconsole.by' + name.get('href'), price_card,
                                                     price_card_discount]
        # print(dict_xbox_card)
    for key, value in dict_xbox_card.items():
        print(key, value)
    return dict_xbox_card


async def collect_data_xbox():
    ua = UserAgent()

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': ua.random
    }

    url = 'https://www.belconsole.by/XBox-Series-X/Igrovye_pristavki_XBox_X/igrovaya-pristavka-xbox-series-s/'
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            url=url,
            headers=headers)

    soup = BeautifulSoup(await response.text(), 'lxml')
    xbox = soup.find('div', class_='l-child-col-indent-half')
    xbox_name = xbox.find('h1', class_='ok-product__cart-name').text.strip()
    xbox_status = xbox.find('div', class_='ok-product__status-box').text.strip()
    if bool(xbox_status) == False:
        xbox_status = 'Нет статуса'
    xbox_price = xbox.find('span', class_='current-price').text.strip()

    xbox_s = {xbox_name: [xbox_status, xbox_price, url]}
    return xbox_s


async def main():
    await collect_data()
    await collect_data_xbox()


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
