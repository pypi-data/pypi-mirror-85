import requests
import CRFPP
import json
import os
import re
import cpca
import codecs
import jieba
from .time_format import TimeFormat

pool = None
basedir = os.path.abspath(os.path.dirname(__file__))


unitAndItem_model_dir = basedir+"/model/model_unitAndItem"
loc_model_dir = basedir+"/model/model_loc"
text_model_dir = basedir+"/model/model_text"


class LocDict:
    def __init__(self):
        self.file_dict = "dict.txt"
        self.wdict = {}

    def get_dict(self):
        f = codecs.open(self.file_dict, 'r', encoding='utf-8')
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            line = line.split('\t')
            w = line[0]
            if w:
                if w[0] in self.wdict:
                    value = self.wdict[w[0]]
                    value.append(w)
                    self.wdict[w[0]] = value
                else:
                    self.wdict[w[0]] = [w]

    def fmm(self, sentence):
        n = len(sentence)
        k = 0
        result = []
        while k < n:
            w = sentence[k]
            max_len = 1
            if w in self.wdict:
                words = self.wdict[w]
                t = ''
                for item in words:
                    item_len = len(item)
                    if sentence[k:k + item_len] == item and item_len >= max_len:
                        t = item
                        max_len = item_len
                if t and t not in result:
                    for i in range(k, k+max_len):
                        result.append(i)
            k = k + max_len
        return result


class BiddingExtract(object):
    """加载模型，并从文本和标题中提取结果

    Attributes:
        unitAndItem_tagger: 从标题中提取招标单位和招标物品的模型的tagger
        loc_tagger: 从标题中提取招标地点的模型的tagger
        text_tagger: 从文本中提取各类标签的模型的tagger
        model_type: 当前对象使用的哪个模型

    """
    def __init__(self, model_type):
        self.unitAndItem_tagger = CRFPP.Tagger("-m " + unitAndItem_model_dir)
        self.loc_tagger = CRFPP.Tagger("-m " + loc_model_dir)
        self.text_tagger = CRFPP.Tagger("-m " + text_model_dir)
        self.model_type = model_type
        self.dict = LocDict()

    def parse_multi_feature(self, content):
        tagger = self.loc_tagger
        fun_format = self.text_format
        self.dict.get_dict()
        loc_indexes = self.dict.fmm(content)
        tagger.clear()
        for i in range(len(content)):
            word = content[i]
            if i in loc_indexes:
                tagger.add(word + '\t' + 'Y\t')
            else:
                tagger.add(word + '\t' + 'N\t')
        tagger.parse()
        size = tagger.size()
        xsize = tagger.xsize()
        ner_tag = []
        label = ''
        words = ''
        for i in range(0, size):
            for j in range(0, xsize-1):
                char = tagger.x(i, j)
                tag = tagger.y2(i)
                if tag[0] == 'B':
                    label = re.sub('B_', '', tag)
                    words = char
                elif tag[0] == 'M':
                    words += char
                elif tag[0] == 'E':
                    words += char
                    ner_tag.append((words, label))
                    label = ''
                    words = ''
                else:
                    continue
        res = fun_format(ner_tag)
        return res

    def parse(self, content):
        """
        将模型输出的结果转换成标准化输出

        Returns:
            dict: 标准化的输出结果
        """
        if self.model_type == "title_unitAndItem":
            tagger = self.unitAndItem_tagger
            fun_format = self.sample_format
        elif self.model_type == "title_loc":
            tagger = self.loc_tagger
            fun_format = self.text_format
        else:
            tagger = self.text_tagger
            fun_format = self.text_format
        tagger.clear()
        for word in content:
            if word:
                tagger.add(word)
        tagger.parse()
        size = tagger.size()
        xsize = tagger.xsize()
        ner_tag = []
        label = ''
        words = ''
        for i in range(0, size):
            for j in range(0, xsize):
                char = tagger.x(i, j)
                tag = tagger.y2(i)
                if tag[0] == 'B':
                    label = re.sub('B_', '', tag)
                    words = char
                elif tag[0] == 'M':
                    words += char
                elif tag[0] == 'E':
                    words += char
                    ner_tag.append((words, label))
                    label = ''
                    words = ''
                else:
                    continue
        res = fun_format(ner_tag)
        return res

    def sample_format(self, res):
        """
        将模型的结果进行简单去重，方式就是set取1
        :param res:
        :return:
        """
        dataset = dict()
        for item in res:
            v = item[0]
            k = item[1]
            if k in dataset:
                dataset[k].append(v)
            else:
                dataset[k] = [v]
        for key in dataset:
            dataset[key] = list(set(dataset[key]))[0]
        return dataset

    def text_format(self, res):
        """
        文本处理模型的格式化输出，将解析的结果进行格式化输出，包括：
        label去重，同一个标签只输出一个结果；
        地址信息只输出省和市
        """
        dataset = self.sample_format(res)

        # 将时间进行格式化
        if "bidding_start_time" in dataset:
            dataset['bidding_start_time']=TimeFormat.time_normalization(dataset['bidding_start_time'])

        if "bidding_deadline" in dataset:
            dataset['bidding_deadline']=TimeFormat.time_normalization(dataset['bidding_deadline'])

        # 对金额进行格式化
        if 'bidding_budget' in dataset:
            dataset['bidding_budget']=self.money_format(dataset['bidding_budget'])
        if 'bidded_money' in dataset:
            dataset['bidded_money']=self.money_format(dataset['bidded_money'])

        # 对招标编号进行格式化
        if 'bidding_no' in dataset:
            dataset['bidding_no'] = dataset['bidding_no'].strip('：').strip('号').strip(':')

        return dataset

    def money_format(self, my):
        """
        将识别的金额进行格式化转换，转成以元为单位
        :param my:
        :return:
        """
        re_num = re.compile('\d+(\.\d+)?')
        try:
            if '亿万元' in my or '亿万' in my:
                my = re_num.search(my).group()
                my = float(my)*100000000
            elif '千万元' in my or '千万' in my:
                my = re_num.search(my).group()
                my = float(my)*10000000
            elif '百万元' in my or '百万' in my:
                my = re_num.search(my).group()
                my = float(my)*1000000
            elif '万元' in my or '万' in my:
                my = re_num.search(my).group()
                my = float(my)*10000
            else:
                my = re_num.search(my).group()
                my = float(my)
        except:
            my = None
        return my


