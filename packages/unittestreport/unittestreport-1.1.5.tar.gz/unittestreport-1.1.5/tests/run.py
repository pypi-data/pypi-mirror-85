"""
============================
Author:柠檬班-木森
Time:2020/8/19   17:48
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""
import unittest

from tests.test_case import TestClass
from unittestreport import TestRunner

suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestClass)
runner = TestRunner(suite=suite,
                    title="前程贷接口自动化执行结果",
                    templates=1)

runner.run()
runner.send_email(host="smtp.qq.com",
                  port=465,
                  user="musen_nmb@qq.com",
                  password="algmmzptupjccbab",
                  to_addrs="3247119728@qq.com")
