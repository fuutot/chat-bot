import os
from slack_bolt import App

from generate import generate_text
#import logging

# ボットトークンと署名シークレットを使ってアプリを初期化します
# SLACK_BOT_TOKENはBot User OAuth Tokenを環境変数に登録したものを参照しています
# SLACK_SIGNING_SECRETはSigning Secretを環境変数に登録したものを参照しています
app = App(token=os.environ.get('SLACK_BOT_TOKEN'),
          signing_secret=os.environ.get('SLACK_SIGNING_SECRET'),
          process_before_response=True)

# chatbotにメンションが付けられたときのハンドラ
@app.event("app_mention")
def handle_mention(event, say):
    #logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s:%(name)s - %(message)s")

    #logging.debug("debug")
    res = str(generate_text(event["text"]))
    for i in range(1, 4):
        if res[i].isascii():
            if i == 3:
                res = "参考となる情報を見つけられません"
        else:
            break
    say(res)



#アプリを起動します（デフォルトポートは3000です）
if __name__ == "__main__":
    app.start()