# encoding:utf-8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import mysql.connector
# from sshtunnel import SSHTunnelForwarder


class SpidermanPipeline:

    config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': '111111',
        'port': 3306,
        'database': 'zhiyuanping',
        'charset': 'utf8'
    }

    def __init__(self):
        # server = SSHTunnelForwarder(
        #     ssh_address_or_host=('47.94.240.242', 22),  # 指定ssh登录的跳转机的address
        #     ssh_username='root',  # 跳转机的用户
        #     ssh_password='258369@!pkPK',  # 跳转机的密码
        #     remote_bind_address=('172.17.230.236', 3306))
        # server.start()

        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if item['t'] == 'sch_info':
            self.operate_sch_info(item)
        elif item['t'] == 'sch_detail_info':
            self.operate_sch_detail_info(item)
        elif item['t'] == 'sch_celebrity_info':
            self.operate_celebrity_info(item)
        elif item['t'] == 'discipline_evaluation':
            self.operate_discipline_evaluation_info(item)
        elif item['t'] == 'lib_evaluation':
            self.operate_lib_evaluation_info(item)
        return item

    def operate_sch_info(self, item):
        values = (
            item['sch_id'],
            item['name'],
            item['english_name'],
            item['logo'],
            item['diploma'],
            item['run_type'],
            item['type'],
            item['tag'],
            item['grad'],
            item['location'],
            item['competent'],
            item['create_year'],
            item['province'],
        )
        sql = """
                  INSERT IGNORE INTO zyp_sch_info
                  (sch_id,`name`,english_name,logo,diploma,run_type,`type`,tag,grad,location,competent,create_year,province)
                  VALUES 
                  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
        self.cursor.execute(sql, values)
        self.conn.commit()

    def operate_sch_detail_info(self, item):
        values = (
            item['sch_faculty_info'],
            item['sch_id'],
            item['sch_intro'],
            item['sch_address'],
            item['sch_tel_num'],
            item['sch_female_ratio'],
            item['sch_master_ratio'],
            item['sch_abroad_ratio'],
            item['sch_scholarship'],
            item['sch_fellowship'],
            item['canteen_desc'],
            item['stu_dorm_desc'],
        )
        sql = """
                  INSERT IGNORE INTO zyp_sch_detail_info
                  (sch_faculty_intro,sch_id,sch_intro,sch_address,sch_tel_num,sch_female_ratio,sch_master_ratio,sch_abroad_ratio,sch_scholarship,sch_fellowship,canteen_desc,stu_dorm_desc)
                  VALUES 
                  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
        self.cursor.execute(sql, values)
        self.conn.commit()

    # 知名校友
    def operate_celebrity_info(self, item):
        values = (
            item['sch_id'],
            item['celebrity_name'],
            item['celebrity_desc'],
        )
        sql = """
                  INSERT IGNORE INTO zyp_sch_celebrity_info
                  (sch_id,celebrity_name,celebrity_desc)
                  VALUES 
                  (%s,%s,%s)
                """
        self.cursor.execute(sql, values)
        self.conn.commit()

    # 重点学科
    def operate_discipline_evaluation_info(self, item):
        values = (
            item['sch_id'],
            item['obj_id'],
            item['obj_name'],
            item['obj_num'],
            item['obj_list'],
        )
        sql = """
                  INSERT IGNORE INTO zyp_sch_discipline_evaluation_info
                  (sch_id,obj_id,obj_name,obj_num,obj_list)
                  VALUES 
                  (%s,%s,%s)
                """
        self.cursor.execute(sql, values)
        self.conn.commit()

    # 特色培养
    def operate_lib_evaluation_info(self, item):
        values = (
            item['sch_id'],
            item['obj_id'],
            item['obj_name'],
            item['obj_num'],
            item['obj_list'],
        )
        sql = """
                  INSERT IGNORE INTO zyp_sch_lib_evaluation_info
                  (sch_id,obj_id,obj_name,obj_num,obj_list)
                  VALUES 
                  (%s,%s,%s)
                """
        self.cursor.execute(sql, values)
        self.conn.commit()

    # def close_spider(self):
    #     self.cursor.close()
    #     self.conn.close()