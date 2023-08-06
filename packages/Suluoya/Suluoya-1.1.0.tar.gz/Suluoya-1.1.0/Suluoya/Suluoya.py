import requests
import urllib.parse as parse
from urllib.request import urlretrieve
import json
import os
import time
import sys
import urllib.request
import turtle
import random
from MyQR import myqr
from bs4 import BeautifulSoup
def search_question(question='',again=False,show=False):
    if question !='':
        url='http://api.xmlm8.com/tk.php?t={}'.format(question)
        response = requests.request("GET", url)
        data=json.loads(response.text)
        if show == True:
            print(data['tm']+'\n'+data['da']+'\n')
        else:
            return(data['tm']+'\n'+data['da']+'\n')
    else:
        if again == False:        
            timu=input('Please input the question:')
            url='http://api.xmlm8.com/tk.php?t={}'.format(timu)
            try:
                response = requests.request("GET", url)
                data=json.loads(response.text)
                print(data['tm']+'\n'+data['da']+'\n')
            except:
                mistake='Could not find the answer!'
                print(mistake) 
        else:
            while 1:
                timu=input('请输入题目：')
                url='http://api.xmlm8.com/tk.php?t={}'.format(timu)
                try:
                    response = requests.request("GET", url)
                    data=json.loads(response.text)
                    print(data['tm']+'\n'+data['da']+'\n')                
                except:
                    mistake='Could not find the answer!'
                    print(mistake)            
def download_music(path='d:\\'):
    w=parse.urlencode({'w':input('请输入歌名:')})
    url='https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=63229658163010696&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=10&%s&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0'%(w)
    content=requests.get(url=url)
    str_1=content.text
    dict_1=json.loads(str_1)
    song_list=dict_1['data']['song']['list']
    str_3='''https://u.y.qq.com/cgi-bin/musicu.fcg?-=getplaysongvkey5559460738919986&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data={"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"1825194589","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"1825194589","songmid":["%s"],"songtype":[0],"uin":"0","loginflag":1,"platform":"20"}},"comm":{"uin":0,"format":"json","ct":24,"cv":0}}'''
    url_list=[]
    music_name=[]
    for i in range(len(song_list)):
        music_name.append(song_list[i]['name']+'-'+song_list[i]['singer'][0]['name'])
        print('{}.{}-{}'.format(i+1,song_list[i]['name'],song_list[i]['singer'][0]['name']))
        url_list.append(str_3 % (song_list[i]['mid']))
    id=int(input('请输入你想下载的音乐序号:'))
    content_json=requests.get(url=url_list[id-1])
    dict_2=json.loads(content_json.text)
    url_ip=dict_2['req']['data']['freeflowsip'][1]
    purl=dict_2['req_0']['data']['midurlinfo'][0]['purl']
    downlad=url_ip+purl    
    try:
        print('开始下载...')
        urlretrieve(url=downlad,filename=r'{}{}.mp3'.format(path,music_name[id-1]))
        print('{}{}.mp3下载完成!'.format(path,music_name[id-1]))
    except Exception as e:
        print('没有{}的版权'.format(music_name[id-1]))
def draw_a_heart(name='Suluoya'):
    try:
        print('\n'.join([''.join([(name[(x-y)%len(list(name))]if((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3<=0 else' ')for x in range(-30,30)])for y in range(15,-15,-1)]))
    except:
        print('请输入字符串！')
def standard_time(show=True):
    t=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    if show == True:
        print(t)
    return t
def xkcd():
    import antigravity
def get_soup(url='https://pypi.org/project/Suluoya-pkg/',code='utf8',headers={},params={},payload={},show=False):
    try:
        response = requests.request("GET", url, headers=headers, data = payload, params = params)
        response.encoding=code
        soup = BeautifulSoup(response.text,'html.parser')
        if show == True:
            print(soup)
        return(soup)
    except:
        try:
            response = requests.request("GET", url, headers=headers, data = payload, params = params)
            if show == True:
                num=str(response)[-5:-2]
                print('HTTP Status Code ='+num)
                print('Please access https://www.cnblogs.com/hao-1234-1234/p/8940079.html')                
        except:
            print('Something went wrong!')    
def get_json(url='',code='utf8',headers={},params={},payload={},show=False):
    try:
        if url == '':
            print('Please add an url!')
        else:
            response = requests.request("GET", url, headers=headers, data = payload, params = params)
            response.encoding=code
            data=json.loads(response.text)
            if show==True:
                print(data)
            return(data)
    except:
        try:
            response = requests.request("GET", url, headers=headers, data = payload, params = params)
            num=str(response)[-5:-2]
            print('HTTP Status Code ='+num)
            print('Please access https://www.cnblogs.com/hao-1234-1234/p/8940079.html')
        except:
            print('Something went wrong!')
def contact(mode='qq'):
    qq='https://qm.qq.com/cgi-bin/qm/qr?k=SQEky7p_hr1bclCGYHLO9YHGEV2SCcg1&noverify=0'    
    wechat='https://u.wechat.com/ELmeETBV3ihbSWAoJogLLp0'
    print('Thanks for your support!\nMy contact code is already created!\nPlease search for QRcode.png in the current directory!\nThanks again! ')
    if mode=='qq':
        myqr.run(words=qq,save_name='qq_QRcode.png')
    elif mode == 'wechat':
        myqr.run(words=wechat,save_name='wechat_QRcode.png')
    else:
        print('Please choose the a mode:\nqq in default or wechat instead')        
def pay(mode='alipay'):
    pay_alipay='https://qr.alipay.com/fkx08434ltweaydof2wuj4b'
    pay_wechat='wxp://f2f0OpF_yJIY9Iag7-EbFI2cjFsZH3wBQoS7'
    print('Thanks for your support!\nThe payment code is already created!\nPlease search for QRcode.png in the current directory!\nThanks again! ')
    if mode=='wechatpay':
        myqr.run(words=pay_wechat,save_name='wechatpay_QRcode.png')
    elif mode == 'alipay':
        myqr.run(words=pay_alipay,save_name='alipay_QRcode.png')
    else:
        print('Please choose the a mode:\nalipay in default or wechatpay instead')
def syy():
    draw_a_heart('syy')
def hqy():
    draw_a_heart('hqy')
def QRcode(content='I Love Suluoya!',name='QRcode'):
    myqr.run(words=pay_alipay,save_name=name+'.png')