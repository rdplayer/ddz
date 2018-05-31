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
    return ''' 斗地主叫分加倍接口   <br>
    
    /jiaodizhu
    返回1叫地主，0不叫
    /jiabei
    返回1加倍，0不加倍
    
    
    '''




@app.route('/jiaodizhu', methods=['POST', 'GET'])
def jiaodizhu():
    data = request.values.get('data', None)

    if not data:
        abort(400)

    data_arr = data.split(',')
    print(data_arr)
    hand_cards = jdz.anti_replace(data_arr)
    print(hand_cards)
    jdz.sort(hand_cards)
    print(hand_cards)
    s = jdz.score(hand_cards)
    print(s)
    if s>25:
        return '1'
    else:
        return '0'

@app.route('/jiabei', methods=['POST', 'GET'])
def jiabei():
    data = request.values.get('data', None)

    if not data:
        abort(400)

    data_arr = data.split(',')
    hand_cards = jdz.anti_replace(data_arr)
    jdz.sort(hand_cards)
    s = jdz.score(hand_cards)
    if s>40:
        return '1'
    else:
        return '0'




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
