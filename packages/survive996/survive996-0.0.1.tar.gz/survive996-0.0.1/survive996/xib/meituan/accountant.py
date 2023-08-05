# -*- coding: UTF-8 -*-
import pandas as pd
from functools import reduce
from spongebox.timebox import timeit
from abc import ABCMeta, abstractmethod


class Product:

    def __init__(self):
        self.META = None
        self.TRADES = None
        self.SEP = None
        self.USECOLS = None
        self.SUBJECT_COL = None
        self.DIRECT_COL = None
        self.TRADE_TYPE_COL = None
        self.AMOUNT_COL = None
        self.DATA_READER = None


class MT(Product):

    def __init__(self, account_book_path: str, encoding="gbk", nrows=None, chunksize=1000000):
        super(MT, self).__init__()
        self.META = "entry_id,fiscal_date,account_no,account_name,loan_id,loan_no,subject_code,subject_name,direct,amount,balance_direct,balance,tran_jrnl_id,remark,id,trade_type".split(
            ",")
        self.SUBJECT_COL = "subject_code"
        self.DIRECT_COL = "direct"
        self.TRADE_TYPE_COL = "trade_type"
        self.AMOUNT_COL = "amount"
        self.USECOLS = "subject_code,direct,amount,trade_type".split(",")
        self.SEP = "\|\+\|"
        self.TRADES = None
        self.nrows = nrows
        self.chunksize = chunksize
        self.account_book_path = account_book_path
        self.encoding = encoding
        self.pick_loader()
        self.load_data()

    def pick_loader(self):
        src = self.account_book_path.split(".")[-1]
        if src == "csv":
            self.load_data = self.load_csv
        else:
            self.load_data = self.load_plaintext

    def load_csv(self):
        self.DATA_READER = pd.read_csv(self.account_book_path, encoding=self.encoding, skiprows=1,
                                       nrows=self.nrows, header=None, names=self.META, usecols=self.USECOLS, iterator=True, chunksize=self.chunksize)
        return self

    def load_plaintext(self):
        self.DATA_READER = pd.read_csv(self.account_book_path, sep=self.SEP, encoding=self.encoding, engine="python", skiprows=0,
                                       nrows=self.nrows, header=None, names=self.META, usecols=self.USECOLS, iterator=True, chunksize=self.chunksize)
        return self


class MTL(MT):

    def __init__(self, account_book_path: str, encoding="gbk", nrows=None, chunksize=1000000):
        super(MTL, self).__init__(
            account_book_path, encoding, nrows, chunksize)
        self.TRADES = [("贷款发放", 11400101, 13300700), ("计提表内利息", 13202001, 50080801), ("计提表内罚息", 13210901, 50080801), ("计提表外利息", 13202001, 13220901), ("计提表外罚息", 13210901, 13220901), ("利息转表外", 50080801, 13220901), ("罚息转表外", 50080801, 13220901), ("利息转表内", 13220901, 50080801),
                       ("罚息转表内", 13220901, 50080801), ("实还本金", 13311700, 11400101), ("实还表内利息", 13311700, 13202001), ("实还表内罚息", 13311700, 13210901), ("实还表外利息", 13311700, 13202001), ("实还表外利息备抵", 13220901, 50080801), ("实还表外利息", 13311700, 13210901), ("实还表外罚息备抵", 13220901, 50080801)]


class MTF(MT):

    def __init__(self, account_book_path: str, encoding="gbk", nrows=None, chunksize=1000000):
        super(MTF, self).__init__(
            account_book_path, encoding, nrows, chunksize)
        self.TRADES = [("贷款发放", 11400301, 13300700), ("计提表内利息", 13202003, 50080803), ("计提每日表内罚息", 13210903, 50080803), ("实还正常本金（应计）", 13311700, 11400301), ("实还正常利息（表内）", 13311700, 13202003), ("实还逾期利息（表内）", 13311700,
                                                                                                                                                                                                13210903), ("ins_rep_prin", 24300400, 11400301), ("ins_rep_inter", 24300400, 13202003), ("ins_rep_penal", 24300400, 13210903), ("cus_rep_ins", 13311700, 24300400), ("cus_rep_xib", 13311700, 50080803)]
        self.TRADES.append(("收取提前还款违约金", 13311700, 50301403))


