"""
@author: tusky
@time: 2019/2/14 下午3:32
@desc: 计算用电量工具
"""
import moment

class PowerUtil(object):

    @classmethod
    def calc_power_by_hour(cls,mid,vals,attrs):
        return cls._calc_power_by_period(mid,vals,attrs,'hour')

    @classmethod
    def calc_power_by_day(cls,mid,vals,attrs):
        return cls._calc_power_by_period(mid,vals,attrs,'day')

    @classmethod
    def calc_power_by_month(cls,mid,vals,attrs):
        return cls._calc_power_by_period(mid,vals,attrs,'month')

    @classmethod
    def _calc_power_by_period(cls,mid,vals,attrs,period):
        if not vals:
            return {}
        period_seconds = 3600
        fmt = '%Y%m%d%H'
        if period == 'day':
            period_seconds *= 24
            fmt = '%Y%m%d'
        elif period == 'month':
            period_seconds *= 24 * 31
            fmt = '%Y%m'
        ret = {}
        pre_val = None
        per_power = 0

        for val in vals:
            if pre_val is None:
                pre_val = val
            else:
                if val['_tm'] - pre_val['_tm'] < period_seconds * 2:
                    hour = moment.unix(pre_val['_tm']).strftime(fmt)
                    attrList = attrs.split(',')
                    for attr in attrList:
                        if attr and attr in val and attr in pre_val:
                            power = val[attr] - pre_val[attr]
                            if hour not in ret:
                                ret[hour] = {}
                            if power < 0:
                                # 小于零的设置为None
                                ret[hour][attr] = None
                            else:
                                ret[hour][attr] = power
                                per_power = power
                pre_val = val
        return ret
