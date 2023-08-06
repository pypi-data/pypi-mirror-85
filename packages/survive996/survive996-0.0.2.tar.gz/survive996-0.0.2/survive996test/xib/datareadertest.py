import unittest
from survive996.xib.meituan.datareader import *
import os


class MyTestCase(unittest.TestCase):
    def test_something(self):
        print(os.getcwd())
        df = TLF().load_data("./data/TLF/bank_instmnt_init_20350501", "bank_instmnt_init")
        print(df.iloc[0])
        print(TLF().normalize(df))
        # df = MTM().load_data("E:\\Documents\\Scripts\\20201012_MTYF_账务文件\\balance.MTYF\\20270101\\bank_loan_create_20270101_1", "bank_loan_create")
        # print(df.iloc[0])
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
