# https://docs.gspread.org
import gspread
from datetime import datetime
import json
import os

# Google Spreadsheet에 접근하기 위한 인증 파일
gc = gspread.oauth(
  credentials_filename='./truss-inbody-rank/credentials.json',
  authorized_user_filename='./truss-inbody-rank/authorized_user.json'
)

# Google Spreadsheet 불러오기
sh = gc.open_by_key("192H5Xt3kudcMavGAJ9-0dhuJCrnr_k51wUPxzWs2WJI")

# 2022/06/01부터 현재까지의 날짜 차이를 계산
# https://jsikim1.tistory.com/144
startDate = datetime.strptime("20220601", "%Y%m%d") # 기준 날짜
now = datetime.now() # 현재 날짜

dateDiff = now - startDate
diffDays = dateDiff.days # 현재 날짜와 2022/06/01과의 차이 일수

# Spreadsheet 전체를 읽음
data = sh.sheet1.get_all_values() # list of 행, 각 행은 list of column으로 저장
# data = sh.sheet1.get_all_records() # list of 행, 각 행은 dictionary로 저장

# 현재 날짜까지 데이터만 포함하도록 list를 자름
slicedData = data[0:diffDays + 2]

# Spreadsheet 데이터를 JSON 파일로 저장
# https://code-study.tistory.com/58
with open('data.json', 'w') as f:
  # 한글 깨짐 문제 해결
  # https://jsikim1.tistory.com/222
  json.dump(slicedData, f, ensure_ascii = False)

os.system("sed -i 's/\[\[/graphData\=\[\[/g' data.json")

# 이후 작업은 index.html 내 JavaScript 코드가 진행함
