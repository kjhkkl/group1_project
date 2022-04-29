import requests
import json
import pandas as pd

rest_api_key = ""

class KakaoLocalAPI:

    def __init__(self, rest_api_key):
        self.rest_api_key = rest_api_key
        self.headers = {'Authorization': 'KakaoAK {}'.format(rest_api_key)}
        self.search_keyword_url = "https://dapi.kakao.com/v2/local/search/keyword.json"

    def search_keyword(self, query):
        params = {"query": f"{query}",
                  'category_group_code': "CS2"}
        res = requests.get(self.search_keyword_url, headers=self.headers, params=params)
        document = json.loads(res.text)
        match_first = document['documents'][0]
        return match_first['address_name'], match_first['road_address_name'], match_first['y'], match_first['x']

kakao = KakaoLocalAPI(rest_api_key)

gs = pd.read_csv("gs.csv")
gs_list = gs.values.tolist()
gs_name_list = []
for i in range(len(gs_list)):
  gs_name_list.append(gs_list[i][0])

lst_final = []
for i in range(len(gs_name_list)):
  sub_list = []
  sub_list.append(gs_name_list[i])
  for j in range(len(kakao.search_keyword(gs_name_list[i]))):
    sub_list.append(kakao.search_keyword(gs_name_list[i])[j])
  lst_final.append(sub_list)

df_lst_final = pd.DataFrame(lst_final, columns=['매장명', '주소', '도로명주소','y', 'x'])
df_lst_final.to_csv("gs25_xy.csv", index = False, encoding='utf-8-sig')