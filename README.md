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

## 启动项目
```sh
git clone https://github.com/zippermonkey/flightbook.git
cd flightbook
# 修改setting.py 中的数据设置
vim filghtbook/setting.py

# 数据库迁移
python manage.py migrate
# 创建超级用户
python manage.py createsuperuser
# run server
python manage.py runserver
```