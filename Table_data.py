# -*- coding: utf-8 -*-
import os
import random
import time
import sys

# reload(sys)
# sys.setdefaultencoding('utf-8')

boolean_list = ['True', 'False']

country = ['China', '中国', 'Afghanistan', '阿富汗', 'Anguilla', '安圭拉', 'Armenia', '亚美尼亚', 'Argentina', '阿根廷', 'Australia',
           ' 澳大利亚', 'Austria', '奥地利'
    , 'Bolivia', '玻利维亚', 'Brazil', '巴西', 'Central African Republic', '中非共和国']

city = ['BeiJing', 'Nanjing', 'Dalian', 'Wuhan', 'Hebei', 'Anhui', 'Birmingham', 'Montgomery', '蒙哥马利', 'Mobile', '莫比尔县',
        'Anniston', '安尼斯顿', 'Gadsden',
        '加兹登', 'Scottsdale', '斯科茨代尔']

localtion = ['chaoyang', 'yuhua', 'xuancheng', 'changan', 'jiangning', 'Tempe', 'Buckeye', 'Chandler', 'ElDorado',
             'Jonesboro', 'PaineBluff', 'LittleRock', 'Fayetteville', 'FortSmith']

xml_label_list = ['bean', 'property', 'type', 'book', 'CATALOG', 'breakfast_menu']

xml_title_list = ['food', 'PLANT', 'script', 'sharp', 'name_label', 'weather', 'TITLE']

xml_element_list = ['COUNTRY', 'callNumber', 'identityID', 'SEX', 'AccountID', 'balance', 'car', 'phone', 'url']

car_list = ['奥迪Q3', '奥迪Q5L', '奥迪A3', '奥迪A8', '奥迪Q5(进口)', '阿斯顿·马丁DB11', '阿斯顿·马丁One-77', '宝马2系多功能旅行车',
            '宝马X5新能源', '宝马5系欧版', '宝马i8', '奔驰GLS AMG', '保时捷918欧版', '丰田凯美瑞', '宾利添越PHEV', '宾利慕尚美规版']

phone_list = ['三星GALAXY Note 10（8GB/256GB/全网通）', '华为Mate 20 X（8GB/256GB/全网通/5G版）', '魅族16s Pro（8GB/128GB/全网通）',
              '三星GALAXY A80（8GB/128GB/全网通）',
              '黑鲨游戏手机2 Pro（12GB/256GB全网通）', '一加7 Pro（12GB/256GB/全网通）', '华为P30（6GB RAM/全网通）', '三星Galaxy S10(8+128)',
              '三星Galaxy S10+(8+12)',
              '三星Galaxy Note9', '三星Galaxy Note8(64G)', '苹果iPhone XS Max（全网通）', '苹果iPhone XR（全网通）', '苹果iPhone X（全网通）',
              '苹果iPhone XS（全网通）',
              '苹果iPhone 11（全网通）', '苹果iPhone 8 Plus（全网通）', '苹果iPhone 8（全网通）']

Charset_list = ['UTF-8', 'UTF-16', 'ISO-8859-1', 'GB2312', 'GBK', 'Unicode', 'GB18030', 'BIG5']


# 随机获取列表中的值
def random_list(list_val):
    if isinstance(list_val, list):
        random_val = list_val[random.randint(0, len(list_val) - 1)]
        return random_val
    else:
        print("Not list,please import list val!!!")


# 生成URL字段

def url_data():
    url = '"' + str(random.randint(1, 256)) + '.' + str(random.randint(1, 256)) + '.' + str(
        random.randint(1, 256)) + '.' + str(random.randint(1, 256)) + ':' + \
          str(random.randint(0, 99999)).zfill(4) + '/' + random_str(random.randint(6, 8)) + '/' + random_str(
        random.randint(6, 8)) + '/' + \
          random_str(random.randint(6, 8)) + '&amp;' + random_str(random.randint(2, 4)) + '=' + random_str(
        random.randint(6, 10)) + '?' + \
          random_str(random.randint(2, 4)) + '=' + china_context(5, 'context') + '&amp;' + 'Charset' + '=' + \
          Charset_list[random.randint(0, len(Charset_list) - 1)] + '"'

    return url


# 性别
def sex_ran():
    sex_list = ['男', '女']
    sex = sex_list[random.randint(0, len(sex_list) - 1)]
    return sex


