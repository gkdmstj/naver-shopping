import requests
from bs4 import BeautifulSoup
import csv

# 사용자로부터 검색어 입력받기
search_query = input("검색어를 입력하세요: ")

# 검색 페이지 URL 생성
url = f"https://search.shopping.naver.com/search/all?query={search_query}&cat_id=&frm=NVSHATC"

# HTTP 요청 보내기
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}
response = requests.get(url, headers=headers)

# HTTP 요청이 성공했는지 확인하기
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    product_items = soup.select(".adProduct_title__amInq")
    product_list = []  # 제품 정보를 담을 리스트

    for idx, product_item in enumerate(product_items, start=1):
        name_element = product_item.select_one('a')
        name = name_element.get('title').strip() if name_element else "No name"
        price_element = product_item.find_next(class_="price_num__2WUXn")
        price = price_element.text.strip() if price_element else "No price"
        detail_element = product_item.find_next(class_="basicList_detail_box__3ta3h")
        detail = detail_element.text.strip() if detail_element else "No detail"
        product_list.append({'번호': idx, '제품명': name, '가격': price, '상세정보': detail})
else:
    print("HTTP 요청 실패")

# CSV 파일로 저장
filename = 'product_list.csv'
fields = ['번호', '제품명', '가격', '상세정보']

with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    writer.writerows(product_list)

print("CSV 파일 저장 완료.")

# 장바구니에 추가
cart_list = []

while True:
    product_number = input("장바구니에 추가할 제품 번호를 입력하세요 (종료: q): ")
    if product_number == 'q':
        break

    product_number = int(product_number)
    if product_number < 1 or product_number > len(product_list):
        print("잘못된 제품 번호입니다. 다시 입력해주세요.")
        continue

    selected_product = product_list[product_number - 1]
    cart_list.append(selected_product)
    print(f"제품 '{selected_product['제품명']}'이 장바구니에 추가되었습니다.")

# 장바구니 CSV 파일로 저장
cart_filename = './cart_list.csv'
fields = ['번호', '제품명', '가격', '상세정보']

with open(cart_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    writer.writerows(cart_list)

print("장바구니 CSV 파일 저장 완료.")