class ZbNer(object):
    """分别得出文本和标题模型的结果，并融合

        Attributes:
            text_model: 文本模型，从text中提取实体
            title_unitAndItem_model: 从标题中提取招标单位和招标物
            title_loc_model： 从标题中提取招标地点

    """
    def __init__(self, text_model, title_loc_model, title_unitAndItem_model):
        self.text_model = text_model
        self.title_unitAndItem_model = title_unitAndItem_model
        self.title_loc_model = title_loc_model

    def get_loc(self, address):
        """
        调用一个网络接口进行地址解析，得到省和市的信息；

        Args:
            address(str): 从语料中提取的位置信息

        Returns:
            dict: {"province":"xxx", "city":"xxx"}
        """
        cpca_text = [address.strip()]
        df = cpca.transform(cpca_text)
        province = df.loc[0, "省"]
        city = df.loc[0, "市"]
        data = dict()
        data["province"] = province
        data["city"] = city
        return data

    # def loc_format(self, data):
    #     """对地址省、市进行标准化输出
    #     把文本中抽到的所有address先通过loc_resolution方法转换成xx省xx市， 然后再选用频率最高的省市作为结果，并标准化输出
    #
    #     Args:
    #         data (list(str)): 从文本中抽出的所有address
    #
    #     Returns:
    #         dict: {'province': province, 'city': city}
    #
    #     """
    #     tmp = dict()
    #     for address in data:
    #         loc_res = self.loc_resolution(address)
    #         if loc_res:
    #             province = loc_res['province']
    #             city = loc_res['city']
    #             key = (province, city)
    #             tmp[key] = tmp.get(key, 0)+1
    #     if tmp:
    #         tmp = sorted(tmp.items(), key=lambda x: x[1], reverse=True)
    #         province = tmp[0][0][0]
    #         city = tmp[0][0][1]
    #         return {'province': province, 'city': city}
    #     else:
    #         return None

    def raw_text_res(self, text):
        # 将位置字段替换为“location”，方便以后处理
        text = re.sub('\s+', u'Ж', text)
        text_res = self.text_model.parse(text)
        if "bidding_address" in text_res:
            text_res["location"] = text_res["bidding_address"]
            text_res.pop("bidding_address")
        return text_res

    def raw_title_res(self, title):
        # 合并loc和unit模型结果，将位置字段替换为“location”，方便以后处理
        title_loc_res = self.title_loc_model.parse_multi_feature(title)
        title_unitAndItem_res = self.title_unitAndItem_model.parse(title)
        if "bidding_location\r" in title_loc_res:
            title_loc_res["location"] = title_loc_res["bidding_location\r"]
            title_loc_res.pop("bidding_location\r")
        title_loc_res.update(title_unitAndItem_res)
        return title_loc_res

    def standard_res(self, raw_res):
        # 返回经过地址解析的结果
        standard_res = raw_res
        if "location" in raw_res:
            standard_res["location"] = self.get_loc(raw_res["location"])
        return standard_res

    def fuse(self, text, title):
        text_res = self.raw_text_res(text)
        title_res = self.raw_title_res(title)
        # 大部分都以文本中提取内容为主
        fuse_res = text_res
        fuse_res['location'] = None
        if "location" in title_res:
            fuse_res["location"] = self.get_loc(title_res['location'])
        else:
            if 'bidding_address' in text_res:
                fuse_res['location'] = self.get_loc(text_res['bidding_address'])
        if "bidding_unit" in title_res and "bidding_unit" not in text_res:
            fuse_res["bidding_unit"] = title_res.get("bidding_unit")
        if "bidding_item" in title_res:
            fuse_res["bidding_product"] = title_res.get("bidding_item")
        return fuse_res

    def cut(self, title_only=False, text_only=False, **corpus):
        # 默认为标题和正文抽取，调用格式为:cut(text=xxx, title=xxx)
        # 若只抽标题，调用格式为:cut(title_only=True, title=xxx)
        # 若只抽正文，调用格式为:cut(text_only=True, text=xxx)
        if title_only:
            raw_res = self.raw_title_res(corpus['title'])
            return self.standard_res(raw_res)
        elif text_only:
            raw_res = self.raw_text_res(corpus['text'])
            return self.standard_res(raw_res)
        else:
            return self.fuse(corpus['text'], corpus['title'])


