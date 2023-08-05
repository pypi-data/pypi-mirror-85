"""
@author: tusky
@time: 2019/3/4 上午9:55
@desc: 电表
"""
# ********************* 基础处理 ********************* #
class BaseMeter(object):

    @classmethod
    def call_ext_method(cls,meter,data,reverse,func_name):
        """
        调用扩展方法
        """
        protocal = data['_protocal']
        model = data['_model']
        ext = func_name + "_%s_%s" % (protocal,model)
        if hasattr(cls,ext):
            method = getattr(cls,ext)
            method(meter,data,reverse)
            return True
        else:
            return False

# ********************* 电表处理 ********************* #
class ElectricMeter(BaseMeter):
    """
    通用电表处理
    """
    # 默认需要处理变比的属性
    # TODO:存入数据库
    DEFAULT_RATE_MAP = {
        'pt': ['Ua','Ub','Uc','Uab','Ubc','Uca'],
        'ct': ['Ia','Ib','Ic'],
        'pct': ['Pa','Pb','Pc','Pt','Qa','Qb','Qc','Qt','Sa','Sb','Sc','St','ImpEp','ExpEp','ImpRp','ExpRp','EPt']
    }
    # 并不是所有的属性需要处理倍率,有些接口返回的一次值,二次值的情况可能有点乱
    # TODO:存入数据库
    RATE_MAP = {
        # 南瑞继保rcx971/972,只需要有功电度、无功电度乘下倍率即可
        '6_1': {
            'pct': ["ImpEp", "ExpEp", "ImpRp", "ExpRp"]
        },
        # 乔宇的表计采集上来的值为一次值,不需要处理倍率
        '3_2': {},
        # (12年产)斯菲尔电气PD194Z-2S4_2S9_2S7
        '3_6': {},
        # (06年以前生产)斯菲尔电气CD194Z
        '3_8': {},
        # 珠海派诺SPM32
        '3_25': {
            'pct': ["Pa", "Pb", "Pc", "Pt", "Qa", "Qb", "Qc", "Qt","Sa", "Sb", "Sc", "St"],
            'pt': ['Ua','Ub','Uc','Uab','Ubc','Uca'],
            'ct': ['Ia','Ib','Ic']
        }
    }
    # 异常值判断
    EXCEPTION_MAP = {
        # 电流小于10000A
        '10000': ['Ia','Ib','Ic'],
        # 电压小于200kV
        '200000': ['Ua','Ub','Uc','Uab','Ubc','Uca'],
        # 功率小于2000000000
        '2000000000': ["Pa", "Pb", "Pc", "Pt", "Qa", "Qb", "Qc", "Qt","Sa", "Sb", "Sc", "St"],
        # 温度小于200
        '200': ['t','t1','t2','t3','t4','t5','t6','t7','t8'],
        # 功率因数小于100
        '100': ['PFt','PFa','PFb','PFc']
    }

    @classmethod
    def process(cls,meter,data,reverse=False):
        """
        数据处理
        """
        # 处理变比
        cls._processRate(meter,data,reverse)
        # 处理单位
        cls._processUnit(meter,data,reverse)
        # 处理缺值
        cls._processMiss(meter,data,reverse)
        # 处理异常值
        cls._processException(meter,data,reverse)

    @classmethod
    def _processRate(cls,meter,data,reverse):
        """
        处理变比
        """
        protocal = data['_protocal']
        model = data['_model']
        key = "%s_%s" % (protocal,model)
        if key in cls.RATE_MAP:
            rateMap = cls.RATE_MAP[key]
        else:
            rateMap = cls.DEFAULT_RATE_MAP
        for key,items in rateMap.items():
            rate = float(meter['rate'][key]) if meter and 'rate' in meter and meter['rate'][key] else 1
            if rate != 1:
                for attr in items:
                    if attr in data:
                        if reverse:
                            data[attr] /= rate
                        else:
                            data[attr] *= rate
        cls.call_ext_method(meter,data,reverse,'_processRate')
    
    @classmethod
    def _processUnit(cls,meter,data,reverse):
        """
        处理单位
        """
        cls.call_ext_method(meter,data,reverse,'_processUnit')

    @classmethod
    def _processMiss(cls,meter,data,reverse):
        """
        处理缺值
        """
        if 'Pt' not in data and 'Pa' in data and 'Pb' in data and 'Pc' in data:
            data['Pt'] = data['Pa'] + data['Pb'] + data['Pc']
        cls.call_ext_method(meter,data,reverse,'_processMiss')
    
    @classmethod
    def _processException(cls,meter,data,reverse):
        """
        处理异常值
        """
        for key,attrs in cls.EXCEPTION_MAP.items():
            for attr in attrs:
                if attr in data and data[attr] and float(data[attr]) >= float(key):
                    del data[attr]
        cls.call_ext_method(meter,data,reverse,'_processException')

    # ********************* 特殊协议处理 ********************* #
    @classmethod
    def _w2kw(cls,attrs,data,reverse):
        """
        w转换为kw
        """
        for attr in attrs:
            if attr in data:
                if reverse:
                    data[attr] *= 1000
                else:
                    data[attr] /= 1000

    @classmethod
    def _processUnit_3_1(cls,meter,data,reverse):
        """
        佳和GEC2050
        """
        for attr in ['Ua','Ub','Uc']:
            if attr in data:
                if reverse:
                    data[attr] /= 0.214844
                else:
                    data[attr] *= 0.214844
        for attr in ['Uab','Ubc','Uca']:
            if attr in data:
                if reverse:
                    data[attr] /= 0.371094
                else:
                    data[attr] *= 0.371094
        for attr in ['Ia','Ib','Ic']:
            if attr in data:
                if reverse:
                    data[attr] /= 0.004883
                else:
                    data[attr] *= 0.004883
        for attr in ['ImpEp','ExpEp','ImpRp','ExpRp']:
            if attr in data:
                if reverse:
                    data[attr] *= 100
                else:
                    data[attr] /= 100
    
    @classmethod
    def _processUnit_3_2(cls,meter,data,reverse):
        """
        乔宇
        """
        cls._w2kw(["Pt", "Pa", "Pb", "Pc", "St", "Sa", "Sb", "Sc", "Qt", "Qa", "Qb", "Qc"],data,reverse)
    
    @classmethod
    def _processUnit_3_8(cls,meter,data,reverse):
        """
        (06年以前生产)斯菲尔电气CD194Z
        """
        cls._w2kw(["Pt", "Pa", "Pb", "Pc", "St", "Sa", "Sb", "Sc", "Qt", "Qa", "Qb", "Qc",'ImpEp','ExpEp','ImpRp','ExpRp'],data,reverse)

    @classmethod
    def _processUnit_3_5(cls,meter,data,reverse):
        """
        斯菲尔电气PD194Z-2S4_2S9_2S7
        """
        cls._w2kw(["Pt", "Pa", "Pb", "Pc", "Qt", "Qa", "Qb", "Qc","St", "Sa", "Sb", "Sc",'ImpEp','ExpEp','ImpRp','ExpRp'],data,reverse)

    @classmethod
    def _processUnit_3_18(cls,meter,data,reverse):
        """
        上海提迈电气PD361H-D14-R
        """
        cls._w2kw(["Pt", "Pa", "Pb", "Pc", "Qt", "Qa", "Qb", "Qc","St", "Sa", "Sb", "Sc",'ImpEp','ExpEp','ImpRp','ExpRp'],data,reverse)

    @classmethod
    def _processUnit_3_17(cls,meter,data,reverse):
        """
        广东雅达电子YD2030系列
        """
        cls._w2kw(["Pt", "Pa", "Pb", "Pc", "Qt", "Qa", "Qb", "Qc","St", "Sa", "Sb", "Sc",'ImpEp','ExpEp','ImpRp','ExpRp'],data,reverse)

    @classmethod
    def _processUnit_6_1(cls,meter,data,reverse):
        """
        南瑞继保rcx971/972
        """
        cls._w2kw(["Pt", "Qt"],data,reverse)

    @classmethod
    def _processUnit_3_102(cls,meter,data,reverse):
        """
        上海易劲YJ194E-2S4
        """
        cls._w2kw(["Pt", "Pa", "Pb", "Pc", "St", "Sa", "Sb", "Sc", "Qt", "Qa", "Qb", "Qc"],data,reverse)

    @classmethod
    def _processUnit_3_104(cls,meter,data,reverse):
        """
        上海易劲YJ194E-2S4-V6.1
        """
        cls._w2kw(["Pt", "Pa", "Pb", "Pc", "St", "Sa", "Sb", "Sc", "Qt", "Qa", "Qb", "Qc",'ImpEp','ExpEp','ImpRp','ExpRp'],data,reverse)