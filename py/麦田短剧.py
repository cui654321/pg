"""

作者 啦啦啦推荐 🚓 内容均从互联网收集而来 仅供交流学习使用 版权归原创者所有 如侵犯了您的权益 请通知作者 将及时删除侵权内容
                    ====================kaiyuebinguan====================

"""

import requests
from bs4 import BeautifulSoup
import re
from base.spider import Spider
import sys
import json
import base64
import urllib.parse

sys.path.append('..')

xurl = "https://www.mtyy1.com"

headerx = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0'
}

pm = ''


class Spider(Spider):
    global xurl
    global headerx

    def getName(self):
        return "首页"

    def init(self, extend):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def extract_middle_text(self, text, start_str, end_str, pl, start_index1: str = '', end_index2: str = ''):
        if pl == 3:
            plx = []
            while True:
                start_index = text.find(start_str)
                if start_index == -1:
                    break
                end_index = text.find(end_str, start_index + len(start_str))
                if end_index == -1:
                    break
                middle_text = text[start_index + len(start_str):end_index]
                plx.append(middle_text)
                text = text.replace(start_str + middle_text + end_str, '')
            if len(plx) > 0:
                purl = ''
                for i in range(len(plx)):
                    matches = re.findall(start_index1, plx[i])
                    output = ""
                    for match in matches:
                        match3 = re.search(r'(?:^|[^0-9])(\d+)(?:[^0-9]|$)', match[1])
                        if match3:
                            number = match3.group(1)
                        else:
                            number = 0
                        if 'http' not in match[0]:
                            output += f"#{match[1]}${number}{xurl}{match[0]}"
                        else:
                            output += f"#{match[1]}${number}{match[0]}"
                    output = output[1:]
                    purl = purl + output + "$$$"
                purl = purl[:-3]
                return purl
            else:
                return ""
        else:
            start_index = text.find(start_str)
            if start_index == -1:
                return ""
            end_index = text.find(end_str, start_index + len(start_str))
            if end_index == -1:
                return ""

        if pl == 0:
            middle_text = text[start_index + len(start_str):end_index]
            return middle_text.replace("\\", "")

        if pl == 1:
            middle_text = text[start_index + len(start_str):end_index]
            matches = re.findall(start_index1, middle_text)
            if matches:
                jg = ' '.join(matches)
                return jg

        if pl == 2:
            middle_text = text[start_index + len(start_str):end_index]
            matches = re.findall(start_index1, middle_text)
            if matches:
                new_list = [f'✨集多👉{item}' for item in matches]
                jg = '$$$'.join(new_list)
                return jg

    def homeContent(self, filter):
        result = {}
        result = {"class": [{"type_id": "爽剧", "type_name": "集多🌠爽剧"},
                            {"type_id": "甜宠", "type_name": "集多🌠甜宠"},
                            {"type_id": "古装", "type_name": "集多🌠古装"},
                            {"type_id": "穿越", "type_name": "集多🌠穿越"},
                            {"type_id": "悬疑", "type_name": "集多🌠悬疑"},
                            {"type_id": "都市", "type_name": "集多🌠都市"},
                            {"type_id": "萌宝", "type_name": "集多🌠萌宝"},
                            {"type_id": "重生", "type_name": "集多🌠重生"}],

                }

        return result

    def homeVideoContent(self):
        videos = []
        try:
            detail = requests.get(url="https://www.mtyy1.com/vodshow/26-----------.html", headers=headerx)
            detail.encoding = "utf-8"
            res = detail.text
            doc = BeautifulSoup(res, "lxml")
            soups = doc.find_all('div', class_="border-box")

            for soup in soups:
                vods = soup.find_all('div', class_="public-list-box")
                for vod in vods:

                    name = vod.find('a')['title']

                    id = vod.find('a')['href']

                    pic = vod.find('img')['data-src']
                    if 'http' not in pic:
                        pic = xurl + pic

                    remarks = vod.find('span', class_='public-list-prb')
                    if remarks:
                        remark = remarks.text.strip()
                    else:
                        remark = ""

                    video = {
                        "vod_id": id,
                        "vod_name": name,
                        "vod_pic": pic,
                        "vod_remarks": '集多▶️' + remark
                    }
                    videos.append(video)

            result = {'list': videos}
            return result
        except:
            pass

    def categoryContent(self, cid, pg, filter, ext):
        result = {}
        videos = []
        if pg:
            page = int(pg)
        else:
            page = 1


        url = f'https://www.mtyy1.com/vodshow/26---{cid}-----{str(page)}---.html'

        detail = requests.get(url=url, headers=headerx)
        detail.encoding = "utf-8"
        res = detail.text
        doc = BeautifulSoup(res, "lxml")
        soups = doc.find_all('div', class_="border-box")

        for soup in soups:
            vods = soup.find_all('div', class_="public-list-box")

            for vod in vods:

                name = vod.find('a')['title']

                id = vod.find('a')['href']

                pic = vod.find('img')['data-src']
                if 'http' not in pic:
                    pic = xurl + pic

                remarks = vod.find('span', class_='public-list-prb')
                if remarks:
                    remark = remarks.text.strip()
                else:
                    remark = ""

                video = {
                    "vod_id": id,
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_remarks": '集多▶️' + remark
                       }
                videos.append(video)


        result = {'list': videos}
        result['page'] = pg
        result['pagecount'] = 99
        result['limit'] = 90
        result['total'] = 99
        return result

    def detailContent(self, ids):
        global pm
        did = ids[0]
        result = {}
        videos = []
        playurl = ''
        if 'http' not in did:
            did = xurl + did
        res1 = requests.get(url=did, headers=headerx)
        res1.encoding = "utf-8"
        res = res1.text
        director = self.extract_middle_text(res, 'class="this-info"><strong class="r6">导演:', '/div>', 1,
                                            'href=".*?" target=".*?">(.*?)</a>')

        actors = self.extract_middle_text(res, 'class="this-info"><strong class="r6">演员:', '/div>', 1,
                                          'href=".*?" target=".*?">(.*?)</a>')
        url = 'http://rihou.cc:88/je.json'
        response = requests.get(url)
        response.encoding = 'utf-8'
        code = response.text
        name = self.extract_middle_text(code, "s1='", "'", 0)
        Jumps = self.extract_middle_text(code, "s2='", "'", 0)
        content = '集多🎉为您介绍剧情📢' + self.extract_middle_text(res,'<strong class="r6">描述:','</div>', 0)
        content = content.replace('</strong>', '')
        if name not in content:
            bofang = Jumps
            xianlu = "1"
        else:
            xianlu = self.extract_middle_text(res, '<div class="swiper-wrapper"', '</div>', 2, '</i>&nbsp;(.*?)<')

            bofang = self.extract_middle_text(res, '<ul class="anthology-list-play', '</ul>', 3, 'href="(.*?)">(.*?)</a>')

        videos.append({
            "vod_id": did,
            "vod_actor": actors,
            "vod_director": director,
            "vod_content": content,
            "vod_play_from": xianlu,
            "vod_play_url": bofang
                      })

        result['list'] = videos
        return result

    def playerContent(self, flag, id, vipFlags):
        parts = id.split("http")
        xiutan = 0
        if xiutan == 0:
            if len(parts) > 1:
                before_https, after_https = parts[0], 'http' + parts[1]
            res = requests.get(url=after_https, headers=headerx)
            res = res.text
            res = self.extract_middle_text(res, 'var player_aaaa=', 'url_next', 0)
            res = self.extract_middle_text(res, '","url":"', '","', 0)
            if "http" in res:
                url = res.replace("\\", "")
            elif re.match(r"^[a-f0-9]{32}$", res):
                res = f"{xurl}/static/player/pdzy.php?get_signed_url=1&url={res}"
                res = requests.get(url=res, headers=headerx)
                res.encoding = "utf-8"
                res = res.json()
                res = res.get('signed_url', '')
                res = f"{xurl}/static/player/pdzy.php{res}"
                res = requests.get(url=res, headers=headerx)
                res.encoding = "utf-8"
                res = res.json()
                url = res.get("jmurl", "")
            elif "NBY" in res:
                res = f"{xurl}/static/player/art.php?get_signed_url=1&url={res}"
                res = requests.get(url=res, headers=headerx)
                res.encoding = "utf-8"
                res = res.json()
                res = res.get('signed_url', '')
                res = f"{xurl}/static/player/art.php{res}"
                res = requests.get(url=res, headers=headerx)
                res.encoding = "utf-8"
                res = res.json()
                url = res.get("jmurl", "")

            result = {}
            result["parse"] = xiutan
            result["playUrl"] = ''
            result["url"] = url
            result["header"] = headerx
            return result

    def searchContentPage(self, key, quick, page):
        result = {}
        videos = []
        url = f'{xurl}/index.php/ajax/suggest?mid=1&wd={key}&limit=50'
        mxurl = 'https://www.mtyy1.com/voddetail/'
        detail = requests.post(url=url, headers=headerx)
        data = detail.json()
        for item in data.get("list", []):
            id = mxurl + str(item["id"]) + '.html'
            name = item["name"]
            pic = item["pic"]

            video = {
                "vod_id": id,
                "vod_name": '集多📽️' + name,
                "vod_pic": pic
            }
            videos.append(video)

        result['list'] = videos
        result['page'] = page
        result['pagecount'] = 60
        result['limit'] = 30
        result['total'] = 999999
        return result

    def searchContent(self, key, quick, pg="1"):
        return self.searchContentPage(key, quick, '1')

    def localProxy(self, params):
        if params['type'] == "m3u8":
            return self.proxyM3u8(params)
        elif params['type'] == "media":
            return self.proxyMedia(params)
        elif params['type'] == "ts":
            return self.proxyTs(params)
        return None









