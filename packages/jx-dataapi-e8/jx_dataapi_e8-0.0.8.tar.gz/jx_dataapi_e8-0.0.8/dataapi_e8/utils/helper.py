"""
@author: tusky
@time: 2019/3/4 上午9:55
@desc: 数据处理工具
"""
import sys
from scipy.interpolate import interp1d
from .meters.electric import ElectricMeter
from .meters.th import THMeter
from .meters.water import WaterMeter

class Protocal(object):
    
    # 累计值
    ACCUM_ATTR = ['ImpEp','ImpRp','ExpEp','ExpRp','EPt']
    # 插值样本大小
    SAMPLE_SIZE = 12
    # 处理类map
    CLASS_MAP = {}

    @classmethod
    def normal_process(cls,meter,data,reverse=False):
        """
        常规处理，包括缺值，变比，单位
        """
        protocal = data['_protocal']
        model = data['_model']
        obj = cls.get_class(protocal,model,meter.get('code') if meter else '')
        obj.process(meter,data,reverse)
        return data

    @classmethod
    def get_class(cls,protocal,model,mid):
        """
        根据表计类型获取处理类
        """
        class_name = 'ElectricMeter'
        # 根据协议来获取处理类
        if protocal in (1,2,3,6) or (protocal == 224 and (model == 254 or model == 6)):
            class_name = 'ElectricMeter'
        elif protocal == 4:
            class_name = 'WaterMeter'
        else:
            class_name = 'THMeter'
        # 根据编号来获取处理类，优先级大于协议
        if mid and mid in (''):
            pass
        if class_name not in cls.CLASS_MAP:
            # 动态加载处理类
            __import__(__name__)
            module = sys.modules[__name__]
            class_obj = getattr(module,class_name)
            if class_obj:
                cls.CLASS_MAP[class_name] = class_obj
            return class_obj
        else:
            return cls.CLASS_MAP[class_name]

    @classmethod
    def check_and_insert(cls,meter,index,val,series,attrs,fill_attrs):
        """
        检查缺值并插值
        """
        if not series:
            return False
        filterAttrs = attrs.split(',') if attrs else []
        meterAttrs = meter['attrs'].keys() if meter and 'attrs' in meter and meter['attrs'] else []
        # 对数据补值
        meterAttrs = list(set(meterAttrs).intersection(set(fill_attrs)))
        if isinstance(series,dict):
            data = series.values()
        else:
            data = series
        totalNum = len(data)
        for attr in meterAttrs:
            if (not filterAttrs or attr in filterAttrs) and attr not in val:
                # 获取样本数据，在缺失值前后取样本，大小为SAMPLE_SIZE
                samples = []
                sampleLeft = []
                sampleRight = []
                insertTm = val['_tm']
                left = right = index
                while left >= 0 and right <= totalNum - 1 and len(sampleLeft) + len(sampleRight) < cls.SAMPLE_SIZE:
                    if attr in data[left]:
                        sampleLeft.insert(0,{'tm':data[left]['_tm'],'data':data[left][attr]})
                    if attr in data[right]:
                        sampleRight.append({'tm':data[right]['_tm'],'data':data[right][attr]})
                    left -= 1
                    right += 1
                if len(sampleLeft) + len(sampleRight) < cls.SAMPLE_SIZE:
                    if left > 0:
                        while left >= 0 and len(sampleLeft) + len(sampleRight) < cls.SAMPLE_SIZE:
                            if attr in data[left]:
                                sampleLeft.insert(0,{'tm':data[left]['_tm'],'data':data[left][attr]})
                            left -= 1
                    if right < totalNum - 1:
                        while right <= totalNum - 1 and len(sampleLeft) + len(sampleRight) < cls.SAMPLE_SIZE:
                            if attr in data[right]:
                                sampleRight.append({'tm':data[right]['_tm'],'data':data[right][attr]})
                            right += 1
                samples.extend(sampleLeft)
                samples.extend(sampleRight)
                if len(samples) != 0:
                    # 累计值用2次样条插值
                    if attr in cls.ACCUM_ATTR:
                        xList = []
                        yList = []
                        for d in samples:
                            xList.append(d['tm'])
                            yList.append(d['data'])
                        if insertTm < xList[0] or insertTm > xList[-1]:
                            # TODO:外插
                            if insertTm < xList[0]:
                                val[attr] = float(yList[0])
                            else:
                                val[attr] = float(yList[-1])
                        else:
                            # 2次样条插值
                            f = interp1d(xList,yList,kind="slinear")
                            val[attr] = round(float(f(insertTm)),2)
                    else:
                        # 瞬时值取平均值
                        vals = [sample['data'] for sample in samples]
                        val[attr] = sum(vals) / len(vals)
                    if 'insert' not in val:
                        val['insert'] = []
                    val['insert'].append(attr)
