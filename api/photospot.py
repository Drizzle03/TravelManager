from bs4 import BeautifulSoup
import requests as req
import json


class Photospot:
    def __init__(self):
        # TODO: Header의 세션 값은 매번 바뀌므로, 초기화해주는 코드 필요함.
        self.header = {
            'x-asbd-id': '437806',
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': 'hmac.AR3PaP-bDTR_oeoJDshsARVmCSEaxtvdlgmeEkWuH2ti5SwH',
            'x-requested-with': 'XMLHttpRequest'
        }
        self.result = None

    def __init_header(self):
        pass

    def __load_posts(self, tag: str):
        url = f'https://www.instagram.com/api/v1/tags/logged_out_web_info/?tag_name={tag}'
        res = req.get(url, headers=self.header)
        return (item['node']['shortcode'] for item in
                json.loads(res.text)['data']['hashtag']['edge_hashtag_to_media']['edges'])

    def __load_post_loaction(self, post_code: str):
        url = f'https://www.instagram.com/p/{post_code}/'
        res = req.get(url, headers=self.header)
        html = BeautifulSoup(res.text, 'html.parser')
        scrap_script = html.find_all('script')
        for item in scrap_script:
            try:
                return json.loads(item.text)['contentLocation']['name']
            except TypeError:
                return ''

    def run(self, place: str):
        self.result = list(
            dict.fromkeys([self.__load_post_loaction(v) for k, v in enumerate(self.__load_posts(tag=place)) if k < 30]))
        return self.result


app = Photospot()
app.run(place='서울특별시')
print(app.result)
