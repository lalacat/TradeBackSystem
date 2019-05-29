import json
import copy
from importlib import import_module
from base_utils.utillibs import arglist_to_dict
from settings import default_settings


class BaseSettings(object):
    """
    这个类是将dict类型的数据赋予一个priorities的优先级
    最终生成：
    常用的API:
    get(name, default=None):根据{name:value}获得value值

    """

    # 针对某些参数不可改变，给出的标志位
    def __init__(self, values=None):
        """

        :param values: 参数对应的对象，可能是字符串，可能是数字也可能是bool值
        :param priority: 要设定的优先级

        attributes存放的是{"name":<SettingsAttribute value=' ' priority= >}
        """

        self.frozen = False
        self.attributes = {}
        self.update(values)

    def __iter__(self):

        return iter(self.attributes.items())

    def __getitem__(self, name):
        # 返回值实际返回的是SettingsAttribute对象，value和Priority都是SettingsAttribute的
        # 优先级，根据实际需要返回的是value，形成name:value的对应关系

        if name not in self:
            return None
        else:
            return self.attributes[name]

    def __contains__(self, item):
        return item in self.attributes

    def __len__(self):
        return len(self.attributes)

    def get(self, name, default=None):
        return self[name] if self[name] is not None else default

    def getbool(self, name, default=False):
        """
        将设定值转化为boolean类型的值：
        1，'1'，True,'true','True'都返回的是True
        0,'0',False,'false','False'都返回的是False


        :param name: the setting name
        :type name: string

        :param default: the value to return if no setting is found
        :type default: any
        """
        got = self.get(name, default)
        try:
            return bool(int(got))
        except ValueError:
            if got in ("True", "true"):
                return True
            if got in ("False", "false"):
                return False
            raise ValueError("仅支持以下的值为boolean类型的值返回 "
                             " 0/1, True/False, '0'/'1', "
                             "'True'/'False' and 'true'/'false'")

    def getint(self,name,default=0):
        return int(self.get(name,default))

    def getfloat(self, name, default=0.0):
        return float(self.get(name, default))

    def update(self, values):
        """
        如果value是string型数据，即value="{name:value}"则需要先将value进行Json编码，
        变成dict型values={name:value}的数据
        """
        if isinstance(values, str):
            """
            将类如'{"a":"b"}'的字符串转变为{"a":"b"}字典型
            """
            values = json.loads(values)
        if values is not None:
            # if isinstance(values, BaseSettings):
            #     for name, value in values.items():
            #         self.set(name, value)
            # else:
            for name, value in values.items():
                '''防止空格的存在导致有相同的name'''
                self.set(name.strip(), value)

    def set(self, name, value):
        self.attributes[name] = value

    def setdict(self, values):
        """针对name1=value1,...,类型的的参数values 是list类型"""
        values = arglist_to_dict(values)
        self.update(values)

    def setmodule(self,module):
        '''用于导入默认的设置包或者自定义的设置文件'''
        if isinstance(module,str):
            module = import_module(module)
        for key in dir(module):
            if key.isupper():
                self.set(key,getattr(module,key))

    def delete(self, name:str):
        del self.attributes[name]

    def copy(self):
        """对当前设置进行深度复制，为的是根据不同的对象，可能在个别的配置上存在着不同"""
        return copy.deepcopy(self)


class Settings(BaseSettings):
    """导入默认的设置文件"""
    def __init__(self,values=None):
        super(Settings,self).__init__()
        """将默认的配置导入进来"""
        self.setmodule(default_settings)
        for name,val in self:
            if isinstance(val,dict):
                self.set(name,BaseSettings(val))
        self.update(values)


def overridden_or_new_settings(settings):
    """返回添加的或者重写的配置"""
    for name, value in settings:
        """检查新写入"""
        if dir(default_settings).__contains__(name):
            """检查重写入"""
            defvalue = getattr(default_settings, name)
            if not isinstance(defvalue, dict) and settings[name] != defvalue:
                yield name, value
        else:
            yield name, value
