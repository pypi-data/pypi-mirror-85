#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: QQHong

"""
一些较为零散的常用函数组成的工具模块
"""

import os
import io
import re
import hmac
import json
import time
import bson
import random
import base64
import socket
import shutil
import urllib3
import hashlib
import zipfile
import requests
import threading
import subprocess
import multiprocessing
from urllib import parse
from bson import json_util
from wsgiref.simple_server import make_server

import exrex
import pymongo
from PIL import Image
from PIL import ImageChops
from Crypto.Cipher import AES
from selenium import webdriver


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_headers(is_random=None, headers=None):
    """
    获取HTTP的请求头
    :param is_random: 请求头的值是否随机
    :param headers: 指定的headers字段s
    :return:
    """
    default_headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    }

    if is_random:
        resource = os.path.join(os.path.dirname(__file__), "./resource/headers")
        for header in ["User-Agent"]:
            default_headers[header] = random.choice(open(os.path.join(resource, header)).readlines()).strip()

    if headers:
        default_headers.update(headers)

    return default_headers


def get_paths(path, recursive=False):
    """
    获取文件夹下的所有文件的路径
    :param path: 文件夹的路径
    :param recursive: 是否递归该文件夹
    :return: 所有文件路径组成的列表
    """
    paths = []
    if os.path.isdir(path):
        if recursive:
            for root, dirs, filenames in os.walk(path):
                for filename in filenames:
                    paths.append(os.path.join(root, filename))
        else:
            for filename in os.listdir(path):
                paths.append(os.path.join(path, filename))
    else:
        paths.append(path)
    return paths


def get_file_hashs(path, hash_algorithms=None):
    """
    获取文件的hash值
    :param path: 文件路径
    :param hash_algorithms: 需要的哈希算法所组成的列表，例如：["md5"]
    :return: hash 字段及值组成的字典
    """
    if hash_algorithms is None:
        hash_algorithms = ["md5", "sha1", "sha256"]

    hash_values = dict()
    for hash_algorithm in hash_algorithms:
        hash_values[hash_algorithm] = getattr(hashlib, hash_algorithm)()

    with open(path, "rb") as file:
        while True:
            content = file.read(1048576)
            if not content:
                break
            for hash_value in hash_values.values():
                hash_value.update(content)

    for hash_algorithm in hash_values.keys():
        hash_values[hash_algorithm] = hash_values[hash_algorithm].hexdigest()

    return hash_values


def file_split(path, size=1024*1024*1024):
    """
    对文件(通常为大文件)进行分割
    :param path: 文件路径
    :param size: 分割后每一份文件的大小，单位为byte
    :return:
    """
    with open(path, "rb") as src:
        index = 0
        if size > 1024*104*1024:
            src.read(size)
        content = src.read(size)
        while content != b"":
            open(path + "." + str(index), "wb").write(content)
            index += 1
            content = src.read(size)


def file_merge(path):
    """
    对文件进行合并
    :param path: 文件路径
    :return:
    """
    with open(path, "wb") as f:
        index = 0
        src = path + "." + str(index)
        while os.path.exists(src):
            content = open(path + "." + str(index), "rb").read()
            f.write(content)
            index += 1
            src = path + "." + str(index)


def deduplicate_list(old_list, sort=False):
    """
    对列表去重
    :param old_list: 原有列表
    :param sort: 是否保持原有排序
    :return: 去重后的新列表
    """
    new_list = list(set(old_list))
    if sort:
        new_list.sort(key=old_list.index)
    return new_list


def duplicate_file_lines(old_file_path, new_file_path, sort=False):
    """
    对文件内容按行进行去重
    :param old_file_path: 需去重的文件路径
    :param new_file_path: 去重后文件的保存路径
    :param sort: 是否需要保持原有排序，默认不保存
    :return:
    """
    lines = [line for line in open(old_file_path, encoding="utf-8").readlines()]
    lines = deduplicate_list(lines, sort)
    open(new_file_path, "w", encoding="utf-8").write("".join(lines))


def deduplicate_json(o):
    """
    对json类型数据的最底层的组合类型（list、tuple）数据进行去重，用于dict、list、tuple、set的多重嵌套的结构中
    :param o:
    :return:
    """
    if type(o) == dict:
        oo = {}
        for key in o:
            oo[key] = deduplicate_json(o[key])
        return oo
    elif type(o) in [set, tuple, list]:
        types = [type(i) for i in o]
        if dict in types or list in types or set in types or tuple in types:
            oo = list()
            for item in o:
                oo.append(deduplicate_json(item))
            return type(o)(oo)
        else:
            return sorted(type(o)(set(o)))
    else:
        return o


