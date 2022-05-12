import os
import schedule

from time import sleep
from bs4 import BeautifulSoup
import requests


# url = 'https://scraping.official.ec/items/40792454'
# url = 'https://scraping.official.ec/items/40792284'


def detect_updates():
    nonet_url = 'https://nonet-inc.com/collections/organic-dark-chocolate'

    r = requests.get(nonet_url)
    sleep(2)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, 'lxml')

    # soldout文字列のテキストの取得
    new_check_ele = soup.select_one('#product-list-item-7352065425571 > a > div.list-text-wrapper > div.list-meta')
    new_check_ele = str(new_check_ele)
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


    if new_check_ele == comp_check_ele:
        print('変化なし')
        return False
    else:
        with open(comp_path_file, 'w') as f:
            f.write(new_check_ele)
            print('更新しました')
            return True

# スケジュールの登録
schedule.every(1).days.do(detect_updates)

while True:
    schedule.run_pending()
    sleep(1)
    
'hjXiOf7HvJkhDmUSy870QFEjJZE62uz7FNbGPwguWmi'