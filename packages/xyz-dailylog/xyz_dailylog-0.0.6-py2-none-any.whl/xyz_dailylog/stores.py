# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals

from xyz_util.mongoutils import Store


class ObjectLog(Store):
    name = 'object_log'
    timeout = 1000

    def log(self, model, id, action='views'):
        self.inc({'model': model, 'id': int(id)}, {action: 1})

    def find(self, model, ids, action='views'):
        return self.collection.find({'model': model, 'id': {'$in': ids}}, {'_id': '$id', 'count': '$' + action})
