# 1.遗留问题
## `redis.exceptions.ConnectionError: Connection closed by server.`
https://github.com/andymccurdy/redis-py/issues/1140

使用`try... except redis.exceptions.ConnectionError:`的方法规避了此问题

    FYI
    - 在本项目下，使用`py37`没有出现此问题
    - 在本项目下，使用`python`没有出现此问题
    - 在`FairMOT`下出现此问题，初步怀疑是`timeout`问题

# 2.依赖
本工具依赖redis服务请先安装redis-server
```
apt install redis-server
```

为Python安装依赖
```
pip3.7 install opencv-python numpy pyyaml hiredis redis
pip2.7 install opencv-python numpy pyyaml hiredis redis
```

- 补充说明

`setup.py` 文件本身指明了相关依赖，但是由于公司网络原因，可能会出现无法正常下载安装的情况，建议在安装之前手动完成依赖包的安装。

# 3.作为程序部署
step1. 在`~`路径下新建路径`robot\configs`，注意：请勿使用其他路径

step2. 将项目目录下的配置文件`config\pubsub.yaml`拷贝到`~\robot\configs`路径下，注意：请勿修改文件名称

step3. 按实际情况修改`~\robot\configs\pubsub.yaml`文件
```
# camera data pub & sub config
mono:
  type: "pub"
  source: "0"
  host: "172.172.0.10"
  port: "6379"
  db: 3
  name: "robot_mono"
  topic: "robot_mono"

# bbox from FairMOT pub & sub config
track:
  type: "pub"
  source: "0"
  host: "172.172.0.11"
  port: "6379"
  db: 3
  name: "robot_track"
  topic: "robot_track"
```

参数说明：
```
mono: 指定为单目相机，该名称请勿修改
  type: 发布消息，请勿修改
  source: camera device id, 通过 ls /dev/video* 配合 v4l2-ctl -d  /dev/video0 --all查看
  host: 消息发布ip，对应部署了pubsub程序的服务器的IP地址
  port: 消息发布端口，对应部署了pubsub程序的服务器的Redis服务的端口
  db: 不需改动
  name: 消息发布服务的名称
  topic: 消息发布话题的名称

track: 指定为跟踪算法，该名称请勿修改
  type: 发布消息，请勿修改
  source: 请勿修改
  host: 消息发布ip，对应部署了tracking算法的服务器的IP地址
  port: 消息发布端口，对应部署了tracking算法的服务器的Redis服务的端口
  db: 不需改动
  name: 消息发布服务的名称
  topic: 消息发布话题的名称
```

step5. 在`~/.bashrc`中声明`configs`地址
- 在`~/.bashrc`的末尾加入以下内容
```
export ROBOT_CONFIGS=$(dirname ~/.)'/robot/configs'
```
- 请务必注意将配置文件放在上述指定文件夹下

## 3.1 开机自启动[未测试]
在`/etc/rc.local`脚本中增加了开机自启动代码，代码如下
```
export PUBLISHERPATH=$(dirname ~/.)'/robot/pubsub'
source $(dirname $(which conda))/activate pubsub
cd $PUBLISHERPATH
python app.py
```
第一段申明了MONOPUB的路径

第二段进入到该路径

第三段在后台启动脚本`publish.sh` 并输出日志到`pub.log`

第三段回到`home`

可使用`ps -ef | grep python`查看

# 4. 作为模块使用

分别在python2.7和python3.7版本下进行测试。

```
pip install aa-pubsub
```

请注意：
- 模块和程序使用同样的配置文件！！！

# 5. 性能

目前`Publisher`端读取摄像头数据到`Subscriber`端得到数据拥有约`100ms`的延时。

![1](images/1.jpg)
![2](images/2.jpg)

# 6. 测试用例

```
python test.py
```

# 7. 提交pip

- 安装提交需要的工具
```
pip install twine
```
- 更新`version.py`的版本号
- 提交
```
python setup.py sdist
twine upload dist/*
```