def start_http_sever_by_wsgi(port=80, root_dir="."):
    """
    WSGI构建的简要的文件下载服务器(不考虑性能|安全等问题，仅供自身使用，切勿对外提供服务)
    :param port: 端口
    :param root_dir: 根目录
    :return:
    """
    # 列目录时展示的文件夹、文件的图标及默认返回的响应体(定义编码方式)
    folder_img = "data:image/gif;base64,R0lGODlhEAAQALMAAJF7Cf8A//zOLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
                 "AAAAAAACH5BAEAAAEALAAAAAAQABAAAAQqMMhJqwQ42wmE/8AWdB+YaWSZqmdWsm9syjJGx/YN6zPv5T4gr0UkikQRADs="
    file_img = "data:image/gif;base64,R0lGODlhEAAQALMAAAAAAIAAAACAAICAAAAAgIAAgACAgMDAwICAgP8AAAD/AP//AAAA//8A/wD" \
               "//////yH5BAEAAA0ALAAAAAAQABAAAAQwsDVEq5V4vs03zVrHIQ+SkaJXYWg6sm5nSm08h3EJ5zrN9zjbLneruYo/JK9oaa4iADs="
    default_body = '<meta charset="UTF-8">'
    # 每次请求所调用的函数

    def application(environ, start_response):
        # Wsgi会对值进行latin1解码，导致中文异常，故此先用latin1编码再用utf-8进行解密
        requests_path = environ['PATH_INFO'].encode("latin1").decode("utf-8")
        local_path = os.path.join(root_dir + requests_path)
        headers = {
            "Content-Type": "text/html"
        }
        if os.path.exists(local_path):
            # 文件直接提供下载
            if os.path.isfile(local_path):
                body = open(local_path, "rb").read()
                headers.update({
                    "Content-Type": "application/octet-stream",
                    "Content-Length": str(len(body))
                })
                start_response('200 OK', list(headers.items()))
            # 文件夹则列出目录
            elif os.path.isdir(local_path):
                start_response('200 OK', list(headers.items()))
                body = default_body + '<style>a {text-decoration: none}</style>'
                dirs, files, show = '', '', '<img src="{}"> <a href="{}">{}<a><br/>'
                for each in os.listdir(local_path):
                    one = os.path.join(local_path, each)
                    if os.path.isdir(one):
                        dirs += show.format(folder_img, os.path.join(requests_path, each), each)
                    else:
                        files += show.format(file_img, os.path.join(requests_path, each), each)
                body += dirs + files
            else:
                start_response('500 Internal Server Error', list(headers.items()))
                body = default_body + "未知错误"
        else:
            start_response('404 Not Found', list(headers.items()))
            body = default_body + "页面不存在"
        if type(body) != bytes:
            body = body.encode("utf-8")
        return [body]
    # 启动WSGI文件服务器
    httpd = make_server('0.0.0.0', port, application)
    httpd.serve_forever()


def request_by_socket(url):
    """
    socket构造的HTTP 协议的GET请求，可在某些特殊场景下使用
    :param url: 需请求的URL
    :return: 响应头, 响应体
    """
    url = parse.urlparse(url)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 80 if url.port is None else url.port
    send_content = "GET " + url.path + "HTTP/1.1\r\nConnection: close\r\n\r\n"
    send_content = send_content.encode()
    client.connect((url.hostname, port))
    client.send(send_content)
    recv_data = b""
    while True:
        content = client.recv(1024)
        if not content:
            break
        recv_data += content
    response_header, response_body = recv_data.split(b"\r\n\r\n", 1)
    return response_header, response_body


