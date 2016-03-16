# treesmth
为水木社区增加树状视图和用户黑名单。

## 使用方法

### 依赖
* Python 2.x
* BeautifulSoup4

### 运行
1. 编辑src/blacklist.txt，加入你想屏蔽的id
2. cd src; python main.py <端口号>
3. 用浏览器打开http://localhost:<端口号>

## 功能规划
### 黑名单
* 隐藏指定id的发帖
* 隐藏回指定id的帖
* id黑名单编辑页面

### 树状视图
参考reddit

### 其它
* 浏览器通知

## 实现规划
1. m.newsmth.net的单机代理。
2. 黑名单：同主题模式/普通模式的信息抽取和html in-place修改。
3. 树状视图：从上一步抽取的信息直接render html。
