# -*-coding:utf-8 -*-
from django.views.decorators.http import require_http_methods
from myapp.models import Book
from django.http import JsonResponse
import json
from django.core import serializers
from .index import *
#from .index import save_root
# Create your views here.
import os


@require_http_methods(["POST"])
def upload_file(request):
    response = {}
    response['msg'] = 'success'
    response['error_num'] = 0
    if request.method == "POST":  # 请求方法为POST时，进行处理
        myFile = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            response['error_num'] = 1
            response['msg'] = 'no file'
            return JsonResponse(response)
        else:
            destination = open(os.path.join(save_root, myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
            for chunk in myFile.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()
            data, header = index_file(save_root+ myFile.name)
            response['data'] = data
            response['header'] = header
        return JsonResponse(response)


@require_http_methods(["GET"])
def init_book(request):
    response = {}
    try:
        response['header'] =index_init()
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(["GET"])
def show_books(request):
    response = {}

    try:
        result = search(request.GET.get('search_mode'), request.GET.get('search_input'), request.GET.get('search_header'))
        result = list(result)
        response['list'] = result
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)
