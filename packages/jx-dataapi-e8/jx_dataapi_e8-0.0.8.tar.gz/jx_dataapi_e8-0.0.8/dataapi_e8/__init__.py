"""
@author: tusky
@time: 2019/5/21 下午16:16
@desc: 嘉迅科技网关数据接口包
"""

from .baseapi import E8Api
import moment
import time
import ujson
from datetime import datetime,timedelta
from .utils.powerUtils import PowerUtil
from .utils.helper import Protocal

class DataApi(E8Api):

    def __init__(self,baseurl,appid,appsecret,configObj=None,debug=False,timeout=30):
        """
        初始化类
        """
        # 需要查询的采集编号
        self._full_mids = []
        # 设备更换信息
        self._link_info = {}
        # 表计信息
        self._meters = {}
        # 设备更换信息配置
        self.E8API_CHANGE_CONFIG = {}
        # 接口数据开始时间配置
        self.E8API_BEG_CONFIG = {}
        # 需要补值的参数
        self.E8API_FILL_ATTR_CONFIG = []
        # 初始化基础api
        super().__init__(baseurl,appid,appsecret,debug,timeout)
        self._load_config(configObj)

    def _load_config(self,obj):
        """
        导入配置文件
        E8API_CHANGE_CONFIG 设备更换信息配置
        E8API_BEG_CONFIG 接口数据开始时间配置
        E8API_FILL_ATTR_CONFIG 需要补值的参数
        """
        if obj and isinstance(obj, object):
            for key in dir(obj):
                if key.isupper() and key in ['E8API_CHANGE_CONFIG','E8API_BEG_CONFIG','E8API_FILL_ATTR_CONFIG']:
                    setattr(self,key,getattr(obj, key))

    def _request(self, method, **kwargs):
        """
        重写_request方法，加入数据处理逻辑
        """
        if not self._need_process(method):
            return super()._request(method,**kwargs)
        else:
            return self._process_api_data(method,**kwargs)

    def _need_process(self,method):
        """
        验证是否为数据接口，数据接口需要处理数据
        部分接口不需要处理数据，如设置告警，获取网关状态等
        """
        if '/' in method or method in ['set_alarm','get_alarm','del_alarm','set_event_callback','global']:
            return False
        else:
            return True

    def _get_meter_info(self):
        """
        获取表计信息，变比、协议、采集属性等信息
        @param mids 采集编号，E80142003_0101
        """
        if not self._full_mids:
            return False
        # 获取网关编号
        wgCodes = [mid[:-5] for mid in self._full_mids]
        wgCodes = list(set(wgCodes))
        wgs = super()._request('wg/get',id=",".join(wgCodes))
        for wg in wgs:
            # 获取协议信息
            protocals = {}
            for item in wg['protocals']:
                key = "%s_%s" % (item['ptcl'],item['model'])
                protocals[key] = item['attrs']
            for index,pipe in enumerate(wg['pipes']):
                for _,dev in pipe.items():
                    mid = "%s_%02d%02X" % (wg['uid'],(index + 1),dev['no'])
                    if mid in self._full_mids:
                        info = {
                            'code': mid
                        }
                        # 变比信息
                        info['rate'] = {
                            'pt': dev['pt'] if dev['pt'] else 1,
                            'ct': dev['ct'] if dev['ct'] else 1,
                            'pct': dev['pct'] if dev['pct'] else 1
                        }
                        # 属性信息
                        key = "%s_%s" % (dev['ptcl'],dev['model'])
                        info['attrs'] = protocals[key] if key in protocals else {}
                        self._meters[mid] = info

    def _get_link_info(self):
        """
        获取设备更换信息
        """
        if not self._full_mids or not self.E8API_CHANGE_CONFIG:
            return False
        # 获取表计更换情况信息
        mids = self._full_mids.copy()
        for mid in mids:
            if mid in self.E8API_CHANGE_CONFIG:
                changeInfo = self.E8API_CHANGE_CONFIG[mid]
                if changeInfo:
                    # 更换网关情况，将更换信息按时间排序
                    if 'wg' in changeInfo:
                        # 需要额外查询的采集编号
                        for it in changeInfo['wg']:
                            self._full_mids.append(it['mid'])
                        changeInfo['wg'] = sorted(changeInfo['wg'],key=lambda x:x['tm'])
                    if 'meter' in changeInfo:
                        changeInfo['meter'] = sorted(changeInfo['meter'],key=lambda x:x['tm'])
                    self._link_info[mid] = changeInfo
                    # 将更换的网关也加到_linkInfo中
                    if 'wg' in changeInfo and 'meter' in changeInfo:
                        for it in changeInfo['wg']:
                            self._link_info[it['mid']] = changeInfo
        # mid去重
        self._full_mids = list(set(self._full_mids))

    def _fill_data(self,method,params,data):
        """
        缺值检测&补齐数据
        """
        if method in ['get_hourly_by_day','get_hourly_by_month','get_hourly_in_range','get_ep_by_day','get_ep_by_month','get_ep_in_range','get_daily_by_month','get_daily_in_range']:
            # 计算查询起始日期
            now = time.time()
            if 'month' in params:
                month = params['month']
                beg_tm = moment.date(month + '01','%Y%m%d').datetime.timestamp()
                end_tm = moment.date(month + '01','%Y%m%d').add(months=1).datetime.timestamp()
            elif 'day' in params:
                day = params['day']
                beg_tm = moment.date(day,'%Y%m%d').datetime.timestamp()
                end_tm = beg_tm + 3600 * 24
            elif 'beg' in params:
                beg = str(params['beg'])
                end = str(params['end'])
                beg_tm = moment.date(beg,'%Y%m%d').datetime.timestamp()
                end_tm = moment.date(end,'%Y%m%d').datetime.timestamp()
            else:
                beg_tm = end_tm = int(now)
            if not beg_tm or not end_tm:
                return None
            beg_tm = int(beg_tm)
            if end_tm > now:
                end_tm = now
            # 加1使range能够取到最后一个值
            end_tm = int(end_tm) + 1
            if method in ['get_daily_by_month','get_daily_in_range']:
                 # 完整的tm
                fullTm = [tm for tm in range(beg_tm,end_tm,86400)]
                # 存在的tm
                hasTm = [item['_tm'] - item['_tm'] % 86400 + 57600 for item in data]
            else:
                intervalTm = 3600
                if 'half_hour' in params and int(params['half_hour']) == 1:
                    intervalTm = 1800
                # 完整的tm
                fullTm = [tm for tm in range(beg_tm,end_tm,intervalTm)]
                # 存在的tm
                hasTm = [item['_tm'] - item['_tm'] % intervalTm for item in data]
            # 做差获取缺失的tm
            loseTm = list(set(fullTm).difference(set(hasTm)))
            if len(data) != 0:
                first = data[0]
                last = data[-1]
                for lose in loseTm:
                    # 前后3小时内可以补数据
                    if lose >= first['_tm'] - 10860 and lose < last['_tm'] + 10860:
                        data.append({
                            '_tm': lose,
                            '_model': first['_model'],
                            '_protocal': first['_protocal']
                        })
                # 按时间排序
                data.sort(key=lambda x:x['_tm'])

    def _process_change_meter(self,mid,data):
        """
        处理表计更换情况，后面的数值需要加上前面换掉的表计的数值
        """
        # 处理表计更换电度数据
        if mid in self._link_info and 'meter' in self._link_info[mid] and self._link_info[mid]['meter']:
            for mc in self._link_info[mid]['meter']:
                if data['_tm'] >= mc['tm']:
                    for ck,cv in mc['vals'].items():
                        if ck in data:
                            # cv[0]为更换前最后读数，cv[1]为更换后起始读数
                            data[ck] = data[ck] + cv[0] - cv[1]

    def _process_api_data(self,method,**kwargs):
        """
        处理接口返回数据
        """
        # 数据处理，包括变比、单位、缺值、更换网关等
        devs = kwargs['devs'].split(',')
        devs = list(set(devs))
        self._full_mids = devs.copy()
        self._get_link_info()
        self._get_meter_info()
        # 是否处理变比、缺值、表计更换等
        rate = kwargs.get('rate',None)
        if 'rate' in kwargs:
            del kwargs['rate']
        kwargs['devs'] = ",".join(self._full_mids)
        attrs = kwargs['attrs'] if 'attrs' in kwargs and kwargs['attrs'] else ''
        # 查询数据
        apiData = super()._request(method,**kwargs)
        ret = {}
        if apiData:
            # 单个数据处理
            if rate:
                for mid,data in apiData.items():
                    # TODO:手动补的数据插入处理
                    if isinstance(data,dict):
                        # 判断是get_latest还是其他的
                        if '_tm' in data:
                            self._process_change_meter(mid,data)
                            Protocal.normal_process(self._meters.get(mid),data)
                        else:
                            for t,d in data.items():
                                self._process_change_meter(mid,d)
                                Protocal.normal_process(self._meters.get(mid),d)
                    else:
                        for val in data:
                            self._process_change_meter(mid,val)
                            Protocal.normal_process(self._meters.get(mid),val)
            # 数据合并
            for mid in devs:
                if mid in self._link_info and 'wg' in self._link_info[mid]:
                    # 记录列表数据的时间，去重复
                    dMap = {}
                    for item in self._link_info[mid]['wg']:
                        if item['mid'] in apiData:
                            if isinstance(apiData[item['mid']],dict):
                                if mid not in ret:
                                    ret[mid] = {}
                                # 判断是get_latest还是其他的
                                if '_tm' in apiData[item['mid']]:
                                    ret[mid].update(apiData[item['mid']])
                                else:
                                    for tm,vals in apiData[item['mid']].items():
                                        ret[mid][tm] = vals
                            else:
                                if mid not in ret:
                                    ret[mid] = []
                                period = 60
                                # 排除重复时间，重复时间取电度较小的那个
                                if method in ['get_daily_by_month','get_daily_in_range']:
                                    period = 86400
                                elif method in ['get_hourly_by_day','get_hourly_by_month','get_hourly_in_range','get_ep_by_day','get_ep_by_month','get_ep_in_range']:
                                    period = 3600
                                    if 'half_hour' in kwargs and int(kwargs['half_hour']) == 1:
                                        period = 1800
                                for d in apiData[item['mid']]:
                                    t = (d['_tm'] - 28800) // period
                                    if t in dMap:
                                        if 'ImpEp' in d and 'ImpEp' in dMap[t] and d['ImpEp'] < dMap[t]['ImpEp']:
                                            dMap[t] = d
                                        elif 'EPt' in d and 'EPt' in dMap[t] and d['EPt'] < dMap[t]['EPt']:
                                            dMap[t] = d
                                    else:
                                        dMap[t] = d
                                ret[mid] = dMap.values()
                else:
                    ret[mid] = apiData.get(mid,None)
            # 数据补缺
            for mid,retData in ret.items():
                if isinstance(retData,list):
                    self._fill_data(method,kwargs,retData)
                    beg = 0
                    flag = False
                    for index,val in enumerate(retData):
                        # 判断接口数据过滤
                        if mid in self.E8API_BEG_CONFIG and '_tm' in val and val['_tm'] >= self.E8API_BEG_CONFIG[mid] and not flag:
                            beg = index
                            flag = True
                        Protocal.check_and_insert(self._meters.get(mid),index,val,retData,attrs,self.E8API_FILL_ATTR_CONFIG)
                    if beg:
                        ret[mid] = retData[beg:]
        return ret

    def process_data(self,data):
        """
        处理数据
        """
        if not data:
            return False
        print(data)
        data = ujson.loads(data)
        if 'mid' not in data or 'vals' not in data:
            return False
        meters,_ = self._get_wg_info([data['mid']])
        meter = meters.get(data['mid'],None)
        for val in data['vals']:
            Protocal.normal_process(meter,val)
        return data

    def _get_wg_info(self,mids):
        """
        获取网关信息
        """
        meters = {}
        # 获取网关编号
        wgCodes = [mid[:-5] for mid in mids]
        wgCodes = list(set(wgCodes))
        wgs = super()._request('wg/get',id=",".join(wgCodes))
        pipes = {}
        for wg in wgs:
            monitorMap = {}
            for ptcl in wg['protocals']:
                if 'monitor' in ptcl:
                    key = "%s_%s" % (ptcl['ptcl'],ptcl['model'])
                    monitorMap[key] = ptcl['monitor']
            pipes[wg['uid']] = wg['pipes']
            for index,pipe in enumerate(wg['pipes']):
                for _,dev in pipe.items():
                    mid = "%s_%02d%02X" % (wg['uid'],(index + 1),dev['no'])
                    if mid in mids:
                        info = {
                            'code': mid
                        }
                        # 变比信息
                        info['rate'] = {
                            'pt': dev['pt'] if dev['pt'] else 1,
                            'ct': dev['ct'] if dev['ct'] else 1,
                            'pct': dev['pct'] if dev['pct'] else 1
                        }
                        # 协议信息
                        info['_protocal'] = dev['ptcl']
                        info['_model'] = dev['model']
                        # 主动监控信息
                        key = "%s_%s" % (dev['ptcl'],dev['model'])
                        if key in monitorMap:
                            info['monitor'] = monitorMap[key]
                        meters[mid] = info
        return meters,pipes

    def set_primary_alarm(self,alarm):
        """
        设置告警规则
        @param alarm: {
            'E80122029_0101': {
                'callback': '',
                's': '',
                'period': 0,
                'type': 1,
                'expression': [
                    {
                        'attr': 'Ia',
                        'up': 100,
                        'down': 20,
                        'switch': '0|0|0|开关1|开关2|0'
                    }
                ]
            }
        }
        """
        if not alarm:
            return False
        alarmMap = ujson.loads(alarm)
        mids = [mid for mid,_ in alarmMap.items()]
        meters,pipes = self._get_wg_info(mids)
        # 主动监控参数
        monitorMap = {}
        # 告警规则处理         
        for mid,item in alarmMap.items():
            meter = meters.get(mid,None)
            # 主动监控
            mMap = {}
            if item and item['expression']:
                if meter and 'monitor' in meter and meter['monitor']:
                    for m in meter['monitor']:
                        mMap[m[0]] = [] if len(m) < 4 else ''
                # 调整为用function的形式
                func = "function check(items){var len=items.length;var now=len>=1?items[len-1]:null;var last=len>=2?items[len-2]:null;"
                for exp in item['expression']:
                    data = {
                        '_protocal': meter['_protocal'],
                        '_model': meter['_model']
                    }
                    if 'down' in exp:
                        downData = data.copy()
                        downData[exp['attr']] = exp['down']
                        Protocal.normal_process(meter,downData,True)
                        func += self._create_function('down',exp['attr'],downData[exp['attr']])
                        # 主动监控
                        if exp['attr'] in mMap and isinstance(mMap[exp['attr']],list):
                            mMap[exp['attr']].append(downData[exp['attr']])
                    if 'up' in exp:
                        upData = data.copy()
                        upData[exp['attr']] = exp['up']
                        Protocal.normal_process(meter,upData,True)
                        func += self._create_function('up',exp['attr'],upData[exp['attr']])
                        # 主动监控
                        if exp['attr'] in mMap and isinstance(mMap[exp['attr']],list):
                            mMap[exp['attr']].append(upData[exp['attr']])
                    if 'switch' in exp:
                        func += self._create_function('switch',exp['attr'],0)
                        # 主动监控
                        if exp['attr'] in mMap and isinstance(mMap[exp['attr']],str):
                            # 转为011011形式
                            switch = ['1' if it != '0' else '0' for it in exp['switch'].split('|')]
                            mMap[exp['attr']] = ''.join(switch)
                del item['expression']
                func += 'return false;}'
                item['function'] = func
                item['type'] = 3
                # 暂时固定设置1小时内的数据
                if 'period' not in item:
                    item['period'] = 3720
            monitorMap[mid] = mMap
        # 组装需要设置的主动监控
        monitorPipes = {}
        for key,item in monitorMap.items():
            code = key[:-5]
            if code not in pipes:
                continue
            pipe = int(key[-3:-2]) - 1
            no = str(eval('0x' + key[-2:]))
            if code not in monitorPipes:
                monitorPipes[code] = {}
            if pipe not in monitorPipes[code]:
                monitorPipes[code][pipe] = pipes[code][pipe]
            if item:
                monitorPipes[code][pipe][no]['monitor'] = item.values()
            elif 'monitor' in monitorPipes[code][pipe][no]:
                del monitorPipes[code][pipe][no]['monitor']
        # 设置主动监控
        for uid,pipes in monitorPipes.items():
            for pipe,conf in pipes.items():
                devs = ujson.dumps(conf.values())
                ret = super()._request('wg/update_pipe',id=uid,pipe=pipe,devs=devs)
        return super()._request('set_alarm',alarm=ujson.dumps(alarmMap))

    def _create_function(self,tp,attr,val):
        """
        创建告警函数
        """
        if tp == 'up':
            return "if(now&&now['%s']&&now['%s']>=%f){return true;}" % (attr,attr,val)
        elif tp == 'down':
            return "if(now&&now['%s']&&now['%s']<%f){return true;}" % (attr,attr,val)
        elif tp == 'switch':
            return "if(now&&last&&now['%s']!==last['%s']){return true;}" % (attr,attr)
        return ''

    ############################ 数据统计类接口 ##############################

    def get_power_houry_by_day(self,devs,day,attrs='ImpEp'):
        """
        获取表计一天内每小时的用电量（包括关门数据）
        """
        if not devs:
            return False
        if not day:
            day = datetime.now().strftime('%Y%m%d')
        data = self.get_hourly_by_day(devs=devs,day=day,half_hour=0,attrs=attrs,rate=1)
        ret = {}
        for mid,d in data.items():
            ret[mid] = PowerUtil.calc_power_by_hour(mid,d,attrs)
        return ret
    
    def get_power_hourly_by_month(self,devs,month,attrs='ImpEp'):
        """
        获取表计一月内每小时的用电量（包括关门数据）
        """
        if not devs:
            return False
        if not month:
            month = datetime.now().strftime('%Y%m')

        data = self.get_hourly_by_month(devs=devs,month=month,half_hour=0,attrs=attrs,rate=1)
        ret = {}
        for mid,d in data.items():
            ret[mid] = PowerUtil.calc_power_by_hour(mid,d,attrs)
        return ret

    def get_power_hourly_in_range(self,devs,beg,end,attrs='ImpEp'):
        """
        获取表计一段时间内每小时的用电量（包括关门数据）
        """
        if not devs or not beg:
            return False
        if not end:
            end = datetime.now().strftime('%Y%m%d')
        # end加一天
        end = (datetime.strptime(end, '%Y%m%d') + timedelta(days=1)).strftime('%Y%m%d')

        data = self.get_hourly_in_range(devs=devs,beg=beg,end=end,half_hour=0,attrs=attrs,rate=1)
        ret = {}
        for mid,d in data.items():
            ret[mid] = PowerUtil.calc_power_by_hour(mid,d,attrs)
        return ret

    def get_power_daily_by_month(self,devs,month,attrs='ImpEp'):
        """
        获取表计一月内每天的用电量（包括关门数据）
        """
        if not devs:
            return False
        if not month:
            month = datetime.now().strftime('%Y%m')
        data = self.get_daily_by_month(devs=devs,month=month,attrs=attrs,rate=1)
        ret = {}
        for mid,d in data.items():
            ret[mid] = PowerUtil.calc_power_by_day(mid,d,attrs)
        return ret

    def get_power_daily_in_range(self,devs,beg,end,attrs='ImpEp'):
        """
        获取表计一段时间内每天的用电量（包括关门数据）
        """
        if not devs or not beg:
            return False
        if not end:
            end = datetime.now().strftime('%Y%m%d')
        # end加一天
        end = (datetime.strptime(end, '%Y%m%d') + timedelta(days=1)).strftime('%Y%m%d')

        data = self.get_daily_in_range(devs=devs,beg=beg,end=end,attrs=attrs,rate=1)
        ret = {}
        for mid,d in data.items():
            ret[mid] = PowerUtil.calc_power_by_day(mid,d,attrs)
        return ret

    def get_power_monthly_by_year(self,devs,year,attrs='ImpEp'):
        """
        获取表计一年内每月的用电量（包括关门数据）
        """
        if not devs:
            return False
        if not year:
            year = datetime.now().strftime('%Y')
        days = []
        # 查询每月第一天
        for month in range(12):
            days.append("%s%02d01" % (year,month + 1))
        # 加上下一年第一天
        days.append("%s0101" % (int(year) + 1,))
        data = self.get_daily_at(devs=devs,days=",".join(days),attrs=attrs,rate=1)
        ret = {}
        for mid,d in data.items():
            d = sorted(d.values(),key=lambda x: x['_tm'])
            ret[mid] = PowerUtil.calc_power_by_month(mid,d,attrs)
        return ret

    def get_power_monthly_in_range(self,devs,beg,end,attrs='ImpEp'):
        """
        获取表计一段时间内每月的用电量（包括关门数据）
        """
        if not devs or not beg:
            return False
        if not end:
            end = datetime.now().strftime('%Y%m')
        days = []
        # end加一月
        m = int(end[-2:])
        y = int(end[:4])
        if m < 12:
            m = m + 1
        else:
            m = 1
            y = y + 1
        end = "%04d%02d" % (y,m)
        # 查询每月第一天
        month = end
        while (month >= beg):
            days.append(month + '01')
            month = (datetime.strptime(month + '01', '%Y%m%d') - timedelta(days=1)).strftime('%Y%m')
        data = self.get_daily_at(devs=devs,days=",".join(days),attrs=attrs,rate=1)
        ret = {}
        for mid,d in data.items():
            d = sorted(d.values(),key=lambda x: x['_tm'])
            ret[mid] = PowerUtil.calc_power_by_month(mid,d,attrs)
        return ret

