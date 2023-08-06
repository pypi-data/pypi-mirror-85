import oss2
from oss2 import Bucket
from oss2.models import PutObjectResult
import sys

__all__ = (
    'init', 'upload_obj', 'upload_file', 'resume_upload_file', 'download_obj', 'resumable_download_obj', 'batch_delete',
    'sign_url')

bucket: Bucket = None


def init(access_key_id, access_key_secret, bucket_name, domain):
    """
    oss 初始化
    :param access_key_id:
    :param access_key_secret:
    :param bucket_name:
    :param domain:
    :return:
    """
    # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
    auth = oss2.Auth(access_key_id, access_key_secret)
    # Endpoint以杭州为例，其它Region请按实际情况填写。
    global bucket
    bucket = oss2.Bucket(auth, domain, bucket_name)


def token_url(url, access_key, secret_key, domain, bucket_name, params=None):
    """
    获取待token的name
    :param url:
    :param access_key:
    :param secret_key:
    :param domain:
    :param bucket_name:
    :param params:
    :return:
    """
    try:
        _auth = oss2.Auth(access_key, secret_key)  # 构建鉴权对象
        bucket = oss2.Bucket(_auth, domain, bucket_name)
        name = url.split('/')[-1]
        result = bucket.sign_url("GET", name, 604800, params=params)
        return result
    except Exception as e:
        return e


def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\r{0}% '.format(rate), end='')
        sys.stdout.flush()


# --------------------------------上传--------------------------------


def upload_obj(obj_name, obj_content, headers=None, progress_callback=percentage):
    """
    对象上传
    用于上传 字符串、二进制、网络流、
    :param obj_name:
    :param obj_content:
    :param headers:
    :param progress_callback:
    :return:
    """
    result = bucket.put_object(obj_name, obj_content, headers=headers, progress_callback=progress_callback)
    return result


def upload_file(obj_name, local_file_path, headers=None, progress_callback=percentage) -> PutObjectResult:
    """
    文件上传
    :param obj_name:
    :param local_file_path:
    :param headers:
    :param progress_callback:
    :return:
    """
    result = bucket.put_object_from_file(obj_name, local_file_path, headers=headers,
                                         progress_callback=progress_callback)
    return result


def resume_upload_file(obj_name, local_file_path, store_dir='/tmp',
                       headers=None,
                       multipart_threshold=None,
                       part_size=None,
                       progress_callback=percentage,
                       num_threads=None,
                       params=None):
    """
    文件断点续传
    https://help.aliyun.com/document_detail/88433.html
    :param obj_name:
    :param local_file_path:
    :param store_dir:
    :param headers:
    :param multipart_threshold:
    :param part_size:
    :param progress_callback:
    :param num_threads:
    :param params:
    :return:
    """
    # 如使用store指定了目录，则保存断点信息在指定目录中。
    # 如使用num_threads设置上传并发数，请将oss2.defaults.connection_pool_size设成大于或等于线程数。默认线程数为1。
    oss2.resumable_upload(bucket, obj_name, local_file_path,
                          store=oss2.ResumableStore(root=store_dir),
                          multipart_threshold=100 * 1024,
                          part_size=100 * 1024,
                          num_threads=4)


# --------------------------------下载--------------------------------

def download_obj(obj_name, local_file_path, byte_range=None, headers=None, progress_callback=percentage, process=None,
                 params=None):
    """
    下载对象到本地文件
    :param obj_name:
    :param local_file_path:
    :param byte_range:
    :param headers:
    :param progress_callback:
    :param process:
    :param params:
    :return:
    """
    bucket.get_object_to_file(obj_name, local_file_path, byte_range=byte_range, headers=headers,
                              progress_callback=progress_callback, process=process, params=params)


def resumable_download_obj(obj_name, local_file_path, store_dir='/tmp', multiget_threshold=None, part_size=None,
                           num_threads=None):
    """
    断点续传下载
    :param obj_name:
    :param local_file_path:
    :param store_dir:
    :param multiget_threshold:
    :param part_size:
    :param num_threads:
    :return:
    """
    oss2.resumable_download(bucket, obj_name, local_file_path,
                            store=oss2.ResumableDownloadStore(root=store_dir),
                            multiget_threshold=multiget_threshold,
                            part_size=part_size,
                            num_threads=num_threads)


# --------------------------------删除--------------------------------

def batch_delete(obj_name_list=[]):
    """
    批量删除
    :param obj_name_list:
    :return:
    """
    # 批量删除3个文件。每次最多删除1000个文件。
    result = bucket.batch_delete_objects(obj_name_list)
    # 打印成功删除的文件名。
    print('\n'.join(result.deleted_keys))
    return result


# --------------------------------其他--------------------------------
def sign_url(obj_name, expires=60 * 60, style=''):
    """
    生成带签名的URL
    :param obj_name:
    :param expires: 过期时间，单位：秒
    :param style:样式
    :return:
    """
    url = bucket.sign_url('GET', obj_name, expires, params={'x-oss-process': style})
    return url


def upload_file_and_fetch_token_url(fp):
    fn = fp.split('/')[-1]
    result = upload_file(fn, fp)
    url = result.resp.response.url
    turl = token_url(url=url, access_key=access_key, secret_key=secret_key, bucket_name=bucket_name,
                     domain=domain)
    return turl


access_key = "LTAI4FnraQiZdE8hr6r69upN"
secret_key = "SRx7f1jzJchAAjeuBK61kCPSTJZcSR"
bucket_name = "tezign-temp"
domain = "http://oss-cn-shanghai.aliyuncs.com"

init(access_key_id=access_key, access_key_secret=secret_key, bucket_name=bucket_name, domain=domain)

if __name__ == '__main__':
    import os

    fp = '../../images/3.mp4'
    fn = fp.split('/')[-1]

    result = upload_file(fn, fp)

    result_url = result.resp.response.url
    token_url = token_url(url=result_url, access_key=access_key, secret_key=secret_key, bucket_name=bucket_name,
                          domain=domain)
    print(token_url)
