# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 06:42:56 2022

@author: Corn
"""
# 載入所有需要的函式庫
import cv2                                    
import mediapipe as mp
import random
import json
import numpy as np
from PIL import ImageFont, ImageDraw, Image  
from json.decoder import JSONDecodeError

# 開啟題目json檔
try:
    with open('question.json', encoding='UTF-8') as qj:
        data = json.load(qj)
except JSONDecodeError:
    print("Cannot open question_jsonfile")

# 開啟紀錄最高分數的json檔
try:
    with open('highscore.json', encoding='UTF-8') as hj:
        highscore = json.load(hj)
except JSONDecodeError:
    print("Cannot open highscore_jsonfile")

# 設置基礎變數
result = True
correctAnswer = "none"
youranswer = "none"
rightCount = 0
allCount = 0

# 在螢幕上顯示出題目以及答對或答錯等等畫面
def ShowQuestion(num, rightCount, allCount, correctAnswer, youranswer):
    Right2 = "恭喜你答對了！\n\n你的答對題數為：" + str(rightCount) + \
             "\n\n總答題數為：" + str(allCount) + \
             "\n\n**按任意鍵進入下一題**\n**如要結束答題請在攝影機畫面時按q**"
    Wrong3 = "你答錯囉！\n\n你的答案是："+ str(youranswer) + \
             "\n\n正確答案是：" + str(correctAnswer) + \
             "\n\n你的答對題數為：" + str(rightCount) + \
             "\n\n總答題數為：" + str(allCount) + \
             "\n\n\n\n\n\n\n**按任意鍵進入下一題**\n**如要結束答題請在攝影機畫面時按q**"
    End5 = ""
    comment = ""
    if num == 1:   # 設定封面文字及背景
        src = cv2.imread("cover.JPG")
        src = cv2.resize(src, (1000, 800))

        text = "NCHU-Quiz Rangers!!!"
        text2 = "Ready?GO!!!"
        text3 = "Press any key to start answering the question"

        cv2.putText(src,text,(60, 150), cv2.FONT_HERSHEY_SIMPLEX,2.5,(100, 255, 250),5)
        cv2.putText(src,text2,(330, 680), cv2.FONT_HERSHEY_SIMPLEX,2.0,(255, 255, 255),5)
        cv2.putText(src,text3,(20, 750), cv2.FONT_HERSHEY_SIMPLEX,1.3,(170, 170, 85),5)

        res = np.hstack([src])
        cv2.imshow('NCHU-Quiz Rangers',res)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    elif num == 2:    # 文字設定為答對題目的文字
        text = Right2
    elif num == 3:    # 文字設定為答錯題目的文字
        text = Wrong3
    elif num == 4:    # 文字設定為題目
        text = withdrawq[0][0] + "\n\n" + "(1)" + withdrawq[0][1] + "\n\n" + "(2)" + \
               withdrawq[0][2] + "\n\n" + "(3)" + withdrawq[0][3] + "\n\n" + "(4)" + withdrawq[0][4]
    elif num == 5:    # 文字設定為結算畫面的文字
        if rightCount > highscore["最高答題數為："]:
            highscore["最高答題數為："] = rightCount
            with open("highscore.json",'w',encoding='utf-8') as hj:
                json.dump(highscore, hj, ensure_ascii = False)
        if allCount == 0:
            pass
        elif rightCount/allCount == 1 and allCount == 30:
            comment = "\n\n\n評語：恭喜你全對！獲頒\"中興知識王\"稱號！！！"
        elif rightCount/allCount == 1:
            comment = "\n\n\n評語：恭喜你答的都對！真厲害～"
        elif rightCount/allCount < 0.5:
            comment = "\n\n\n評語：要再加油喔！"
        elif rightCount/allCount == 0.5:
            comment = "\n\n\n評語：還可以但要再努力喔～"
        elif rightCount/allCount > 0.5:
            comment = "\n\n\n評語：不錯喔！可以往全對邁進～"
        
        text = "[結算]\n\n你的答對題數為：" + str(rightCount) + \
               "\n\n總答題數為：" + str(allCount) + comment + \
               "\n\n最高答題數為：" + str(highscore["最高答題數為："])
    # 設定各種畫面(答對答錯等等)
    if num != 1:    
        imgOpenCV = cv2.imread('darkbackground.jpg')  # 把影象從OpenCV格式轉換成PIL格式(為了可以顯示中文)
        imgOpenCV = cv2.resize(imgOpenCV, (1000, 800))
        if (isinstance(imgOpenCV, np.ndarray)):
            imgOpenCV = Image.fromarray(cv2.cvtColor(imgOpenCV, cv2.COLOR_RGB2BGR))
        drawPIL = ImageDraw.Draw(imgOpenCV)
        fontText = ImageFont.truetype("font/simsun.ttc", 40, encoding = "utf-8")

        if num == 4:
            drawPIL.text((75, 100),text,(255, 255, 255),font = fontText)
            imgPutText = cv2.cvtColor(np.asarray(imgOpenCV),cv2.COLOR_RGB2BGR)
        else:
            drawPIL.text((60, 100),text,(255, 255, 255),font = fontText)
            imgPutText = cv2.cvtColor(np.asarray(imgOpenCV),cv2.COLOR_RGB2BGR)
        
        cv2.imshow("NCHU-Quiz Rangers",imgPutText)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
ShowQuestion(1, rightCount, allCount, correctAnswer, youranswer)    # 秀出封面

while(result):    # 進入答題迴圈
    if len(data) == 0:
        break
    withdrawq = random.sample(data, 1)
    data.remove(withdrawq[0])
    
    ShowQuestion(4, rightCount, allCount, correctAnswer, youranswer)    # 秀出題目
    correctAnswer = "(" + str(withdrawq[0][5]) + ")" + withdrawq[0][withdrawq[0][5]]
    mpDraw = mp.solutions.drawing_utils     # 使用mediapipe的繪圖方法
    mpHands = mp.solutions.hands     # 設定使用mediapipe的偵測手掌方法
    mpDrawStyles = mp.solutions.drawing_styles    # 設定mediapipe的繪圖樣式

    VideoCap = cv2.VideoCapture(0)
    
    # 開啟mediapipe偵測手掌
    with mpHands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        if (not VideoCap.isOpened()):
            print("Cannot open camera")
            exit()
        check = False
        while True:
            answer = 0
            if check:    # 判斷食指末端是否已觸碰到選項
                check = False  
                break
            ret, img = VideoCap.read()
            if not ret:
                print("Cannot receive frame")
                break
            img = cv2.resize(img,(1000,800))   # 攝影機相關設定
            size = img.shape   
            width = size[1]
            height = size[0]
            img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(img2)   # 偵測手掌
            if results.multi_hand_landmarks:
                for fingerPoints in results.multi_hand_landmarks:
                    x = fingerPoints.landmark[7].x * width   # 偵測食指末端的x和y座標
                    y = fingerPoints.landmark[7].y * height
                    # 判斷食指末端在1.2.3.4選項的範圍
                    if x>0 and x<120 and y>300 and y<500:
                        check = True
                        answer = 1
                    elif x>400 and x<600 and y>0 and y<120:
                        check = True
                        answer = 2
                    elif x>880 and x<1000 and y>300 and y<500:
                        check = True
                        answer = 3
                    elif x>400 and x<600 and y>680 and y<880:
                        check = True
                        answer = 4
                    youranswer = "(" + str(answer) + ")" + withdrawq[0][answer]
                    if answer == withdrawq[0][5] and answer != 0:    # 答對則實施以下步驟
                        rightCount += 1
                        allCount += 1
                        ShowQuestion(2, rightCount, allCount, correctAnswer, youranswer)    # 秀出答對畫面
                    elif answer != 0:    # 答錯則實施以下步驟
                        allCount += 1
                        ShowQuestion(3, rightCount, allCount, correctAnswer, youranswer)    # 秀出答錯畫面
                    # 將mediapipe繪製的骨架放置在影像中
                    mpDraw.draw_landmarks(img,fingerPoints, mpHands.HAND_CONNECTIONS,
                                              mpDrawStyles.get_default_hand_landmarks_style(),
                                              mpDrawStyles.get_default_hand_connections_style())
    
            cv2.rectangle(img,(0,300),(120,500),(0,0,255),5)       # 1的選項框
            cv2.rectangle(img,(400,0),(600,120),(0,255,0),5)       # 2的選項框
            cv2.rectangle(img,(880,300),(1000,500),(225,255,0),5)  # 3的選項框
            cv2.rectangle(img,(400,680),(600,880),(255,0,0),5)     # 4的選項框
            
            cv2.putText(img, "1", (15,470), cv2.FONT_HERSHEY_SIMPLEX, 5, (0,0,255), 10)     # 1
            cv2.putText(img, "2", (450,110), cv2.FONT_HERSHEY_SIMPLEX, 5, (0,255,0), 10)    # 2
            cv2.putText(img, "3", (900,470), cv2.FONT_HERSHEY_SIMPLEX, 5, (225,255,0), 10)  # 3
            cv2.putText(img, "4", (450,790), cv2.FONT_HERSHEY_SIMPLEX, 5, (255,0,0), 10)    # 4
            cv2.imshow('NCHU-Quiz Rangers', img)
            if cv2.waitKey(5) == ord('q'):    # 偵測鍵盤如果按下'q'鍵即跳出迴圈停止作答
                result = False
                break

ShowQuestion(5, rightCount, allCount, correctAnswer, youranswer)    # 秀出結算畫面

VideoCap.release()
cv2.destroyAllWindows()