# 随机中文
def china_context(num, a):
    # 名字列表
    N = ['嘉', '琼', '桂', '娣', '叶', '璧', '璐', '娅', '琦', '晶', '妍', '茜', '秋', '珊', '莎', '锦', '黛', '青', '倩', '婷', '姣', '婉',
         '娴', '瑾', '颖', '露', '瑶', '怡', '婵', '雁', '蓓', '纨', '仪', '荷', '丹', '蓉', \
         '眉', '君', '琴', '蕊', '薇', '菁', '梦', '岚', '苑', '婕', '馨', '瑗', '琰', '韵', '融', '园', '艺', '咏', '卿', '聪', '澜', '纯',
         '毓', '悦', '昭', '冰', '爽', '琬', '茗', '羽', '希', '宁', '欣', '飘', '育', '滢', '馥', '筠', '柔', '竹', '霭', \
         '凝', '晓', '欢', '霄', '枫', '芸', '菲', '寒', '伊', '亚', '宜', '可', '姬', '舒', '影', '荔', '枝', '思', '丽', '秀', '娟', '英',
         '华', '慧', '巧', '美', '娜', '静', '淑', '涛', '昌', '进', '林', '有', '和', '彪', '博', '诚', '先', '敬', '震', \
         '振', '壮', '会', '群', '豪', '心', '邦', '承', '乐', '绍', '功', '松', '善', '厚', '庆', '磊', '民', '友', '裕', '河', '哲', '江',
         '超', '浩', '亮', '政', '谦', '亨', '奇', '固', '之', '轮', '翰', '朗', '伯', \
         '宏', '言', '若', '鸣', '朋', '斌', '梁', '栋', '维', '启', '克', '伦', '惠', '珠', '翠', '雅', '芝', '玉', '萍', '红', '娥', '玲',
         '芬', '芳', '燕', '彩', '春', '菊', '勤', '珍', '贞', '莉', '兰', '凤', '洁', '梅', '琳', '素', '云', \
         '莲', '真', '环', '雪', '荣', '爱', '妹', '霞', '香', '月', '莺', '媛', '艳', '瑞', '凡', '佳']

    # 常用汉字列表

    C = ['春', '集', '丈', '木', '研', '班', '普', '导', '顿', '睡', '展', '跳', '获', '艺', '六', '波', '察', '群', '皇', '段', '急', '庭',
         '创', '区', '奥', '器', '谢', '弟', '店', '否', '害', '草', '排', '背', '止', \
         '组', '州', '朝', '封', '睛', '板', '角', '况', '曲', '馆', '育', '忙', '质', '河', '续', '哥', '呼', '若', '推', '境', '遇', '雨',
         '标', '姐', '充', '围', '案', '伦', '护', '冷', '警', '贝', '著', '雪', '索', '剧', '啊', '船', '险', '烟', '依', '斗', \
         '值', '帮', '汉', '慢', '佛', '肯', '闻', '唱', '沙', '局', '伯', '族', '低', '玩', '资', '屋', '击', '速', '顾', '泪', '洲', '团',
         '圣', '旁', '堂', '兵', '七', '露', '园', '牛', '哭', '旅', '街', '劳', '型', '烈', '姑', '陈', '莫', \
         '鱼', '异', '抱', '宝', '权', '鲁', '简', '态', '级', '票', '怪', '寻', '杀', '律', '胜', '份', '汽', '右', '洋', '范', '床', '舞',
         '秘', '午', '登', '楼', '贵', '吸', '责', '例', '追', '较', '职', '属', '渐', '左', '录', '丝', \
         '牙', '党', '继', '托', '赶', '章', '智', '冲', '叶', '胡', '吉', '卖', '坚', '喝', '肉', '遗', '救', '修', '松', '临', '藏', '担',
         '戏', '善', '卫', '药', '悲', '敢', '靠', '伊', '村', '戴', '词', '森', '耳', '差', '短', '祖', '云', \
         '规', '窗', '散', '迷', '油', '旧', '适', '乡', '架', '恩', '投', '弹', '铁', '博', '雷', '府', '压', '超', '负', '勒', '杂', '醒',
         '洗', '采', '毫', '嘴', '毕', '九', '冰', '既', '状', '乱', '景', '席', '珍', '童', '顶', '派', \
         '素', '脱', '农', '疑', '练', '野', '犯', '拍', '征', '坏', '骨', '余', '承', '置', '臓', '彩', '灯', '巨', '琴', '免', '环', '姆',
         '暗', '换', '技', '翻', '束', '增', '忍', '餐', '洛', '塞', '缺', '忆', '判', '欧', '层', '付', '阵', \
         '玛', '批', '岛', '项', '狗', '休', '懂', '武', '革', '良', '恶', '恋', '委', '拥', '娜', '妙', '探', '呀', '营', '退', '摇', '弄',
         '桌', '熟', '诺', '宣', '银', '势', '奖', '宫', '忽', '套', '康', '供', '课', '鸟', \
         '喊', '降', '夏', '困', '刘', '罪', '亡', '鞋', '健', '模', '败', '伴', '守', '挥', '鲜', '财', '孤', '枪', '禁', '恐', '伙', '杰',
         '迹', '妹', '藸', '遍', '盖', '副', '坦', '牌', '江', '顺', '秋', '萨', '菜', '划', '授', '归', '听', \
         '凡', '预', '奶', '雄', '升', '碃', '编', '典', '袋', '莱', '含', '盛', '济', '蒙', '棋', '端', '腿', '招', '释', '介', '烧', '误']

    china_val = ''
    if a == 'name':
        for i in range(num):
            china_val += random.choice(N)
    elif a == 'context':
        for i in range(num):
            # china_val += random.choice(C)
            china_val += C[random.randint(0, len(C) - 1)]


    else:
        print("sry,please import 'name'/'context'!!!")

    return china_val


