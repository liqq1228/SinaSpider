##**博客见: 《[新浪微博爬虫分享（一天可抓取 1300 万条数据）](http://blog.csdn.net/bone_ace/article/details/50903178)》**##
--------

<p>
#**SinaSpider1:**#
###**爬虫功能：**###

 - 此项目和[QQ空间爬虫](http://blog.csdn.net/bone_ace/article/details/50771839)类似，主要爬取新浪微博用户的个人信息、微博信息、粉丝和关注（[详细见此](#Database)）。
 - 代码获取新浪微博Cookie进行登录，可通过多账号登录来防止新浪的反扒（用来登录的账号可从淘宝购买，一块钱七个）。
 - 项目爬的是新浪微博wap站，结构简单，速度应该会比较快，而且反扒没那么强，缺点是信息量会稍微缺少一些（可见[爬虫福利：如何爬wap站](http://blog.csdn.net/bone_ace/article/details/50814101)）。
 - 爬虫抓取微博的速度可以达到 **1300万/天** 以上，具体要视网络情况，我使用的是校园网（广工大学城校区），普通的家庭网络可能才一半的速度，甚至都不到。

<p>
<p>
###**环境、架构：**###
开发语言：Python2.7
开发环境：64位Windows8系统，4G内存，i7-3612QM处理器。
数据库：MongoDB 3.2.0
（Python编辑器：Pycharm 5.0.4；MongoDB管理工具：MongoBooster 1.1.1）

 - 主要使用 scrapy 爬虫框架。
 - 下载中间件会从Cookie池和User-Agent池中随机抽取一个加入到spider中。
 - start_requests 中根据用户ID启动四个Request，同时对个人信息、微博、关注和粉丝进行爬取。
 - 将新爬下来的关注和粉丝ID加入到待爬队列（先去重）。

<p>
<p>
###**使用说明：**###
启动前配置：

 - MongoDB安装好 能启动即可，不需要配置。
 - Python需要安装好scrapy（64位的Python尽量使用64位的依赖模块）
 - 另外用到的python模块还有：pymongo、json、base64、requests。
 - 将你用来登录的微博账号和密码加入到 cookies.py 文件中，里面已经有两个账号作为格式参考了。
 - 另外一些scrapy的设置（如间隔时间、日志级别、Request线程数等）可自行在setting里面调。

<p>
<p>
###**运行截图：**###
![新浪微博爬虫程序](http://img.blog.csdn.net/20160316115233421)

![新浪微博爬虫数据](http://img.blog.csdn.net/20160316115321843)

<div id="Database"></div>

<p>
<p>
###**数据库说明：**###
SinaSpider主要爬取新浪微博的个人信息、微博数据、关注和粉丝。
数据库设置 Information、Tweets、Follows、Fans四张表，此处仅介绍前面两张表的字段。

> 
**Information 表：**
\_id：采用 "用户ID" 作为唯一标识。
Birthday：出生日期。
City：所在城市。
Gender：性别。
Marriage：婚姻状况。
NickName：微博昵称。
Num_Fans：粉丝数量。
Num_Follows：关注数量。
Num_Tweets：已发微博数量。
Province：所在省份。
Signature：个性签名。
URL：微博的个人首页。

<p>
> 
**Tweets 表：**
\_id：采用 "用户ID-微博ID" 的形式作为一条微博的唯一标识。
Co_oridinates：发微博时的定位坐标（经纬度），调用地图API可直接查看具体方位，可识别到在哪一栋楼。
Comment：微博被评论的数量。
Content：微博的内容。
ID：用户ID。
Like：微博被点赞的数量。
PubTime：微博发表时间。
Tools：发微博的工具（手机类型或者平台）
Transfer：微博被转发的数量。
