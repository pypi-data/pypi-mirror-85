from requests_html import HTMLSession
from bs4 import BeautifulSoup

session = HTMLSession()


def get_price(lse_price_url):
    resp = session.get(lse_price_url)
    resp.html.render()
    soup = BeautifulSoup(resp.html.html, "lxml")
    bid, offer = [t.text for t in
                  soup.find(
                      'span', {'class': 'bid-offer-value'}).find_all('span')]
    return (bid, offer)
