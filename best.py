import requests
import pandas as pd
from bs4 import BeautifulSoup

bestbook_list = []

for i in range(1, 43):  # 1페이지부터 42페이지까지
    url = (
        f"https://www.yes24.com/product/category/bestseller?categoryNumber=001&pageNumber={i}&pageSize=24"
    )
    res = requests.get(url)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, 'html.parser')
    items = soup.select('li[data-goods-no]')

    if not items:
        print(f"페이지 {i}에 데이터가 없어 중단합니다.")
        break

    for item in items:
        # 순위
        rank = item.select_one('em.ico.rank').text.strip()

        # 책제목
        title = item.select_one('a.gd_name').text.strip()

        # 저자
        author_tag = item.select_one('span.authPub.info_auth a')
        author = author_tag.text.strip() if author_tag else ''

        # 출판사
        pub_tag = item.select_one('span.authPub.info_pub a')
        publisher = pub_tag.text.strip() if pub_tag else ''

        bestbook_list.append([rank, title, author, publisher])

df = pd.DataFrame(bestbook_list, columns=['순위', '책제목', '저자', '출판사'])
print(f"\n총 {len(df)}권을 수집했습니다.")
print(df)
df.to_csv("best_list.csv", index=False, encoding="utf-8-sig")
