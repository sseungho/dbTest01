from urllib.request import *
from urllib.parse import quote
import json
import datetime

class NaverApi:
    def getRequestUrlCode(self, url):
        requestUrl = Request(url)

        client_id = "npUTBllHPTYmbUeZzDNR"
        client_secret = "M2VxrCx4X8"

        requestUrl.add_header("X-Naver-Client-Id", client_id)
        requestUrl.add_header("X-Naver-Client-Secret", client_secret)

        naverResult = urlopen(requestUrl)     # 네이버에서 요청에 대한 응답 반환

        if naverResult.getcode() == 200:    # 응답 결과 정상
            print(f"네이버 API 요청 OK : {datetime.datetime.now()}")
            return naverResult.read().decode('utf-8')
            # 응답 결과 정상이면 네이버에서 받은 결과를 utf-8로 인코딩해서 반환
        else:
            print(f"네이버 API 요청 Failed : {datetime.datetime.now()}")
            return None
            # 응답 결과 error 아무것도 반환하지 않음

    def getNaverSearch(self, node, keyword, start, display):
        baseUrl = "https://openapi.naver.com/v1/search/"    #   네이버 API 기본 url
        node = f"{node}.json"
        params = f"?query={quote(keyword)}&start={start}&display={display}"

        url = baseUrl+node+params
        result = self.getRequestUrlCode(url)

        if result != None:  # 네이버에서 결과가 정상도착
            return json.loads(result)   # json 형식으로 반환
        else:
            print("네이버 응답 실패! 에러 발생")
            return None


