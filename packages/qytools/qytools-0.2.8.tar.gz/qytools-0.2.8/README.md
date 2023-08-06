📦 qytools
=======================

## 文件内容
 `db_read.py`数据库取出数据  
 `db_maintain.py`数据库录入数据  
 `tools.py`数据库/因子构造相关实用工具包  
 `stack.py`堆栈  

## 前言
* 操作中财量化研究院所拥有的全部sqlite3数据库，具体操作见下面相关文件描述
* 比常规select语句速度高出数倍~数十倍，数据量越大提升速度越明显
* 仅供中财量化研究院成员学习使用
* dbread采取内置文档的形式，对接口使用有疑问可以直接参考README+内置文档

## 作者

**qytools** © [yulin qiu](https://gitee.com/yulin_qiu/projects), Released under the [MIT](./LICENSE) License.<br>
> qq: 492876854  
> Weixin: QQ492876854  
> e-mail: x492876854@qq.com


## 环境准备
pipreqs==0.4.10  
pandas>=1.0.1  
numpy>=1.16.2  
tushare>=1.2.52  


## 使用准备
* dbread接口功能需要使用tushare，需要确保本机拥有tushare包并且已经执行过[set_token](https://tushare.pro/document/1?doc_id=37)
* 尽量确保tushare拥有[200以上积分，或者入tushare官方群联系管理员](https://tushare.pro/document/1?doc_id=13) 学生可以拥有免费使用权限
* 首次使用tushare需要根据官网指示设置token[200以上积分，或者入tushare官方群联系管理员](https://tushare.pro/document/1?doc_id=40) 否则qytools部分功能无法使用，之后全局有效，无需设置

## 文件文档
 ### `db_read.py`  
基于股票sqlite数据库的通用型接口`class: DbReader`，  
**使用流程**  

1. `from qyltools import Dbreader`

2. 首次使用时预先执行一次，执行成功后略过，进行步骤3（类似tushare set_token）：  
   `Dbreader.firsttime_setconfig(sqlite3数据文件存放目录)`  
    例如：
    `Dbreader.firsttime_setconfig(r'D:\learn\navicat\data'）`
3. `read = Dbreader`  
    `read.read_ts_day_data(参数)`

主要拥有以下功能
1. 读取数据类  
    * `read_tdx_1min_data` 获取分钟数据
    * `read_ts_top_inst` 获取龙虎榜机构明细
    * `read_ts_top_list` 获取龙虎榜股票明细
    * `read_ts_day_data` 获取日线综合数据
    * `read_ts_index_daily` 获取指数日线数据
    * `read_ts_limit_list` 获取每日涨停板数据
    * `read_ts_moneyflow_hsgt` 获取沪深港通资金流数据
    * `read_concept_data` 获取板块信息
    * `read_jj_1min_index_data` 获取指数分钟数据（掘金数据源）
    * `read_fundamentals` 获取股票公司财务数据
    * `read_strategy` 获取AI策略因子表
    * `read_cal_market_1min_data` 获取计算因子表
    * `query_stock_day` 通用型股票日线数据表接口
    * `query_stock_min` 通用型股票分钟数据表接口
    * `query_index_day` 通用型指数日线数据表接口
    * `query_index_min` 通用型指数分钟数据表接口  
    * `query_market_min` 通用型市场分钟数据表接口  
    * `query_market_day` 通用型市场日线数据表接口  
    * `query_stock_limitday` 获取股票指定时间长度的日线数据接口（处理停牌股专用）  
       
        * 主要参数说明   
        `start` – 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')  
        `end` – 结束日期 ，必选，支持同start  
        `fields` – 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']  
        `code` – 代码，默认取所有，支持int如300, list如[1, '300', 399905]列表内可以是数值或str  
        `shift` – 往前推的时间，默认0，仅支持int  
        `forward` – 往后推的时间，默认0，仅支持int  
        `newdrop` – 新股上市多少交易日内不交易，默认0，仅支持int  
        `stdrop` – 是否剔除st股，True剔除，默认True  
        `deldrop` – 是否剔除退市股，True剔除，默认False  
        `stardrop` – 是否剔除科创板股，True剔除，默认True  
        `time_start` – 分钟数据的可选参数，开始时间，默认None，支持str如'09:35:30'  
		`time_end` – 分钟数据的可选参数，结束时间，默认None，支持str如'09:35:30'  
        `tablename` – 查询表名，str类型  
        `dbname` – 数据库名，str类型，后缀可加可不加，如test或test.sqlite3均合法  
        
            返回值为`dataframe`格式数据表.
        * 示例1：
        > 
            [In]: read.read_ts_day_data(start='20200313', end=20200313, forward=1, shift=1, newdrop=60)  # 参数见文档（ctrl+Q）
            
            [Out]:
                        id             code         date  ...   up_limit    vol     volume_ratio
                        10575  1753771  603998  2020-03-13  ...      7.67   59193.06          1.01
                        10576  1757673  603998  2020-03-16  ...      7.45   65566.00          1.11
                        10577  1751490  603999  2020-03-12  ...      7.12   94223.01          1.06
                        10578  1755746  603999  2020-03-13  ...      6.89  112777.40          1.29
                        10579  1756595  603999  2020-03-16  ...      6.64   83763.32          0.89
                        [5 rows x 42 columns]
         
         * 示例2：
        > 
            [In]: query_index_min(start=20200402, end=20200402, tablename='jj_1min_index_data', dbname='jj_data')
            
            [Out]: 
                    code        date  ...      volume             datetime
            1915  399006  2020-04-02  ...  17922320.0  2020-04-02 14:56:00
            1916  399006  2020-04-02  ...  16854299.0  2020-04-02 14:57:00
            1917  399006  2020-04-02  ...   1227189.0  2020-04-02 14:58:00
            1918  399006  2020-04-02  ...         0.0  2020-04-02 14:59:00
            1919  399006  2020-04-02  ...  33783690.0  2020-04-02 15:00:00
            [5 rows x 10 columns]


2. 工具箱
    * `get_tableinfo_cols` 获取某个数据库某个表的所有列名
    * `check_time` 修正时间格式，输入`str` `int` `datetime`统一变为`str: '2018-09-08'`型
    * `get_timesection` 获取指定起止日期的交易日历  
        * 示例1：
        >
            [In]: read.get_timesection(start='20200313', end=20200315, shift=5)  # shift为参数，取前n交易日  
           
            [Out]:  
            ['2020-03-06', '2020-03-09', '2020-03-10', '2020-03-11', '2020-03-12', '2020-03-13']
    * `get_opendate` 查找指定时间附近的交易日  
    
        * 示例2：
        >
            [In]: read.get_opendate(time=20200315, shift=1)  # shift为参数，取前n交易日`
            
            [Out]:
            `2020-03-13
  
    
    
### `db_maintain.py`
> #### 注意事项
 >* 使用`db_maintain.py`只需要了解最基础的`sql`语法含义即可使用，如有疑问，参考[sql语法文档](https://www.runoob.com/sql/sql-syntax.html)
 >* 接口`db_maintain.py`文件里均有主要功能的详细参数说明，可以通过`main`里的示例，对上述4个功能ctrl+鼠标左键或Ctrl+Q查看
 >* 基本功能包括4个:  
>`update_data`  
>`replace_data`  
>`rebuild_data`  
>`insert_data`    
>下面逐一介绍
>

***

* #### `update_data`  
此接口掌管数据更新，与`sql`中的`update`含义类似，将原来表的某些已有数据更新，比如将`test`表中2018年10月15日到16日的`volume`改变为输入`df`中的对应值，相比`sql`语句的`update`，直接额外添加列，以及自动裁剪重复数据  
示例：
>
    factor.update_data(
            dbpath='D/fundamentals.sqlite3', tablename='test',
            newcols={'circ_mv': 'real'}, df_data=df, index_col='code,date', autoadd=True)  
上述代码基本含义为：在`D`盘更新`fundamental`数据库中的`test`表，新增一列`circ_mv`且定义格式为`real`，
传入的`dataframe`为`df`，test表的索引为`code,date`，`autoadd`打开则剩余未像`circ_mv`定义为`real`的额外列
（df有而数据库没有的列）将按照`sqlite`默认格式入库
>
    使用场景：某段时间区间的某几列数据有问题，重新入库对应几列时使用 

* #### `replace_data`  
此接口掌管数据表完全替换，谨慎使用，使用后原表会删除，操作和`update`大体一致，额外多参数`index_name`，为替换后新表的创建的索引名称如`'index_b1' ` 

    使用场景：整个表过于老旧或出于其他原因要整表替换时使用


* #### `rebuild_data`  
此接口掌管已有数据的替换，相对于`replace`更为温和，相对于`update`更为激进，是在原表基础上修改一部分数据，但是是按照时间区间，起始时间到终止时间的所有数据会被清空后重新写入，不能指定某一列，操作方法同`update`  

    使用场景：某段时间区间的数据整体性入错，重新入库时使用

* #### `insert_data`  
此接口掌管数据插入，与`sql`中的`insert`含义类似，但是相比`sql`语句，该接口可以额外添加列，以及自动裁剪和库里重复数据，操作方式与`update`基本一致,额外多了`insertmode`参数，详细解释见`db_maintain`  

    使用场景：添加新数据，每日更新数据库等

* #### `creat_dbtable`  
此接口掌管建库建表或者在已存在的库里建表，详细解释见`db_maintain`  

    使用场景：新建了数据库或者因子表，用于他人使用时无库建库，无表建表，使得使用者完全不需要掌握数据库操作即可完成相关需求

License
-------

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any means.

