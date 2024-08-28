from urllib.parse import urlencode
from urllib.request import urlopen
import json

def mareacode(area):#根据区号查询地方
    url = 'http://api.k780.com'
    params = {
      'app' : 'life.areacode',
      'areacode' : area,
      'appkey' : '73847',
      'sign' : '66107e84b89b9eba439b35daa9eb54a4',
      'format' : 'json',     
    }
    params = urlencode(params)
    f = urlopen('%s?%s' % (url, params))
    nowapi_call = f.read()
    a_result = json.loads(nowapi_call)
    if a_result:
      if a_result['success'] != '0':
        print(a_result['result'])
        data=a_result['result']
        simcalls = [item['simcall'] for item in data['lists']]  
        return simcalls
      else:
        print(a_result['msgid']+' '+a_result['msg'])
        return a_result['msgid']+' '+a_result['msg']
    else:
      print('Request nowapi fail.')
      return 'Request nowapi fail.'
def mareaname(area):#根据地方查询区号
    url = 'http://api.k780.com'
    params = {
      'app' : 'life.areacode',
      'areaname' : area,
      'appkey' : '73847',
      'sign' : '66107e84b89b9eba439b35daa9eb54a4',
      'format' : 'json',
    }
    params = urlencode(params)
    f = urlopen('%s?%s' % (url, params))
    nowapi_call = f.read()
    a_result = json.loads(nowapi_call)
    if a_result:
      if a_result['success'] != '0':
        print(a_result['result'])
        data=a_result['result']
        simcalls = [item['areacode'] for item in data['lists']]  
        return simcalls
      else:
        return a_result['msgid']+' '+a_result['msg']
    else:
      return 'Request nowapi fail.'