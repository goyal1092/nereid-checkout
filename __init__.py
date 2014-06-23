# -*- coding: utf-8 -*-
'''

    nereid_checkout

    :copyright: (c) 2010-2014 by Openlabs Technologies & Consulting (P) Ltd.
    :license: GPLv3, see LICENSE for more details

'''
from trytond.pool import Pool

from sale import Sale
from payment import Website, NereidPaymentMethod
from checkout import Cart, Checkout
from party import Party


def register():
    Pool.register(
        Cart,
        Sale,
        Party,
        Website,
        Checkout,
        NereidPaymentMethod,
        type_="model", module="nereid_checkout"
    )
