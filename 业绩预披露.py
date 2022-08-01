def getToken():
  with open('./hexin-v.js', 'r') as f:
    jscontent = f.read()
  context= execjs.compile(jscontent)
  return context.call("v")
  
def get_url_data(page_num, url):
    v = getToken()
    if page_num != 0:
      url = url + str(page_num) + '/ajax/1/free/1/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 
              'Referer': 'http://data.10jqka.com.cn/financial/yjyg/',
               'Accept': 'text/html, */*; q=0.01', 
               'hexin-v': v,
               'Cookie': 'Hm_lvt_60bad21af9c824a4a0530d5dbf4357ca=1659118409; Hm_lvt_f79b64788a4e377c608617fba4c736e2=1659118409; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1659118409; Hm_lpvt_60bad21af9c824a4a0530d5dbf4357ca=1659118913; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1659118913; Hm_lpvt_f79b64788a4e377c608617fba4c736e2=1659118913; v=' + v, 
               'X-Requested-With': 'XMLHttpRequest'}
    response = requests.post(url, headers=headers).text
    return response
    
def get_data_date(date_type='2022年中报'):

  dict_date = {
    '2022年年报': '2022-12-31',
    '2022年三季报': '2022-09-30',
    '2022年中报': '2022-06-30',
    '2022年一季报': '2022-03-31',

    '2021年年报': '2021-12-31',
    '2021年三季报': '2021-09-30',
    '2021年中报': '2021-06-30',
    '2021年一季报': '2021-03-31',

    '2020年年报': '2020-12-31',
    '2020年三季报': '2020-09-30',
    '2020年中报': '2020-06-30',
    '2020年一季报': '2020-03-31',
    }
    
  return dict_date[date_type]
  
def update_yjypl(h5file_name='同花顺数据.h5', content='业绩预披露', date_type='2022年中报', download_first_time=True):

  url = 'http://data.10jqka.com.cn/ajax/yypl/date/' + get_data_date(date_type) + '/board/ALL/field/sc/order/desc/page/'
  page_num = 1
  data = pd.DataFrame(columns=["股票代码",'股票简称','首次预约时间','变更时间','实际披露时间'])

  while True:

    format_data = get_url_data(page_num, url)
    stock_code = re.findall('target="_blank"  code="hs_(.*)" class="J_showCanvas">',format_data)
    stock_name = re.findall('class="J_showCanvas">(.*)</a>',format_data)
    date = re.findall('<td class="tc cur">(.*)</td>',format_data)
    change_time = [re.sub('[^0-9-]', '', i) for i in re.findall('<td>\n            \t(.*)',format_data)]
    true_time = re.findall('<td class="tc">(.*)</td>',format_data)[1::2]

    if len(stock_code) == 0:
      break

    result = [stock_code, stock_name, date, change_time, true_time]
    data = data.append(pd.DataFrame(np.array(result).T, columns=data.columns), ignore_index = True)

    print(page_num)
    # if not download_first_time: ############
    #   last_data_in_this_page = data["公告日期"].tail(1).item()######################################。记住查一下是不是都用公告日期
    #   last_data_in_this_page = datetime.datetime.strptime(last_data_in_this_page, '%Y-%m-%d')######################################
    #   current_Beijing_time = datetime.datetime.now(pytz.timezone('Asia/Shanghai')).replace(tzinfo=None)######################################
    #   timediff = current_Beijing_time - last_data_in_this_page # #####################################
    #   if timediff.days-1>=0 : ######################################
    #     break    ######################################

    page_num += 1

  h5file_name = h5file_name
  name = content + '/' + date_type

  if len(data) == 0:
    return

  try:
    old_data = pd.read_hdf(h5file_name, name, encoding="utf-8-sig")
  except:
    data.to_hdf(h5file_name, name, append=True, encoding="utf-8-sig")  
    old_data = pd.read_hdf(h5file_name, name, encoding="utf-8-sig")

  common = data.merge(old_data, on=["股票代码",'股票简称','首次预约时间','变更时间','实际披露时间'])
  add_in_data = data[~data["股票代码"].isin(common["股票代码"]) 
                | ~data["股票简称"].isin(common["股票简称"]) 
                | ~data["首次预约时间"].isin(common["首次预约时间"]) 
                | ~data["变更时间"].isin(common["变更时间"]) 
                | ~data["实际披露时间"].isin(common["实际披露时间"])]

  if len(add_in_data) == 0:###############################
    return ###############################

  updated_data = pd.concat([add_in_data, old_data]).sort_values(['首次预约时间', '股票代码'], ascending = [False, True]).reset_index(drop=True)

  updated_data.to_hdf(h5file_name, name, append=False, encoding="utf-8-sig")

if __name__ == "__main__":
  import requests
  import re
  import os
  import execjs
  import json
  import h5py
  import datetime ######################################
  import pytz######################################
  import numpy as np
  import pandas as pd
  import requests as rq
  from requests.utils import default_headers

  h5file_name = '同花顺数据.h5'
  content = '业绩预披露'
  download_first_time = True   ######################

  # update_yjypl(h5file_name, content, '2022年年报', download_first_time)
  # update_yjypl(h5file_name, content, '2022年三季报', download_first_time)
  update_yjypl(h5file_name, content, '2022年中报', download_first_time)
  # update_yjypl(h5file_name, content, '2022年一季报', download_first_time)

  # update_yjypl(h5file_name, content, '2021年年报', download_first_time)
  # update_yjypl(h5file_name, content, '2021年三季报', download_first_time)
  # update_yjypl(h5file_name, content, '2021年中报', download_first_time)
  # update_yjypl(h5file_name, content, '2021年一季报', download_first_time)

  # update_yjypl(h5file_name, content, '2020年年报', download_first_time)
  # update_yjypl(h5file_name, content, '2020年三季报', download_first_time)
  # update_yjypl(h5file_name, content, '2020年中报', download_first_time)
  # update_yjypl(h5file_name, content, '2020年一季报', download_first_time)