class DataApiLocal(DataApi):
    """
    本地版接口
    """

    def __init__(self,baseurl,appid,appsecret,configObj=None,debug=False,timeout=30):
        """
        初始化类
        """
        super().__init__(baseurl=baseurl,appid=appid,appsecret=appsecret,configObj=configObj,debug=debug,timeout=timeout)

    def _get_meter_info(self):
        """
        （本地版接口）
        获取表计信息，变比、协议、采集属性等信息
        @param mids 采集编号，E80142003_0101
        """
        if not self._full_mids:
            return False
        # 获取全部网关信息
        ret = super()._request('global')
        if ret:
            wgs = ret['wg_list']
            # 获取协议信息
            protocals = {}
            for item in ret['model_list']:
                key = "%s_%s" % (item['ptcl'],item['model'])
                protocals[key] = item['attrs']
            for wg in wgs:
                for index,pipe in enumerate(wg['pipes']):
                    for _,dev in pipe.items():
                        mid = "%s_%02d%02X" % (wg['uid'],(index + 1),dev['no'])
                        if mid in self._full_mids:
                            info = {
                                'code': mid
                            }
                            # 变比信息
                            info['rate'] = {
                                'pt': dev['pt'] if dev['pt'] else 1,
                                'ct': dev['ct'] if dev['ct'] else 1,
                                'pct': dev['pct'] if dev['pct'] else 1
                            }
                            # 属性信息
                            key = "%s_%s" % (dev['ptcl'],dev['model'])
                            info['attrs'] = protocals[key] if key in protocals else {}
                            self._meters[mid] = info

    def _get_wg_info(self,mids):
        """
        获取网关信息
        """
        if not mids:
            return False
        meters = {}
        # 获取全部网关信息
        ret = super()._request('global')
        pipes = {}
        if ret:
            wgs = ret['wg_list']
            # 获取协议信息
            monitorMap = {}
            for item in ret['model_list']:
                if 'monitor' in item:
                    key = "%s_%s" % (item['ptcl'],item['model'])
                    monitorMap[key] = item['monitor']
            for wg in wgs:
                pipes[wg['uid']] = wg['pipes']
                for index,pipe in enumerate(wg['pipes']):
                    for _,dev in pipe.items():
                        mid = "%s_%02d%02X" % (wg['uid'],(index + 1),dev['no'])
                        if mid in mids:
                            info = {
                                'code': mid
                            }
                            # 变比信息
                            info['rate'] = {
                                'pt': dev['pt'] if dev['pt'] else 1,
                                'ct': dev['ct'] if dev['ct'] else 1,
                                'pct': dev['pct'] if dev['pct'] else 1
                            }
                            # 协议信息
                            info['_protocal'] = dev['ptcl']
                            info['_model'] = dev['model']
                            # 主动监控信息
                            key = "%s_%s" % (dev['ptcl'],dev['model'])
                            if key in monitorMap:
                                info['monitor'] = monitorMap[key]
                            meters[mid] = info
        return meters,pipes