# encoding:utf-8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import mysql.connector
# from sshtunnel import SSHTunnelForwarder
# import pymysql



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
        # with SSHTunnelForwarder(
        #         ("47.94.240.242", "22"),
        #         ssh_username="root",
        #         ssh_password="258369@!pkPK",
        #         remote_bind_address=('127.0.0.1', "3306")) as tunnel:
        #     self.conn = pymysql.connect(host='localhost', user="root",
        #                            passwd="lfbbw", db="zhiyuanping",
        #                            port=tunnel.local_bind_port)

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
        elif item['t'] == 'major':
            self.operate_major_info(item)
        elif item['t'] == 'major_detail':
            self.operate_major_detail_info(item)
        elif item['t'] == 'career':
            self.operate_career_info(item)
        elif item['t'] == 'major_enroll':
            self.operate_major_enroll_info(item)
        elif item['t'] == 'enroll_major_select':
            self.operate_enroll_major_select(item)
        elif item['t'] == 'em_enroll_data':
            self.operate_em_enroll_data(item)
        elif item['t'] == 'em_adm_data':
            self.operate_em_adm_data(item)
        elif item['t'] == 'em_detail':
            self.operate_em_detail(item)
        elif item['t'] == 'enroll_unit_list':
            self.operate_enroll_unit_list(item)
        elif item['t'] == 'sch_enroll_rule_info':
            self.operate_sch_enroll_rule_info(item)
        elif item['t'] == 'sch_info_ext':
            self.operate_sch_info_ext(item)
        elif item['t'] == 'sch_enroll_data':
            self.operate_sch_enroll_data(item)
        elif item['t'] == 'major_enroll_data':
            self.operate_major_enroll_data(item)
        elif item['t'] == 'major_enroll_ext_data':
            self.operate_major_enroll_ext_data(item)
        elif item['t'] == 'province_register_config':
            self.operate_province_register_config(item)
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
                  (%s,%s,%s,%s,%s)
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
                  (%s,%s,%s,%s,%s)
                """
        self.cursor.execute(sql, values)
        self.conn.commit()

    # 专业信息
    def operate_major_info(self, item):
        values = (
            item['sid'],
            item['sname'],
            item['cid'],
            item['cname'],
            item['mid'],
            item['mname'],
            item['diploma'],
        )
        sql = """
                  INSERT IGNORE INTO zyp_major_info
                  (sid,sname,cid,cname,mid,mname,diploma)
                  VALUES 
                  (%s,%s,%s,%s,%s,%s,%s)
                """
        self.cursor.execute(sql, values)
        self.conn.commit()

    # 专业详细信息
    def operate_major_detail_info(self, item):
        values = (
            item['mid'],
            item['intro'],
            item['academic_rule'],
            item['degree'],
            item['training_objective'],
            item['training_requirement'],
            item['employment_info'],
            item['main_course'],
            item['knowledge_requirement'],
            item['teaching_practice'],
        )
        sql = """
                  INSERT IGNORE INTO zyp_major_detail_info
                  (mid,intro,academic_rule,degree,training_objective,training_requirement,employment_info,
                  main_course,knowledge_requirement,teaching_practice)
                  VALUES 
                  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """

        self.cursor.execute(sql, values)
        self.conn.commit()

    # 事业信息
    def operate_career_info(self, item):
        values = (
            item['career_id'],
            item['name'],
            item['desc'],
        )
        sql = """
                  INSERT IGNORE INTO zyp_careers_info
                  (career_id,name,`desc`)
                  VALUES 
                  (%s,%s,%s)
                """
        self.cursor.execute(sql, values)
        self.conn.commit()

    # 注册专业信息
    def operate_major_enroll_info(self, item):
        values = (
            item['mid'],
            item['wenli'],
            item['sch_id'],
            item['province_id'],
            item['city_id'],
            item['city_id_desc'],
            item['eu_code'],
            item['stu_province_id'],

            item['diploma_desc'],
            item['diploma_id'],
            item['enroll_group_no'],
            item['eu_id'],
            item['eu_name'],
            item['has_grad_sch'],
            item['independent_college'],
            item['major_diploma_id'],
            item['province_id_desc'],
            item['required_course_desc'],
            item['required_course_num'],
        )
        sql = """
                  INSERT IGNORE INTO zyp_major_enroll_info
                  (mid,wenli,sch_id,province_id,city_id,city_id_desc,eu_code,stu_province_id,
                  diploma_desc,diploma_id,enroll_group_no,eu_id,eu_name,has_grad_sch,independent_college,major_diploma_id,
                  province_id_desc,required_course_desc,required_course_num)
                  VALUES 
                  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                   %s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
        print("----------")
        print(sql)
        self.cursor.execute(sql, values)
        self.conn.commit()

    #
    def operate_enroll_major_select(self, item):
        values = (
            item['batch'],
            item['batch_ex'],
            item['batch_name'],
            item['diploma_id'],
            item['enroll_major_code'],
            item['enroll_major_id'],
            item['enroll_major_name'],
            item['enroll_stage'],
            item['enroll_unit_id'],
            item['major_diploma_id'],
            item['wenli'],
        )
        sql = """
                  INSERT IGNORE INTO zyp_enroll_major_select
                  (batch,batch_ex,batch_name,diploma_id,enroll_major_code,enroll_major_id,enroll_major_name,enroll_stage,
                  enroll_unit_id,major_diploma_id,wenli)
                  VALUES 
                  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
        self.cursor.execute(sql, values)
        self.conn.commit()

    def operate_em_enroll_data(self, item):
        values = (
            item['academic_rule'],
            item['academic_year'],
            item['batch_name'],
            item['enroll_plan_count'],
            item['tuition'],
            item['sch_id'],
            item['major_id'],
            item['enroll_major_id'],
            item['diploma_id'],
            item['major_diploma_id'],
            item['wenli'],
            item['province_id'],
        )
        sql = """
                  INSERT IGNORE INTO zyp_em_enroll_data
                  (academic_rule,academic_year,batch_name,enroll_plan_count,tuition,
                  sch_id,major_id,enroll_major_id,diploma_id,major_diploma_id,wenli,province_id)
                  VALUES 
                  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                  %s,%s)
                """
        self.cursor.execute(sql, values)
        self.conn.commit()

    def operate_em_detail(self, item):
        values = (
            item['batch_name'],
            item['diploma_id'],
            item['enroll_group_no'],
            item['enroll_major_code'],
            item['enroll_major_id'],
            item['enroll_major_name'],
            item['enroll_unit_code'],
            item['enroll_unit_id'],
            item['enroll_unit_name'],
            item['major_id'],
            item['major_logo'],
            item['major_teach_location'],
            item['ncee_type'],
            item['optional_course_desc'],
            item['optional_course_level'],
            item['require_language'],
            item['required_course_desc'],
            item['required_course_level'],
            item['required_course_num'],
            item['sch_id'],
            item['wenli'],
        )
        sql = """
                  INSERT IGNORE INTO zyp_em_detail
                  (batch_name,diploma_id,enroll_group_no,enroll_major_code,
                  enroll_major_id,enroll_major_name,enroll_unit_code,enroll_unit_id,
                  enroll_unit_name,major_id,major_logo,
                  major_teach_location,ncee_type,optional_course_desc,
                  optional_course_level,require_language,required_course_desc,
                  required_course_level,required_course_num,sch_id,wenli)
                  VALUES 
                  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                   %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                   %s)
                """
        self.cursor.execute(sql, values)
        self.conn.commit()

    def operate_em_adm_data(self, item):
        values = (
            item['academic_year'],
            item['admission_count'],
            item['avg_score'],
            item['avg_score_rank'],
            item['batch'],
            item['batch_ex'],
            item['batch_name'],
            item['enroll_group_no'],
            item['max_score'],
            item['max_score_rank'],
            item['min_score'],
            item['min_score_diff'],
            item['min_score_rank'],
            item['major_id'],
            item['enroll_major_id'],
            item['diploma_id'],
            item['major_diploma_id'],
            item['province_id'],
            item['sch_id'],
            item['wenli'],
        )
        sql = """
                  INSERT IGNORE INTO zyp_em_adm_data
                  (academic_year,admission_count,avg_score,avg_score_rank,
                  batch,batch_ex,batch_name,enroll_group_no,max_score,
                  max_score_rank,min_score,min_score_diff,min_score_rank,major_id,
                  enroll_major_id,diploma_id,major_diploma_id,province_id,sch_id,
                  wenli)
                  VALUES 
                  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                   %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
        self.cursor.execute(sql, values)
        self.conn.commit()

    # unit list
    def operate_enroll_unit_list(self, item):
        values = (
            item['enroll_unit_code'],
            item['enroll_unit_id'],
            item['enroll_unit_name'],
            item['stu_province_id'],
            item['sch_id'],
        )
        sql = """
                 INSERT IGNORE INTO zyp_enroll_unit
                 (enroll_unit_code,enroll_unit_id,enroll_unit_name,stu_province_id,sch_id)
                 VALUES 
                 (%s,%s,%s,%s,%s)
               """
        self.cursor.execute(sql, values)
        self.conn.commit()

    # sch_enroll_rule_info
    def operate_sch_enroll_rule_info(self, item):
        values = (
            item['sch_id'],
            item['academic_year'],
            item['enroll_rule_title'],
            item['content'],
        )
        sql = """
                 INSERT IGNORE INTO zyp_sch_rule_info
                 (sch_id,academic_year,enroll_rule_title,content)
                 VALUES 
                 (%s,%s,%s,%s)
               """
        self.cursor.execute(sql, values)
        self.conn.commit()

    # sch_info_ext
    def operate_sch_info_ext(self, item):
        values = (
            item['province_id'],
            item['latest_admission_year'],
            item['latest_enroll_year'],
            item['city_id'],
            item['city_id_desc'],
            item['region_id'],
            item['regioin_id_desc'],
            item['sch_code'],
            item['nation_id'],
            item['sch_id']
        )
        sql = """
                UPDATE zyp_sch_info set province_id = %s,latest_admission_year = %s,latest_enroll_year = %s,city_id = %s,
                city_id_desc = %s,region_id  = %s,regioin_id_desc = %s,sch_code = %s,nation_id = %s where sch_id=%s
            """
        self.cursor.execute(sql, values)
        self.conn.commit()

    def operate_sch_enroll_data(self, item):
        values = (
            item['sch_id'],
            item['enroll_unit_id'],
            item['stu_province_id'],
            item['wenli'],
            item['diploma_id'],
            item['academic_year'],
            item['admission_count'],
            item['admission_ratio'],
            item['avg_score'],
            item['avg_score_diff'],
            item['avg_score_equal'],
            item['avg_score_rank'],
            item['bao_lower_boundary_rank'],
            item['batch'],
            item['batch_ex'],
            item['batch_name'],
            item['chong_lower_boundary_rank'],
            item['course_level_order'],
            item['cwbn_type'],
            item['fluctuation'],
            item['match_select_course_all'],
            item['max_score'],
            item['max_score_diff'],
            item['max_score_equal'],
            item['max_score_rank'],
            item['min_score'],
            item['min_score_diff'],
            item['min_score_equal'],
            item['min_score_rank'],
            item['optional_course_desc'],
            item['predict_rank'],
            item['required_course_desc'],
            item['sch_teach_location'],
            item['special_policy'],
            item['special_policy_tags'],
            item['special_policy_tags_desc'],
            item['wen_lower_boundary_rank'],
        )
        sql = """
                INSERT IGNORE INTO zyp_sch_enroll_data
                 (sch_id,enroll_unit_id,stu_province_id,wenli,diploma_id,academic_year,
                 admission_count,admission_ratio,avg_score,avg_score_diff,avg_score_equal,
                 avg_score_rank,bao_lower_boundary_rank,batch,batch_ex,batch_name,
                 chong_lower_boundary_rank,course_level_order,cwbn_type,
                 fluctuation,match_select_course_all,max_score,max_score_diff,
                 max_score_equal,max_score_rank,min_score,min_score_diff,min_score_equal,
                 min_score_rank,optional_course_desc,predict_rank,required_course_desc,
                 sch_teach_location,special_policy,special_policy_tags,
                 special_policy_tags_desc,wen_lower_boundary_rank)
                 VALUES 
                 (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                 %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                 %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                 %s,%s,%s,%s,%s,%s,%s)
              """
        self.cursor.execute(sql, values)
        self.conn.commit()

    def operate_major_enroll_data(self, item):
        values = (
            item['stu_province_id'],
            item['wenli'],
            item['enroll_year'],
            item['enroll_unit_id'],
            item['batch'],
            item['diploma_id'],
            item['year'],
            item['major_id'],
            item['enroll_major_code'],
            item['enroll_major_id'],
            item['academic_year'],
            item['admission_year'],
            item['batch_ex'],
            item['enroll_category'],
            item['enroll_mode'],
            item['enroll_stage'],
            item['academic_rule'],
            item['admission_count'],
            item['avg_score'],
            item['avg_score_diff'],
            item['avg_score_rank'],
            item['enroll_major_name'],
            item['enroll_plan_count'],
            item['max_score'],
            item['max_score_diff'],
            item['max_score_rank'],
            item['min_score'],
            item['min_score_diff'],
            item['min_score_rank'],
            item['tuition']
        )
        sql = """
                INSERT IGNORE INTO zyp_major_enroll_data
                 (stu_province_id,wenli,enroll_year,enroll_unit_id,batch,diploma_id,year,major_id,
                 enroll_major_code,enroll_major_id,academic_year,admission_year,batch_ex,
                 enroll_category,enroll_mode,enroll_stage,academic_rule,admission_count,avg_score,
                 avg_score_diff,avg_score_rank,enroll_major_name,enroll_plan_count,max_score,
                 max_score_diff,max_score_rank,min_score,min_score_diff,min_score_rank,tuition)
                 VALUES 
                 (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                 %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                 %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
              """

        self.cursor.execute(sql, values)
        self.conn.commit()

    def operate_major_enroll_ext_data(self, item):
        values = (
            item['stu_province_id'],
            item['sch_id'],
            item['enroll_unit_id'],
            item['diploma_id'],
            item['batch'],
            item['wenli'],
            item['enroll_year'],
            item['enroll_plan_count'],
            item['enroll_unit_code'],
            item['batch_ex'],
            item['enroll_category'],
            item['enroll_mode'],
            item['enroll_stage'],
            item['enroll_declare'],
            item['optional_course_desc'],
            item['optional_course_level'],
            item['required_course_desc'],
            item['required_course_level'],
        )
        sql = """
                        INSERT IGNORE INTO zyp_major_enroll_ext_data
                         (stu_province_id,sch_id,enroll_unit_id,diploma_id,batch,
                         wenli,enroll_year,enroll_plan_count,enroll_unit_code,batch_ex,
                         enroll_category,enroll_mode,enroll_stage,enroll_declare,optional_course_desc,
                         optional_course_level,required_course_desc,required_course_level)
                         VALUES 
                         (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                         %s,%s,%s,%s,%s,%s,%s,%s
                         )
                      """

        self.cursor.execute(sql, values)
        self.conn.commit()

    def operate_province_register_config(self, item):
        values = (
            item['province_id'],
            item['enroll_category'],
            item['bk_max_score'],
            item['bk_rank_type'],
            item['course_info'],
            item['course_level_info'],
            item['diploma_type'],
            item['max_score'],
            item['need_course'],
            item['need_course_level'],
            item['need_diploma'],
            item['need_wenli'],
            item['province_score_has_publish'],
            item['rank_type'],
            item['ysw_max_score'],
            item['zk_max_score'],
            item['zk_rank_type'],
        )
        sql = """
                                INSERT IGNORE INTO zyp_province_register_config
                                 (province_id,enroll_category,bk_max_score,bk_rank_type,course_info,course_level_info,
                                 diploma_type,max_score,need_course,need_course_level,need_diploma,need_wenli,
                                 province_score_has_publish,rank_type,ysw_max_score,zk_max_score,zk_rank_type)
                                 VALUES 
                                 (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                                 %s,%s,%s,%s,%s,%s,%s
                                 )
                              """

        self.cursor.execute(sql, values)
        self.conn.commit()



    # def close_spider(self):
    #     self.cursor.close()
    #     self.conn.close()