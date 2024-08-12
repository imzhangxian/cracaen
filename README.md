# 使用说明
## 环境配置
1. 安装 python
下载并安装python 3.10 以上的版本 (例如 3.12.4)：

https://www.python.org/downloads/

2. (建议) 安装 anaconda

Anaconda 是一个虚拟环境，可以更方便的管理 python 的包，比如安装失败需要执行清理的时候，只需要删除虚拟环境即可。否则可能就需要清理 python 安装并重新安装，就比较麻烦。

下载并安装 miniconda： https://docs.anaconda.com/miniconda/

miniconda 是 Anaconda 的一个轻量级版本，完整安装 Anaconda 非常大，没有必要。

3. (如果安装了 Anaconda ) 创建一个虚拟环境，并激活虚拟环境
```
conda create -n <环境名称>
conda activate <环境名称>
```
环境名称可以自行命名，比如这里可以是 cracaen：
```
conda create -n cracaen
conda activate cracaen
```

创建环境之后，安装一下 pip ：
```
conda install pip
```

如果环境装乱掉了，删除环境重新创建一下就可以了(以 cracaen 为例️)：
```
conda remove --name cracaen --all
conda create -n cracaen
```

查看已有的环境：
```
conda env list
```

** conda 常用的环境管理的命令可参考： https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

4. 安装 Google Chrome 浏览器

Selenium 需要使用 Chrome 浏览器来解析网页和执行 javascript 。其他浏览器的目前的支持度都不好。

5. 安装 scrapy，Selenium，和 scapy-selenium

```
pip install Scrapy
pip install selenium
pip install scrapy-selenium
```

* selenium 依赖的 webdriver-manager 无法自动安装，需要单独手动执行安装：
```
pip install webdriver-mananger
```


## 运行程序

1. 从 github 复制代码库：

复制代码库到一个本地位置，例如 Documents：

```
cd ~/Documents
git clone https://github.com/imzhangxian/cracaen.git
```

2. 安装 scrapy-selenium 补丁：

2.1 首先找到 scrapy-selenium 的安装位置：
```
pip show scrapy-selenium
```

命令返回的信息大概如下所示，找到 Location 后面的路径就是 scrapy-selenium 的安装路径。（！！注意：每个人的安装位置不一样！！）

```
Name: scrapy-selenium
Version: 0.0.7
Summary: Scrapy with selenium
Home-page: https://github.com/clemfromspace/scrapy-selenium
Author: UNKNOWN
Author-email: UNKNOWN
License: UNKNOWN
Location: /Users/<user>/App/miniconda3/envs/<env>/lib/python3.12/site-packages
Requires: scrapy, selenium
Required-by: 
```

2.2 把 Location 后面的路径复制下来，下文中用 \<location> 代替；

然后把补丁文件复制到 scrapy-seleium 的安装目录，命令中的\<location>是之前复制的目录：
```
cd cracaen
cp ssedata/patches/middlewares/middlewares.py <location>/scrapy_selenium/
```

3. 执行爬虫程序

运行如下命令执行爬虫：
```
scrapy crawl sse_scraper -a starts_page=xxx -a ends_page=xxx -O outputs/xxxxx.csv
```

程序中的参数：
starts_page 起始页码，对应上证所信息披露网页（ http://www.sse.com.cn/ipo/disclosure/ ） 上对应的页码，目前一共 1233 页；
ends_page 结束页码，
-O 后面是输出文件位置和名称，

例如：
```
scrapy crawl sse_scraper -a starts_page=1 -a ends_page=20 -O outputs/1-20.csv
```
表示抓取从第1页到第20页的所有招股书链接，输出到outputs目录下 1-20.csv 文件。

输出的格式是 csv 格式，第一列是文件 url，第二列是文件名称，中间以逗号隔开，例如
```
url,name,files
https://static.sse.com.cn/disclosure/listedinfo/announcement/c/new/2024-08-09/603310_20240809_XAT9.pdf,巍华新材首次公开发行股票并在主板上市招股说明书,
https://static.sse.com.cn/disclosure/listedinfo/announcement/c/new/2024-08-01/688721_20240801_5GIW.pdf,龙图光罩首次公开发行股票并在科创板上市招股说明书,
https://static.sse.com.cn/disclosure/listedinfo/announcement/c/new/2024-07-26/603391_20240726_EZF5.pdf,力聚热能首次公开发行股票并在主板上市招股说明书,
https://static.sse.com.cn/disclosure/listedinfo/announcement/c/new/2024-07-02/603285_20240702_BGFM.pdf,键邦股份首次公开发行股票并在主板上市招股说明书,
.........
```

4. 通过链接下载文件

通过之前获得的链接直接无法使用类似 wget 这样的下载工具下载文件，需要通过浏览器才能打开，通过 Selenium 可以调用浏览器下载。

这里写了一个脚本来执行下载程序：

```
python utils/download_file.py url_list.txt
```

输入是一个url列表的文本文件，一行一个 url, 例如：
```
https://static.sse.com.cn/disclosure/listedinfo/announcement/c/new/2024-08-09/603310_20240809_XAT9.pdf
https://static.sse.com.cn/disclosure/listedinfo/announcement/c/new/2024-08-01/688721_20240801_5GIW.pdf
https://static.sse.com.cn/disclosure/listedinfo/announcement/c/new/2024-07-26/603391_20240726_EZF5.pdf
https://static.sse.com.cn/disclosure/listedinfo/announcement/c/new/2024-07-02/603285_20240702_BGFM.pdf
```

4.1 如果发现无法下载文件的情况，可能是 selenium 包和 scrapy-selenium 发生冲突，可以重新创建一个 conda 环境(例如 dl)，只安装 selenium 即可：
```
conda create -n dl
conda activate dl
conda install pip
pip install selenium
python utils/download_file.py url_list.txt
```
