import requests

def line_notify():

    TOKEN = 'EPIUPC3KnMK3MH0IR2wKIGOSLAokCqbj0dLFnnoI674'

    api_url = 'https://notify-api.line.me/api/notify'

    send_contents = 'てすとテストテストテストテスト！'

    TOKEN_dic = {'Authorization' : 'Bearer' + ' ' + TOKEN}
    send_dic = {'message': send_contents}
    print(TOKEN_dic)
    print(send_dic)

    r = requests.post(api_url, headers=TOKEN_dic, data=send_dic)
    print(r)

line_notify()