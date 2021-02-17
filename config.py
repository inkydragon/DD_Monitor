# -*- coding: utf-8 -*-
"""配置文件
"""
import os.path
import logging
import codecs
import json


class GlobalConfig:
    def __init__(self, root_path):
        self.cfg_dir = os.path.join(root_path, 'utils')
        self.config_path = os.path.join(self.cfg_dir, 'config.json')
        self.config = {}

    def read_config_file(self):
        """读取配置文件
        仅对文件名进行检验，不处理读取文件抛出的错误
        :return: None
        """
        cfg_name = self.config_path
        # 判断是否为合法的配置文件
        if os.path.isfile(cfg_name) and os.path.getsize(cfg_name):
            with codecs.open(cfg_name, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            logging.warning(f'无效的文件名: {cfg_name}')

    def read_main_config(self):
        """读取默认的 config"""
        try:
            self.read_config_file()
        except:
            logging.exception('json 配置读取失败')
            self.config = {}

    def read_backup_config(self):
        """读取config失败时, 尝试读取备份"""
        for backupNumber in [1, 2, 3]:  # 备份预设123
            self.config_path = os.path.join(self.cfg_dir, f'config_备份{backupNumber}.json')
            try:
                self.read_config_file()
                break
            except:
                logging.exception('json 备份配置读取失败')
                self.config = {}

    def read_json_config(self):
        """尝试读取json配置文件
        读取失败则使用默认配置
        """
        self.read_main_config()

        if self.config == {}:
            self.read_backup_config()

        if self.config == {}:
            self.config = {
                'roomid': {'21396545': False, '21402309': False, '22384516': False, '8792912': False},  # 置顶显示
                'layout': [(0, 0, 1, 1), (0, 1, 1, 1), (1, 0, 1, 1), (1, 1, 1, 1)],
                'player': ['0'] * 9,
                'quality': [80] * 9,
                'audioChannel': [0] * 9,
                'muted': [1] * 9,
                'volume': [50] * 9,
                'danmu': [[True, 50, 1, 7, 0, '【 [ {', 10]] * 9,  # 显示,透明,横向,纵向,类型,同传字符,字体大小
                'globalVolume': 30,
                'control': True,
                'hardwareDecode': True,
                'maxCacheSize': 2048000,
                'saveCachePath': '',
                'startWithDanmu': True,
                'showStartLive': True,
            }

    def check_config(self):
        """检查读取到的配置"""
        # 成功读取到 config
        while len(self.config['player']) < 9:
            self.config['player'].append('0')
        self.config['player'] = list(map(str, self.config['player']))
        if type(self.config['roomid']) == list:
            roomIDList = self.config['roomid']
            self.config['roomid'] = {}
            for roomID in roomIDList:
                self.config['roomid'][roomID] = False
        if '0' in self.config['roomid']:  # 过滤0房间号
            del self.config['roomid']['0']

        if 'quality' not in self.config:
            self.config['quality'] = [80] * 9
        if 'audioChannel' not in self.config:
            self.config['audioChannel'] = [0] * 9
        if 'translator' not in self.config:
            self.config['translator'] = [True] * 9
        for index, textSetting in enumerate(self.config['danmu']):
            if type(textSetting) == bool:
                self.config['danmu'][index] = [textSetting, 20, 1, 7, 0, '【 [ {']
        if 'hardwareDecode' not in self.config:
            self.config['hardwareDecode'] = True
        if 'maxCacheSize' not in self.config:
            self.config['maxCacheSize'] = 2048000
            logging.warning('最大缓存没有被设置，使用默认1G')
        if 'saveCachePath' not in self.config:
            self.config['saveCachePath'] = ''
            logging.warning('默认缓存备份路径为空 即自动清空')
        if 'startWithDanmu' not in self.config:
            self.config['startWithDanmu'] = True
            logging.warning('启动时加载弹幕没有被设置，默认加载')
        if 'showStartLive' not in self.config:
            self.config['showStartLive'] = True
        for danmuConfig in self.config['danmu']:
            if len(danmuConfig) == 6:
                danmuConfig.append(10)

    def load_config(self):
        """加载配置文件并填充默认配置"""
        self.read_json_config()
        self.check_config()
        logging.info('配置读取完毕')
