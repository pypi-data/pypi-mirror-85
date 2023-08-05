# -*- coding: utf-8 -*-
# @Time    : 2020/6/6 16:03
# @Author  : Yinglin Zheng
# @Email   : zhengyinglin@stu.xmu.edu.cn
# @File    : config.py
# @Software: PyCharm
# @Affiliation: VCG@XMU
from argparse import ArgumentParser
import yaml
from collections import OrderedDict


class Config(ArgumentParser):
    def __init__(self, *args, **kwargs):
        if "key" in kwargs:
            self.key = kwargs["key"]
        else:
            self.key = None
        del kwargs["key"]
        super(Config, self).__init__(*args, **kwargs)
        self.add_argument("--" + self.key, type=str, default=None, help="config file")
        self.post_args = OrderedDict()

    def parse_args(self, args=None, namespace=None):
        args = super(Config, self).parse_args()
        if self.key is not None:
            cfg_file = getattr(args, self.key)
            assert cfg_file is not None
            with open(cfg_file, "r", encoding="utf-8") as stream:
                args_from_file = yaml.load(stream, Loader=yaml.FullLoader)
            for key, val in args_from_file.items():
                assert hasattr(args, key)
                setattr(args, key, val)
        for key, func in self.post_args.items():
            setattr(args, key, func(args))
        return args

    def add_post_arg(self, key, func):
        assert key not in self.post_args
        if "--" + key in self._option_string_actions:
            raise Exception("duplicated keys")
        self.post_args[key] = func
