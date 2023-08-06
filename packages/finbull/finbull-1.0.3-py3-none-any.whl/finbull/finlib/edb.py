# -*- coding: utf-8 -*-
"""

EDB取数 
Wed Nov 4 2020

@author: Wu Yiyang
"""
import pandas as pd
from sqlalchemy import create_engine
import time
import numpy as np
from datetime import datetime

def mysql_replace_into(table, conn, keys, data_iter):
    from sqlalchemy.dialects.mysql import insert
    from sqlalchemy.ext.compiler import compiles
    from sqlalchemy.sql.expression import Insert
    @compiles(Insert)
    def replace_string(insert, compiler, **kw):
        s = compiler.visit_insert(insert, **kw)
        s = s.replace("INSERT INTO", "REPLACE INTO")
        return s
    data = [dict(zip(keys, row)) for row in data_iter]
    conn.execute(table.table.insert(replace_string=""), data)


class edb(object):
    
    def __init__(self,host,user,pwd,port,db,dicttb,valuetb):
        self.host= host
        self.user= user
        self.pwd= pwd
        self.port = port
        self.db= db
        self.dicttb = dicttb
        self.valuetb = valuetb
        mysql_driver = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8" % (self.user, self.pwd, self.host, self.port, self.db)
        self.engine = create_engine(mysql_driver)

    def say(self):
        print("在哥牛逼")
    
    #建立数据库连接
    # def create_engine(self):
    #     mysql_driver = "mysql://%s:%s@%s:%s/%s?charset=utf8" % (self.user, self.pwd, self.host, self.port, self.db)
    #     engine = create_engine(mysql_driver)
    #     return engine
    
    #从txt导入wind代码
    def code_from_txt(self,txt_dir):
        edb_code = list()
        with open(txt_dir, 'r') as f:
            for line in f.readlines():
                line = line.strip('\n')
                edb_code.append(line)
        edb_code = list(set(edb_code))
        return edb_code
    
    #从excel导入wind代码
    def code_from_excel(self,excel_dir,colname):
        edb_code_excel = pd.read_excel(excel_dir)
        edb_code = list(edb_code_excel[colname])
        edb_code = list(set(edb_code))
        return edb_code
    
    #区分旧数据与新数据
    def split_new_and_old(self,wcodelist,colname):
        cur_code = pd.read_sql("SELECT DISTINCT %s FROM %s" % (colname,self.valuetb),self.engine)
        cur_code_list = list(cur_code)
        old_code = list(set(wcodelist) & set(cur_code_list))
        new_code = list(set(wcodelist) - set(cur_code_list))
        return old_code,new_code
    
    #将wind取数的格式转换为mysql存储格式
    def reformat(self,wdata,idxname='index'):
        colname = list(wdata.columns)
        colnamelen = set([len(x) for x in colname])       
        if colnamelen == {8}:
            wdata = wdata.reset_index(drop=False)
            wdata = wdata.melt(id_vars = idxname,value_vars = wdata.columns[1:])
            wdata = wdata.rename(columns = {idxname:'hc_ts_data_day','variable':'wind_code','value':'hc_ts_data_value'})
            return wdata
        else:
            raise AttributeError('headers are not valid, please make sure column names consist of wind codes')
            return
        
        
    ##定义一个处理Wind数据之外数据的转换方法(new)
    def reformat_new(self,wdata,idxname='index'):
            wdata = wdata.reset_index(drop=False)
            wdata = wdata.melt(id_vars = idxname,value_vars = wdata.columns[1:])
            wdata = wdata.rename(columns = {idxname:'hc_ts_data_day','variable':'hc_ts_data_code','value':'hc_ts_data_value'})
            return wdata

        
    #从excel读入数据字典
    def dict_from_excel(self,excel_dir):
        dict_data = pd.read_excel(excel_dir)
        return dict_data
    
    #清除txt中数据代码的所有数据
    def clear_data_from_txt(self,txt_dir,clear_dict = False):
        hc_ts_data_code = list()
        with open(txt_dir, 'r') as f:
            for line in f.readlines():
                line = line.strip('\n')
                hc_ts_data_code.append(line)
        hc_ts_data_code = list(set(hc_ts_data_code))
        hc_ts_data_code = ["'%s'" % k for k in hc_ts_data_code]
        hc_ts_data_code = ','.join(hc_ts_data_code)
        self.engine.execute("DELETE FROM %s WHERE hc_ts_data_code IN (%s)" % (self.valuetb,hc_ts_data_code))
        if clear_dict:
            self.engine.execute("DELETE FROM %s WHERE hc_ts_data_code IN (%s)" % (self.dicttb,hc_ts_data_code))
        return 0
    
    #清除单条数据    
    def clear_single_data(self,hc_ts_data_code,clear_dict = False):           
        self.engine.execute("DELETE FROM %s WHERE hc_ts_data_code = '%s'" % (self.valuetb,hc_ts_data_code))
        if clear_dict:
            self.engine.execute("DELETE FROM %s WHERE hc_ts_data_code = '%s'" % (self.dicttb,hc_ts_data_code))
        return 0
    
 
    
    #将做好的数据字典存入mysql
    def dict_tosql(self,dict_data):
        if len(dict_data) == 0:
            return
        header={"id","tsd_industry","tsd_original_source",'hc_ts_data_code','hc_ts_data_name','tsd_source','tsd_source_code','tsd_unit','tsd_freq','tsd_source_type','tsd_formula',"tsd_remark"}      
        header_diff = header - set(dict_data.columns)
        if len(header_diff)>0:
            lack_list = list(header_diff)
            lack_str = ','.join(lack_list)
            raise AttributeError('headers do not meet the requirement,please add columns %s' % lack_str)
            return
        
        fulllen = len(dict_data)
        notnullcol = ['hc_ts_data_code','hc_ts_data_name','tsd_source','tsd_freq','tsd_source_type']
        dict_data = dict_data.dropna(subset = ['hc_ts_data_code','hc_ts_data_name','tsd_source','tsd_freq','tsd_source_type'])
        newlen = len(dict_data)
        if fulllen>newlen:
            raise ValueError('the following columns cannot be null:%s' % ','.join(notnullcol))
            return
            
        dict_data = dict_data[list(header)]
        dict_data['create_time'],dict_data['update_time']= datetime.now(),datetime.now()
        dict_data.to_sql(self.dicttb,self.engine,index = False, chunksize = 10000, if_exists = 'append', method=mysql_replace_into)
        return
    
    #将做好的数据历史值存入mysql
    def value_tosql(self,value_data):
        new_data_list = set(list(value_data['wind_code']))
        dict_data = pd.read_sql("SELECT hc_ts_data_code,tsd_source_code FROM %s" % self.dicttb, self.engine)
        exist_data_list = set(list(dict_data['tsd_source_code']))
        unsuccessful_code = new_data_list - exist_data_list
        value_data = pd.merge(left = value_data,right = dict_data,left_on = 'wind_code',right_on = 'tsd_source_code', how = 'right')
        value_data = value_data.drop(columns = 'tsd_source_code')
        value_data.dropna(subset = ['hc_ts_data_value'],inplace = True)
        value_data['hc_ts_data_day'] = value_data['hc_ts_data_day'].apply(lambda x: '%s%s%s' % (str(x.year),'0'*(2-len(str(x.month)))+str(x.month),'0'*(2-len(str(x.day)))+str(x.day)))
        value_data['id'] = np.nan
        value_data['create_time'],value_data['update_time']= datetime.now(),datetime.now()
        value_data.to_sql(self.valuetb,self.engine,index = False, chunksize = 10000, if_exists = 'append', method=mysql_replace_into)
        return unsuccessful_code
    
    #下载数据字典到excel
    def download_dict_excel(self,target_dir,subset = 'all',filtercol = 'hc_ts_data_code'):       
        if subset =='all':
            dict_data = pd.read_sql("SELECT * FROM %s" % self.dicttb,self.engine)
        else:
            if not isinstance(subset,list):
                raise TypeError('subset must be a list')
            return
            subset = ["'%s'" % str(k) for k in subset]
            subset = ','.join(subset)
            dict_data = pd.read_sql("SELECT * FROM %s WHERE %s IN (%s)" % (self.dicttb,filtercol,subset),self.engine)
        curtime = datetime.now().strftime('%Y%m%d%H%M%S')
        dict_data.to_excel('%s/dict_%s.xlsx' % (target_dir,curtime), index= False)
        return dict_data
    
    #下载不超过20个历史数据值到excel        
    def download_value_excel(self,target_dir,subset,is_pivot = True):        
        if not isinstance(subset,list):
            raise TypeError('subset must be a list')
            return
        
        if len(subset)>20:
            raise ValueError ('cannot download over 20 data')
            return
                
        is_index = False
        subset = ["'%s'" % str(k) for k in subset]
        subset = ','.join(subset)
        value_data = pd.read_sql("SELECT hc_ts_data_code,hc_ts_data_name,hc_ts_data_day,hc_ts_data_value FROM %s WHERE hc_ts_data_code IN (%s)" % (self.valuetb,subset), self.engine)
        if is_pivot:        
            value_data = value_data.pivot(index = 'hc_ts_data_day',columns = 'hc_ts_data_name', values = 'hc_ts_data_value')
            is_index = True
            
        curtime = datetime.now().strftime('%Y%m%d%H%M%S')
        value_data.to_excel('%s/value_%s.xlsx' % (target_dir,curtime), index = is_index)
        return value_data
    
    #增加新数据
    #检查运算符是否为四则运算
    def check_function_sign(self,var):
        if var not in ["+","-","*","/"]:
            raise ValueError('function sign must be one of +,-,*,/')
            return
        return
    
    #检查变量是否为整数
    def check_integer(self,var,minvalue):
        if not (isinstance(var,int) and var>=minvalue):
            raise TypeError('variable must be integer greater than or equal to %s' % str(minvalue))
            return
        return
    
    #检查两个列表变量是否有相同的元素数
    def check_equal_element(self,lista,listb):
        if len(lista) != len(listb):
            raise ValueError('two lists must have the same length')
            return
        return
    
    #检查列表的最小元素数
    def check_min_element(self,lst,thres):
        if len(lst)<thres:
            raise ValueError('list must have at least %s elements' % str(thres))
            return
        return
    
    #提取并检查目标数据是否已经在字典表里有
    def fetch_dict_data(self,target_hc_ts_data_code):
        dict_data = pd.read_sql("SELECT hc_ts_data_code,hc_ts_data_name FROM %s WHERE hc_ts_data_code = '%s'" % (self.dicttb,target_hc_ts_data_code),self.engine)
        if len(dict_data) == 0:
            raise ValueError('please add data to data dictionary first')
            return
        return dict_data
    
    #提取源数据的历史值并查询源数据是否已入库
    def fetch_tsd_source_data(self,tsd_source_hc_ts_data_code,is_pivot = True):
        if isinstance(tsd_source_hc_ts_data_code,str):       
            value_sql = "SELECT hc_ts_data_day,hc_ts_data_value,hc_ts_data_code FROM %s WHERE hc_ts_data_code = '%s' ORDER BY hc_ts_data_day" % (self.valuetb,tsd_source_hc_ts_data_code)
            valuedata = pd.read_sql(value_sql,self.engine)
            if len(valuedata)==0:
                raise ValueError('please add original data to data history first')
                return
              
        if isinstance(tsd_source_hc_ts_data_code,list):
            tsd_source_hc_ts_data_code_list = ["'" + k + "'" for k in tsd_source_hc_ts_data_code]
            tsd_source_hc_ts_data_code_list = ','.join(tsd_source_hc_ts_data_code_list)
            value_sql = "SELECT hc_ts_data_day,hc_ts_data_value,hc_ts_data_code FROM %s WHERE hc_ts_data_code IN (%s) ORDER BY hc_ts_data_day" % (self.valuetb,tsd_source_hc_ts_data_code_list)
            valuedata = pd.read_sql(value_sql,self.engine)
            datalist = list(set(list(valuedata['hc_ts_data_code'])))
            if len(datalist)<len(tsd_source_hc_ts_data_code):
                raise ValueError('please add original data to data history first')
                return
    
        if is_pivot:
            valuedata = valuedata.pivot_table(index = 'hc_ts_data_day',columns = 'hc_ts_data_code', values = 'hc_ts_data_value')
            valuedata=valuedata[tsd_source_hc_ts_data_code]
        return valuedata
    
    #定义一个新的调用滚动计算函数并入库的函数 PS:新增需求产生更新需求  final (new)
    def roll(self,tsd_source_hc_ts_data_code,target_hc_ts_data_code,t,ratio=1):
        dict_data = self.fetch_dict_data(target_hc_ts_data_code) 
        rollvalue=self.f(tsd_source_hc_ts_data_code,t,ratio=1)
        if rollvalue is np.nan:
            raise ValueError ("emmm...it doesn't have so many years to roll...")
        result= self.reformat_new(rollvalue,idxname='hc_ts_data_day') 
        returncode = self.new_data_tosql(result,target_hc_ts_data_code,dict_data)  
        return returncode
    
    
    #定义一个处理总需求产生更新需求的函数并入库的函数  假设条件_永续类型 不采用(new)
    def roll_total_2(self,tsd_source_hc_ts_data_code,target_hc_ts_data_code,t,ratio=1):
        valuedata = self.fetch_tsd_source_data(tsd_source_hc_ts_data_code, is_pivot = True) 
        rollvalue=0
        i=1
        while i<=100:#数字取了个超级大的，没有实际参考意义
            w=i-1
            n=((1+ratio)**w)*valuedata
            a=n.shift(t*i)*ratio
            a[a.isnull()]=0
            rollvalue+=a
            i+=1
        if rollvalue is np.nan:
            raise ValueError ("emmm...it doesn't have so many years to roll...")
        result= self.reformat_new(rollvalue,idxname='hc_ts_data_day') 
        returncode = self.new_data_tosql(result,target_hc_ts_data_code,dict_data)  
        return returncode
    
    #比较复杂的加约束条件的处理总需求产生更新需求的滚动计算(new)  final
    def roll_total(self,tsd_source_hc_ts_data_code,target_hc_ts_data_code,t,ratio=1):
        dict_data = self.fetch_dict_data(target_hc_ts_data_code) 
        valuedata = self.fetch_tsd_source_data(tsd_source_hc_ts_data_code, is_pivot = True)
        rollvalue0=0
        rollvalue1=0
        rollvalue2=0
        i=1
        while i<=100:#数字取了个超级大的，没有实际参考意义
            if i<=1/ratio:   
                w=i-1
                n=((1+ratio)**w)*valuedata
                a=n.shift(t*i)*ratio
                a[a.isnull()]=0
                rollvalue0+=a
                i+=1
            rollvalue0
            if i>1/ratio:
                w=i-1
                n=((1+ratio)**w)*valuedata
                v=n.shift(t*i)*ratio
                h=i-int(1/ratio)-1
                m=((1+ratio)**h)*valuedata
                b=m.shift(t*i)*ratio
                v[v.isnull()]=0
                b[b.isnull()]=0
                rollvalue1+=v
                rollvalue2+=b
                i+=1
        rollvalue=rollvalue1-rollvalue2+rollvalue0
        if rollvalue is np.nan:
            raise ValueError ("emmm...it doesn't have so many years to roll...")
        result= self.reformat_new(rollvalue,idxname='hc_ts_data_day') 
        returncode = self.new_data_tosql(result,target_hc_ts_data_code,dict_data)  
        return returncode
    
    #定义一个新的滚动计算的函数(new)  PS:关于新增需求产生更新需求 final
    def f(self,tsd_source_hc_ts_data_code,t,ratio=1):
        valuedata = self.fetch_tsd_source_data(tsd_source_hc_ts_data_code, is_pivot = True) 
        y=0
        i=1
        while i<=1/ratio:
            a=valuedata.shift(t*i)*ratio
            a[a.isnull()]=0
            y+=a
            i+=1
        return y
    
    
    #处理叠加不同年份产生不同比例更新需求的总需求的数据，每八、九、十各产生更新需求0.5,0.3,0.2倍(new)  final
    def f_r(self,tsd_source_hc_ts_data_code):
        valuedata = self.fetch_tsd_source_data(tsd_source_hc_ts_data_code, is_pivot = True) 
        o=0
        i=1
        while i<=1/0.5:
            a=valuedata.shift(8*i)*0.5
            a[a.isnull()]=0
            o+=a
            i+=1
        p=0
        i=1
        while i<=1/0.3:
            a=valuedata.shift(9*i)*0.3
            a[a.isnull()]=0
            p+=a
            i+=1
        q=0
        i=1
        while i<=1/0.2:
            a=valuedata.shift(10*i)*0.2
            a[a.isnull()]=0
            q+=a
            i+=1
        roll_value_total=o+p+q
        return roll_value_total
          
        
    ##处理叠加不同年份产生不同比例更新需求的总需求的数据，每八、九、十各产生更新需求0.5,0.3,0.2倍(new) 不采用
    def f_r_old(self,tsd_source_hc_ts_data_code,target_hc_ts_data_code):
        dict_data = self.fetch_dict_data(target_hc_ts_data_code) 
        valuedata = self.fetch_tsd_source_data(tsd_source_hc_ts_data_code, is_pivot = True) 
        if int((len(valuedata)/8))>=1: 
            o=0
            i=1
            while i<=int((len(valuedata)/8)) :     
                a=valuedata.shift(8*i)*0.5
                a[a.isnull()]=0
                o+=a
                i+=1  
        if int((len(valuedata)/9))>=1: 
            p=0
            i=1
            while i<=int((len(valuedata)/9)) :     
                a=valuedata.shift(9*i)*0.3
                a[a.isnull()]=0
                p+=a
                i+=1
        if int((len(valuedata)/10))>=1: 
            q=0
            i=1
            while i<=int((len(valuedata)/10)) :     
                a=valuedata.shift(10*i)*0.2
                a[a.isnull()]=0
                q+=a
                i+=1
        roll_value_total=o+p+q
        if roll_value_total is np.nan:
            raise ValueError ("emmm...it doesn't have so many year to roll...")
        result= self.reformat_new(roll_value_total,idxname='hc_ts_data_day') 
        returncode = self.new_data_tosql(result,target_hc_ts_data_code,dict_data)  
        return returncode
    
    ##定义一个拼接的函数,根据第二个传入的对象“修补”第一个对象时间轴上的缺失值,拼接后入库,并将x字段之前数据库里的记录删除掉，去除冗余(new)
    def joint(self,x,y): 
        value_sql = "SELECT hc_ts_data_day,hc_ts_data_value,hc_ts_data_code FROM %s ORDER BY hc_ts_data_day"%(self.valuetb)
        valuedata = pd.read_sql(value_sql,self.engine)
        valuedata = valuedata.pivot_table(index = 'hc_ts_data_day',columns = 'hc_ts_data_code', values = 'hc_ts_data_value')
        tog=valuedata[x].dropna().combine_first(valuedata[y].dropna())
        valuedata = self.reformat_new(tog,idxname='hc_ts_data_day')
        valuedata['wind_code'] = 'CAL_DATA'   
        valuedata['id'] = np.nan
        valuedata['create_time'],valuedata['update_time']=datetime.now(),datetime.now()
        valuedata.to_sql(self.valuetb,self.engine,index = False, chunksize = 10000, if_exists = 'append', method=mysql_replace_into)
        self.engine.execute("DELETE FROM %s WHERE hc_ts_data_code= '%s'and create_time < '%s'" %(self.valuetb,x,valuedata['create_time'][1]))
        returncode = 0
        return returncode

    ##定义一个混合计算的函数，计算后入库,a*b/c得到target_hc_ts_data_code(new)
    def mix_cal(self,a,b,c,target_hc_ts_data_code,is_ffill=False):
        dict_data = self.fetch_dict_data(target_hc_ts_data_code) 
        value_sql = "SELECT hc_ts_data_day,hc_ts_data_value,hc_ts_data_code FROM %s ORDER BY hc_ts_data_day"%(self.valuetb)
        valuedata = pd.read_sql(value_sql,self.engine)
        if is_ffill== True:
            valuedata = valuedata.pivot_table(index = 'hc_ts_data_day',columns = 'hc_ts_data_code', values = 'hc_ts_data_value').fillna(method="ffill")
        else:
            valuedata = valuedata.pivot_table(index = 'hc_ts_data_day',columns = 'hc_ts_data_code', values = 'hc_ts_data_value') 
        result=valuedata[a]*valuedata[b]/valuedata[c]
        valuedata = self.reformat_new(result,idxname='hc_ts_data_day')
        returncode = self.new_data_tosql(valuedata, target_hc_ts_data_code, dict_data)     
        return returncode
    
    ##定义一个参数里固定出现“***”指标的函数简化计算(new)  PS：2个指标
    def fixed(self,c,target_hc_ts_data_code,d="V011kltstwqhkd88hglc",is_ffill=True):
        dict_data = self.fetch_dict_data(target_hc_ts_data_code) 
        value_sql = "SELECT hc_ts_data_day,hc_ts_data_value,hc_ts_data_code FROM %s ORDER BY hc_ts_data_day"%(self.valuetb)
        valuedata = pd.read_sql(value_sql,self.engine)
        if is_ffill== True:
            valuedata = valuedata.pivot_table(index = 'hc_ts_data_day',columns = 'hc_ts_data_code', values = 'hc_ts_data_value').fillna(method="ffill")
        else:
            valuedata = valuedata.pivot_table(index = 'hc_ts_data_day',columns = 'hc_ts_data_code', values = 'hc_ts_data_value')  
        result=valuedata[d]*valuedata[c]/10000
        valuedata = self.reformat_new(result,idxname='hc_ts_data_day')
        returncode = self.new_data_tosql(valuedata, target_hc_ts_data_code, dict_data)     
        return returncode
    
    ##定义一个参数里固定出现“***”指标的函数简化计算(new) PS：3个指标
    def fixed_2(self,c,f,target_hc_ts_data_code,d="V01128pg31llkd88hgln",is_ffill=True):
        dict_data = self.fetch_dict_data(target_hc_ts_data_code) 
        value_sql = "SELECT hc_ts_data_day,hc_ts_data_value,hc_ts_data_code FROM %s ORDER BY hc_ts_data_day"%(self.valuetb)
        valuedata = pd.read_sql(value_sql,self.engine)
        if is_ffill== True:
            valuedata = valuedata.pivot_table(index = 'hc_ts_data_day',columns = 'hc_ts_data_code', values = 'hc_ts_data_value').fillna(method="ffill")
        else:
            valuedata = valuedata.pivot_table(index = 'hc_ts_data_day',columns = 'hc_ts_data_code', values = 'hc_ts_data_value')  
        result=valuedata[d]*valuedata[c]*valuedata[f]/10000
        valuedata = self.reformat_new(result,idxname='hc_ts_data_day')
        returncode = self.new_data_tosql(valuedata, target_hc_ts_data_code, dict_data)     
        return returncode
    
    #计算完成之后补充字段 添加到mysql
    def new_data_tosql(self,valuedata,target_hc_ts_data_code,dict_data):
        valuedata = valuedata.dropna(subset = ['hc_ts_data_value'])
        valuedata['hc_ts_data_code'] = target_hc_ts_data_code
        valuedata['wind_code'] = 'CAL_DATA'   
        valuedata['id'] = np.nan
        valuedata['create_time'],valuedata['update_time']=datetime.now(),datetime.now()       
        valuedata.to_sql(self.valuetb,self.engine,index = False, chunksize = 10000, if_exists = 'append', method=mysql_replace_into)
        returncode = 0
        return returncode
  
    #增加新数据的具体算法
    #Algo1:与单一常数值进行运算
    def constant_cal(self,tsd_source_hc_ts_data_code,function_type,constant,target_hc_ts_data_code):
        
        self.check_function_sign(function_type)       
        dict_data = self.fetch_dict_data(target_hc_ts_data_code)
        valuedata = self.fetch_tsd_source_data(tsd_source_hc_ts_data_code,is_pivot=False)
        
        if function_type == "+":
            valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'] + constant
        elif function_type == "-":
            valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'] - constant
        elif function_type == "*":
            valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'] * constant
        elif constant == 0:
            raise ZeroDivisionError('cannot divide by zero')
            return
        else:
            valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value']/constant
            
        returncode = self.new_data_tosql(valuedata, target_hc_ts_data_code, dict_data)               
        return returncode
    
    #Algo2:绝对值换成百分比
    def abstopct(self,tsd_source_hc_ts_data_code,target_hc_ts_data_code):
        dict_data = self.fetch_dict_data(target_hc_ts_data_code)       
        valuedata = self.fetch_tsd_source_data(tsd_source_hc_ts_data_code,is_pivot=False)        
        valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'] * 100
        returncode = self.new_data_tosql(valuedata, target_data_code, dict_data)              
        return returncode
 
    
    #Algo3:多值的同符号计算（允许最后进行一次常数计算）
    def multidatacal_wind(self,tsd_source_hc_ts_data_code_list,target_hc_ts_data_code,function_type = '+',constant=0,constant_function_type = '+',is_ffill=False,idxname='hc_ts_data_day'):
        self.check_function_sign(function_type)
        self.check_function_sign(constant_function_type)
        self.check_min_element(tsd_source_hc_ts_data_code_list,2)
              
        dict_data = self.fetch_dict_data(target_hc_ts_data_code) 
        if is_ffill== True:
            valuedata = self.fetch_tsd_source_data(tsd_source_hc_ts_data_code_list).fillna(method="ffill")
        else:      
            valuedata = self.fetch_tsd_source_data(tsd_source_hc_ts_data_code_list)
        valuedata['hc_ts_data_value'] = valuedata[valuedata.columns[0]] 
        i = 1
        if function_type == "+":
            while i < valuedata.shape[1] - 1:
                valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'] + valuedata[valuedata.columns[i]]
                i +=1                
        elif function_type == "-":
            while i < valuedata.shape[1] - 1:
                valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'] - valuedata[valuedata.columns[i]]
                i +=1
        elif function_type == "*":
            while i < valuedata.shape[1] - 1:
                valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'] * valuedata[valuedata.columns[i]]
                i +=1
        else:
            while i < valuedata.shape[1] - 1:
                valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'] / (valuedata[valuedata.columns[i]] +10e-6)
                i +=1
        
        valuedata = valuedata[['hc_ts_data_value']]
        if constant_function_type == "+":
            valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'] + constant
        elif constant_function_type == "-":
            valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'] - constant
        elif constant_function_type == "*":
            valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'] * constant
        elif constant == 0:
            raise ZeroDivisionError('cannot divide by zero')
            return
        else:
            valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value']/constant
        
        valuedata = self.reformat(valuedata,idxname)
        returncode = self.new_data_tosql(valuedata, target_hc_ts_data_code, dict_data)     
        return returncode
    

    ##连除或者连减的另一种多余的解决方案(new)
    def division(self,tsd_source_hc_ts_data_code_list,target_hc_ts_data_code,function_type = '/',constant=0,constant_function_type = '+',is_ffill=False,idxname='hc_ts_data_day'): 
        self.check_function_sign(function_type)
        self.check_function_sign(constant_function_type)
        self.check_min_element(tsd_source_hc_ts_data_code_list,2)
              
        dict_data = self.fetch_dict_data(target_hc_ts_data_code) 
        if is_ffill== True:
            valuedata = self.fetch_tsd_source_data(tsd_source_hc_ts_data_code_list).fillna(method="ffill")
        else:
            valuedata = self.fetch_tsd_source_data(tsd_source_hc_ts_data_code_list)
        if function_type == "/":
            valuedata['hc_ts_data_value'] = valuedata[tsd_source_hc_ts_data_code_list[0]] / (valuedata[tsd_source_hc_ts_data_code_list[1]] +10e-6)
        else:
            valuedata['hc_ts_data_value'] = valuedata[tsd_source_hc_ts_data_code_list[0]] - valuedata[tsd_source_hc_ts_data_code_list[1]]  
        valuedata = valuedata[['hc_ts_data_value']]
        if constant_function_type == "+":
            valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'] + constant
        elif constant_function_type == "-":
            valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'] - constant
        elif constant_function_type == "*":
            valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'] * constant
        elif constant == 0:
            raise ZeroDivisionError('cannot divide by zero')
            return
        else:
            valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value']/constant
        
        valuedata = self.reformat_new(valuedata,idxname)
        returncode = self.new_data_tosql(valuedata, target_hc_ts_data_code, dict_data)     
        return returncode    
    
    ##下面的for除Wind外的其他衍生计算数据(new)
    def multidatacal(self,tsd_source_hc_ts_data_code_list,target_hc_ts_data_code,function_type = '+',constant=0,constant_function_type = '+',is_ffill=False,idxname='hc_ts_data_day'):
        self.check_function_sign(function_type)
        self.check_function_sign(constant_function_type)
        self.check_min_element(tsd_source_hc_ts_data_code_list,2)
              
        dict_data = self.fetch_dict_data(target_hc_ts_data_code)
        if is_ffill== True:
            valuedata = self.fetch_tsd_source_data(tsd_source_hc_ts_data_code_list).fillna(method="ffill")
        else:
            valuedata = self.fetch_tsd_source_data(tsd_source_hc_ts_data_code_list)
        valuedata['hc_ts_data_value'] = valuedata[valuedata.columns[0]] 
        i = 1
        if function_type == "+":
            while i < valuedata.shape[1] - 1:
                valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'] + valuedata[valuedata.columns[i]]
                i +=1                
        elif function_type == "-":
            while i < valuedata.shape[1] - 1:
                valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'] - valuedata[valuedata.columns[i]]
                i +=1
        elif function_type == "*":
            while i < valuedata.shape[1] - 1:
                valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'] * valuedata[valuedata.columns[i]]
                i +=1
        else:
            while i < valuedata.shape[1] - 1:
                valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'] / (valuedata[valuedata.columns[i]] +10e-6)
                i +=1
        
        valuedata = valuedata[['hc_ts_data_value']]
        if constant_function_type == "+":
            valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'] + constant
        elif constant_function_type == "-":
            valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'] - constant
        elif constant_function_type == "*":
            valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'] * constant
        elif constant == 0:
            raise ZeroDivisionError('cannot divide by zero')
            return
        else:
            valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value']/constant
        
        valuedata = self.reformat_new(valuedata,idxname)
        returncode = self.new_data_tosql(valuedata, target_hc_ts_data_code, dict_data)     
        return returncode
    
    #定义一个处理计算公式里含滚动计算但是库里没有事先存好的滚动计算字段code的数据的函数(灵活版）(new)
    def virtual(self,r,tsd_source_hc_ts_data_code_list,target_hc_ts_data_code,t,constant=1,constant_function_type = '/',idxname='hc_ts_data_day',ratio=1):
        dict_data = self.fetch_dict_data(target_hc_ts_data_code)  
        valuedata = self.fetch_tsd_source_data(tsd_source_hc_ts_data_code_list, is_pivot = True)
        
        valuedata['hc_ts_data_value'] = valuedata[valuedata.columns[0]] 
        i=1
        while i < valuedata.shape[1] - 1:
                valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'] * valuedata[valuedata.columns[i]]
                i +=1  
        valuedata = valuedata[['hc_ts_data_value']]
        if constant_function_type == "+":
            valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'] + constant
        elif constant_function_type == "-":
            valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'] - constant
        elif constant_function_type == "*":
            valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'] * constant
        elif constant == 0:
            raise ZeroDivisionError('cannot divide by zero')
            return
        else:
            valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value']/constant
        
        rolldata=self.f(r,t,ratio=1)
        hh=pd.concat([valuedata,rolldata],axis=1).fillna(method="ffill")
        result=hh[r]*hh['hc_ts_data_value']
        valuedata = self.reformat_new(result,idxname='hc_ts_data_day')
        returncode = self.new_data_tosql(valuedata, target_hc_ts_data_code, dict_data)
        return returncode
    
    ##计算公式里含滚动计算但是库里没有事先存好的滚动计算字段code的函数并入库PS:个性定制版(new)
    def virtual_2(self,r,target_hc_ts_data_code,t,ratio=1):
        dict_data = self.fetch_dict_data(target_hc_ts_data_code)  
        vluedata = self.fetch_tsd_source_data(tsd_source_hc_ts_data_code, is_pivot = True)
        rolldata=self.f(r,t,ratio)
        hh=pd.concat([vluedata,rolldata],axis=1).fillna(method="ffill")
        result=hh[r]+hh[tsd_source_hc_ts_data_code]
        valuedata = self.reformat_new(result,idxname='hc_ts_data_day')
        returncode = self.new_data_tosql(valuedata, target_hc_ts_data_code, dict_data)
        return returncode
    
    #定义一个789加n年更新需求的函数并入库 PS；个性定制(new)
    def vir_mix(self,r,target_hc_ts_data_code,t,ratio=1):
        dict_data = self.fetch_dict_data(target_hc_ts_data_code)  
        rolldata_01=self.f(r,t,ratio)
        rolldata_02=self.f_r(r)
        result=rolldata_01+rolldata_02
        valuedata = self.reformat_new(result,idxname='hc_ts_data_day')
        returncode = self.new_data_tosql(valuedata, target_hc_ts_data_code, dict_data)
        return returncode
        
  
    #Algo4:多值的加权和
    def sumproduct(self,tsd_source_hc_ts_data_code_list,coeff_list,target_hc_ts_data_code,idxname = 'hc_ts_data_day'):
        self.check_equal_element(tsd_source_hc_ts_data_code_list, coeff_list)
        self.check_min_element(tsd_source_hc_ts_data_code_list, 1)
        
        dict_data = self.fetch_dict_data(target_hc_ts_data_code)
        valuedata = self.fetch_tsd_source_data(tsd_source_hc_ts_data_code_list)
        
        valuedata['hc_ts_data_value'] = 0
        i = 0 
        while i < valuedata.shape[1] - 1:
            valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'] + coeff_list[i] * valuedata[valuedata.columns[i]]
            i += 1
        valuedata = valuedata[['hc_ts_data_value']]        
        valuedata = self.reformat(valuedata,idxname)       
        returncode = self.new_data_tosql(valuedata, target_hc_ts_data_code, dict_data)     
        return returncode
    
    #Algo5:原值转移动平均    
    def ma(self,tsd_source_hc_ts_data_code,target_hc_ts_data_code,step = 1,startpos = 0,avgnum = 12, isskipna = True):
        self.check_integer(step,1)
        self.check_integer(startpos,0)
        self.check_integer(avgnum,1)
        
        dict_data = self.fetch_dict_data(target_hc_ts_data_code)
        valuedata = self.fetch_tsd_source_data(tsd_source_hc_ts_data_code,is_pivot = False)
        
        shiftnum = np.arange(startpos,avgnum*step+startpos,step)
        for i in shiftnum:
            valuedata['hc_ts_data_value_%s' % str(i)] = valuedata['hc_ts_data_value'].shift(i)
        valuedata = valuedata.set_index('hc_ts_data_day')
        valuedata = valuedata.drop(columns = ['hc_ts_data_code','hc_ts_data_value'])
        valuedata['hc_ts_data_value'] = valuedata.mean(axis = 1, skipna = isskipna)
        valuedata = valuedata.reset_index(drop = False)
        valuedata = valuedata[['hc_ts_data_day','hc_ts_data_value']]
        returncode = self.new_data_tosql(valuedata, target_hc_ts_data_code, dict_data)     
        return returncode
        
    #Algo6:绝对值转差额
    def abstodiff(self,tsd_source_hc_ts_data_code,target_hc_ts_data_code,step = 1,intrayear=True):
        self.check_integer(step,1)      
        dict_data = self.fetch_dict_data(target_hc_ts_data_code)
        valuedata = self.fetch_tsd_source_data(tsd_source_hc_ts_data_code, is_pivot = False)       
        valuedata['hc_ts_data_value_last'] = valuedata['hc_ts_data_value'].shift(step)
        if intrayear:
            valuedata['year'] = valuedata['hc_ts_data_day'].apply(lambda x:str(x)[:4])
            valuedata['year_last'] = valuedata['year'].shift(step)
            valuedata['hc_ts_data_value'] = valuedata.apply(lambda x:x['hc_ts_data_value'] - x['hc_ts_data_value_last'] if x['year'] == x['year_last']  else x['hc_ts_data_value'],axis =1) 
            valuedata = valuedata.dropna(subset = ['year_last'])
        else:
            valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'] - valuedata['hc_ts_data_value_last']
        valuedata = valuedata[['hc_ts_data_day','hc_ts_data_value']]   
        returncode = self.new_data_tosql(valuedata, target_hc_ts_data_code, dict_data)     
        return returncode
    
    
    #将上述函数分拆一个部件函数方便后续简化计算
    def part(self,tsd_source_hc_ts_data_code,step = 1,intrayear=True):
        self.check_integer(step,1)      
        valuedata = self.fetch_tsd_source_data(tsd_source_hc_ts_data_code, is_pivot = False)       
        valuedata['hc_ts_data_value_last'] = valuedata['hc_ts_data_value'].shift(step)
        if intrayear:
            valuedata['year'] = valuedata['hc_ts_data_day'].apply(lambda x:str(x)[:4])
            valuedata['year_last'] = valuedata['year'].shift(step)
            valuedata['hc_ts_data_value'] = valuedata.apply(lambda x:x['hc_ts_data_value'] - x['hc_ts_data_value_last'] if x['year'] == x['year_last']  else x['hc_ts_data_value'],axis =1) 
            valuedata = valuedata.dropna(subset = ['year_last'])
        else:
            valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'] - valuedata['hc_ts_data_value_last']
        valuedata = valuedata[['hc_ts_data_day','hc_ts_data_value']]       
        return valuedata
    
    
    #定义一个处理两个累计值较上期增长的数据相除的简化计算公式函数
    def abstodiff_2(self,tsd_source_hc_ts_data_code_1,tsd_source_hc_ts_data_code_2,target_hc_ts_data_code,step = 1):
        dict_data = self.fetch_dict_data(target_hc_ts_data_code)
        valuedata_1=self.part(tsd_source_hc_ts_data_code_1,step = 1)
        valuedata_2=self.part(tsd_source_hc_ts_data_code_2,step = 1)
        valuedata_1=valuedata_1.set_index(["hc_ts_data_day"])
        valuedata_2=valuedata_2.set_index(["hc_ts_data_day"])
        result=valuedata_1/valuedata_2
        result=result.dropna().reset_index()
        returncode = self.new_data_tosql(result, target_hc_ts_data_code, dict_data)     
        return  returncode
        
        
     
    #Algo7:绝对值转增长率    
    def abstodivdiff(self,tsd_source_hc_ts_data_code,target_hc_ts_data_code,step = 1):
        self.check_integer(step,1)
        dict_data = self.fetch_dict_data(target_hc_ts_data_code)
        valuedata = self.fetch_tsd_source_data(tsd_source_hc_ts_data_code, is_pivot = False)       
        valuedata['hc_ts_data_value_last'] = valuedata['hc_ts_data_value'].shift(step)
        valuedata = valuedata.replace(0,np.nan)
        valuedata['hc_ts_data_value'] = 100 * (valuedata['hc_ts_data_value'] / valuedata['hc_ts_data_value_last'] - 1)
        valuedata = valuedata[['hc_ts_data_day','hc_ts_data_value']]   
        returncode = self.new_data_tosql(valuedata, target_hc_ts_data_code, dict_data)     
        return returncode
    
    #PS：上面这个函数处理同比计算时只适用于时间序列分布均匀且连续的业务场景，比如每月或者每日等
    #定义一个处理同比计算的，适用范围更广的函数（无条件限制）
    
    def abstodivdiff_2(self,tsd_source_hc_ts_data_code,target_hc_ts_data_code):
        dict_data = self.fetch_dict_data(target_hc_ts_data_code)
        df = self.fetch_tsd_source_data(tsd_source_hc_ts_data_code, is_pivot = False)     
        del df["hc_ts_data_code"]
        df['*rest'] = df['hc_ts_data_day'].apply(lambda x:'%s' % (str(x)[-2:]))
        df['hc_ts_data_day'] = df['hc_ts_data_day'].apply(lambda x:'%s' % (str(x)[:6]))
        df['hc_ts_data_day']=df['hc_ts_data_day'].astype(int)
        last_df_day= df['hc_ts_data_day']-100
        last_df=pd.merge(df,last_df_day,on='hc_ts_data_day',how="right")
        last_df = last_df.replace(0,np.nan)
        last_df=last_df.sort_values(by="hc_ts_data_day",ascending=True).reset_index(drop=True)
        df['hc_ts_data_day']=df['hc_ts_data_day'].astype(str)+df['*rest'] 
        df['hc_ts_data_value'] =100*(df['hc_ts_data_value']/last_df['hc_ts_data_value']-1)
        df = df[['hc_ts_data_day','hc_ts_data_value']] 
        returncode = self.new_data_tosql(df, target_hc_ts_data_code, dict_data)     
        return  returncode

    
    #Algo8:绝对值转累计值 
    def abstocumu(self,tsd_source_hc_ts_data_code,target_hc_ts_data_code,intrayear=True):
        dict_data = self.fetch_dict_data(target_hc_ts_data_code)
        valuedata = self.fetch_tsd_source_data(tsd_source_hc_ts_data_code, is_pivot = False) 
        if intrayear:
            valuedata['year'] = valuedata['hc_ts_data_day'].apply(lambda x:str(x)[:4])
            yearlist = list(set(list(valuedata['year'])))
            yearlist.sort()
            resultdata = pd.DataFrame()
            for i in yearlist:
                tmp = valuedata[valuedata['year'] == i]
                tmp['hc_ts_data_value'] = tmp['hc_ts_data_value'].cumsum(skipna = True)
                resultdata = pd.concat([resultdata,tmp], axis =0)
            valuedata = resultdata.copy()
        else:
            valuedata['hc_ts_data_value'] = valuedata['hc_ts_data_value'].cumsum(skipna = True)
        valuedata = valuedata[['hc_ts_data_day','hc_ts_data_value']]
        returncode = self.new_data_tosql(valuedata, target_hc_ts_data_code, dict_data)     
        return returncode      
         
    #Algo9:构造与数据库中某数据频率一致的常数数据
    def gen_constant_given_data(self,tsd_source_hc_ts_data_code,target_hc_ts_data_code,constantvalue):
        dict_data = self.fetch_dict_data(target_hc_ts_data_code)
        valuedata = self.fetch_tsd_source_data(tsd_source_hc_ts_data_code, is_pivot = False)
        valuedata['hc_ts_data_value'] = constantvalue
        returncode = self.new_data_tosql(valuedata, target_hc_ts_data_code, dict_data)     
        return returncode
    
    #Algo10:自定义构建数据
    def gen_data_customized(self,tsd_freq,datelist,valuelist,target_hc_ts_data_code):
        self.check_equal_element(datelist,valuelist)
        self.check_min_element(datelist,1)
        for i in datelist:
            if len(i)!=8 or '-' in i or not isinstance(i,str):
                raise ValueError("date must have string format yyyymmdd, for example '20190605'")
                return
            
        sorted_datelist = sorted(datelist)
        if sorted_datelist != datelist:
            raise ValueError("datelist must have ascending date order")
            return
        
        if tsd_freq not in ['D','M','Q','Y']:
            raise ValueError("tsd_freq must be one of 'D'(for day),'M'(for month),'Q'(for season),'Y'(for year)")
            return
        dict_data = self.fetch_dict_data(target_hc_ts_data_code)
        datelist += [datetime.now().strftime('%Y%m%d')]
        valuelist += [valuelist[-1]]
        valuedata = pd.DataFrame({'hc_ts_data_day':datelist,'hc_ts_data_value':valuelist})
        valuedata['tmp'] = valuedata['hc_ts_data_day'].apply(lambda x:datetime.strptime(x,'%Y%m%d'))
        valuedata = valuedata.set_index('tmp')
        valuedata = valuedata.resample(tsd_freq,closed='left').pad()
        valuedata = valuedata.reset_index(drop = False)
        valuedata['hc_ts_data_day'] = valuedata['tmp'].apply(lambda x:x.strftime('%Y%m%d'))
        valuedata = valuedata.drop(columns = 'tmp').dropna()
        returncode = self.new_data_tosql(valuedata, target_hc_ts_data_code, dict_data)     
        return returncode