# 万郡绿建图片上传服务器
import hashlib
import os
import time
import requests
import redis

pic_list = [
    'https://f.zhaogang.com/o_w-f65ae506de3842f2ba2f94ec5af8a45f.jpg',
    'https://f.zhaogang.com/o_w-67f0a013a16b4879983e80930907164f.jpg',
    'https://f.zhaogang.com/o_w-a1189f094cc84566aab3f3ed246ef34e.jpg',
    'https://f.zhaogang.com/o_w-244266b00c784e50829148cd074540e9.jpg',
    'https://f.zhaogang.com/o_w-a1189f094cc84566aab3f3ed246ef34e.jpg',
    'https://f.zhaogang.com/o_w-244266b00c784e50829148cd074540e9.jpg',
    'https://f.zhaogang.com/o_w-244266b00c784e50829148cd074540e9.jpg',
    'https://f.zhaogang.com/o_w-244266b00c784e50829148cd074540e9.jpg',
    'https://f.zhaogang.com/o_w-244266b00c784e50829148cd074540e9.jpg',
    'https://f.zhaogang.com/o_w-244266b00c784e50829148cd074540e9.jpg',
    'https://f.zhaogang.com/o_w-244266b00c784e50829148cd074540e9.jpg',
    'https://f.zhaogang.com/o_w-244266b00c784e50829148cd074540e9.jpg',
    'https://f.zhaogang.com/o_w-8fcb1745ae0d4bfc8b61a4416483cfc4.jpg',
    'https://f.zhaogang.com/o_w-244266b00c784e50829148cd074540e9.jpg',
    'https://f.zhaogang.com/o_w-244266b00c784e50829148cd074540e9.jpg',
    'https://f.zhaogang.com/o_w-67f0a013a16b4879983e80930907164f.jpg',
    'https://f.zhaogang.com/o_w-67f0a013a16b4879983e80930907164f.jpg',
    'https://f.zhaogang.com/o_w-67f0a013a16b4879983e80930907164f.jpg',
    'https://f.zhaogang.com/o_w-8fcb1745ae0d4bfc8b61a4416483cfc4.jpg',
    'https://f.zhaogang.com/o_w-244266b00c784e50829148cd074540e9.jpg',
    'https://f.zhaogang.com/o_w-244266b00c784e50829148cd074540e9.jpg',
    'https://f.zhaogang.com/o_w-244266b00c784e50829148cd074540e9.jpg',
    'https://f.zhaogang.com/o_w-a98f1bbba47944eaabb6d0773d9e5d5f.jpg',
    'https://f.zhaogang.com/o_w-244266b00c784e50829148cd074540e9.jpg',
    'https://f.zhaogang.com/o_w-244266b00c784e50829148cd074540e9.jpg',
    'https://f.zhaogang.com/o_w-67f0a013a16b4879983e80930907164f.jpg',
    'https://f.zhaogang.com/o_w-f65ae506de3842f2ba2f94ec5af8a45f.jpg',
    'https://f.zhaogang.com/o_w-80ee62b4a63d4f29ab80f8d7a0ec73b2.jpg',
    'https://f.zhaogang.com/o_w-67f0a013a16b4879983e80930907164f.jpg',
    'https://f.zhaogang.com/o_w-244266b00c784e50829148cd074540e9.jpg',
    'https://f.zhaogang.com/o_w-67f0a013a16b4879983e80930907164f.jpg']


class UploadPic:
    vandream_url = 'http://b-weed.vandream.com/dir/assign'
    pic_file = '.'

    def __init__(self):
        self.url = None
        self.van_url = None
        self.info = {'code': 1, 'msg': ''}
        self.file_path = None
        self.redis_pool = redis.ConnectionPool(host='47.113.200.109', port=63791)
        self.redis_conn = redis.Redis(connection_pool=self.redis_pool)

    def get_url(self):
        try:
            r = requests.get(self.vandream_url, timeout=0.5)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except Exception as e:
            self.info['code'] = 101
            self.info['msg'] = str(e)

    def send_file(self, upload_url, file_path):
        try:
            files = {'file': open(file_path, 'rb')}
            r = requests.post(upload_url, files=files, timeout=0.5)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except Exception as e:
            self.info['code'] = 102
            self.info['msg'] = str(e)

    def down_picture(self, img_name, img_url):
        try:
            r = requests.get(img_url, stream=True)
            r.raise_for_status()
            pic_file_name = self.pic_file + '/' + img_name
            self.file_path = pic_file_name
            with open(pic_file_name, 'wb') as f:
                f.write(r.content)
            return True
        except Exception as e:
            self.info['code'] = 104
            self.info['msg'] = str(e)

    def upload(self, img_name, img_url):
        img_name = str(time.time())
        res = self.down_picture(img_name, img_url)
        try:
            if res:
                url_text = self.get_url()
                if url_text:
                    pic_id = eval(url_text).get('fid')
                    true_id = pic_id.replace(',', '/') + '.jpg'
                    pic_url = eval(url_text).get('publicUrl')
                    self.url = 'http://' + pic_url + '/' + pic_id
                    self.van_url = 'http://' + pic_url + '/' + true_id
                    res = self.send_file(self.url, self.file_path)
                    if res:
                        self.info['code'] = 0
                        self.info['msg'] = self.van_url
                    else:
                        raise Exception
        except Exception as e:
            self.info['code'] = 103
            self.info['msg'] = str(e)
        finally:
            # del file
            if os.path.exists(self.file_path): # True/False
                os.remove(self.file_path)  # True/False
            return self.info

    def generate(self, img_url):  # redis判断与图片处理
        if 'http' in img_url:  # 单个图片
            msg = self.redis_conn.get(img_url)  # 根据名称获取redis中数据
            if msg:  # 判断数据是否存在与redis中
                return msg.decode('utf-8')
            else:  # 不存在则上传并存入redis
                result = self.upload(img_url, img_url)  # 上传
                if result['code'] == 0:
                    self.redis_conn.set(img_url, result['msg'])
                    return result['msg']
                else:
                    return None
        else:
            urls = []  # 新图片链接
            for url in img_url:
                msg = self.redis_conn.get(url)  # 根据名称获取redis中数据
                if msg:  # 判断数据是否存在与redis中
                    urls.append(msg.decode('utf-8'))
                else:
                    result = self.upload(url, url)  # 上传
                    if result['code'] == 0:
                        self.redis_conn.set(url, result['msg'])
                        urls.append(result['msg'])
                    else:
                        print('图片上传失败！！！')
            return ';'.join(urls) if urls else None


if __name__ == '__main__':
    u = UploadPic()
    # u.upload('213','http://files.cailiao.com/member/465823/goods/20200619/f0991cc2d2fded0945e83d5e0e056dc1.jpg?x-oss-process=image/resize,p_200')
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    print(u.generate(pic_list[:3]))
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