def export_mongodb_data_to_json_file(host, port, database_name, collection_name,
                                     filter_condition=None, save_mode="all", save_dir="./"):
    """
    导出mongodb的数据到json文件中
    :param host: 网络地址
    :param port: 端口
    :param database_name: 数据库名
    :param collection_name: 集合名
    :param filter_condition: 数据过滤条件
    :param save_mode: 数据保存方式，all/one，all将所有数据保存至一个json文件，one将每一份数据单独保存至一个json文件
    :param save_dir: json文件保存的路径，文件名函数自生成
    :return:
    """
    client = pymongo.MongoClient(host, port)
    collection = client[database_name][collection_name].with_options(
        codec_options=bson.CodecOptions(unicode_decode_error_handler="ignore"))
    if not filter_condition:
        filter_condition = {}
    documents = collection.find(filter_condition)
    if save_mode == "all":
        data = [document for document in documents]
        save_path = os.path.join(save_dir, collection_name + ".json")
        open(save_path, "w", encoding="utf-8").write(json_util.dumps(data, indent=4, ensure_ascii=False))
    elif save_mode == "one":
        for document in documents:
            save_path = os.path.join(save_dir, str(document["_id"]) + ".json")
            try:
                open(save_path, "w", encoding="utf-8").write(
                    json_util.dumps(document, indent=4, ensure_ascii=False))
            except Exception as e:
                print("{}: {}".format(document["_id"], repr(e)))


def multiple_decompress(path):
    """
    对文件夹（含子文件夹）下的所有压缩文件或某个单独的压缩文件进行递归形式的解压缩，实现对多重压缩包的解压
    :param path: 文件夹或文件路径
    :return:
    """
    if os.path.isdir(path):
        compressed_files = get_paths(path, recursive=True)
    else:
        compressed_files = [path]
    for compressed_file in compressed_files:
        target_dir = os.path.splitext(compressed_file)[0]
        command = "7z x -r -aos {} -o{}".format(compressed_file, target_dir)
        pi = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        for i in iter(pi.stdout.readline, b""):
            print(i.decode("GBK"), end="")
        if os.path.exists(target_dir) and os.path.isdir(target_dir):
            multiple_decompress(target_dir)


class Proxy:
    def __init__(self, data5u_order=None):
        self.proxy_pool = []
        self.data5u_order = data5u_order
        threading.Thread(target=self.add_proxies).start()
        threading.Thread(target=self.verify_proxies).start()

    def get_proxies(self):
        return self.proxy_pool[-1]

    def add_proxies(self):
        while True:
            if self.data5u_order:
                while True:
                    try:
                        self.proxy_pool.append(self.get_proxies_by_data5u(self.data5u_order))
                    except Exception as e:
                        print(repr(e))
                    time.sleep(1)

    def verify_proxies(self):
        while True:
            self.proxy_pool = self.proxy_pool[-10:]
            time.sleep(1)

    @staticmethod
    def get_proxies_by_data5u(order, is_random=1):
        """
        通过无忧代理（http://www.data5u.com/）API接口获取代理
        :param order: IP提取码
        :param is_random: 结果定制，默认优先返回速度快的IP
        :return:
        """
        url = "http://api.ip.data5u.com/dynamic/get.html?order={}&ttl=1&json=1&random={}&sep=3".format(order, is_random)
        proxies = dict()
        response = requests.get(url, timeout=(10, 10))
        if response.status_code != 200:
            raise Exception("data5u exception, status code: {}, response: {}".format(response.status_code, response.text))
        response = json.loads(response.text)
        if response["success"]:
            proxy = "http://{}:{}".format(response["data"][0]["ip"], response["data"][0]["port"])
            proxies["http"] = proxy
            proxies["https"] = proxy
            return proxies
        else:
            raise Exception("data5u exception, status code: 200, response: {}".format(response["msg"]))


def start_web_server(protocol="http", host="0.0.0.0", port=None, cert="./resource/cert.crt",
                     private_key="./resource/private.key"):
    """
    启动一个web服务器
    :param protocol: 服务器的协议类型，默认为http
    :param host: 监听地址
    :param port: 监听端口，http默认80端口，https默认443端口
    :param cert: SSL证书文件路径，如果类型类型为https，此项有效，已内置默认证书
    :param private_key: 证书的私钥文件路径，如果类型类型为https，此项有效，已内置默认私钥
    :return:
    """
    from flask import Flask
    app = Flask(__name__)

    @app.errorhandler(404)
    def page_not_found(e):
        return "Hello World"

    if not port:
        port = 443 if protocol == "https" else 80

    if protocol == "http":
        app.run(host=host, port=port, threaded=True)
    elif protocol == "https":
        os.chdir(os.path.dirname(__file__))
        app.run(host=host, port=port, ssl_context=(cert, private_key), processes=True)
    else:
        raise Exception("{}: 本函数不支持该协议".format(protocol))


