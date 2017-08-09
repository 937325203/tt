import urllib.request as request
import urllib.parse as parse
import json

url="http://fanyi.baidu.com/v2transapi"
sugUrl='http://fanyi.baidu.com/sug'


def trans(src):
    # 设置post提交的数据
    #sugData
    #parse.quote(src)就是对src进行url编码，url编码也可以像这样拼接获得
    sugData = 'kw=' + parse.quote(src)
    sugData = sugData.encode('utf-8')
    print(sugData)
    #Data
    # parse.urlencode用于对post表单提交中的的data中的数据进行url编码,然后encode('utf-8')对他再进行一次编码
    data = {'from': 'en', 'to': 'zh', 'query': src, 'transtype': 'realtime', 'simple_means_flag': '3'}
    print(parse.urlencode(data))

    data = parse.urlencode(data).encode('utf-8')
    print(data)

    #发送请求，返回一个response，这里写错了一直写了个req。。。
    #传入一个data时进行post表单提交
    req = request.urlopen(url, data)
    sugReq = request.urlopen(sugUrl, sugData)

    '''也可以这样进行请求 把一个Request对象传入urlopen方法
    requestC=request.Request(url,data)
    req=request.urlopen(requestC)'''

    # 处理返回的数据
    req = req.read().decode('utf-8')
    sugReq = sugReq.read().decode('utf-8')

    # 返回值是一个json格式的字符串，将字符串扔进json.loads()得到解析后的json数据
    restList = json.loads(req)
    sugRestList = json.loads(sugReq)

    dst=restList['trans_result']['data'][0]['dst']
    sugRestListData = sugRestList['data']

    # 返回一个字典,dst为翻译目标,sugRestListData为建议内容
    return {'dst':dst,'sugRestListData':sugRestListData}