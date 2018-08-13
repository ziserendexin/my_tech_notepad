# -*- coding: utf-8 -*-
import time

from redis import StrictRedis
from ziyan.ziyan_main import Command, Check, Handler

from lib.AK_process import *
from lib.ak import AKClient

log = Logger('plugins')


class MyCommand(Command):
    def __init__(self, configuration):
        super(MyCommand, self).__init__(configuration=configuration)
        self.cmd_conf = configuration['user_conf']['command']

        pass

    def user_create_command(self):
        """
        put your command here to activate the request data logic.

        :return: cmd, this variable will be send to user_check as a command parameter.
        """
        cmds = self.cmd_conf['commands']
        return cmds


class MyCheck(Check):
    def __init__(self, configuration):
        self.check_conf = configuration['user_conf']['check']

        self.ak = AKClient(self.check_conf['ak'])
        self.ak.connect()
        self.error_counts = 0
        super(MyCheck, self).__init__(configuration=configuration)

    def user_check(self, command):
        """

        :param command: user defined parameter.
        :return: the data you requested.
        """
        data = dict()
        good_working = True

        try:
            error_data = self.query_dyno_error()
            data.update(error_data)
        except Exception as e:
            log.error(e)
            log.error('cant request error data.')
            good_working = True
            self.error_counts += 1

        if good_working:
            try:
                for each_command in command:
                    data.update(self.ak.query(each_command.encode()))
                yield data

            except Exception as e:
                log.error('can\'t request data')
                log.error(e)
                self.error_counts += 1
                yield None
        else:
            yield None

        if self.error_counts > 10:
            log.debug('sleep for a while, 300s')
            time.sleep(300)
            try:
                self.reconnect_ak()
                self.error_counts = 0
            except:
                pass

    def query_dyno_error(self):
        """
        use ASTF command to query dyno error.
    
        if code == ASTF: text = ''
        if code == 1123(some number), use AFLT　to get corresponding text.
    
        :return: dict {'ASTF'：{'code':xxx, 'text':yyy}} 
        """

        # get error code with ASTF
        error_code_list = self.ak.query('ASTF')['ASTF'].split(',')

        # if code is ASTF
        if error_code_list[0] == 'ASTF':
            error_data = {'ASTF': {'Code': 'ASTF', 'Text': ''}}
            return error_data

        # is code is number
        else:
            details = self.connect_error(error_code_list)
            error_data = {'ASTF': details}
            return error_data

    def connect_error(self, error_code_list):
        error_code_str = '|'.join(error_code_list)
        text_list = []
        for each in error_code_list:
            text = self.ak.query('AFLT ' + each)['AFLT ' + each]
            text_list.append(text)
        text_str = '|'.join(text_list)
        return {'Code': error_code_str, 'Text': text_str}

    def reconnect_ak(self):
        del self.ak

        self.ak = AKClient(self.check_conf['ak'])
        self.ak.connect()


class MyHandler(Handler):
    def __init__(self, configuration):
        super(MyHandler, self).__init__(configuration=configuration)
        self.myredis = self.get_a_redis(configuration['sender']['redis'])
        self.process_functions = {'ASIE': process_asie,
                                  'AFAN': process_afan,
                                  'AGST': process_agst,
                                  'AKON': process_akon,
                                  'ASTZ': process_astz,
                                  'AVFI': process_avfi,
                                  'AWRT': process_awrt,
                                  'ASTF': process_astf}

    def user_handle(self, raw_data):
        """
        用户须输出一个dict，可以填写一下键值，也可以不填写
        timestamp， 从数据中处理得到的时间戳（整形?）
        tags, 根据数据得到的tag
        data_value 数据拼接形成的 list 或者 dict，如果为 list，则上层框架
         对 list 与 field_name_list 自动组合；如果为 dict，则不处理，认为该数据
         已经指定表名
        measurement 根据数据类型得到的 influxdb表名

        e.g:
        list:
        {'data_value':[list] , required
        'tags':[dict],        optional
        'measurement',[str]   optional
        'timestamp',int}      optional

        dict：
        {'data_value':{'fieldname': value} , required
        'tags':[dict],        optional
        'measurement',[str]   optional
        'timestamp',int}      optional
        
        :param raw_data: 
        :return: 
        """
        # exmple.
        # 数据经过处理之后生成 value_list
        # data_value_list = [raw_data]
        #
        # tags = {'user_defined_tag': 'data_ralated_tag'}
        # # user 可以在handle里自己按数据格式制定tags
        # user_postprocessed = {'data_value': data_value_list,
        #                       'tags': tags, }

        for each_command in raw_data:
            if each_command == 'ASIE':
                user_postprocessed = self.process_functions[each_command](raw_data[each_command], self.myredis)
                yield user_postprocessed

            else:
                user_postprocessed = self.process_functions[each_command](raw_data[each_command])
                yield user_postprocessed
                # if each_command == 'ASTF':
                #     user_postprocessed = self.process_functions[each_command](raw_data[each_command])
                #     yield user_postprocessed

    def get_a_redis(self, conf):
        redis = StrictRedis(host=conf['host'], port=conf['port'],
                            db=conf['db'], socket_timeout=3)
        return redis
