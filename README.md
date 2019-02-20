# DVue

> 使用django+vue超快速搭建单页面web应用

## Build Setup

### 生成前端页面
``` bash
cd frontend
# install dependencies
npm install

# build for production with minification
npm run build

生成的前端页面储存在frontend/dist中，
DVue/settings.py 中加载了该路径，若加载失败可以调整该路径
```
### 启动web应用
```
# 在主目录下
# 安装依赖
pip install -r requirements.txt
# 启动web应用
python manage.py runserver
```


## Edit

### 前端页面编辑
```
直接编辑 frontend/src/components/HelloWorld.vue
其中 frontend/src/components/Global.vue 用于存储全局参数
```
### 后端api编辑
在 myapp/urls.py 中命名api接口 关联函数 
```
urlpatterns = [
url(r'init_book$', views.init_book, ),
url(r'upload_file$', views.upload_file, ),
]

```

在 myapp/views.py 中实现函数
