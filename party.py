# -*- coding: utf-8 -*-
'''
    party

    :copyright: (c) 2014 by Openlabs Technologies & Consulting (P) Ltd.
    :license: GPLv3, see LICENSE for more details

'''
from trytond.pool import PoolMeta, Pool
from nereid import route, login_required, render_template, request, \
    current_user, redirect, url_for, flash, abort
from trytond.model import fields
from wtforms import IntegerField, validators, ValidationError
from checkout import CreditCardForm
from .i18n import _
from trytond.error import UserError

__metaclass__ = PoolMeta
__all__ = ['Party']


class PaymentProfileForm(CreditCardForm):
    address = IntegerField([validators.Required()])

    def validate_address(form, field):
        """
        Validate address selected by user.
        """
        address = Pool().get('party.address').search([
            ('party.id', '=', current_user.party.id),
            ('id', '=', field.data),
        ], limit=1)
        if not address:
            raise ValidationError('Address you selected is not valid.')


class Party:
    __name__ = 'party.party'

    # The nereid session which created the party. This is used for
    # vaccuming parties which dont need to exist, since they have only
    # carts abandoned for a long time
    nereid_session = fields.Char('Nereid Session')

    def get_payment_profiles(self, method='credit_card'):
        '''
        Return all the payment profiles of the type
        '''
        PaymentProfile = Pool().get('party.payment_profile')

        return PaymentProfile.search([
            ('party', '=', self.id),
            ('gateway.method', '=', method),
        ])

    @classmethod
    @route('/my-cards', methods=['GET'])
    @login_required
    def view_payment_profiles(cls):
        """
        Render all the cards available in user account.
        """
        if not request.nereid_website.save_payment_profile:
            abort(404)
        return render_template('my-cards.jinja')

    @classmethod
    @route('/my-cards/add-card', methods=['GET', 'POST'])
    @login_required
    def add_payment_profile(cls):
        """
        Add card to user profile.
        """
        AddPaymentProfileWizard = Pool().get(
            'party.party.payment_profile.add', type='wizard'
        )
        Address = Pool().get('party.address')

        gateway = request.nereid_website.credit_card_gateway
        form = PaymentProfileForm()

        if not request.nereid_website.save_payment_profile:
            abort(404)
        if form.validate_on_submit():

            profile_wiz = AddPaymentProfileWizard(
                AddPaymentProfileWizard.create()[0]
            )
            profile_wiz.card_info.party = current_user.party
            profile_wiz.card_info.address = Address(form.address.data)
            profile_wiz.card_info.provider = gateway.provider
            profile_wiz.card_info.gateway = gateway
            profile_wiz.card_info.owner = form.owner.data
            profile_wiz.card_info.number = form.number.data
            profile_wiz.card_info.expiry_month = form.expiry_month.data
            profile_wiz.card_info.expiry_year = \
                unicode(form.expiry_year.data)
            profile_wiz.card_info.csc = form.cvv.data

            try:
                profile_wiz.transition_add()
                flash(_('Credit Card added successfully!'))
            except UserError, e:
                flash(_(e.message))
            finally:
                return redirect(url_for('party.party.view_payment_profiles'))
        return render_template('add-card.jinja', form=form)