# 分别实例化文本抽取，标题位置抽取和标题公司招标物抽取对象
# 传入融合模型类中，进行操作
BEText = BiddingExtract("text")
BETitle_loc = BiddingExtract("title_loc")
BETitle_unitAndItem = BiddingExtract("title_unitAndItem")
FM = ZbNer(BEText, BETitle_loc, BETitle_unitAndItem)
zb_ner_extract = FM.cut


def _cut(text, title):
    return FM.cut(text=text, title=title)


def _cut_text_only(text):
    return FM.cut(text_only=True, text=text)


def _cut_title_only(title):
    return FM.cut(title_only=True, title=title)


def enable_parallel(processnum=None):
    global pool, zb_ner_extract, FM
    from multiprocessing import cpu_count
    if os.name == 'nt':
        raise NotImplementedError(
            "jieba: parallel mode only supports posix system")
    else:
        from multiprocessing import Pool
    if processnum is None:
        processnum = cpu_count()
    pool = Pool(processnum)
    zb_ner_extract = _pcut


def _pcut(text_only=False, title_only=False, **corpus):
    if text_only:
        result = pool.map(_cut_text_only, corpus['text'])
    elif title_only:
        result = pool.map(_cut_title_only, corpus['title'])
    else:
        result = pool.starmap(_cut, zip(corpus['text'], corpus['title']))
    return result


def test():
    with open("data/test_title.txt", 'r', encoding="utf-8") as titles:
        test_title = titles.readlines()
    with open("data/test_text.txt", 'r', encoding="utf-8") as texts:
        test_text = texts.readlines()
    test_title = "华润雪花啤酒(安徽)有限公司六安工厂ЖD线增加标准瓶检测回流带、A线卸罐垛机垛位公告"
    test_text = "华润雪花啤酒(安徽)有限公司六安工厂ЖD线增加标准瓶检测回流带、A线卸罐垛机垛位公告Ж寻源公告公告编号:XHXYGG202009090103一、采购项目基本情况采购人:华润雪花啤酒(安徽)有限公司采购项目编号:XHCGXY202009090103采购项目名称:六安工厂ЖD线增加标准瓶检测回流带、A线卸罐垛机垛位采购内容和范围:1)Ж包装A线卸罐垛机新增垛位Ж负责在包装A线卸罐垛机的上垛区始端增加1个转向输垛机,在转向输送垛机后增加4个1.6米链条垛板输送机;Ж负责提供配套使用的变频器、光电等电器元件的提供,详见附件1.3:报价单;1.4:设备平面布置图;Ж负责上述设备的运输、安装、调试及售后服务。2)Ж包装D线增加标准瓶检测回流带Ж负责包装D线验瓶机后增加标准瓶检测回流带,包括:输瓶机、磁性弯头、防尘罩、减速机等,详见1.3:报价单、1.4:设备平面布置图;负责上述设备的运输、安装、调试及售后服务。质保期:不低于一年。二、供应商资格要求Ж资审方式:资格后审供应商必须具备的资格和要求:三证合一,具备机械设备加工能力三、采购文件的获取采购文件在华润集团守正电子招标平台发布,不再另行线下提供纸质采购文件,凡有意参与者可在本公告期间自行登陆守正平台查看和下载采购文件。四、响应文件的提交响应文件提交/报价截止时间:Ж2020-09-17Ж12:00:00Ж(北京时间,若有变化另行通知)。响应文件提交/报价方式:在响应文件提交/报价截止时间前,通过华润集团守正电子招标平台提交电子响应文件或报价,逾期提交将被拒收,五、采购人联系方式Ж联系人:刘婷婷电话:13003058989邮箱:liutingting2@crb.cn六、采购明细行号物品/项目名称单位需求数量补充说明1D线增加标准瓶检测回流带、A线卸罐垛机垛位套2具体详见附件七、采购说明具体内容详见附件Ж八、其它事项1.本公告在华润集团守正电子招标平台(https://szecp.crc.com.cn)上公开发布。2.本项目采购通过守正平台线上进行,供应商需注册华润集团守正电子招标平台,按需办理CA电子钥匙(用于需插CA锁报价的项目),通过平台进行响应文件的递交或报价,具体操作步骤可查阅网站首页帮助中心的操作手册,也可以联系守正客服。3.答疑澄清、通知等文件一经在华润集团守正电子招标平台发布,视为已发放给相应供应商(发放时间即为发出时间),请随时关注华润集团守正电子招标平台发布的相关信息,并及时查阅和处理。"
    res = zb_ner_extract(text=test_text, title=test_title)
    print(res)


if __name__ == "__main__":
    test()
