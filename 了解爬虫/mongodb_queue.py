from pymongo import MongoClient,errors
from datetime import datetime,timedelta


class MongoQueue(object):
    OUTSTANDING = 1  ##初始状态
    PROCESSING = 2  ##正在下载状态
    COMPLETE = 3  ##下载完成状态


    def __init__(self, db, collection, timeout=300):
        self.client = MongoClient()
        self.Client = self.client[db]
        self.db = self.Client[collection]
        self.timeout = timeout

    def __bool__(self):
        '''
        判断是否还有未完成的线程
        '$ne'表示取反
        :return:boolean
        '''
        record = self.db.find_one(
            {'status': {'$ne':self.COMPLETE}}
        )
        return True if record else False

    def push(self, url, title):
        '''
        将要下载的url插入队列
        :param url: url地址
        :param title: 标题
        :return:
        '''
        try:
            self.db.insert(
                {'_id':url, 'status':OUTSTANDING, 'title':title}
            )
            print(url,'已插入队列')
        except errors.DuplicateKeyError as e:
            print('已经存在于队列中了')
            pass


    def pop(self):
        '''
        取出一个未开始的进程开始进程
        :return: url
        '''

        record = self.db.find_and_modify(
            query={ 'status': self.OUTSTANDING},
            update={'$set':{'status':self.PROCESSING,'timestemp':datetime.now()}}
        )

        if record:
            return record['_id']
        else:
            self.repair()
            raise KeyError

    def peek(self):
        '''
        找到一个正在等待中的进程并返回它的url
        :return: url
        '''
        record = self.db.find_one(
            {'status' : self.OUTSTANDING}
        )
        if record:
            return record['_id']


    def complete(self, url):
        '''
        更新已完成的url
        :param url: url
        :return:
        '''
        self.db.update(
            {'_id':url},
            {'$set' : {'status' : self.COMPLETE}}
        )

    def repair(self):
        record = self.db.find_and_modify(
            query={
                'timestemp': datetime.now() - timedelta(seconds=self.timeout),
                'status': {'$ne': self.COMPLETE}
            },
            update={'$set': {'status': self.OUTSTANDING}}
        )

        if record:
            print('重置url状态',record['_id'])






