# Perfect-Love
[HEROES LEAGUE 2021]("https://heroes-league.net/") 応募作品

## How to use
### Flaskアプリの作成
#### 1. 作業ディレクトリ作成
```
$ mkdir app-name
$ cd app-name
```

#### 2. 仮想環境作成・有効化
```
$ pip install virtualenv
$ virtualenv env

# MacOS
$ source env/bin/activate
# Windows
$ env\Scripts\activate
```

#### 3.ソースコードのクローン
```git clone https://github.com/rikako1021/Perfect-Love.git```
<hr>

### ライブラリのインストール
``` 
pip install flask flask-sqlalchemy 

# 音声認識に必要なライブラリ
$ pip install pyaudio

# 表情解析に必要なライブラリ
$ pip install cv2
```

<hr>

### APIの利用手続き
#### Speech-to-Text API
* [Google Cloud Platform]("https://console.cloud.google.com/home")にてアカウントを作成
* プロジェクトの作成
* 「APIとサービス」の「ライブラリ」からSpeech to Textを選択し、APIを有効にする
* 認証情報の作成
* サービスアカウントの作成をした後、再度、「APIとサービス」の「認証情報」の画面を開き、作成したサービスアカウントをクリック
* 「キー」と書かれている部分を選択し、「鍵を追加」の画面からjsonファイルを選択すると、jsonファイルがダウンロードされる→これを、作成するプログラムのあるプロジェクト内のディレクトリに入れる
* ```$ pip install –upgrade google-cloud-speech```

#### Microsoft Azure Face API
* [公式サイト]("https://azure.microsoft.com/ja-jp/services/cognitive-services/face/#overview")に入り、Face APIについてのページが表示されるので「無料で始める」を押す
* Azureのアカウントを作成後
* 「すべてのサービス」から```Cognitive Service```と検索し、選択して「追加」をクリック →「Marketplace」のページに移動
* 「Face」と検索し、「作成」をクリック
* 必要情報を入力する画面が表示されますので、適宜必要情報を入力し「作成」をクリック
* 利用準備が終了次第、「リソースに移動」を押し、メニューバーから「キーとエンドポイント」をクリック
(キーはキー１とキー2が表示されるが、キー２は予備なのでキー1とエンドポイントを使用していく)
* コマンドにて、
```$ pip install --upgrade azure-cognitiveservices-vision-face```
を入力し、クライアントライブラリをインストールする必要がある。

#### メタデータ 高精度ネガポジAPI
* [こちら]("http://ap.mextractr.net/ma9/ma9signup")からメタデータ株式会社のAPI利用登録を行います。

利用登録終了後、指定したメールアドレスにてメガデータ株式会社からAPIキーが送られくるため、メールに従ってプログラムを記述することでAPIを活用する環境を構築することができる。
