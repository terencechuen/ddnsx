## 0x01 前言  
&emsp;&emsp;作为运维渣渣的我对DDNS有需求，目前使用阿里云的DNS解析服务。但最近发现阿里云的DNS定制版解析套餐已经做出了修改，
价格急剧攀升，同时发现身边好多朋友都需要DDNS服务。在实际的应用场景中我无法要求别人购买昂贵的阿里云DNS解析服务，所以才有
编写适用于绝大部分厂商的DDNS解析脚本。  
&emsp;&emsp;可惜我只是一个渣渣运维，只懂Python的皮毛，写出来的程序能满足需求，至于效率则是另一回事了。  
  
## 0x02 应用场景  
&emsp;&emsp;基本上需要DDNS服务的场景都能使用此程序，但它只能通过Python3执行。你可以在Linux或Windows系统中运行，只需要有
Python3即可。  
&emsp;&emsp;在我的应用场景中还有一种比较特殊的情况。我在家里的服务器中运行着Minecraft服务器，为了让大家能连入我的服务器，
我需要将PPPoE的动态公网地址通过我指定的域名（mc.ngx.hk）进行解析。另外，我还需要将我自用的域名（如：home.ngx.hk）指向这个
动态的IP。  
&emsp;&emsp;为什么要这样做？这个自用的域名只有我自己知道，当在某些情况下停止对外服务的域名的解析时，不会影响我自身的使用。
这是提高安全性的一个操作。  
&emsp;&emsp;也就是说，DDNSx支持将同一个IP解析到多个域名，同时支持不通厂商。比如在某台机器中执行该程序，而配置文件中配置了
DNS服务商为 he.net 的域名 mc1.ngx.hk 与DNS服务商为 gandi.net 的域名 home.enginx.net ，他们将同时指向该机器的公网IP。  
&emsp;&emsp;由于IPv6也在大力推进，所以该程序支持IPv6的AAAA解析类型。另外还支持IPv4的A解析类型与TXT解析类型。  
  
## 0x03 支持的厂商  
&emsp;&emsp;程序目前支持的厂商如下：
* he.net
* gandi.net
* godaddy.net
* dnspod.cn  
  
## 0x04 配置文件  
&emsp;&emsp;因为能力有限，所以程序的逻辑异常复杂，而我选用json为配置文件的编写格式，对于大众来说还是挺麻烦的。所以我编写
了配置文件生成助手，通过简单的交互将大家从编写json的工作中解脱出来，同时也提高了配置文件的正确率。  
&emsp;&emsp;在执行程序之前请执行该命令并跟随交互填写相关信息：``python3 configuration_file_create_assistant.py``  
  
## 0x05 解决依赖问题  
&emsp;&emsp;目前程序需要安装以下依赖包，但目前还没有编写相关检测与安装模块，请根据实际情况手动安装：  
* 全局模块：  
    * requests
* 可选模块：  
    * dnspod.cn（腾讯云）：qcloudapi-sdk-python
    
&emsp;&emsp;全局模块必须全部安装，可通过以下命令进行安装：  
``pip3 install requests``  
&emsp;&emsp;可选模块则根据实际情况选择安装，可通过以下命令进行安装：  
``pip3 install [模块名称]``

## 0x06 执行程序  
&emsp;&emsp;完成配置文件的建立与依赖模块的安装后即可通过以下命令执行程序：  
``python3 main.py``  
&emsp;&emsp;为了实现自动化，你还可以将其加入系统的定时任务中，如Linux的crontab：  
``* * * * * /us/bin/python3 /usr/local/shell/ddnsx/main.py``

## 0x07 结语  
&emsp;&emsp;如果有任何建议或意见，欢迎通过邮件联系我：`contact@ngx.hk`。  
&emsp;&emsp;另外，我也欢迎您加入我的QQ群：`682045871`或造访我的博客：[NGX Proj](https://ngx.hk)  
&emsp;&emsp;因为程序还处于开发完善阶段，难免有BUG，也欢迎大家提issue。与此同时，如果大家有需要增加的DNS服务商，请通过邮件
告知，我会及时回复并加入到程序中。  
