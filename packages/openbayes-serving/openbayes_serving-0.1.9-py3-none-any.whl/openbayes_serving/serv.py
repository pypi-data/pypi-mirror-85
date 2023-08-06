# -*- coding: utf-8 -*-

# -- stdlib --
from urllib.parse import urlparse
import argparse
import inspect
import json
import logging
import os
import re
import sys

# -- third party --
from flask import Blueprint, Flask, Response, current_app, jsonify, request
from werkzeug.exceptions import HTTPException
import msgpack
import requests
import uvicorn

# -- own --
from . import debug
from .common import detect_env
from .utils.log import init as init_logging, patch_formatter as patch_log_formatter


# -- code --
log = logging.getLogger('openbayes_serving.serv')


class ServingError(Exception):

    def __init__(self, message, status_code=400, payload={}):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = {**payload, 'error': message}


# -----------------------------
class ONNXInit:
    @staticmethod
    def register_parameters(parser):
        env = detect_env()
        if env == 'local':
            path = os.getcwd()
        elif env == 'gear':
            path = os.getcwd()
        elif env == 'production':
            path = '/mnt/project'

        parser.add_argument(
            '--model-path',
            default=path,
            help='ONNX 模型（.onnx 文件）搜索地址',
        )

    @staticmethod
    def init():
        search_path = current_app.config['OPENBAYES_SERVING_RUN_OPTIONS'].model_path
        log.debug(f'ONNX: 在 {search_path} 搜寻 ONNX 模型...')

        path = None
        if os.path.isdir(search_path):
            for fn in os.listdir(search_path):
                if not fn.endswith('.onnx'):
                    continue
                path = os.path.join(search_path, fn)
                break
            else:
                raise Exception('没有找到 ONNX 模型')
        elif os.path.isfile(search_path):
            path = search_path
        else:
            raise Exception('没有找到 ONNX 模型')

        log.info('正在加载 ONNX 模型：%s ...', path)

        try:
            import onnxruntime
        except ImportError:
            log.exception('无法加载 onnxruntime 库，请确认已经安装了它。如果没有使用特定的包管理工具，可以通过 `pip install onnxruntime` 安装。')
            sys.exit(1)

        # TODO: plain onnxruntime object or a wrapped one?
        model = onnxruntime.InferenceSession(path)
        return model


INIT_ARG_HANDLERS = {
    'onnx': ONNXInit,
}


def parse_type(tp):
    if not tp or tp == '*/*':
        return 'octet-stream'

    m = re.match(r'^application/([a-z0-9\.\-]+)', tp)
    if not m:
        return 'octet-stream'

    enc, *_ = m.groups()

    COALESCE = {
        'octet-stream':    'octet-stream',
        'msgpack':         'msgpack',
        'x-msgpack':       'msgpack',
        'vnd.msgpack':     'msgpack',
        'vnd.messagepack': 'msgpack',
        'json':            'json',
    }

    return COALESCE.get(enc, 'octet-stream')


def get_payload():
    tp = parse_type(request.mimetype)

    if not tp:
        raise ServingError("无效的 Content-Type", 415)

    if tp == 'msgpack':
        try:
            payload = msgpack.unpackb(request.get_data(), raw=False)
        except Exception as e:
            raise ServingError("无法解析输入的 MessagePack 消息", 400) from e
    elif tp == 'json':
        try:
            payload = json.loads(request.get_data())
        except Exception as e:
            raise ServingError("无法解析输入的 JSON 消息", 400) from e
    elif tp == 'octet-stream':
        payload = request.get_data()
    else:
        raise Exception(f'BUG: unknown mime type {tp}')

    return tp, payload


def get_json():
    tp, payload = get_payload()
    if tp not in ('msgpack', 'json'):
        raise ServingError('输入必须是 JSON 或者 MessagePack 格式')

    return payload


PREDICT_ARG_HANDLERS = {
    'data': lambda: request.data,
    'json': get_json,
    'payload': lambda: get_payload()[1],
    'params': lambda: request.args,
    'headers': lambda: request.headers,
    'request': lambda: request,
}

predict_blueprint = Blueprint('openbayes-serv-predict', __name__)


CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
    'Access-Control-Allow-Credentials': 'true',
    'Access-Control-Allow-Headers': 'Accept,Content-Type,Accept-Encoding,User-Agent',
    'Access-Control-Max-Age': '86400',
}


@predict_blueprint.route('', methods=['GET'], provide_automatic_options=False)
def help_message():
    return {'message': 'Serving 服务正常工作，可以发送 POST 请求到此地址进行推理。'}, 200, CORS_HEADERS


@predict_blueprint.route('', methods=['OPTIONS'], provide_automatic_options=False)
def request_options():
    return b'', 200, CORS_HEADERS


