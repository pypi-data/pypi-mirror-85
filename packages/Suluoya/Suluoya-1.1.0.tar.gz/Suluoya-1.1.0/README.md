# Suluoya

## This is a package written by Suluoya just for fun!

### import

```python
import Suluoya as sly
```

search_question

```python
#search question by inputting for only once
sly.search_question()
#search question by inputting for many times
sly.search_question(again=True)
#search question by calling parameters and return answer
print(sly.search_question(question='Besides key points, the other element a summary should include is:'))
#search question by calling parameters and directly print answer 
sly.search_question(question='Besides key points, the other element a summary should include is:',show=True)
```

download_music

```python
#download music to d:\ 
sly.download_music()
#download music to any path you want
sly.download_music(path='c:\\')
```

draw_a_heart

```python
#draw a Suluoya heart
sly.draw_a_heart()
#draw any hearts you want
sly.draw_a_heart(name='any name you like')
```

xkcd

```python
#You know what I mean!
sly.xkcd()
```

get_soup

```python
#directly get soup from url
#not need to fill all
#url='https://pypi.org/project/Suluoya-pkg/' in default
#code='utf8' in default
#payloads means data in module 'requests' 
#'show=False' means show the soup instead of return it
get_soup(url='',code='',headers='',params={},payloads={},show=False)
```

get_json

```python
#directly get json from url
#not need to fill all
#if url='',Suluoya will go on strike
#code='utf8' in default
#payloads means data in module 'requests'
#'show=False' means show the json instead of return it
get_soup(url='',code='',headers='',params={},payloads={},show=False)
```

QRcode

```python
#make a QRcode
#fill in an url or some strings in content
#fill in the name of the QRcode in name
sly.QRcode(content='',name='')
```

contact

```python
#If you wanna contact Suluoya...
sly.contact(mode='wechat')
sly.contact(mode='qq')
```

pay

```
#If you wanna make a donation...
sly.pay(mode='alipay')
sly.apy(mode='wechatpay')
```

