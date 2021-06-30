## 华中科技大学数据库实验

## 环境

- python3
- django 3.24
- django-filter
- django-mathfilters

## 环境配置

```sh
# create env
conda create -n django-env
conda activate django-env
# install packages
conda install django
pip install django-filter django-mathfilters
```
## MySql 设置

本项目的setting.py中使用MySQL作为数据库，需要修改为自己的数据库的连接信息，同时在MySql数据库中新建一个名为`login`的数据库
```sql
create database login;
```
## 启动项目
```sh
git clone https://github.com/zippermonkey/flightbook.git
cd flightbook
# 修改setting.py 中的数据设置
vim filghtbook/setting.py
# 如果使用mysql 请新建名为login的数据库
# 如果使用sqlite 修改setting.py为sqlite

# 数据库迁移
python manage.py migrate
# 创建超级用户
python manage.py createsuperuser
# run server
python manage.py runserver
```