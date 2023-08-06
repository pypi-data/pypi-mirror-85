# Copyright (C) 2019 Majormode.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Majormode or one of its subsidiaries.  You shall not disclose this
# confidential information and shall use it only in accordance with the
# terms of the license agreement or other applicable agreement you
# entered into with Majormode.
#
# MAJORMODE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY
# OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE, OR NON-INFRINGEMENT.  MAJORMODE SHALL NOT BE LIABLE FOR ANY
# LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING
# OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.

from majormode.perseus.client.service.base_service import BaseService
from majormode.perseus.model.obj import Object


class SimCardService(BaseService):
    BaseService._declare_custom_exceptions({
#        'AuthenticationFailureException': AccountService.AuthenticationFailureException,
    })


    def __init__(self, connection):
        super(SimCardService, self).__init__(connection)


    def set_sim_card(self, iccid,
            balance=None,
            billing_frequency=None,
            billing_method=None,
            billing_time=None,
            ownership=None,
            currency_code=None,
            data_fee=None,
            data_limit=None,
            data_used=None,
            payment_method=None,
            unlimited_data=None):
        """
        Specify the properties of the SIM card, such as its billing and data
        plan information.


        @param iccid: integrated Circuit Card IDentifier (ICCID) stored in the
            SIM card.

        @param balance: current balance amount of a prepaid SIM card.  This
            parameter is required when the card owner is the service provider
            and when using a prepaid billing method.

        @param billing_frequency: an item of the enumeration
            ``BillingFrequency`` that indicates the billing frequency for the
            data service.  This parameter is required when data are not
            unlimited.

        @param billing_method: an item of the enumeration ``BillingMethod``
            that indicates the billing method of this SIM card.  This
            parameter is required when the card owner is the service provider.

        @param billing_time: the time of the last billing for the data
            service.  Monthly subscription charges generally commence at this
            time.  This parameter is required when data are not unlimited.

        @param ownership: an item of the enumeration ``Ownership`` that
            indicates who the owner of this SIM card is, and therefore who is
            responsible for paying the SIM card fee to the carrier.  Only an
            administrator of the platform can specified this information,
            otherwise the function raises the exception
            ``IllegalAccessException``.

        @param currency_code: ISO 4217 alphabetical code representing the
            currency of the SIM card's balance and data fee.  This alphabetic
            code is based on another ISO standard, ISO 3166, which lists the
            codes for country names.  The first two letters of the ISO 4217
            three-letter code are the same as the code for the country name,
            and where possible the third letter corresponds to the first
            letter of the currency name.  This parameter is required when the
            parameter ``data_fee`` or ``balance`` is passed to this function.

        @param data_fee: Fee for the data plan depending on the billing
            frequency.  This parameter is only when the card owner is the
            service provider and when the data are not unlimited.

        @param data_limit: monthly data usage in MB the plan allows.  Once
            data usage exceeds this limit, the customer may be charged a data
            overage rate.  This parameter is required when data are not
            unlimited.

        @param data_used: current amount of data in MB that has been used
            since the last billing time.  This parameter is required if data
            are not unlimited.

        @param payment_method: an item of the enumeration ``PaymentMethod``
            that indicates the payment method to be used to increase the
            remaining balance of the SIM card.  This parameter is required
            when the card owner is the service provider and when using a
            prepaid billing method.

        @param unlimited_data: indicate whether the data plan includes
            unlimited data.  The carrier may reduce the bandwidth when data
            usage exceeds the data speed reduction threshold (cf. parameter
            ``data_limit``). This parameter is required when the user on
            behalf of whom this function is an administrator of the platform
            and the parameter ``ownership`` identifies the service provider,
            or when this user is the customer.


        @raise DeletedObjectException: if the SIM card cannot be used anymore
            (expired, destroyed, lost, etc.).

        @raise DisabledObjectException: if the SIM card is not currently used;
            its properties, such as the billing and data plan information, may
            not be up-to-date.

        @raise IllegalAccessException: if the argument ``ownership`` has been
            passed to this function while the user is not an administrator of
            the platform.

        @raise InvalidArgumentException: if some arguments have not been
            passed to this function while they are required.

        @raise InvalidOperationException: if the argument ``ownership`` has
            been passed to this function while the SIM card is active.  It's
            not allowed to change the ownership of a SIM card in that context.

        @raise UndefinedObjectException: if no SIM card has been registered to
            the platform with the specified ICCID.
        """
        return Object.from_json(
                self.send_request(
                        http_method=self.HttpMethod.PUT,
                        path='/sim_card/(iccid)',
                        url_bits={
                            'iccid': iccid,
                        },
                        message_body={
                            'balance': balance,
                            'billing_frequency': billing_frequency,
                            'billing_method': billing_method,
                            'billing_time': billing_time,
                            'ownership': ownership,
                            'currency_code': currency_code,
                            'data_fee': data_fee,
                            'data_limit': data_limit,
                            'data_used': data_used,
                            'payment_method': payment_method,
                            'unlimited_data': unlimited_data
                        },
                        authentication_required=True,
                        signature_required=True))
