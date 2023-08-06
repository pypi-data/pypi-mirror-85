# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src\\plugins'}

packages = \
['haruka_bot']

package_data = \
{'': ['*']}

install_requires = \
['nonebot2[scheduler]>=2.0.0-alpha.4,<3.0.0',
 'psutil>=5.7.3,<6.0.0',
 'pyppeteer>=0.2.2,<0.3.0',
 'qrcode[pil]>=6.1,<7.0']

extras_require = \
{'cli': ['hb-cli>=0.1.0,<0.2.0']}

setup_kwargs = {
    'name': 'haruka-bot',
    'version': '1.0.6',
    'description': 'Push dynamics and live informations from bilibili to QQ. Based on nonebot2.',
    'long_description': '  \n  \n<div align="center">\n  <img src="logo.png" width="200" height="200" alt="logo">\n  \n# HarukaBot\n  \n[![VERSION](https://img.shields.io/github/v/release/SK-415/HarukaBot )](https://github.com/SK-415/HarukaBot/releases/latest)\n[![time tracker](https://wakatime.com/badge/github/SK-415/HarukaBot.svg )](https://wakatime.com/badge/github/SK-415/HarukaBot)\n[![STARS](https://img.shields.io/github/stars/SK-415/HarukaBot )](https://github.com/SK-415/HarukaBot/stargazers)\n[![qq group](https://img.shields.io/badge/QQ%E7%BE%A4-629574472-orange )](https://jq.qq.com/?_wv=1027&k=sHPbCRAd)\n[![LICENSE](https://img.shields.io/github/license/SK-415/HarukaBot )](https://github.com/SK-415/HarukaBot/blob/master/LICENSE)\n  \n**由于学业原因, HarukaBot 将停更一段时间, 等我成绩恢复稳定后会继续更新.**  \n**虽然暂时不更新新功能, 但是在此期间我依然会继续完善文档同时在[QQ群](https://jq.qq.com/?_wv=1027&k=DveS3XKI )答疑.**\n  \n</div>\n  \n##  目录\n  \n  \n- [简介](#简介 )\n- [功能介绍](#功能介绍 )\n- [已知问题](#已知问题 )\n  - [推送延迟](#推送延迟 )\n  - [动态推送失效](#动态推送失效 )\n- [部署指南](#部署指南 )\n  - [部署 go-cqhttp](#部署-go-cqhttp )\n  - [部署 HarukaBot](#部署-harukabot )\n    - [方法一 手动安装 (较为复杂全平台通用)](#方法一-手动安装-较为复杂全平台通用 )\n    - [方法二 插件广场安装 (适用于 `NoneBot2` 用户)](#方法二-插件广场安装-适用于-nonebot2-用户 )\n- [支持作者](#支持作者 )\n  \n##  简介\n  \n  \n一款将哔哩哔哩UP主的直播与动态信息推送至QQ的机器人. 基于 [`NoneBot2`](https://github.com/nonebot/nonebot2 ) 开发, 前身为 [`dd-bot`](https://github.com/SK-415/dd-bot ) .\n  \n项目名称来源于B站 [@白神遥Haruka](https://space.bilibili.com/477332594 )\n  \nlogo 画师: [秦无](https://space.bilibili.com/4668826 )\n  \nHarukaBot 致力于为B站UP主们提供一个开源免费的粉丝群推送方案. 极大的减轻管理员负担, 不会再遇到突击无人推送的尴尬情况. 同时还能将B博动态截图转发至粉丝群, 活跃群内话题.\n  \n> 介于作者技术力低下, HarukaBot 的体验可能并不是很好. 如果使用中有任何意见或者建议都欢迎提出, 我会努力去完善它. \n  \n##  功能介绍\n  \n  \n**以下仅为功能介绍, 并非实际命令名称. 具体命令向 bot 发送 `帮助` 查看, 群里要在所有命令前需加上@**\n  \nHarukaBot 专注于订阅B站UP主们的动态与开播提醒, 并转发至QQ群/好友.\n  \n同时 HarukaBot 针对粉丝群中的推送场景进行了若干优化: \n  \n- **权限开关**: 指定某个群只有管理员才能触发指令\n  \n- **@全体开关**: 指定群里某位订阅的主播开播推送带@全体\n  \n- **动态/直播开关**: 可以自由设置每位主播是否推送直播/动态\n  \n- **订阅列表**: 每个群/好友的订阅都是分开来的\n  \n- **多端推送**: 受限于一个QQ号一天只能@十次全体成员, 因此对于粉丝群多的UP来说一个 bot 的次数完全不够推送. 因此一台 HarukaBot 支持同时连接多个QQ, 分别向不同的群/好友同时推送\n  \n##  已知问题\n  \n  \n###  推送延迟\n  \n  \n受限于B站对API爬取频率限制, 目前 HarukaBot 会将所有UP主排成一列, 每隔十秒检查一位. 因此如果 HarukaBot 订阅了 x 位UP主最高延迟就是 10x 秒.\n  \n> 虽然 HarukaBot 目前的推送延迟对于粉丝群来说是足够了, 但是很显然对于广大dd们来说并不友好, 随便订阅30+个主播延迟就能超过5分钟. \n> 因此, 未来的 HarukaBot v2 版中计划支持绑定B站账号, 将摆脱订阅数量越多推送越慢的窘境.\n  \n###  动态推送失效\n  \n  \n在早晨约两点到八点期间, 部分服务器出现动态获取 api 失效的现象, 具体原因不明, 预计在 v2 中通过登录改善.\n  \n##  部署指南\n  \n  \n**只有同时启动 go-cqhttp 和 HarukaBot 机器人才能正常运行.**\n  \n###  部署 go-cqhttp\n  \n  \n1. 下载 [`go-cqhttp`](https://github.com/Mrs4s/go-cqhttp/releases/latest ) (Windows 用户选择 `windows-amd64.zip` 结尾).\n  \n2. 解压至一个空文件夹后, 双击启动, 此时文件夹内会生成一个 `config.json` 文件, 打开并编辑. \n以下折叠部分为参考 (中文部分记得替换): \n  \n\t</br>\n  \n\t<details>\n\t<summary>config.json 设置参考</summary>\n  \n\t```json\n\t{\n\t\t"uin": 机器人QQ号,\n\t\t"password": "QQ密码",\n\t\t"encrypt_password": false,\n\t\t"password_encrypted": "",\n\t\t"enable_db": true,\n\t\t"access_token": "",\n\t\t"relogin": {\n\t\t\t"enabled": true,\n\t\t\t"relogin_delay": 3,\n\t\t\t"max_relogin_times": 0\n\t\t},\n\t\t"_rate_limit": {\n\t\t\t"enabled": false,\n\t\t\t"frequency": 1,\n\t\t\t"bucket_size": 1\n\t\t},\n\t\t"ignore_invalid_cqcode": false,\n\t\t"force_fragmented": false,\n\t\t"heartbeat_interval": 0,\n\t\t"http_config": {\n\t\t\t"enabled": false,\n\t\t\t"host": "0.0.0.0",\n\t\t\t"port": 5700,\n\t\t\t"timeout": 0,\n\t\t\t"post_urls": {}\n\t\t},\n\t\t"ws_config": {\n\t\t\t"enabled": false,\n\t\t\t"host": "0.0.0.0",\n\t\t\t"port": 6700\n\t\t},\n\t\t"ws_reverse_servers": [\n\t\t\t{\n\t\t\t\t"enabled": true,\n\t\t\t\t"reverse_url": "ws://127.0.0.1:8080/cqhttp/ws",\n\t\t\t\t"reverse_api_url": "",\n\t\t\t\t"reverse_event_url": "",\n\t\t\t\t"reverse_reconnect_interval": 3000\n\t\t\t}\n\t\t],\n\t\t"post_message_format": "string",\n\t\t"debug": false,\n\t\t"log_level": "",\n\t\t"web_ui": {\n\t\t\t"enabled": false,\n\t\t\t"host": "127.0.0.1",\n\t\t\t"web_ui_port": 9999,\n\t\t\t"web_input": false\n\t\t}\n\t}\n\t```\n\t</details>\n  \n</br>\n  \n3. 编辑完重启 `go-cqhttp.exe`, 跟着提示完成安全验证即可\n  \n###  部署 HarukaBot\n  \n  \n####  方法一 手动安装 (较为复杂全平台通用)\n  \n  \n1. 安装 [Python3.7+](https://www.python.org/downloads/release/python-386/ ) (推荐 `3.8.6` 安装的时候一定要[**勾选 "Add Python 3.x to PATH"**](https://www.liaoxuefeng.com/wiki/1016959663602400/1016959856222624 ) )\n  \n2. 克隆 or [下载](https://github.com/SK-415/HarukaBot/releases/latest ) HarukaBot 源码到本地\n  \n3. 在源码根目录打开命令提示符 (对着文件夹内, 按住 shift 同时鼠标右键 -> 在此处打开 Powershell 窗口)\n  \n3. 输入 `pip install -r requirements.txt` 安装依赖\n  \n4. 输入 `python bot.py` 启动 HarukaBot\n  \n> 以后每次启动只需重复 3, 5 两步\n  \n####  方法二 插件广场安装 (适用于 `NoneBot2` 用户)\n  \n  \n- 使用[插件广场](https://v2.nonebot.dev/plugin-store.html )或者 `pip install haruka-bot`, 安装 `HarukaBot`\n  \n- 如果使用 pip 下载的还需要手动在 `bot.py` 中添加 `nonebot.load_plugin("haruka_bot")`\n  \n- (可选) 在 `.env.prod` 或 `.env.dev` 中添加 `HARUKA_DIR="./data/"`, 你也可以将 `./data/` 改成任何其他路径. \n  > 如果不添加, HarukaBot 会将配置文件保存于其安装包位置 (site-packages/haruka_bot) 的 `data` 文件夹中, 之后迁移会很麻烦, 并不推荐.\n  \n- 完成后重启 `NoneBot2` 实例即可使用\n  \n##  支持作者\n  \n  \n点个小星星就是对我最好的支持. 感谢使用 HarukaBot. 也欢迎有能man对本项目pr.\n  ',
    'author': 'SK-415',
    'author_email': '2967923486@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SK-415/HarukaBot',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
