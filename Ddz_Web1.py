#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, abort, Response
from time import time
from uuid import uuid4
import json

import Ddz_jiaofen as jdz

app = Flask(__name__)


@app.route('/')
def index():
    return ''' 斗地主接口   <br>
    
    role  身份  0 地主 1 地主下  2 地主上 <br>
    
    
    手牌数据  一个长度15的数组，数组里的值是 张数   <br>
     [ 0,3,0,1,3,0,0,0 ,0,0,0,0,0, 0, 0] 表示 手牌 4 4 4 6 7 7 7  <br>
  牌面  3 4 5 6 7 8 9 10 J Q K A 2  小 大  <br>
        
    
    data 数据 : <br>


    
    
    '''




@app.route('/jiaodizhu', methods=['POST', 'GET'])
def jiaodizhu():
    data = request.values.get('data', None)

    if not data:
        abort(400)

    data = list(data)
    data_arr = []
    for d in data:
        if d != ',' and d != ' ':
            data_arr.append(d)
    hand_cards = jdz.anti_replace(data_arr)
    jdz.sort(hand_cards)
    s = jdz.score(hand_cards)
    if s>25:
        return '叫地主'
    else:
        return '不叫'

@app.route('/jiabei', methods=['POST', 'GET'])
def jiabei():
    data = request.values.get('data', None)

    if not data:
        abort(400)

    data = list(data)
    data_arr = []
    for d in data:
        if d != ',' and d != ' ':
            data_arr.append(d)
    hand_cards = jdz.anti_replace(data_arr)
    jdz.sort(hand_cards)
    s = jdz.score(hand_cards)
    if s>40:
        return '加倍'
    else:
        return '不加倍'




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