def start_https_server(host="0.0.0.0", port=443, cert="./resource/cert.crt", private_key="./resource/private.key",
                       handler="SimpleHTTPRequestHandler"):
    """
    启动一个https服务器
    PS：在shell中运行该函数，按下两次 Ctrl+C 才能结束，IDLE 中需 restart shell
    :param host: 监听地址
    :param port: 监听端口
    :param cert: SSL证书文件路径
    :param private_key: 私钥文件路径
    :param handler: 如何响应，默认使用SimpleHTTPRequestHandler进行响应，如果不是，则对任意路径都响应"hello, world"
    :return:
    """
    import ssl
    from http import server

    if handler == "SimpleHTTPRequestHandler":
        https_server = server.HTTPServer((host, port), server.SimpleHTTPRequestHandler)
    else:
        """
        响应任意路径
        """
        class ResponseAnyPathHttpServer(server.BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200, message='OK')
                self.end_headers()
                self.wfile.write("hello, world".encode())
        https_server = server.HTTPServer((host, port), ResponseAnyPathHttpServer)
    os.chdir(os.path.dirname(__file__))
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(cert, private_key)
    https_server.socket = context.wrap_socket(https_server.socket, server_side=True)
    https_server.serve_forever()


def get_subs(src, limit_deep=None, current_deep=1):
    """
    递归获取所有子项
    :param src:
    :param limit_deep: 最大递归深度
    :param current_deep: 当前递归深度
    :return:
    """
    results = []
    if type(src) in [list, set, dict] and (not limit_deep or (limit_deep and current_deep <= limit_deep)):
        if type(src) == dict:
            src = list(src.values())
        for sub in src:
            results.extend(get_subs(sub, limit_deep=limit_deep, current_deep=current_deep+1))
    else:
        results.append(src)
    return results


def normalize(path, format_="json"):
    """
    将文件中的内容的格式进行标准化
    :param path: 文件路径
    :param format_: 文件格式，如json、javascript等
    :return:
    """
    if format_ == "json":
        content = open(path, "r", encoding="utf-8")
        content = json.load(content)
        content = json.dumps(content, indent=4, ensure_ascii=False)
        open(path, "w", encoding="utf-8").write(content)
    elif format_ == "javascript":
        pass
    else:
        raise Exception("{} format error".format(path))


def base64urlencode(plaintext):
    if type(plaintext) is not bytes:
        plaintext = plaintext.encode("utf-8")
    return base64.b64encode(plaintext).strip(b"=").replace(b'+', b'-').replace(b'/', b'_')


def base64urldecode(ciphertext):
    if type(ciphertext) is not bytes:
        ciphertext = ciphertext.encode("utf-8")
    plaintext = ciphertext.replace(b'-', b'+').replace(b'_', b'/')
    plaintext = plaintext + b'=' * ((4 - (len(plaintext) % 4)) % 4)
    return base64.b64decode(plaintext)


class JWT:
    def __init__(self):
        self.typ = "JWT"
        self.alg = "HS256"

    @staticmethod
    def decode(message):
        message = message.split(".")
        header, payload, signature = message[0], message[1], message[2]
        header = base64urldecode(header)
        payload = base64urldecode(payload)
        return header, payload

    @staticmethod
    def encode(header, payload, key=None):
        data = base64urlencode("{}.{}".format(header, payload))
        if header["alg"].lower() == "none":
            return data
        elif header["alg"] == "HS256":
            return hmac.new(key, data, digestmod="sha256")
        else:
            raise Exception("暂不支持该种加密方式")

    @staticmethod
    def crack(message, dictionary=None, reg="[0-9]{1,6}"):
        message = message.split(".")
        header, payload, signature = message[0], message[1], message[2]
        return Cracker().run(alg=json.loads(base64urldecode(header))["alg"],
                             dictionary=dictionary, reg=reg, args=(header+"."+payload, signature, ))


