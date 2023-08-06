"""
Name : Format.py
Author  : Cash
Contact : tkggpdc2007@163.com
Time    : 2020-01-08 10:52
Desc:
"""

import os

import oss2
import requests
from tqdm import tqdm

__all__ = ['get_random_md5',
           'get_file_md5',
           'upload_obj',
           'upload_file',
           'resume_upload_file',
           'token_url',
           'download_image',
           'download_video',
           'convert_png2jpg',
           'get_file_list']


def get_random_md5():
    import uuid
    uid = str(uuid.uuid4())
    md5 = ''.join(uid.split('-'))
    return md5


def get_file_md5(file):
    import hashlib
    m = hashlib.md5()
    with open(file, 'rb') as f:
        for line in f:
            m.update(line)
    return m.hexdigest()


def upload_obj(data, oss_params, suffix=".png"):
    """
    通过二进制流生成图片
    :param data: 二进制信息
    :param oss_params: oss参数
    :param suffix: 图片后缀
    :return: oss2生成url
    """
    md5 = get_random_md5()
    response = {}
    try:
        auth = oss2.Auth(oss_params['access_key'], oss_params['secret_key'])  # 构建鉴权对象
        bucket = oss2.Bucket(auth, oss_params['domain'], oss_params['bucket_name'])
        result = bucket.put_object(md5 + suffix, data)
        if result.status == 200:
            response["url"] = oss_params['domain'] + '/' + md5 + suffix
            response["md5"] = md5
            response["size"] = int(result.resp.response.request.headers._store['content-length'][1])
            response["type"] = result.resp.response.request.headers._store['content-type'][1]
            return response
    except Exception as e:
        return e


def upload_file(file_path, oss_params):
    """
    上传本地文件
    :param file_path: 文件路径
    :param oss_params: oss参数
    :return: oss2生成url
    """
    response = {}
    try:
        auth = oss2.Auth(oss_params['access_key'], oss_params['secret_key'])  # 构建鉴权对象
        bucket = oss2.Bucket(auth, oss_params['domain'], oss_params['bucket_name'])
        result = bucket.put_object_from_file(file_path.split('/')[-1], file_path)
        if result.status == 200:
            response["url"] = oss_params['domain'] + '/' + file_path.split('/')[-1]
            response["md5"] = get_file_md5(file_path)
            response["size"] = int(result.resp.response.request.headers._store['content-length'][1])
            response["type"] = result.resp.response.request.headers._store['content-type'][1]
            return response
    except Exception as e:
        return e


def resume_upload_file(file_path, oss_params, store_dir='/tmp'):
    """
    文件断点续传: https://help.aliyun.com/document_detail/88433.html
    :param file_path: 文件路径
    :param oss_params: oss参数
    :param store_dir:
    :return:
    """
    # 如使用store指定了目录，则保存断点信息在指定目录中。
    # 如使用num_threads设置上传并发数，请将oss2.defaults.connection_pool_size设成大于或等于线程数。默认线程数为1。
    response = {}
    try:
        auth = oss2.Auth(oss_params['access_key'], oss_params['secret_key'])  # 构建鉴权对象
        bucket = oss2.Bucket(auth, oss_params['domain'], oss_params['bucket_name'])
        result = oss2.resumable_upload(bucket, file_path.split('/')[-1], file_path,
                                       store=oss2.ResumableStore(root=store_dir),
                                       multipart_threshold=100 * 1024,
                                       part_size=100 * 1024,
                                       num_threads=4)
        if result.status == 200:
            response["url"] = oss_params['domain'] + '/' + file_path.split('/')[-1]
            response["md5"] = get_file_md5(file_path)
            response["size"] = int(result.resp.response.request.headers._store['content-length'][1])
            response["type"] = result.resp.response.request.headers._store['content-type'][1]
            return response
    except Exception as e:
        return e


def token_url(url, oss_params):
    """
    获取待token的name
    :param url: 需要添加token的url
    :param oss_params: oss参数
    :return: 带token的url
    """
    if '?' in url:
        url = url[0: url.find('?')]
    try:
        auth = oss2.Auth(oss_params['access_key'], oss_params['secret_key'])  # 构建鉴权对象
        bucket = oss2.Bucket(auth, oss_params['domain'], oss_params['bucket_name'])
        url_token = bucket.sign_url("GET", url.split('/')[-1], 3600)
        return url_token
    except Exception as e:
        return e


def download_image(file_path):
    try:
        import re
        res = re.match("https?://", file_path)
        if res:
            response = requests.get(file_path)
            data = response.content
        else:
            with open(file_path, "rb") as fr:
                data = fr.read()
    except Exception as e:
        return e
    return data


def download_video(file_path, path_to_save):
    try:
        import re
        res = re.match("https?://", file_path)
        if res:
            r = requests.get(file_path, stream=True)
            total_length = r.headers.get('content-length')
            with open(path_to_save, 'wb') as f:
                if total_length is None:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                else:
                    total_length = int(total_length)
                    for chunk in tqdm(r.iter_content(chunk_size=1024),
                                      total=int(total_length / 1024. + 0.5),
                                      unit='KB', unit_scale=False, dynamic_ncols=True):
                        f.write(chunk)
    except Exception as e:
        return e
    return path_to_save


def convert_png2jpg(file_path):
    """
    图像格式转换: png转jpg
    :param file_path:
    :return:
    """
    from PIL import Image

    out_file = os.path.splitext(file_path)[0] + ".jpg"
    image = Image.open(file_path)
    try:
        if len(image.split()) == 4:
            r, g, b, a = image.split()
            image = Image.merge("RGB", (r, g, b))
            image.convert('RGB').save(out_file, quality=70)
            os.remove(file_path)
        else:
            image.convert('RGB').save(out_file, quality=70)
            os.remove(file_path)
        return out_file
    except:
        return None


def get_file_list(path, suffix='.jpg'):
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith(suffix)]


def analysis_facebook_video(url, quality='HD'):
    try:
        import re
        x = re.match(r'^(https:|)[/][/]www.([^/]+[.])*facebook.com', url)
        if x:
            html = requests.get(url).content.decode('utf-8')
        else:
            print("\nNot related with Facebook domain.")
            return url
        video_url = re.search(rf'{quality.lower()}_src:"(.+?)"', html).group(1)
        return video_url
    except:
        return url
