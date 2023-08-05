# -*- encoding: utf-8 -*-
# @ModuleName: FutureReader
# @Author: Yulin Qiu
# @Time: 2020-3-6 20:08:00


import datetime
import os
import sqlite3
from pathlib import Path

import pandas as pd
import tushare as ts


class FutureReader:
	def __init__(self, *args, **kwargs):
		self.dbpath = None
		configpath = Path.home().joinpath('.qytools')
		if os.path.exists(str(configpath.joinpath('dbname_config.json'))):
			df_config = pd.read_json(str(configpath.joinpath('dbname_config.json')))
			self.config = df_config
			self.file_used = df_config.loc[0, 'file_used']
			self.dbpath = df_config.loc[0, 'dbpath']
			self.configpath = str(configpath)
			print('配置文件dbname_config.json读取成功')
		else:
			raise FileNotFoundError('配置文件不存在,请执行DBreader.firsttime_setconfig')

		try:
			pro = ts.pro_api()
		except:
			print('tushare连接出错，使用配置文件中token重新尝试连接')
			try:
				ts.set_token(df_config.loc[0, 'tushare_token'])
				pro = ts.pro_api()
			except:
				raise ConnectionError('使用配置文件中token连接tushare失败，请联系管理员')

		df_opendate = pro.query('trade_cal', start_date='20150101', end_date='20991231')  # 获取交易日
		df_opendate = df_opendate[df_opendate.is_open == 1]['cal_date']
		self.open_date = df_opendate.apply(lambda x: x[0:4] + '-' + x[4:6] + '-' + x[6:])

		self.future_ordinary = dict()
		self.future_main = dict()

		# 目前正常交易股票代码和名称
		# 大商所
		self.future_ordinary['DCE'] = pro.fut_basic(
			exchange='DCE',
			fut_type='1',
			fields='symbol,fut_code,name,list_date,delist_date'
		)
		self.future_main['DCE'] = pro.fut_basic(
			exchange='DCE',
			fut_type='2',
			fields='symbol,fut_code,name'
		)
		# 中金所
		self.future_ordinary['CFFEX'] = pro.fut_basic(
			exchange='CFFEX',
			fut_type='1',
			fields='symbol,fut_code,name,list_date,delist_date'
		)
		self.future_main['CFFEX'] = pro.fut_basic(
			exchange='CFFEX',
			fut_type='2',
			fields='symbol,fut_code,name'
		)

		# 郑商所
		self.future_ordinary['CZCE'] = pro.fut_basic(
			exchange='CZCE',
			fut_type='1',
			fields='symbol,fut_code,name,list_date,delist_date'
		)
		self.future_main['CZCE'] = pro.fut_basic(
			exchange='CZCE',
			fut_type='2',
			fields='symbol,fut_code,name'
		)

		# 上期所
		self.future_ordinary['SHFE'] = pro.fut_basic(
			exchange='SHFE',
			fut_type='1',
			fields='symbol,fut_code,name,list_date,delist_date'
		)
		self.future_main['SHFE'] = pro.fut_basic(
			exchange='SHFE',
			fut_type='2',
			fields='symbol,fut_code,name'
		)

		# 上海国际能源交易中心
		self.future_ordinary['INE'] = pro.fut_basic(
			exchange='INE',
			fut_type='1',
			fields='symbol,fut_code,name,list_date,delist_date'
		)
		self.future_main['INE'] = pro.fut_basic(
			exchange='INE',
			fut_type='2',
			fields='symbol,fut_code,name'
		)

		for v in self.future_ordinary.values():
			self._date_str_change(v)

		for v in self.future_main.values():
			self._date_str_change(v)

	@staticmethod
	def _date_str_change(df):
		df.rename(columns={'symbol': 'code'}, inplace=True)
		if 'list_date' in df.columns:
			df['list_date'] = pd.to_datetime(df['list_date'])
			df['delist_date'] = pd.to_datetime(df['delist_date'])

			# df['list_date'] = df['list_date'].apply(lambda x: f"{x[0:4]}-{x[4:6]}-{x[6:8]}")
			# df['delist_date'] = df['delist_date'].apply(lambda x: f"{x[0:4]}-{x[4:6]}-{x[6:8]}")

	def __check_path(self, dbname, dbpath):
		path = os.path.join(self.config.loc[0, 'dbpath'], dbname) if dbpath == 'default' else dbpath
		if not os.path.exists(path):
			raise FileNotFoundError(f'{path}不存在')
		if '.sqlite3' in dbname:
			pass
		else:
			dbname = dbname + '.sqlite3'
		if '.sqlite3' not in path:
			path = os.path.join(path, dbname)

		return dbname, path

	@staticmethod
	def get_tableinfo_cols(dbfile, tablename):
		df_tableinfo = pd.read_sql('PRAGMA table_info([' + tablename + '])', con=sqlite3.connect(str(dbfile)))
		return df_tableinfo['name'].to_list()

	@staticmethod
	def check_date(date):
		if isinstance(date, int):
			date = str(date)
		date = pd.to_datetime(date)
		return date

	@staticmethod
	def check_time(start_time, end_time):
		if start_time:
			start_time = pd.to_datetime(start_time).time()
		else:
			start_time = pd.to_datetime('00:00:00').time()
			
		if end_time:
			end_time = pd.to_datetime(end_time).time()
		else:
			end_time = pd.to_datetime('23:59:59').time()
		str_time = f" AND time >= '{start_time}' AND time <= '{end_time}'"
		return start_time, end_time, str_time

	@staticmethod
	def _change_datetime(dt_start: datetime.datetime, dt_end: datetime.datetime, time_start, time_end):
		# time_start = pd.to_datetime(time_start).time()
		# time_end = pd.to_datetime(time_end).time()
		dt_start = dt_start.replace(hour=time_start.hour, minute=time_start.minute, second=time_start.second)
		dt_end = dt_end.replace(hour=time_end.hour, minute=time_end.minute, second=time_end.second)
		return dt_start, dt_end

	@staticmethod
	def _sql_format(origin, mode='datetime'):
		if mode == 'date':
			origin = origin.date()
		return f"'{str(origin)}'"

	def __check_code(self, code, exchange, fut_type, start, end):
		if code is None:
			if fut_type == 0:
				df = self.future_ordinary[exchange]
				code = df.loc[(df['list_date'] < end) & (df['delist_date'] > start), :]['code'].to_list()
			else:
				code = self.future_main[exchange]['code'].to_list()
		if len(code) == 0:
			code = ['xxxxx']

		if isinstance(code, list):
			str_code = str(code).replace('[', '(').replace(']', ')')
		elif isinstance(code, str):
			code = code.split(',')
			str_code = str(code).replace('[', '(').replace(']', ')')
		else:
			raise TypeError('code必须为None, list, str三种类型之一')

		str_code = f' code in {str_code}'

		return str_code

	@staticmethod
	def __check_fields(fields, standard_fields):
		# 全选处理
		if fields == '*':
			return fields
		else:
			# str形式处理
			if isinstance(fields, str):
				fieldslist = fields.split(',')
				errorlist = []
				for column in fieldslist:
					if column in standard_fields:
						pass
					else:
						errorlist.append(column)
				if len(errorlist) == 0:
					return fields
				else:
					raise ValueError('当前查询表内不存在列名：{}'.format(errorlist))

			# list形式处理
			if hasattr(fields, "__iter__"):
				errorlist = []
				for column in fields:
					if column in standard_fields:
						pass
					else:
						errorlist.append(column)
				if len(errorlist) == 0:
					str_fields = ','.join(fields)
					return str_fields
				else:
					raise ValueError('当前查询表内不存在列名：{}'.format(errorlist))

	def query_future_day(
		self, start, end, tablename: str, dbname: str, exchange: str, fut_type: int, fields: str = '*', code=None,
		dbpath='default'
	):
		"""
		:param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
		:param end: 结束日期 ，必选，支持同start
		:param tablename: 查询表名，str类型
		:param dbname: 数据库名，str类型，后缀可加可不加，如test或test.sqlite3均合法
		:param exchange: 交易所代码 CFFEX-中金所 DCE-大商所 CZCE-郑商所 SHFE-上期所 INE-上海国际能源交易中心
		:param fut_type: 合约类型 int, 1 普通合约 2主力与连续合约
		:param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
		:param code: 代码，默认取所有，支持str如'ZC011', list如['SA011', 'ZC011']
		:param dbpath: 数据库目录，无需传入具体的数据库文件名，比如传入 'D:/test'即可

		:return: dataframe格式数据表.
		"""

		dbname, path = self.__check_path(dbname, dbpath)
		dbname_date = 'date'
		exchange = exchange.upper()

		col = self.get_tableinfo_cols(path, tablename)

		start_date = self.check_date(date=start)
		end_date = self.check_date(date=end)

		str_code = self.__check_code(code=code, exchange=exchange, fut_type=fut_type, start=start_date, end=end_date)

		str_fields = self.__check_fields(fields=fields, standard_fields=col)

		start_date, end_date = self._sql_format(start_date, 'date'), self._sql_format(end_date, 'date')

		str_sql = \
			'SELECT ' + str_fields + ' FROM ' + tablename + ' WHERE ' + str_code + ' AND (' + \
			dbname_date + '>=' + start_date + ' AND ' + dbname_date + '<=' + end_date + ')'

		try:
			connect = sqlite3.connect(path)
			df = pd.read_sql(str_sql, con=connect)
			connect.close()
		except Exception:
			raise ConnectionError(f'数据库数据获取失败，请确保{dbname}库以及{tablename}表存在')

		return df

	def query_future_min(
			self, start, end, tablename: str, dbname: str, exchange: str, fut_type: int, fields: str = '*', code=None,
			start_time=None, end_time=None, dbpath='default'
	):
		"""
		:param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
		:param end: 结束日期 ，必选，支持同start
		:param tablename: 查询表名，str类型
		:param dbname: 数据库名，str类型，后缀可加可不加，如test或test.sqlite3均合法
		:param exchange: 交易所代码 CFFEX-中金所 DCE-大商所 CZCE-郑商所 SHFE-上期所 INE-上海国际能源交易中心
		:param fut_type: 合约类型 int, 1 普通合约 2主力与连续合约
		:param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
		:param code: 代码，默认取所有，支持str如'ZC011', list如['SA011', 'ZC011']
		:param dbpath: 数据库目录，无需传入具体的数据库文件名，比如传入 'D:/test'即可
		:param start_time: 开始时间，默认None，支持str如'09:35:30'
		:param end_time: 结束时间，默认None，支持str如'09:35:30'

		:return: dataframe格式数据表.
		"""

		dbname, path = self.__check_path(dbname, dbpath)
		dbname_date = 'datetime'
		exchange = exchange.upper()

		col = self.get_tableinfo_cols(path, tablename)

		start_date = self.check_date(date=start)
		end_date = self.check_date(date=end)
		start_time, end_time, str_time = self.check_time(start_time, end_time)
		start_date, end_date = self._change_datetime(start_date, end_date, start_time, end_time)

		str_code = self.__check_code(code=code, exchange=exchange, fut_type=fut_type, start=start_date, end=end_date)

		str_fields = self.__check_fields(fields=fields, standard_fields=col)

		start_date, end_date = self._sql_format(start_date), self._sql_format(end_date)

		str_sql = \
			'SELECT ' + str_fields + ' FROM ' + tablename + ' WHERE ' + str_code + ' AND (' + \
			dbname_date + '>=' + start_date + ' AND ' + dbname_date + '<=' + end_date + str_time + ')'

		try:
			connect = sqlite3.connect(path)
			df = pd.read_sql(str_sql, con=connect)
			connect.close()
		except Exception:
			raise ConnectionError(f'数据库数据获取失败，请确保{dbname}库以及{tablename}表存在')

		return df


if __name__ == '__main__':
	f = FutureReader()
	# f.query_future_day(start=20200911, end=20200911, dbname='future_day', tablename='day', exchange='DCE', fut_type=0, fields='code')
	t = f.query_future_min(
		start=20200911, end=20200911,
		dbname='test', tablename='xxxxxx', exchange='DCE', fut_type=0,
		start_time='09:30:00', end_time='09:50:00', dbpath='D:/',
		fields='code,datetime'
	)

	a = 1
