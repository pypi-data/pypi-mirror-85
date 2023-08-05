# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals

from xyz_util.mongoutils import Store


class ObjectLog(Store):
    name = 'object_log'
    timeout = 1000

    def log(self, model, id, action='views'):
        key = '%s:%s' % (id, model)
        self.inc({'model': key}, {action: 1})

    def query(self, model, id, prejection={'_id': False, 'object': True, 'views': True}):
        key = '%s:%s' % (id, model)
        return self.collection.find_one({'model': key}, prejection)
