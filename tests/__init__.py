# -*- coding: utf-8 -*-
"""
    __init__

    Add the test suite here so that setup.py test loader picks it up

    :copyright: © 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: GPLv3, see LICENSE for more details.
"""
import unittest
import trytond.tests.test_tryton
from test_checkout import TestCheckoutSignIn, TestCheckoutShippingAddress, \
    TestCheckoutDeliveryMethod, TestCheckoutBillingAddress, TestCheckoutPayment
from test_party import TestCreditCard


def suite():
    test_suite = trytond.tests.test_tryton.suite()
    test_suite.addTests([
        unittest.TestLoader().loadTestsFromTestCase(TestCreditCard),
        unittest.TestLoader().loadTestsFromTestCase(TestCheckoutSignIn),
        unittest.TestLoader().loadTestsFromTestCase(
            TestCheckoutShippingAddress),
        unittest.TestLoader().loadTestsFromTestCase(TestCheckoutDeliveryMethod),
        unittest.TestLoader().loadTestsFromTestCase(TestCheckoutBillingAddress),
        unittest.TestLoader().loadTestsFromTestCase(TestCheckoutPayment),
    ])

    return test_suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
