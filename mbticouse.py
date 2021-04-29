import random
from flask import Flask, render_template, request, jsonify
import json
import math
from haversine import haversine
import pandas as pd
import numpy as np
from math import sin,cos,sqrt,atan2,radians
from scipy.spatial import distance
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/info')
def start():
    return render_template('info.html')

@app.route('/select/<name>')
def select(name):
    return 'hi %s' % name

@app.route('/cgvdaegu')
def cgvdaegu():
    return render_template('cgvdaegu.ipynb')

@app.route('/megabox')
def megabox():
    return render_template('megabox.ipynb')

@app.route('/lottecinema')
def lottecinema():
    return render_template('lottecinema.ipynb')

# @app.route('/course',methods = ['POST'])
# def course():
#     print(request.is_json)
#     request.on_json_loading_failed = on_json_loading_failed_return_dict
#     course = request.get_json()
#     print(course)
#
#
#     return jsonify("AAA")

@app.route('/mbti', methods=['POST'])
def mbti():
    print(request.is_json)
    request.on_json_loading_failed = on_json_loading_failed_return_dict
    mbti = request.get_data().decode('utf-8') #json 데이터를 받아옴
    mbti = mbti.replace('{[','{"mbti" : [').replace('],[','],"hotples" : [')
    # print(mbti)
    # print(type(mbti))
    msg = json.loads(mbti)
    # print(type(msg))
    # print(msg)
    # js = json.dumps(msg)
    # print(type(js),js
    lst = []
    a = []
    x = []
    x1 = []
    y = []
    y1 = []
    xy = []
    x_y = []
    max_x = None
    min_x = None
    max_y = None
    min_y = None
    center_x = None
    center_y = None
    xy0 = []
    xy1 = []
    xy2 = []
    xy3 = []
    hh = []
    ht = []
    ht.append(ht)
    htIndex=[]
    htIndex.append(hh)  # [0] 순서 1번 = 가장먼장소
    for h in random.sample(msg['hotples'],4):
        print(h['htId'],h['htLat'],h['htLng'])
        lst = h['htId'] # htId
        x = h['htLat']  # lat
        y = h['htLng']  # lng
        xy = (h['htLat'],h['htLng'])
        a.append(lst)   # htId 리스트 생성
        x1.append(x)    # lat 리스트 생성
        y1.append(y)    # lng 리스트 생성
        x_y.append(xy)  # lat lng 리스트 생성
    # for num in x1:      # max lat
    #     if(max_x is None or num > max_x):
    #         max_x = num
    # for num in y1:
    #     if(max_y is None or num > max_y):
    #         max_y = num
    max_x = max(x1) # 최대값x
    min_x = min(x1) # 최소값x
    max_y = max(y1) # 최대값y
    min_y = min(y1) # 최소값y
    center_x = (max_x + min_x) /2 # 중심좌표x
    center_y = (max_y + min_y) /2 # 중심좌표y
    print(a)    # htId 4개 출력
    center_xy = [center_x,center_y] # 중심좌표xy
    #print(center_xy)
    xy0 = x1[0],y1[0]
    xy1 = x1[1],y1[1]
    xy2 = x1[2],y1[2]
    xy3 = x1[3],y1[3]
    print(xy0)
    print(xy1)
    print(xy2)
    print(xy3)
    #---------------기준점에서 가장 멀리있는 장소 찾기
    distance0 = math.sqrt( ((center_xy[0]-xy0[0])**2)+((center_xy[1]-xy0[1])**2))   #0번째 핫플 과 중심좌표 거리
    distance1 = math.sqrt( ((center_xy[0]-xy1[0])**2)+((center_xy[1]-xy1[1])**2))   #1번째 핫플 과 중심좌표 거리
    distance2 = math.sqrt( ((center_xy[0]-xy2[0])**2)+((center_xy[1]-xy2[1])**2))   #2번째 핫플 과 중심좌표 거리
    distance3 = math.sqrt( ((center_xy[0]-xy3[0])**2)+((center_xy[1]-xy3[1])**2))   #3번째 핫플 과 중심좌표 거리

    # if (distance0 >= distance1) and (distance0 >= distance2) and (distance0 >= distance3):
    #     print('1번째핫플',distance0)
    #     htIndex[0]= xy0
    # elif(distance1 >= distance0) and (distance1 >= distance2) and (distance1 >= distance3):
    #     print('2번째핫플',distance1)
    #     htIndex[0]= xy1
    # elif(distance2 >= distance0) and (distance2 >= distance1) and (distance2 >= distance3):
    #     print('3번째핫플',distance2)
    #     htIndex[0]= xy2
    # else:
    #     print('4번째핫플',distance3)
    #     htIndex[0]= xy3
    if (distance0 >= distance1) and (distance0 >= distance2) and (distance0 >= distance3):
        print('1번째핫플',distance0)
        htIndex= [xy0]
        #hh = [a[0]]
        if(distance1 >= distance2) and (distance1 >= distance3):
            print('2번째핫플',distance1)
            htIndex+= [xy1]
            #hh += [a[1]]
            if(distance2 >= distance3):
                print('3번째핫플', distance2)
                htIndex += [xy2]
                #hh += [a[2]]
                if(distance3 == distance3):
                    print('4번째핫플',distance3)
                    htIndex += [xy3]
                    #hh += [a[3]]
            elif(distance3 >= distance2):
                print('3번째핫플',distance3)
                htIndex += [xy3]
                #hh += [a[3]]
                if(distance2 == distance2):
                    print('4번째핫플',distance2)
                    htIndex += [xy2]
                    #hh += [a[2]]
        elif (distance2 >= distance1) and (distance2 >= distance3):
            print('2번째핫플', distance2)
            htIndex += [xy2]
            #hh += [a[2]]
            if (distance3 >= distance1):
                print('3번째핫플', distance3)
                htIndex += [xy3]
                #hh += [a[3]]
                if(distance1==distance1):
                    print('4번째핫플',distance1)
                    htIndex += [xy1]
                    #hh += [a[1]]
            elif (distance1 >= distance3):
                print('3번째핫플',distance1)
                htIndex += [xy1]
                #hh += [a[1]]
                if(distance3 == distance3):
                    print('4번째핫플',distance3)
                    htIndex += [xy3]
                    #hh += [a[3]]
        elif (distance3 >= distance1) and (distance3 >= distance2):
            print('2번째핫플', distance3)
            htIndex += [xy3]
            #hh += [a[3]]
            if (distance2 >= distance1):
                print('3번째핫플', distance2)
                htIndex += [xy2]
                #hh += [a[2]]
                if(distance1 == distance1):
                    print('4번째핫플',distance1)
                    htIndex += [xy1]
                    #hh += [a[1]]
            elif (distance1 >= distance2):
                print('3번째핫플', distance1)
                htIndex += [xy1]
                #hh += [a[1]]
                if(distance2 == distance2):
                    print('4번째핫플',distance2)
                    htIndex += [xy2]
                    #hh += [a[2]]
    elif (distance1 >= distance0) and (distance1 >= distance2) and (distance1 >= distance3):
        print('1번째핫플',distance1)
        htIndex = [xy1]
        #hh = [a[1]]
        if(distance0 >= distance2) and (distance0 >= distance3):
            print('2번째핫플',distance0)
            htIndex+= [xy0]
            #hh += [a[0]]
            if (distance3 >= distance2):
                print('3번째핫플', distance3)
                htIndex += [xy3]
                #hh += [a[3]]
                if (distance2 == distance2):
                    print('4번째핫플', distance2)
                    htIndex += [xy2]
                    #hh += [a[2]]
            elif (distance2 >= distance3):
                print('3번째핫플', distance2)
                htIndex += [xy2]
                #hh += [a[2]]
                if(distance3 == distance3):
                    print('4번째핫플',distance3)
                    htIndex += [xy3]
                    #hh += [a[3]]
        elif (distance2 >= distance3) and (distance2 >= distance0):
            print('2번째핫플', distance2)
            htIndex += [xy2]
            #hh += [a[2]]
            if (distance3 >= distance0):
                print('3번째핫플', distance3)
                htIndex += [xy3]
                #hh += [a[3]]
                if (distance0 == distance0):
                    print('4번째핫플', distance0)
                    htIndex += [xy0]
                    #hh += [a[0]]
            elif (distance0 >= distance3):
                print('3번째핫플', distance0)
                htIndex += [xy0]
                #hh += [a[0]]
                if(distance3 == distance3):
                    print('4번째핫플',distance3)
                    htIndex += [xy3]
                    #hh += [a[3]]
        elif (distance3 >= distance0) and (distance3 >= distance2):
            print('2번째핫플', distance3)
            htIndex += [xy3]
            #hh += [a[3]]
            if (distance0 >= distance2):
                print('3번째핫플', distance0)
                htIndex += [xy0]
                #hh += [a[0]]
                if (distance2 == distance2):
                    print('4번째핫플', distance2)
                    htIndex += [xy2]
                    #hh += [a[2]]
            elif (distance2 >= distance0):
                print('3번째핫플', distance2)
                htIndex += [xy2]
                #hh += [a[2]]
                if(distance0 == distance0):
                    print('4번째핫플',distance0)
                    htIndex += [xy0]
                    #hh += [a[0]]
    elif (distance2 >= distance0) and (distance2 >= distance1) and (distance2 >= distance3):
        print('1번째핫플',distance2)
        htIndex= [xy2]
        #hh = [a[2]]
        if(distance0 >= distance1) and (distance0 >= distance3):
            print('2번째핫플',distance0)
            htIndex+= [xy0]
            #hh += [a[0]]
            if (distance1 >= distance3):
                print('3번째핫플', distance1)
                htIndex += [xy1]
                #hh += [a[1]]
                if (distance3 == distance3):
                    print('4번째핫플', distance3)
                    htIndex += [xy3]
                    #hh += [a[3]]
            elif (distance3 >= distance1):
                print('3번째핫플', distance3)
                htIndex += [xy3]
                #hh += [a[3]]
                if(distance1 == distance1):
                    print('4번째핫플',distance1)
                    htIndex += [xy1]
                    #hh += [a[1]]
        elif (distance1 >= distance3) and (distance1 >= distance0):
            print('2번째핫플', distance1)
            htIndex += [xy1]
            #hh += [a[1]]
            if (distance3 >= distance0):
                print('3번째핫플', distance3)
                htIndex += [xy3]
                #hh += [a[3]]
                if (distance0 == distance0):
                    print('4번째핫플', distance0)
                    htIndex += [xy0]
                    #hh += [a[0]]
            elif (distance0 >= distance3):
                print('3번째핫플', distance0)
                htIndex += [xy0]
                #hh += [a[0]]
                if(distance3 == distance3):
                    print('4번째핫플',distance3)
                    htIndex += [xy3]
                    #hh += [a[3]]
        elif (distance3 >= distance0) and (distance3 >= distance1):
            print('2번째핫플', distance3)
            htIndex += [xy3]
            #hh += [a[3]]
            if (distance1 >= distance0):
                print('3번째핫플', distance1)
                htIndex += [xy1]
                #hh += [a[1]]
                if (distance0 == distance0):
                    print('4번째핫플', distance0)
                    htIndex += [xy0]
                    #hh += [a[0]]
            elif (distance0 >= distance1):
                print('3번째핫플', distance0)
                htIndex += [xy0]
                #hh += [a[0]]
                if(distance1 == distance1):
                    print('4번째핫플',distance1)
                    htIndex += [xy1]
                    #hh += [a[1]]
    elif (distance3 >= distance0) and (distance3 >= distance1) and (distance3 >= distance2):
        print('1번째핫플',distance3)
        htIndex= [xy3]
        #hh = [a[3]]
        if(distance0 >= distance2) and (distance0 >= distance1):
            print('2번째핫플',distance0)
            htIndex+= [xy0]
            #hh += [a[0]]
            if (distance1 >= distance2):
                print('3번째핫플', distance1)
                htIndex += [xy1]
                #hh += [a[1]]
                if (distance2 == distance2):
                    print('4번째핫플', distance2)
                    htIndex += [xy2]
                    #hh += [a[2]]
            elif (distance2 >= distance1):
                print('3번째핫플', distance2)
                htIndex += [xy2]
                #hh += [a[2]]
                if(distance1 == distance1):
                    print('4번째핫플',distance1)
                    htIndex += [xy1]
                    #hh += [a[1]]
        elif (distance1 >= distance0) and (distance1 >= distance2):
            print('2번째핫플', distance1)
            htIndex += [xy1]
            #hh += [a[1]]
            if (distance0 >= distance2):
                print('3번째핫플', distance0)
                htIndex += [xy0]
                #hh += [a[0]]
                if (distance2 == distance2):
                    print('4번째핫플', distance2)
                    htIndex += [xy2]
                    #hh += [a[2]]
            elif (distance2 >= distance0):
                print('3번째핫플', distance2)
                htIndex += [xy2]
                #hh += [a[2]]
                if(distance0 == distance0):
                    print('4번째핫플',distance0)
                    htIndex += [xy0]
                    #hh += [a[0]]
        elif (distance2 >= distance0) and (distance2 >= distance1):
            print('2번째핫플', distance2)
            htIndex += [xy2]
            #hh += [a[2]]
            if (distance1 >= distance0):
                print('3번째핫플', distance1)
                htIndex += [xy1]
                #hh += [a[1]]
                if (distance0 == distance0):
                    print('4번째핫플', distance0)
                    htIndex += [xy0]
                    #hh += [a[0]]
            elif (distance0 >= distance1):
                print('3번째핫플', distance0)
                htIndex += [xy0]
                #hh += [a[0]]
                if(distance1 == distance1):
                    print('4번째핫플',distance1)
                    htIndex += [xy1]
                    #hh += [a[1]]
    print(htIndex)
    #print(hh)
    #--------------------기준점에서 가장 멀리있는 장소 찾기 끝

    #------------------------코스 적용 확인
    #     lst = h['htId']
    #     a.append(lst)
    # print(a)
    #--------------------------




    return jsonify("sss") # 받아온 데이터를 다시 전송


def on_json_loading_failed_return_dict(e):
    return {}

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",port=5000)