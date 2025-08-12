# FlangeSheet法兰管件尺寸查询软件
右上角的下载是下载源代码
flangesheet_V0.0.1_Android测试版已更新，地址在这里：
https://gitee.com/upcyoung/flangesheet/releases/download/flangesheet_V0.0.1_Android%E7%89%88/app_flangesheet.apk

桌面版地址在这里：
[点击这里下载桌面版](https://gitee.com/upcyoung/flangesheet/releases/download/flangesheet_V1.00/FlangeSheet_V1.00.zip)
下载后解压，找到并点击文件夹中的flangesheet.exe文件即可使用。
pyinstaller打包的exe程序，有些杀毒软件会报毒，可放心添加到信任白名单。

#### 介绍
FlangeSheet是一款法兰管件尺寸图形化显示的查询软件。
FlangeSheet V1.00当前纳入的法兰及管道壁厚标准有：
1. 管道法兰
   - HG/T20592钢制管法兰PN系列（公制）
   - HG/T钢制管法兰20615Class系列（英制）
   - 大直径钢制管法兰HG/T20613Class系列（英制）
2. 压力容器法兰
   - 长颈对焊法兰NB/T47023Class系列
3. 管道壁厚标准
   - HG20533（Ia系列）
   - GB12459 & GB/T13401
   - ANSI B36.10M & B36.19M（A）
   - HGJ514无缝管（标准已被替代，尺寸可供选择参考）
   - HGJ528有缝管（标准已被替代，尺寸可供选择参考）
#### 软件架构
本软件编程语言为python3，界面制作使用PyQt5。各种尺寸数据放置于Data文件夹下。
使用python的pandas包来读取及选择明细数据。

#### 安装使用说明
1. 如果仅是想使用该软件的桌面版本，可下载发行版<https://gitee.com/upcyoung/flangesheet/releases/tag/flangesheet_V1.00>，解压，找到并点击文件夹中的flangesheet.exe文件即可使用。
2. 如果您想改动这个软件或者参与这个软件的进一步制作，可使用git来下载整个源代码。（注意您的python需安装软件中用到的库，你可以在源码的import中查看用到了哪些库）
3. 如果软件打不开,windows提示未知作者等，按如下操作：
   * 右键点击应用程序的可执行文件，选择“属性”。 
   * 在“常规”选项卡中，找到“安全”部分并点击“解除锁定”。 
   * 点击“应用”和“确定”按钮。 
   * 再次尝试运行应用程序，如果仍然无法打开，请在弹出的警告窗口中选择“仍要运行”。

#### 参与贡献

1. 作者：杨建（upcyoung）
2. 您可以关注我的公众号：flangesheet
![输入图片说明](img/qrcode_flangesheet_2.jpg)
3. 您可以访问我的网站<http://www.flangesheet.com>并给我留言
4. 作者邮箱：upcyoung@foxmail.com

#### 其他说明
作者是一个机械专业工程师，基于工作中的一些不便，学习编程并制作了这个软件。
这样的软件确实既需要机械专业知识，又需要一定的编程能力。
作者水平有限，编程也仅学习了一点皮毛。
我想，把这个软件开源出来，让更多的专业工程师加入，方能为更多的人提供方便。
如蒙贡献您的力量，谢谢您的支持！本软件遵循GPL3.0开源协议
