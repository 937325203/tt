import easygui as ui
import urllib.request as request
import urllib.parse as parse
import json
from sys import argv


url="http://fanyi.baidu.com/v2transapi"
sugUrl='http://fanyi.baidu.com/sug'


def trans(src):
    # 设置post提交的数据
    #sugData
    #parse.quote(src)就是对src进行url编码，url编码也可以像这样拼接获得
    sugData = 'kw=' + parse.quote(src)
    sugData = sugData.encode('utf-8')
    # print(sugData)
    #Data'from': 'en', 'to': 'zh',
    # parse.urlencode用于对post表单提交中的的data中的数据进行url编码,然后encode('utf-8')对他再进行一次编码
    data = { 'query': src, 'transtype': 'realtime', 'simple_means_flag': '3'}
    # print(parse.urlencode(data))
    data = parse.urlencode(data).encode('utf-8')
    # print(data)

    # 处理返回的数据
    # 传入一个data时进行post表单提交
    req = request.urlopen(url, data)
    sugReq = request.urlopen(sugUrl, sugData)

    req = req.read().decode('utf-8')
    sugReq = sugReq.read().decode('utf-8')

    # 返回值是一个json格式的字符串，将字符串扔进json.loads()得到解析后的json数据
    restList = json.loads(req)
    sugRestList = json.loads(sugReq)

    dst=restList['trans_result']['data'][0]['dst']
    sugRestListData = sugRestList['data']
    # print(dst)
    # for dic in sugRestListData:
    #     print(dic['k'], dic['v'])

    return {'dst':dst,'sugRestListData':sugRestListData}


def loop():
    log = open('/Users/BigBai/Desktop/字典记录.txt', 'a')
    while True:
        src = ui.enterbox(msg='英翻汉')

        #调用方法获得数据
        zidian = trans(src)
        dst = zidian['dst']
        sugRestList = zidian['sugRestListData']

        #拼串
        msg ='\n原文：'+src+'\n翻译：'+ dst + '\n'+'建议:\n'
        for dic in sugRestList:
            msg = msg + dic['k'] + ' ' + dic['v'] + '\n'

        #文件写入
        log.write(msg)
        log.write('\n------------------------------\n')
        ui.msgbox(msg)
    log.close()

def cmd():
    #获得命令行参数
    try:
        src=argv[1]
        zidian = trans(src)
        dst = zidian['dst']
        sugRestList = zidian['sugRestListData']
        msg = '\n原文：' + src + '\n翻译：' + dst + '\n' + '建议:\n'
        for dic in sugRestList:
            msg = msg + dic['k'] + ' ' + dic['v'] + '\n'

        print(msg)
    except(IndexError):
        print("请输入一个英文单词")




if __name__ == "__main__":
    cmd()