class Accountant(metaclass=ABCMeta):

    def __init__(self, product: Product):
        self.product = product

    @abstractmethod
    def check(self, chunk):
        pass

    @abstractmethod
    def merge(self, x, y):
        pass

    @abstractmethod
    def normalize(self, _):
        return _

    def display(func):
        def accounting(*args, **kwargs):
            _ = func(*args, **kwargs)
            print(_)
            return _
        return accounting

    @timeit
    @display
    def accounting(self):
        _ = reduce(self.merge, map(self.check, self.product.DATA_READER))
        return self.normalize(_)


class AccountantV2(Accountant):

    def check(self, chunk):
        print("process chunk {}-{}".format(chunk.iloc[0].name, chunk.iloc[-1].name))
        return chunk.groupby([self.product.SUBJECT_COL, self.product.DIRECT_COL, self.product.TRADE_TYPE_COL]).sum().reset_index()

    def merge(self, x, y):
        return pd.concat([x, y], sort=False).groupby([self.product.TRADE_TYPE_COL, self.product.SUBJECT_COL, self.product.DIRECT_COL]).sum().reset_index()

    def normalize(self, _):
        _ = _.pivot(self.product.TRADE_TYPE_COL,
                    self.product.DIRECT_COL, self.product.AMOUNT_COL)
        _["diff"] = _.iloc[:, 0] - _.iloc[:, 1]
        return _


class AccountantV1(Accountant):

    def check(self, chunk):

        def check_single_subject(trade):
            trade_type, subject_code_D, subject_code_C = trade[
                0], trade[1], trade[2]
            # 核算借方科目
            C_1 = chunk[(chunk.trade_type == trade_type) & (
                chunk.subject_code == subject_code_D) & (chunk.direct == "C")]["amount"].sum()
            D_1 = chunk[(chunk.trade_type == trade_type) & (
                chunk.subject_code == subject_code_D) & (chunk.direct == "D")]["amount"].sum()
            _D = D_1 - C_1
            # 核算贷方科目
            C_2 = chunk[(chunk.trade_type == trade_type) & (
                chunk.subject_code == subject_code_C) & (chunk.direct == "C")]["amount"].sum()
            D_2 = chunk[(chunk.trade_type == trade_type) & (
                chunk.subject_code == subject_code_C) & (chunk.direct == "D")]["amount"].sum()
            _C = D_2 - C_2
            return {trade_type: [_D, _C]}

        return reduce(self.merge, map(check_single_subject, self.product.TRADES))

    def merge(self, x, y):
        for y_key in y:
            if y_key in x:
                x[y_key] = [i + j for i, j in zip(x[y_key], y[y_key])]
            else:
                x[y_key] = y[y_key]
        return x

    def normalize(self, _):
        _ = pd.DataFrame(_)
        _.index = ["D", "C"]
        _ = pd.DataFrame(_.values.T, index=_.columns, columns=_.index)
        _["diff"] = _["D"] + _["C"]
        return _


class AccountantV3(Accountant):

    def haha(self):
        pass

if __name__ == "__main__":
    # acct = AccountantV3()
    _ = AccountantV2(MTF("E:\\下载\\subject_detail_20350501", encoding="utf-8")).accounting()
    _ = AccountantV2(MTF("E:\\Documents\\Scripts\\20201023_美团等本等息\\acc_2035-05-01\\2035-06-01\\subject_detail_20350601",
                         encoding="utf-8")).accounting()
    # _ = AccountantV1(MTL("E:\\XIBDATA\\MTL\\科目明细账表20200923.csv")).accounting()
    # _ = AccountantV2(MTL(
    #     "E:\\Documents\\Scripts\\20200907_美团生意贷联调\\2040-01-08 (4)\\2040-01-08\\subject_detail_20400108", encoding="UTF-8")).accounting()
    # _ = AccountantV1(MTF(
    #     "E:\\Documents\\Scripts\\20200611_MT_ACC_消费贷全账务、负值测试\\subject_detail_20210102", encoding="UTF-8")).accounting()