class Cracker:
    def __init__(self, process_number=1):
        self.passwords_queue = multiprocessing.Manager().Queue(1000000)
        self.process_number = process_number

    def run(self, alg=None, dictionary=None, reg="[0-9]{1,6}", args=None):
        p = multiprocessing.Process(target=self.put_passwords, args=(dictionary, reg,))
        p.start()

        pool = multiprocessing.Pool(self.process_number)
        results = []
        for i in range(self.process_number):
            if alg.lower() == "hs256":
                result = pool.apply_async(func=self.hs256, args=args)
                results.append(result)
            else:
                raise Exception("暂不支持该种加密方式")
        while True:
            for result in results:
                if result.ready():
                    p.terminate()
                    return result.get()

    def put_passwords(self, dictionary, reg):
        """
        生成密码并放入队列
        :param dictionary: 字典文件路径
        :param reg: 如果没有字典文件，则根据正则表达式生成符合条件的字典
        :return:
        """
        if dictionary:
            passwords = [line.strip() for line in open(dictionary, "rb").readlines()]
        else:
            passwords = exrex.generate(reg)
        for password in passwords:
            self.passwords_queue.put(password)
        self.passwords_queue.put(None)

    def md5(self):
        pass

    def hs256(self, plaintext, ciphertext):
        while True:
            password = self.passwords_queue.get()
            if not password:
                self.passwords_queue.put(None)
                break
            if base64urlencode(hmac.new(password.encode(), plaintext.encode(), digestmod="sha256").digest())\
                    == ciphertext.encode():
                print("[-] password: {}".format(password))
                self.passwords_queue.put(None)
                return password
            else:
                print("[-] error: {}".format(password))


class AESCipher:
    def __init__(self, key):
        self.key = self.handle_key(key)
        self.mode = AES.MODE_ECB

    @staticmethod
    def handle_key(key):
        """
        对密钥进行处理
        :param key: 密钥
        :return:
        """
        if type(key) != bytes:
            key = key.encode("utf-8")
        if len(key) < 16:
            key += (16 - len(key)) * b"\x00"
        return key[:16]

    @staticmethod
    def handle_plaintext(plaintext):
        """
        对明文进行处理
        :param plaintext: 明文
        :return:
        """
        if type(plaintext) != bytes:
            plaintext = plaintext.encode("utf-8")
        if len(plaintext) % 16 != 0:
            plaintext += (16 - len(plaintext) % 16) * b"\x00"
        return plaintext

    @staticmethod
    def handle_ciphertext(ciphertext):
        """
        对密文进行处理
        :param ciphertext: 密文
        :return:
        """
        if type(ciphertext) != bytes:
            ciphertext = ciphertext.encode("utf-8")
        ciphertext = base64.b64decode(ciphertext)
        return ciphertext

    def encode(self, plaintext):
        """
        AES加密
        :param plaintext: 明文
        :return:
        """
        plaintext = self.handle_plaintext(plaintext)
        ciphertext = AES.new(self.key, self.mode).encrypt(plaintext)
        ciphertext = base64.b64encode(ciphertext)
        return ciphertext

    def decode(self, ciphertext):
        """
        AES解密
        :param ciphertext: 密文
        :return:
        """
        ciphertext = self.handle_ciphertext(ciphertext)
        plaintext = AES.new(self.key, self.mode).decrypt(ciphertext)
        return plaintext

    def encode_by_opensslway(self):
        pass

    def decode_by_opensslway(self):
        pass


class CaptchaCracker:
    def __init__(self):
        pass

    def slide(self):
        pass

    def tup(self):
        pass

    def huidu(self):
        pass

    def jiangzao(self):
        pass


