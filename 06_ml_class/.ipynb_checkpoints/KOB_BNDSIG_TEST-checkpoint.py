

import time
import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup

def kob_bndsiga(std_dt):

    df_all = pd.DataFrame()
    for bnd_type in ['C00', 'C02']:

        # URL & Form Data
        gen_req_url = 'http://www.kofiabond.or.kr/proframeWeb/XMLSERVICES/'

        if bnd_type == 'C00':
            form_data = '''<message>
                            <proframeHeader>
                                <pfmAppName>BIS-KOFIABOND</pfmAppName>
                                <pfmSvcName>BISBndSrtPrcSrchSO</pfmSvcName>
                                <pfmFnName>selectDay</pfmFnName>
                            </proframeHeader>
                            <systemHeader></systemHeader>
                            <BISBndSrtPrcDayDTO>
                                <standardDt>''' + str(std_dt) + '''</standardDt>
                                <reportCompCd></reportCompCd>
                                <applyGbCd>''' + str(bnd_type) + '''</applyGbCd>
                            </BISBndSrtPrcDayDTO>
                           </message>'''
        else:
            form_data = '''<message>
                            <proframeHeader>
                                <pfmAppName>BIS-KOFIABOND</pfmAppName>
                                <pfmSvcName>BISBndSrtPrcSrchSO</pfmSvcName>
                                <pfmFnName>selectDay2</pfmFnName>
                            </proframeHeader>
                            <systemHeader></systemHeader>
                            <BISBndSrtPrcDayDTO>
                                <standardDt>''' + str(std_dt) + '''</standardDt>
                                <reportCompCd></reportCompCd>
                                <applyGbCd>''' + str(bnd_type) + '''</applyGbCd>
                            </BISBndSrtPrcDayDTO>
                            </message>'''

        # Request & Response -> Soup
        r = requests.post(gen_req_url, form_data)
        soup = BeautifulSoup(r.content, 'lxml-xml')

        # Result & Tag List
        res_li = soup.find_all('BISBndSrtPrcDayDTO')
        
        if len(res_li) >= 1:
            tag_li = [tag.name for tag in res_li[0]]
            tag_li = [tag for tag in tag_li if tag is not None]

            # Line by Line Dictionary -> DataFrame
            df = pd.DataFrame()
            for i in range(len(res_li)):
                res = res_li[i]
                dt = dict()
                for t in range(len(tag_li)):
                    tag = tag_li[t]
                    val = [res.find(tag).text]
                    if val == ['']:
                        val = [None]
                    else:
                        pass
                    dt[tag] = val
                df_sub = pd.DataFrame.from_dict(dt)
                df = df.append(df_sub, sort=None)

            df_all = df_all.append(df, sort=None)
            df_all['standardDt'] = str(std_dt)

        else:
            pass

    obs_cnt = len(df_all)
    file_dir = 'D://Crawling//04_KOB//KOB_BNDSIGA//'
    file_nm = 'KOB_BNDSIGA_' + str(std_dt) + '.xlsx'

    if obs_cnt >= 1:
        df_all.to_excel(file_dir + file_nm, index=False, index_label=None)
    else:
        pass

    print('KOB_BNDSIGA_DONE_' + str(std_dt) + '_DATA_' + str(obs_cnt))

    return 



#
#   크롤링, XLSX 파일생성
#       - 소급기간: 2010.01.01-2018.12.31
#

fr_date = 20100101
to_date = 20181231
date_li = pd.date_range(str(fr_date), str(to_date), freq='D').sort_values(ascending=False)

for d in range(len(date_li)):
    date = date_li[d]
    std_dt = date.strftime('%Y%m%d')
    kob_bndsiga(std_dt)
    time.sleep(3.0)



