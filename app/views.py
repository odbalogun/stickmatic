from flask import Blueprint, render_template_string, request, redirect, url_for
from .models import DepositTransaction, User
from .payments import PaystackPay
import requests


blueprint = Blueprint("pages", __name__)


@blueprint.route('/webpay', methods=['POST'])
def webpay():
    # check that form has necessary fields
    form = request.form

    if not form.get('user_id') or not form.get('amount'):
        return render_template_string("Error: Mandatory field not provided")

    user = User.query.get(form.get('user_id'))

    if not user:
        return render_template_string("Error: User does not exist")

    # create Transaction item
    tran = DepositTransaction(user_id=user.id, amount=form.get('amount'), mode='paystack')
    tran.save()

    # call Paystack api to create transaction
    paystack = PaystackPay()
    response = paystack.fetch_authorization_url(email=user.identity_email, amount=tran.price)

    # save transaction information
    data = response.json()
    if data.get('status'):
        tran.txn_reference = data.get('data').get('reference')
        tran.save()

        # redirect to paystack payment page
        redirect(data.get('data').get('authorization_url'))
    return render_template_string("Error: Something went wrong. Please contact an administrator")


@blueprint.route('/process-transaction', methods=['GET', 'POST'])
def process_txn():
    reference = request.args.get('reference')

    if not reference:
        return render_template_string("Error: No reference found")

    # fetch transaction
    tran = DepositTransaction.query.filter_by(txn_reference=reference).first()

    if tran:
        # check if value has already been given
        if tran.status != 0:
            return render_template_string("Error: This transaction is no longer valid")
        # verify transaction
        paystack = PaystackPay()
        response = paystack.verify_reference_transaction(reference=reference)

        if response.status_code == 200:
            # update transaction
            tran.status = 1
            tran.save()

            payload = {'mode': "paystack", 'amount': tran.amount}
            r = requests.post(url_for('api.deposit_endpoint', wallet_id=tran.user.wallet.id, _external=True),
                              data=payload)

            return render_template_string("Success: Transaction has been completed")
        else:
            return render_template_string("Error: The transaction could not be completed")
    return render_template_string("Error: No transaction found")


@blueprint.route('/process-transaction-hook', methods=['GET', 'POST'])
def process_txn_hook():
    # todo this function should return JSON
    reference = request.args.get('reference')

    if not reference:
        return render_template_string("Error: No reference found")

    # fetch transaction
    tran = DepositTransaction.query.filter_by(txn_reference=reference).first()

    if tran:
        # check if value has already been given
        if tran.status != 0:
            return render_template_string("Error: This transaction is no longer valid")
        # verify transaction
        paystack = PaystackPay()
        response = paystack.verify_reference_transaction(reference=reference)

        if response.status_code == 200:
            # update transaction
            tran.status = 1
            tran.save()

            payload = {'mode': "paystack", 'amount': tran.amount}
            r = requests.post(url_for('api.deposit_endpoint', wallet_id=tran.user.wallet.id, _external=True),
                              data=payload)

            return render_template_string("Success: Transaction has been completed")
        else:
            return render_template_string("Error: The transaction could not be completed")
    return render_template_string("Error: No transaction found")
