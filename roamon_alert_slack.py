# encoding: UTF-8

# Copyright (c) 2019-2020 Japan Network Information Center ("JPNIC")
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute and/or sublicense of
# the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import requests
import json
import slackweb
import asyncio

def send_slack(text, url = 'https://slack.com/api/chat.postMessage'):
    # TODO: もっと凝ったメッセージを送る
    # TODO: 送信失敗時のリトライの実装
    async def worker():
        slackweb.Slack(url="https://hooks.slack.com/services/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").notify(text=text)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(worker())
    # try:
    #     loop.run_until_complete(worker())
    # finally:
    #     loop.close()

    # username = "roamon_notify"
    # link_names = 3
    #
    # requests.post(url, data=json.dumps({
    #     'text': text,  # 通知内容
    #     'username': username,  # ユーザー名
    #     'icon_emoji': u':smile_cat:',  # アイコン
    #     'link_names': link_names,  # 名前をリンク化
    # }))


# def send_slack(token, channel, text, username, url = 'https://slack.com/api/chat.postMessage'):
#     # post
#     post_json = {
#         'token': token,
#         'text': text,
#         'channel': channel,
#         'username': username,
#         'link_names': 1
#     }
#     requests.post(URL, data = post_json)
