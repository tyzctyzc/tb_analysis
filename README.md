## 项目依赖
* python 2.7.12
* Django
* django-crontab
* scrapy   
* requests
* pymysql
* pandas
* numpy
* matplotlib
* wordcloud
* Markdown2
* chardet
* redis
* redis 数据库
* mysql 数据库


安装命令：

```
$ pip install Django django-crontab Scrapy requests pymysql pandas numpy wordcloud Markdown2 redis chardet
```
安装 matplotlib 请参考：[matplotlib github](https://github.com/ehmatthes/pcc/blob/master/chapter_15/README.md#installing-matplotlib)

## 克隆使用
将项目克隆到本地

```
$ git clone https://github.com/tyzctyzc/tb_analysis.git
```

进入工程目录

```
$ cd tb_analysis
```
进入mysql命令界面

```
$ mysql -u root -p 
```

创建 Django 使用的数据库

```
$ create database tb_analysis default character set utf8;
```

修改 Django 配置

```
$ vim tb_analysis/settings.py
----------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tb_analysis',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '',
        'PORT': '',
    }
}
```

修改配置文件中连接数据库配置

```
$ vim config.py
----------
# local
database_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'charset': 'utf8',
}
```

修改 redis 的连接用户名和密码

```
$ vim config.py
----------
redis_pass = ''
redis_host = 'localhost'
redis_part = '6379'
redis_db = 10
```

部分设置参数说明：

| param | Description | 默认值 |
| ----| ---- | ---- |
| is_distributed | 是否分布式抓取 | False |
| is_proxy | 是否使用代理 | False |
| proxy_address | 代理地址 | <http://127.0.0.1:8000/>|
| email_type | 使用哪个邮箱发送邮件 | gmail |
| self_email | 邮箱地址 | 填写自己的邮箱地址 |
| self_password | 邮箱密码 | 填写自己的邮箱密码 |


生成 Django 数据库

```
$ python manage.py makemigrations
$ python manage.py migrate
```

运行 Django 服务器

```
$ python manage.py runserver
```

在浏览器中访问 <http://127.0.0.1:8000/tb/> 进行测试

