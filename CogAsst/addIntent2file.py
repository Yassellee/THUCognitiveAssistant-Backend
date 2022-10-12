import codecs
import csv
import manage       


file_path = 'intent2db.csv'

def addIntent2file():
    file = open(file_path, 'a+', encoding='utf-8', newline='')
    csv_writer = csv.writer(file)
    csv_writer.writerow([f'Name', 'Entity', 'Features'])
    csv_writer.writerow(['体育馆预约', "{'体育馆': ['体育馆名称', '体育场地'], 'datetimeV2': 0}", "{'体育馆名称':['综体', '西体', '气膜馆', '体育馆' ,'西湖游泳馆', '游泳馆']}"])
    csv_writer.writerow(['图书馆选座', "{'选座': ['图书馆名称', '图书馆座位'], 'datetimeV2': 0}", "{'图书馆名称':['北馆', '西馆', '文图', '法图' ,'美术图书馆', '金融图书馆']}"])
    csv_writer.writerow(['微信发消息', "{'微信': ['消息内容'], 'personName': 0}", "{}"])
    csv_writer.writerow(['微信发红包', "{'微信': [], 'personName': 0, 'money': 0}", "{}"])
    csv_writer.writerow(['微信视频通话', "{'微信': [], 'personName': 0}", "{}"])
    csv_writer.writerow(['微信语音通话', "{'微信': [], 'personName': 0}", "{}"])
    csv_writer.writerow(['美团打开共享单车', "{'美团': ['单车编号']}", "{}"])
    csv_writer.writerow(['报修', "{'报修': []}", "{}"])
    csv_writer.writerow(['支付宝充话费', "{'支付宝': [], 'personName': 0, 'money': 0}", "{}"])
    csv_writer.writerow(['支付宝查看健康码', "{'支付宝': []}", "{}"])
    csv_writer.writerow(['支付宝转账', "{'支付宝': [], 'personName': 0, 'money': 0}", "{}"])
    csv_writer.writerow(['微信新建标签', "{'微信': ['标签'], 'personName': 0}", "{}"])
    csv_writer.writerow(['校医院挂号', "{'挂号': ['科室'], 'datetimeV2': 0}", "{'科室':['发热门诊', '内科', '外科', '眼科' ,'耳鼻喉科', '中医科', '妇科', '保健科', '针灸科', '儿科', '理疗科', '结核科', '核酸检测']}"])
    csv_writer.writerow(['微信清空聊天记录', "{'微信': [], 'personName': 0}", "{}"])
    csv_writer.writerow(['淘宝清空购物车', "{'淘宝': []}", "{}"])
    csv_writer.writerow(['申请出校', "{'出校': ['班级', '事由类型', '事由描述', '往来地点'], 'datetimeV2': 0, 'phoneNumber': 0}", "{'事由类型':['出校科研', '出校就医', '出校实习', '出校其他']}"])
    csv_writer.writerow(['电表充值', "{'电费': [], 'money': 0}", "{}"])
    csv_writer.writerow(['淘宝询问客服', "{'淘宝': ['店铺名称', '消息内容']}", "{}"])
    csv_writer.writerow(['淘宝进入店铺', "{'淘宝': ['店铺名称']}", "{}"])
    csv_writer.writerow(['None', "{}", "{}"])
    file.close()


addIntent2file()
