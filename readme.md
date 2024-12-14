# QUST WLAN LOGIN HELPER

Headless QUST Campus Web Service Client.

青岛科技大学校园网登录客户端，用于登录校园网。 （如果有一天你的服务器没有用户界面不能装浏览器，你可以用这个客户端登录校园网。）

很久不用了不知道还好不好用。。。

## 使用方法
```python
python LanHelper.py -u 1234567890 -p password123
```

## 全部参数

| 选项              | 描述                |
|-----------------|-------------------|
| -o              | 登出                |
| --local         | 仅使用校园网而不是互联网      |
| --url           | 使用自定义网址代替默认网址     |
| -u 或 --userid   | 用户 ID（手机号还是学号来着?） |
| -p 或 --password | 密码                |
| -v 或 --verbose  | 详细模式（输出调试信息）      |

