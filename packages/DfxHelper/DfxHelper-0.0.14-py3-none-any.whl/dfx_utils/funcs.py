import random, string, hashlib, json, datetime
from typing import Any


def random_str(length: int) -> str:
    seed = string.digits + string.ascii_letters
    return ''.join(random.choices(seed, k=length))


def md5(_str: str):
    return hashlib.md5(_str.encode()).hexdigest()


def json_encoder(obj: Any):
    """ JSON 序列化, 修复时间 """
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')

    return super().default(obj)


def json_decoder(obj: Any):
    """ JSON 反序列化，加载时间 """
    ret = obj
    if isinstance(obj, list):
        obj = enumerate(obj)
    elif isinstance(obj, dict):
        obj = obj.items()
    else:
        return obj

    for key, item in obj:
        if isinstance(item, (list, dict)):
            ret[key] = json_decoder(item)
        elif isinstance(item, str):
            try:
                ret[key] = datetime.datetime.strptime(item, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                ret[key] = item
        else:
            ret[key] = item
    return ret


def json_friendly_loads(obj: Any):
    return json.loads(obj, object_hook=json_decoder)


def json_friendly_dumps(obj: Any, **kwargs):
    return json.dumps(obj, ensure_ascii=False, default=json_encoder, **kwargs)


class DfxDict:

    def __init__(self, dict_ins=None, sep='.'):
        self.sep = sep
        self.dict_ins = dict_ins or dict()

    def __getitem__(self, item):
        return self.get(item)

    def __delitem__(self, key):
        if self.sep in key:
            ret_data = self.dict_ins
            keys = key.split(self.sep)
            for item in keys:
                if item in ret_data and item == keys[-1]:
                    del ret_data[item]
                ret_data = ret_data.get(item)
        elif key in self.dict_ins:
            del self.dict_ins[key]

    def __setitem__(self, key, value):
        if self.sep in key:
            use_dict = self.dict_ins
            keys = key.split(self.sep)
            for item in keys:
                if item == keys[-1]:
                    use_dict[item] = value
                else:
                    use_dict[item] = use_dict.get(item, {})
                    use_dict = use_dict[item]
        else:
            self.dict_ins[key] = value

    def __str__(self):
        return json_friendly_dumps(self.dict_ins)

    def __iter__(self):
        return self.dict_ins.__iter__()

    def keys(self):
        return self.dict_ins.keys()

    def values(self):
        return self.dict_ins.values()

    def items(self):
        return self.dict_ins.items()

    def get(self, key, default=None):
        if self.sep in key:
            ret_data = self.dict_ins
            keys = key.split(self.sep)
            for item in keys:
                if item in ret_data:
                    ret_data = ret_data.get(item, {})
                else:
                    return default
        else:
            ret_data = self.dict_ins.get(key, default)
        return DfxDict(ret_data) if isinstance(ret_data, dict) else ret_data


class SuperDict(dict):

    def __init__(self, init_dict=None, sep='.'):
        self.sep = sep
        super(SuperDict, self).__init__(init_dict or {})

    def __str__(self):
        return json_friendly_dumps(self)

    def __set_item__(self, keys, value, use_dict={}):
        if len(keys) > 1:
            use_dict[keys[0]] = {}
            self.__set_item__(keys[1:], value, use_dict[keys[0]])
        else:
            use_dict[keys[0]] = value
        return use_dict

    def __setitem__(self, key, value):
        if isinstance(key, str):
            self.update(self.__set_item__(key.split(self.sep), value))
        else:
            super(SuperDict, self).__setitem__(key, value)

    def __getitem__(self, item):
        resp = super(SuperDict, self).__getitem__(item)
        return SuperDict(init_dict=resp, sep=self.sep) if isinstance(resp, dict) else resp

    def get(self, key, default=None):
        if self.sep not in key:
            return self[key] if key in self else default
        keys = key.split(self.sep)
        if keys[0] not in self:
            return default
        return self[keys[0]].get(self.sep.join(keys[1:]), default)


if __name__ == "__main__":
    tmp = SuperDict()
    tmp[2] = 1
    tmp['f'] = 22
    tmp['a.b'] = 'c'
    tmp['d.f.x'] = 'e'
    tmp['date'] = datetime.datetime.now()
    # print(tmp['d.f'])
    print('tmp', tmp)
    print(tmp.get('d.f'))
    # tmp = DfxDict()
    # tmp['data.ip.value'] = '0.0.0.0'
    # tmp['data.domain.value'] = 'www.baidu.com'
    # del tmp['data.ip.value']
    # print(tmp)
    # for item in tmp['data'].values():
    #     print(item)
