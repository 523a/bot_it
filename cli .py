# -*- coding: utf-8 -*-
'''
Created on Fri Jun 19 15:41:50 2020

@author: nnig9
'''
from requests import post

ph='Здравствуйте, чем могу вам помочь?'
while ph != "К":
    ph=input('Ч-----')
    text={'id':'ч','sent': 0,'text':ph,'time':''}
    res = post('http://84.201.170.162:5000/bot', json=text).json()
    print(res)
    
    