@predict_blueprint.route('', methods=['POST'], provide_automatic_options=False)
def model_predict():
    try:
        obj = current_app.config['OPENBAYES_SERVING_PREDICTOR_OBJECT']
        args = current_app.config['OPENBAYES_SERVING_PREDICT_ARGS']
        kwargs = {k: PREDICT_ARG_HANDLERS[k]() for k in args}
        # TODO: Parse Accept and optionally send msgpack payload
        rst = obj.predict(**kwargs)
        if isinstance(rst, (dict, list, tuple)):
            resp = jsonify(rst)
            resp.headers.extend(CORS_HEADERS)
            return resp
        elif isinstance(rst, bytes):
            mimetype = 'application/octet-stream'
            if rst.startswith(b'\x89PNG'):
                mimetype = 'image/png'
            elif rst.startswith(b'\xff\xd8') and rst.endswith(b'\xff\xd9'):
                mimetype = 'image/jpeg'
            return Response(rst, mimetype=mimetype, headers=CORS_HEADERS)
        elif callable(rst):
            return rst
        else:
            log.error('predict 函数返回了无效的结果：%s', rst)
            log.debug('有效的结果有 dict、list、tuple 对象，会被编码成 JSON；bytes、str 对象，会直接返回给客户端。')
            return {}, 500, CORS_HEADERS
    except ServingError as e:
        response = jsonify(e.payload)
        response.headers.extend(CORS_HEADERS)
        response.status_code = e.status_code
        return response
    except HTTPException:
        raise
    except Exception:
        state = current_app.config.get('OPENBAYES_SERVING_DEBUGGER_STATE')
        log.exception('predict 函数发生了异常，请检查代码')
        if state:
            rv = state.collect_exception()
            log.error(f'使用浏览器打开 {rv["url"]} 调试此次失败的请求')
            return {'debug_url': rv['url']}, 500, CORS_HEADERS

        return {}, 500, CORS_HEADERS


@predict_blueprint.app_errorhandler(400)
def handle_bad_request(e):
    return {'error': '无效的请求，请检查一下你的请求格式'}, 400


def make_app(predictor_cls):
    env = detect_env()
    if env == 'production':
        init_logging(logging.INFO)
    else:
        init_logging(logging.DEBUG)

    parser = argparse.ArgumentParser('openbayes-serv')
    parser.add_argument('--host', default='0.0.0.0', help='服务监听地址')

    port = 25252
    if env == 'gear':
        port = 8080
    elif env == 'production':
        port = 80

    parser.add_argument('--port', type=int, default=port, help='服务监听端口')

    app = Flask('model-serving')

    log.info('Openbayes Serving 正在启动...')

    with app.app_context():
        lst = inspect.signature(predictor_cls).parameters.keys()
        clsname = getattr(predictor_cls, '__name__', repr(predictor_cls))
        args = {}
        for arg in lst:
            if arg not in INIT_ARG_HANDLERS:
                log.error(f"{clsname} 初始化失败: 不知道该如何提供 `{arg}`。支持的有：{list(INIT_ARG_HANDLERS.keys())}。请参考文档。")
                return

        for arg in lst:
            INIT_ARG_HANDLERS[arg].register_parameters(parser)

        options = parser.parse_args()
        app.config['OPENBAYES_SERVING_RUN_OPTIONS'] = options

        for arg in lst:
            args[arg] = INIT_ARG_HANDLERS[arg].init()

        user_obj = predictor_cls(**args)
        user_predict = getattr(user_obj, 'predict', None)
        if not user_predict:
            log.error(f"{clsname} 初始化失败: 没有实现 `predict` 接口。请参考文档。")
            return

        lst = inspect.signature(user_predict).parameters.keys()
        for arg in lst:
            if arg not in PREDICT_ARG_HANDLERS:
                log.error(f"{clsname} 执行失败: 在 `predict` 函数中，不知道该如何提供 `{arg}`。支持的有：{list(PREDICT_ARG_HANDLERS.keys())}。请参考文档。")
                return

        app.config['OPENBAYES_SERVING_PREDICTOR_OBJECT'] = user_obj
        app.config['OPENBAYES_SERVING_PREDICT_ARGS'] = lst

    if env == 'local':
        log.info('检测到本地开发环境，开启调试模式')
        app.register_blueprint(predict_blueprint, url_prefix='/')
        debug.install(app)
    elif env == 'gear':
        log.info('检测到 Openbayes 算力容器环境，开启调试模式')

        try:
            prefix = None
            meta = requests.get('http://localhost:21999/gear-status').json()
            url = meta['links']['auxiliary']
            prefix = urlparse(url).path
            app.config['OPENBAYES_EXTERNAL_ROOT'] = url
            log.info('外部可访问的 URL：%s', url)
        except Exception:
            log.exception('无法获取 Openbayes 算力容器的元信息，不再进行对接，将不能正常从容器外部访问。')

        app.register_blueprint(predict_blueprint, url_prefix=prefix)
        debug.install(app, url_prefix=prefix)

    elif env == 'production':
        log.info('检测到生产环境，关闭调试模式。请求的统计信息可以在 Openbayes 的控制台上查看。')
        app.register_blueprint(predict_blueprint, url_prefix='/')

    return app


def run(predictor_cls):
    app = make_app(predictor_cls)
    options = app.config['OPENBAYES_SERVING_RUN_OPTIONS']

    config = uvicorn.Config(app,
        host=options.host, port=options.port,
        log_level='info', interface='wsgi',
    )

    logger = logging.getLogger('uvicorn')
    logger.handlers[:] = []

    patch_log_formatter(logging.getLogger('uvicorn.access'))

    server = uvicorn.Server(config=config)
    log.info(f'Openbayes Serving 开始服务（{options.host}:{options.port}）')
    log.info('-' * 60)
    server.run()

# def obt.serv.check(pattern, obj=<payload>):
#     '''检查指定的对象是否满足 pattern，在 predict 处使用，默认检查 payload。要实现一个后门，用来给前端暴露这个 pattern 具体是什么。'''

# def obt.serv.emit_event(filename, data):
#     '''记录自定义事件。filename 是指事件的名字，约定使用文件名样子的名字。data 是实际的数据。如果 data 是 dict 或者 list，则会做 json encode；若为 string 或者 bytes，直接存储，否则报错。'''