# 账户ID
def Account_ID():
    accountid = random.randint(100000000, 9999999999999999)
    return accountid


# 随机数
def Random_ID():
    Random_ID = random.randint(200000000, 300000000)
    return Random_ID


# 账户余额
def Balance(a=1):
    balance = str(random.randint(100, 9999999999999999) / a)
    return balance


# 随机英文+字母字符串
def random_str(num):
    H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    str_val = ''
    for i in range(num):
        str_val += random.choice(H)

    return str_val


# 随机小写英文+字母字符串
def random_lower_str(num):
    H = 'abcdefghijklmnopqrstuvwxyz0123456789'

    str_val = ''
    for i in range(num):
        str_val += random.choice(H)

    return str_val


# 随机字符串
def random_spec_str(num):
    H = r'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_=`~-+?><.,:; '

    str_val = ''
    for i in range(num):
        str_val += random.choice(H)

    return str_val


# 随机小写字符串
def random_lowerspec_str(num):
    H = r'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_=`~-+?><.,:;'

    str_val = ''
    for i in range(num):
        str_val += random.choice(H)

    return str_val


# 随机大写字符串
def random_upperspec_str(num):
    H = r'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_=`~-+?><.,:;'

    str_val = ''
    for i in range(num):
        str_val += random.choice(H)

    return str_val


# 年、月、日
def random_time(time):
    if time == 'year':
        time = str(random.randint(1900, 2019)).zfill(4)
    elif time == 'moon':
        time = str(random.randint(1, 12)).zfill(2)
    # 这样编码不规范但是简洁
    elif time == 'day':
        moon = random.randint(1, 12)

        time = str(random.randint(1, 31) if moon in [1, 3, 5, 7, 8, 10, 12] else random.randint(1,
                                                                                                28) if moon == 2 else random.randint(
            0, 30)).zfill(2)
    else:
        print("Not date! Please import 'year'/'moon'/'day'")
    return time


# 用户手机号码
def callNumber():
    number = str(1) + str(random.randint(0, 99)).zfill(2) + str(random.randint(0, 9999)).zfill(4) + \
             str(random.randint(0, 9999)).zfill(4)
    return number


# 用户身份证号码
def identity():
    identityID = str(random.randint(1, 999)).zfill(3) + str(random.randint(0, 999)).zfill(3) + str(
        random_time('year')).zfill(4) \
                 + str(random_time('moon')).zfill(2) + str(random_time('day')).zfill(2) + str(
        random.randint(0, 9999)).zfill(4)
    return identityID


# 邮箱地址
def mail():
    mail_list = ['163', 'QQ', 'GMAIL', '126', 'sina', 'hao123']
    mail = str(random_str(random.randint(6, 15))) + '@' + mail_list[random.randint(0, len(mail_list) - 1)] + '.COM'
    return mail


# 当前13位时间戳
def currentimestamp():
    currentimestamp = int(round(time.time() * 1000))
    return currentimestamp


if __name__ == "__main__":
    # print (china_context(1000,"context"))
    print(random_spec_str(1000))