class Gestest:
    def __init__(self, browser):
        self.browser = browser

    def start(self, by="class name", value="geetest_btn"):
        self.browser.find_element(by, value).click()

    def fullpage(self, by="class name", value="geetest_btn"):
        """
        智能组合
        :return:
        """
        self.start(by, value)
        time.sleep(1)
        if "验证成功" in self.browser.find_element(by, value).text:
            return
        elif "请完成验证" in self.browser.find_element(by, value).text:
            self.slide()

    def slide(self):
        """
        滑动验证
        :return:
        """
        distance = self.get_distance()
        tracks = self.generate_tracks(distance)
        self.move(tracks)

    def get_distance(self):
        """
        比对背景图与全图，获取验证码缺口距离
        :return:
        """
        bg = self.get_image("geetest_canvas_bg")
        fullpg = self.get_image("geetest_canvas_fullbg")
        diff = ImageChops.difference(bg, fullpg).convert("L")
        diff.save(r"C:\Users\LQH\Desktop\fullpage.png")
        for x in range(diff.width):
            difference = 0
            for y in range(diff.height):
                difference += diff.getpixel((x, y))
            if difference > 2000:
                print("distance: ", x)
                return x

    def get_image(self, classname):
        """
        获取页面图片的Image对象
        :param classname:
        :return:
        """
        image = self.browser.execute_script(
            "return document.getElementsByClassName('{}')[0].toDataURL('image/png');".format(classname))
        image = base64.b64decode(image.replace("data:image/png;base64,", ""))
        image = io.BytesIO(image)
        image = Image.open(image)
        return image

    @staticmethod
    def generate_tracks(distance):
        """
        轨迹
        :return:
        """
        distance += 20
        v = 0
        t = 0.2
        forward_tracks = []
        current = 0
        mid = distance * 3 / 5  # 减速阀值
        while current < distance:
            if current < mid:
                a = 2  # 加速度为+2
            else:
                a = -3  # 加速度-3
            s = v * t + 0.5 * a * (t ** 2)
            v = v + a * t
            current += s
            forward_tracks.append(round(s))
        back_tracks = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -1]
        forward_tracks.extend(back_tracks)
        print("forward_tracks: ", forward_tracks)
        return forward_tracks

    def move(self, tracks):
        """
        移动
        :return:
        """
        slider = self.browser.find_element("class name", "geetest_slider_button")
        action = webdriver.ActionChains(self.browser)
        webdriver.ActionChains(self.browser).click_and_hold(slider).perform()
        for x in tracks:
            action.move_by_offset(x, 0)
        action.release().perform()

    def client(self):
        """
        点选验证
        :return:
        """


def binary_search(arr, judge_function, mode="three"):
    """
    二分查找法
    :param arr:
    :param judge_function: < 为 -1, = 为 0, > 为 1,
    :param mode: 模式，分为 three 或者 two
    :return:
    """
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        judge_result = judge_function(arr[mid])
        if mode == "three":
            if judge_result == -1:
                left = mid - 1
            elif judge_result == 1:
                right = mid + 1
            elif judge_result == 0:
                return mid
            else:
                raise Exception("判断函数编写错误，请检查所有输入都有对应且正确的输出")
        elif mode == "two":
            if judge_result == -1:
                left = mid
            elif judge_result == 1:
                right = mid
            else:
                raise Exception("判断函数编写错误，请检查所有输入都有对应且正确的输出")
            if right - left == 1:
                return left

        print(left, right)


def shell():
    """
    :return:
    """
    pass


def dns_shell():
    """
    dns隧道
    :return:
    """
    pass


def get_ioc_type(ioc):
    """
    判定ioc的类型
    :param ioc:
    :return:
    """
    try:
        if is_ipv4(ioc):
            return "ipv4"
        if is_url(ioc):
            return "url"
        if is_domain(ioc):
            return "domain"
        if is_email(ioc):
            return "email"
        if is_md5(ioc):
            return "md5"
        if is_sha1(ioc):
            return "sha1"
        if is_sha256(ioc):
            return "sha256"
    except Exception:
        pass
    return "unknown"


def is_domain(string):
    """
    判断字符串是否符合域名格式
    :param string:
    :return:
    """
    domain = re.compile(r"([0-9a-zA-Z][-0-9a-zA-Z]{0,62}\.)+[0-9a-zA-Z][-0-9a-zA-Z]{0,62}$")
    return True if re.match(domain, string) else False


def is_ipv4(string):
    """
    判断字符串是否符合ip格式
    :param string:
    :return:
    """
    ip = re.compile(r"^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])(\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])){3}$")
    return True if re.match(ip, string) else False


def is_url(string):
    """
    判断字符串是否符合url格式
    :param string:
    :return:
    """
    url = parse.urlparse(string)
    if url.hostname and (is_domain(url.hostname) or is_ipv4(url.hostname)):
        return True
    return False


def is_email(string):
    """
    判断字符串是否符合email格式
    :param string:
    :return:
    """
    if string.count("@") == 1:
        return is_domain(string.split("@")[-1])
    return False


def is_md5(string):
    """
    判断字符串是否符合32位md5格式
    :param string:
    :return:
    """
    md5 = re.compile(r"^[0-9a-fA-F]{32}$")
    return True if re.match(md5, string) else False


def is_sha1(string):
    """
    判断字符串是否符合40位sha1格式
    :param string:
    :return:
    """
    sha1 = re.compile(r"^[0-9a-fA-F]{40}$")
    return True if re.match(sha1, string) else False


