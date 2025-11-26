import json
import datetime
import requests
from bs4 import BeautifulSoup
import os

# 관심 종목 리스트 (원하는 대로 수정 가능)
STOCK_LIST = [
    {"code": "005930", "name": "삼성전자"},
    {"code": "000660", "name": "SK하이닉스"},
    {"code": "035420", "name": "NAVER"},
    {"code": "035720", "name": "카카오"},
    {"code": "005380", "name": "현대차"},
    {"code": "000270", "name": "기아"},
    {"code": "247540", "name": "에코프로비엠"},
    {"code": "051910", "name": "LG화학"},
    {"code": "003490", "name": "대한항공"},
    {"code": "373220", "name": "LG에너지솔루션"}
]

def get_consensus(code):
    try:
        url = f"https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A{code}&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        price_tag = soup.select_one('#svdMainChartTxt11')
        price = price_tag.text.strip() if price_tag else "-"

        consensus = 0.0
        opinion = "의견없음"
        target_price = "-"
        
        summary_table = soup.select('#corp_group2 dl')
        for item in summary_table:
            dt = item.select_one('dt').text
            dd = item.select_one('dd').text
            if '투자의견' in dt:
                opinion = dd.strip()
                try:
                    consensus = float(opinion.split('점')[0]) if '점' in opinion else 0.0
                    if ']' in opinion: opinion = opinion.split(']')[1].strip()
                except: pass
            elif '목표주가' in dt:
                target_price = dd.strip()

        return {"code": code, "price": price, "consensus": consensus, "opinion": opinion, "target_price": target_price, "url": url}
    except:
        return None

result_list = []
for stock in STOCK_LIST:
    data = get_consensus(stock['code'])
    if data:
        data['name'] = stock['name']
        result_list.append(data)

output = {
    "updated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "stocks": result_list
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=4)


