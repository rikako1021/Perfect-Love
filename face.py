import requests  # apiをたたくために必要
import json
import cv2
import os
import math

class Myself:

    # opencvで写真撮る
    def __init__(self) -> None:
        pass

    def cap_face(self, ext='jpg', delay=1, window_name='frame'):
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            return

        # os.makedirs('data/temp', exist_ok=True)
        base_path = os.path.join('static', 'sample')
        n = 0
        while True:
            ret, frame = cap.read()
            # cv2.imshow(window_name, frame)
            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break
            if n == 15:
                cv2.imwrite('{}.{}'.format(
                    base_path, ext), frame)
                break
            n += 1

        # cv2.destroyWindow(window_name)

        with open('./env/faceAPI.json') as j:
            secret_json = json.load(j)
            subscription_key = secret_json['subscription_key']
            face_api_url = secret_json['face_api_url']

        assert subscription_key  # keyがあってるかどうかの判定？

        # img = Image.open('sample.jpg')

        with open('./static/sample.jpg', 'rb') as f:
            binary_img = f.read()

        # apiを使う
        headers = {
            'Content-Type': 'application/octet-stream',  # binaryデータを使うから
            'Ocp-Apim-Subscription-Key': subscription_key}

        params = {
            'returnFaceId': 'true',
            'returnFaceAttributes': 'emotion'
        }

        response = requests.post(face_api_url, params=params,headers=headers, data=binary_img)

        face_data = response.json()
        b = face_data[0]["faceAttributes"]["emotion"]["happiness"] #幸福
        c = face_data[0]["faceAttributes"]["emotion"]["neutral"] #中立
        d = face_data[0]["faceAttributes"]["emotion"]["anger"] #怒り
        e = face_data[0]["faceAttributes"]["emotion"]["contempt"] #軽蔑
        f = face_data[0]["faceAttributes"]["emotion"]["disgust"] #嫌悪感
        g = face_data[0]["faceAttributes"]["emotion"]["fear"] #恐怖
        h = face_data[0]["faceAttributes"]["emotion"]["sadness"] #悲しみ
        
        # 以下にhappinessの値をどう返すか処理を書く
        # happinessとneutralの値を使って重み付けをして点数化したうえで○○点以上を目指そうという形にしてみる！(面白さも含めて完全にブラックボックス化)

        face_result = int((b*0.3 + c*1.0 - d*1 - e*1 - f*1 - g*1 - h*1)*100)
        # --------------------------------------
        print(face_result)
        return face_result

# myself = Myself()
# myself.cap_face()
