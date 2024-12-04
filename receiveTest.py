import websocket
import json
import time
import csv
import atexit
from datetime import datetime
import threading
from flask import Flask, jsonify

############################################################
#########################  接收端统计 ########################
############################################################


# 初始化 Flask 应用
app = Flask(__name__)
# 初始化OpenAI配置

# WebSocket客户端实例
ws = None
is_connected = False

# 假设res是一个全局变量
res = []


# 初始化ws连接
def on_open(ws):
    def run(*args):
        global is_connected
        print('已成功连接到WebSocket服务器')
        is_connected = True
        # 发送初始化消息
        init_message = {
            "chatMsg": {
                "senderId": "2222222222222222222",
                "msgType": 0
            },
            "serverNode": {
                "ip": "127.0.0.1",
                "port": 875,
                "onlineCounts": 0
            }
        }
        ws.send(json.dumps(init_message))

    threading.Thread(target=run).start()  # 使用threading.Thread来启动线程


# ... 省略中间代码 ...

def on_close(ws):
    def run(*args):
        global is_connected
        print('WebSocket连接已关闭')
        is_connected = False
        # 5秒后尝试重新连接
        time.sleep(5)
        connect_websocket()

    threading.Thread(target=run).start()  # 使用threading.Thread来启动线程


def on_message(ws, message):
    global res
    try:
        message = json.loads(message)
        # 只处理类型为1的聊天消息
        if (message.get("chatMsg")
                and message["chatMsg"].get("msgType") == 1
                and message["chatMsg"].get("communicationType") == 1):
            # 获取chatMsg.msg，里面是 jmeter的"msg": "${__time(YMDHMS)}",
            # 对比当前时间 ，算出毫秒级的延迟差
            # 输出，并统一记录在一个值键对数组里
            # 获取chatMsg.msg，里面是 jmeter的"msg": "${__time(YMDHMS)}",
            msg = message["chatMsg"].get("msg")

            # 解析msg中的日期时间字符串
            print(f"消息: {msg}")  # 例如：消息: 1733299445602 毫秒戳
            # 解析消息中的毫秒级时间戳
            sent_time_ms = int(msg)

            # 获取当前时间的毫秒级时间戳
            current_time_ms = int(datetime.now().timestamp() * 1000)

            # 计算毫秒级的延迟差
            delay_ms = current_time_ms - sent_time_ms
            res.append([sent_time_ms, current_time_ms, delay_ms])

            # 输出延迟差
            print(f"延迟差: {delay_ms} ms")

            # 用一个新线程，这个线程专门把数值对记录在csv文件里

    except Exception as error:
        print('消息处理错误:', error)


def on_error(ws, error):
    print('WebSocket错误:', error)


def connect_websocket():
    global ws
    ws = websocket.WebSocketApp("ws://127.0.0.1:875/ws",
                                on_open=on_open,
                                on_message=on_message,
                                on_close=on_close,
                                on_error=on_error)
    ws.run_forever()


# 函数用于将所有延迟数据写入CSV文件
def write_to_csv():
    csv_filename = "E:\\PC_Desktop\\AAAAATEST\\时差统计单.csv"

    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["发送时间戳", "当前时间戳", "延迟差(ms)"])
        writer.writerows(res)
    print(f"已将所有延迟数据写入CSV文件：{csv_filename}")

# 方案二
# # 这个函数会无限循环，每65秒调用一次write_to_csv函数
# def periodic_write():
#     while True:
#         time.sleep(85)  # 等待85秒
#         write_to_csv()
#
#
# # 启动周期性写入CSV的线程
# threading.Thread(target=periodic_write, daemon=True).start()


# 启动WebSocket客户端
connect_websocket()
atexit.register( write_to_csv())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


