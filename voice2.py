import wave
import pyaudio
from google.cloud import speech
import io
import os
import math
import json
import requests

# Imports the Google Cloud client library
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './env/api.json'

class speek_to_text:

    def __init__(self) -> None:
        pass    

    text = ''

    def record(self): #recordメソッド
        RECORD_SECONDS = 5  # 録音する時間の長さ（秒）
        WAVE_OUTPUT_FILENAME = "sample.wav"  # 音声を保存するファイル名
        iDeviceIndex = 0  # 録音デバイスのインデックス番号
        # 基本情報の設定
        FORMAT = pyaudio.paInt16  # 音声のフォーマット
        CHANNELS = 1  # モノラル
        RATE = 44100  # サンプルレート
        CHUNK = 2**11  # データ点数
        audio = pyaudio.PyAudio()  # pyaudio.PyAudio()
        
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        input_device_index=iDeviceIndex,  # 録音デバイスのインデックス番号
                        frames_per_buffer=CHUNK)
                        # --------------録音開始---------------
        print("録音しています。話しかけてください")
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("録音終了しました")
        # --------------録音終了---------------
        stream.stop_stream()  #streamをストップする
        stream.close()  #streamを閉じる
        audio.terminate() #PyAudioインスタンスを破棄する
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')  #録音ファイル（バイナリファイル）（現時点では空）を書き込みモードで開き、waveFileと名付ける
        waveFile.setnchannels(CHANNELS) #waveFileのチャンネル数をCHANNELSに指定
        waveFile.setsampwidth(audio.get_sample_size(FORMAT)) #setsampwidthでサンプルサイズをaudio.get_sample_size（FOMAT）バイトに設定　get_sample_size（FOMAT）は話す声の音圧によって変わる
        waveFile.setframerate(RATE) #waveFileのサンプリングレートをRATEに設定  音質を設定　大きいほどなめらか　
        waveFile.writeframes(b''.join(frames)) #framesに格納されたチャンクをbyte型で結合し（まとめ）、waveFileに書き込む。要するにエンコード⁉
        waveFile.close()  #waveFileを閉じる
    
        lang_code = {
            '英語': 'en-US',
            '日本語': 'ja-JP'
            }
        client = speech.SpeechClient()  # Instantiates a client
        speech_file = "sample.wav"

        with io.open(speech_file, 'rb') as f:
            content = f.read()
        
        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,  # エンコード指定なし
            language_code="ja-JP",
        )
        # Detects speech in the audio file
        response = client.recognize(config=config, audio=audio)
        for result in response.results:
            
            print("認識結果: {}".format(result.alternatives[0].transcript))
            global text
            text = result.alternatives[0].transcript

        return text

    def point(self):
        API_Endpoint = 'http://ap.mextractr.net/ma9/negaposi_analyzer'

        # リクエストヘッダを指定
        headers = {
            "content-type":"application/json"
            }

        # URLパラメータを指定
        params = {
            'apikey':'72D84641718C12C98AE030F7118F7D932DD7A1F0',
            'out':'json',
            'text':text
            }

        # request.getを使いレスポンスオブジェクトとしてresultをたてる
        result=requests.get(API_Endpoint,headers=headers,params=params)
        # json()メソッドを使うとレスポンスの内容を辞書または辞書のリストに変換して取得
        json_data = result.json()
        # negaposi要素(=ネガポジ度合いの数値)をaにいれる
        a = json_data['negaposi']

        # aが0以上だった場合には切り捨て+1、0未満だった場合には全てパラメータを0に変換
        if(a>=0):
            a = math.floor(a)+1
        else:
            a=0

        print(a)

        return a