def is_sha256(string):
    """
    判断字符串是否符合64位sha256格式
    :param string:
    :return:
    """
    sha256 = re.compile(r"^[0-9a-fA-F]{64}$")
    return True if re.match(sha256, string) else False


def get_second_level_domain(domain):
    """
    获取域名的二级域名
    :param domain:
    :return:
    """
    domain = domain.split(".")
    second_level_domain = domain[-2] + "." + domain[-1]
    return second_level_domain


class Alexa:
    def __init__(self):
        self.rank = self.__get_alexa_rank()

    @staticmethod
    def __get_alexa_rank():
        """
        获取 alexa 的排名数据
        :return:
        """
        file = os.path.join(os.path.dirname(__file__), r"./resource/top-1m.csv")
        # 当不存在alexa的排名记录文件或者文件的下载日期超过了三个月时，重新获取排名记录文件
        if not os.path.exists(file) or time.time() - os.path.getmtime(file) > 3600 * 24 * 30 * 3:
            api = "http://s3.amazonaws.com/alexa-static/top-1m.csv.zip"
            alexa = requests.get(api).content
            alexa = zipfile.ZipFile(io.BytesIO(alexa))
            alexa = alexa.read(alexa.namelist()[0])
            open(file, "wb").write(alexa)
        # 将排名记录文件读取并解析
        lines = open(file).readlines()
        rank = {}
        for line in lines:
            i, j = line.strip().split(",")
            rank[j] = int(i)
        return rank

    def get_domain_rank(self, domain):
        """
        获取网站在alexa的排名
        :param domain: 域名
        :return: dict, 先判断域名是否在alexa排名中，如果不在，则尝试根据上级域名获取alexa排名，直至获取到排名为止，否则返回-1
        """
        judge_domain = domain
        while True:
            if judge_domain in self.rank:
                return self.rank[judge_domain]
            judge_domain = judge_domain.split(".", 1)[-1]
            if not judge_domain.count("."):
                return 0


def port_reuse():
    """ 端口复用 """
    pass


def download_file(url, path="./temp", rename_by_md5=False, timelimit=None, **kwargs):
    """
    下载文件
    :param url: 下载链接
    :param path: 文件保存路径
    :param rename_by_md5: 是否以md5重命名
    :param timelimit: 总时间限制，用来限制一些超慢请求
    :param kwargs:
    :return: requests.get的其余关键字参数
    """
    # 下载文件
    start_time = time.time()
    response = requests.get(url, verify=False, stream=True, **kwargs)
    with open(path, "wb") as file:
        for chunk in response.iter_content(chunk_size=1048576):
            if timelimit and time.time() - start_time > timelimit:
                raise Exception("时间已超出限制")
            if chunk:
                file.write(chunk)
    # 文件以md5值进行重命名
    if rename_by_md5:
        md5 = get_file_hashs(path, ["md5"])["md5"]
        fin_path = os.path.join(os.path.dirname(path), md5)
        shutil.move(path, fin_path)
        path = fin_path
    # 返回文件路径
    return path


def failure_retry(*funs, max_retries=5, interval_time=1, print_exception=False):
    """
    用于函数运行失败后进行重试的装饰器
    :param funs: 需运行的函数，用*funs再包装一层，兼容直接使用装饰器与是否直接调用
    :param max_retries: 最大重试次数
    :param interval_time: 失败后重试的运行间隔时间
    :param print_exception: 是否打印中间的失败过程中的异常信息
    :return: 成功返回运行结果，失败则抛出最后一次运行时产生的异常
    """
    def wrapper(fun):
        def wrapper_inter(*args, **kwargs):
            raise_exception = Exception()
            for i in range(max_retries):
                try:
                    return fun(*args, **kwargs)
                except Exception as e:
                    if print_exception:
                        print(repr(e))
                    raise_exception = e
                time.sleep(interval_time)
            raise raise_exception
        return wrapper_inter
    # @failure_retry() 的调用形式
    if len(funs) == 0:
        return wrapper
    # @failure_retry 的调用形式
    elif len(funs) == 1 and callable(funs[0]):
        return wrapper(funs[0])
    # 错误传参
    else:
        raise Exception("参数异常，请重新检查参数")


if __name__ == '__main__':
    pass
