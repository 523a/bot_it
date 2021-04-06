# -*- coding: utf-8 -*-
'''
Created on Sun Jun 14 10:41:44 2020

@author: nnig9
'''
import json
import datetime
from acapp import client
import warnings

warnings.filterwarnings('ignore')
id='ч'
res = client.get('/bot')
print(res.get_json())
ph='Здравствуйте, чем могу вам помочь?'


while ph != "К":
    ph=input('Ч-----')
    now = datetime.datetime.now()
    text={'id':id,'sent': 0,'text':ph,'time':now}
    res = client.post('/bot', json=text)
    frame=res.get_json()
    print(res.get_json())

# json.dump(frame,open('test.json','w+',encoding='utf-8'))




