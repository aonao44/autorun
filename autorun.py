import os
import re
from this import d

import schedule
from time import sleep
from bs4 import BeautifulSoup
import requests

def line_notify(si, st):

    TOKEN = 'EPIUPC3KnMK3MH0IR2wKIGOSLAokCqbj0dLFnnoI674'

    api_url = 'https://notify-api.line.me/api/notify'

    send_contents = 'Flover:{}, Stock_status:{}'.format(si, st)

    TOKEN_dic = {'Authorization' : 'Bearer' + ' ' + TOKEN}
    send_dic = {'message': send_contents}
    print(TOKEN_dic)
    print(send_dic)

    r = requests.post(api_url, headers=TOKEN_dic, data=send_dic)
    print(r)

d_dict = []
def detect_updates():
    nonet_url = 'https://nonet-inc.com/collections/organic-dark-chocolate'

    r = requests.get(nonet_url)
    sleep(2)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, 'lxml')

    # 売れきれなのかそうでないのか判断/要素の取得
    new_check_ele = soup.select_one('#product-list-item-7352065425571 > a > div.list-text-wrapper > div.list-meta')
    # 文字にしておく
    stock_status = new_check_ele.text
    # txtファイルに書き込みのに文字列にしておく
    new_check_ele = str(new_check_ele)
    # シナモン味のタイトル取得
    sinamon_flover = soup.select_one('#product-list-item-7352065425571 > a > div.list-text-wrapper > div.list-title').text
    
    # 改行を消す
    stock_status = re.sub('\n', ' ', stock_status)
    sinamon_flover = re.sub('\n', ' ', sinamon_flover)
    stock_status = stock_status.replace(' ','')
    sinamon_flover = sinamon_flover.replace(' ', '')

    # フォルダのパス
    fold_path = os.path.dirname(os.path.abspath(__file__))
    # textファイルをフォルダのパスごと変数に入れておく
    comp_path_file = os.path.join(fold_path, 'comp_chek.txt')
    new_path_file = os.path.join(fold_path, 'new_check.txt')

    try:
        # フォルダのパス込みのファイル名を読み込む
        with open(comp_path_file) as f:
            # ファイル内のテキストの文字の取得
            comp_check_ele = f.read()
    except:
        comp_check_ele = ''

    # 34で取得した文字列とtxtファイル内の文字列を比較する
    # 同==[変化なし],異==[更新内容をtxtに書き込む]
    if new_check_ele == comp_check_ele:
        # line_notify関数の呼び出し
        line_notify(sinamon_flover,stock_status)
        return False
    else:
        with open(comp_path_file, 'w') as f:
            f.write(new_check_ele)
            # line_notify関数の呼び出し
            line_notify(sinamon_flover,stock_status)
            return True


# スケジュールの登録/実行.do
schedule.every(5).seconds.do(detect_updates)
while True:
    schedule.run_pending()
    sleep(1)