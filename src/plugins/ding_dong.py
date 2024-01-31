from wechaty import WechatyPlugin, Message
from quart import Quart, render_template_string
from wechaty_plugin_contrib.message_controller import message_controller
from wechaty import WechatyPlugin
import requests
import json

class DingDongPlugin(WechatyPlugin):
    VIEW_URL = '/api/plugins/ding_dong/view'

    @message_controller.may_disable_message
    async def on_message(self, msg: Message) -> None:
        text = msg.text()
        if text == "ding":
            await msg.say("dong")
            
        # use your own IP !!!
        url = 'http://127.0.0.1:9527/api'
        data = {
            'query': text
        }
        data_json = json.dumps(data)
        headers = {
            'Content-Type': 'application/json'
        }

        # 发起 POST 请求
        response = requests.post(url, data=data_json, headers=headers, timeout=200)
        response_text = json.loads(response.text)
        reply_value = response_text.get("reply", "")
        if reply_value:
            await msg.say(reply_value)

        message_controller.disable_all_plugins(msg)

    async def blueprint(self, app: Quart) -> None:
        
        @app.route('/api/plugins/ding_dong/view')
        async def get_ding_dong_view():
            
            # with open("./src/plugins/views/table.jinja2", 'r', encoding='utf-8') as f:
            with open("./src/plugins/views/vue.html", 'r', encoding='utf-8') as f:
                template = f.read()

            data = [i for i in range(20)]
            response = await render_template_string(template, tables=data)
            return response
