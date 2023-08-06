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

from majormode.perseus.constant.obj import ObjectStatus
from majormode.perseus.service.base_rdbms_service import BaseRdbmsService
from majormode.perseus.utils import cast
from majormode.xeberus.constant.sim import BillingFrequency
from majormode.xeberus.constant.sim import BillingMethod
from majormode.xeberus.constant.sim import Ownership
from majormode.xeberus.constant.sim import PaymentMethod


class SimCardService(BaseRdbmsService):
    def get_sim_card(
            self,
            iccid,
            check_status=False,
            connection=None,
            include_billing_info=False,
            include_data_info=False):
        """
        Return the specified SIM card worth of extended information.


        :param iccid: Integrated Circuit Card IDentifier (ICCID) stored in the
            SIM card.

        :param check_status: indicate whether to check the current status of
            this SIM card and raise an exception if this SIM card is not
            enabled.

        :param connection: A `RdbmsConnection` object to be used supporting
            the Python clause `with ...:`.

        :param include_billing_info: Indicate whether to include billing
            information about this SIM card.
            
        :param include_data_info: Indicate whether to include data plan
            information about this SIM card.


        :return: an object containing the following attributes:

            * `balance` (optional): Current balance amount of a prepaid SIM card.
              This information is defined when the card owner is the service
              provider and when using a prepaid billing method.  This attribute is
              provided only if the argument `include_billing_info` is `true`.

            * `billing_frequency` (optional): An item of the enumeration
              `BillingFrequency` that indicates the billing frequency for the data
              service.  This information is defined when the card owner is the
              service provider.  This attribute is provided only if the argument
              `include_billing_info` is `true`.

            * `billing_method` (optional): An item of the enumeration
              `BillingMethod` that indicates the billing method of this SIM card.
              This attribute is provided only if the argument
              `include_billing_info` is `true`.

            * `billing_time` (optional): Time of the last billing for the data
              service.  Monthly subscription charges generally commence at this
              time. This attribute is provided only if the argument
              `include_billing_info` is `true`.

            * `ownership` (required): An item of the enumeration `Ownership`
              that indicates who the owner of this SIM card is, and therefore who is
              responsible for paying the SIM card fee to the carrier

            * `creation_time` (required): Time when this SIM card has been
              registered to the platform.

            * `currency_code` (optional): ISO 4217 alphabetical code representing
              the currency of the SIM card's balance and data fee.  This alphabetic
              code is based on another ISO standard, ISO 3166, which lists the codes
              for country names.  The first two letters of the ISO 4217 three-letter
              code are the same as the code for the country name, and where possible
              the third letter corresponds to the first letter of the currency name.
              This attribute is provided only if at least one of the arguments
              `include_billing_info` and `include_data_info` is `true`.

            * `data_fee` (optional): Fee for the data plan depending on the
              billing frequency.  This information is defined when the card owner is
              the service provider and when using a prepaid billing method.  This
              attribute is provided only if the argument `include_data_info` is
              `true`.

            * `data_limit` (optional): Monthly data usage in MB the plan allows,
              or `None` if unlimited.  Once data usage exceeds this limit, the
              customer may be charged a data overage rate.  This attribute is
              provided only if the argument `include_data_info` is `true`.

            * `data_used` (optional): Current amount of data in MB that has been
              used since the last top-up.  This attribute is provided only if the
              argument `include_data_info` is `true`.

            * `iccid` (required): Integrated Circuit Card IDentifier (ICCID)
              stored in the SIM card and also engraved or printed on the SIM card
              body during a process called personalization.  The ICCID is defined by
              the ITU-T recommendation E.118 as the Primary Account Number.  It is
              also known as the serial number of the Subscriber Identity Module
              (SIM) card of the mobile phone, or SIMID.

            * `imsi` (required): International Mobile Subscriber Identity (IMSI)
              as stored in the SIM card.  The first 3 digits are the mobile country
              code (MCC), which are followed by the mobile network code (MNC),
              either 2 digits (European standard) or 3 digits (North American
              standard).

            * `msisdn` (required): Mobile Subscriber Integrated Services Digital
              Network Number (MSISDN) currently associated to the SIM card.

            * `object_status` (required): An item of the enumeration
              `ObjectStatus` that indicates the current status of this SIM card.

            * `operator_code` (required): Identification of the mobile network
              operator (carrier) that provides the SIM card.  This identification is
              composed of the mobile country code (MCC) used in combination with the
              mobile network code (MNC) of this carrier.

              The mobile country code consists of 3 decimal digits and the mobile
              network code consists of 2 or 3 decimal digits.  The first digit of
              the mobile country code identifies the geographic region as follows
              (the digits 1 and 8 are not used):

              * `0`: Test networks

              * `2`: Europe

              * `3`: North America and the Caribbean

              * `4`: Asia and the Middle East

              * `5`: Oceania

              * `6`: Africa

              * `7`: South and Central America

              * `9`: Worldwide (Satellite, Air - aboard aircraft, Maritime -
                aboard ships, Antarctica)

            * `payment_method (optional): An item of the enumeration
              `PaymentMethod` that indicates the payment method to be used to
              increase the remaining balance of the SIM card.  This information is
               defined when the card owner is the service provider and when using a
               prepaid billing method.  This attribute is provided only if the
               argument `include_billing_info` is `true`.

            * `unlimited_data` (optional): Indicate whether the data plan includes
              unlimited data.  The carrier may reduce the bandwidth when data usage
              exceeds the data speed reduction threshold (cf. `data_limit`).
              This attribute is provided only if the argument `include_data_info`
              is `true`.

            * `update_time` (required): Time of the most recent modification of
              any variable attribute of this SIM card, such as its status, the most
              recent top-up of the SIM balance.


        :raise DeletedObjectException: if the SIM card cannot be used anymore
            (expired, destroyed, lost, etc.).

        :raise DisabledObjectException: if the SIM card is not currently used;
            its properties, such as the billing and data plan information, may
            not be up-to-date.

        :raise UndefinedObjectException: if no SIM card has been registered to
            the platform with the specified ICCID.
        """
        with self.acquire_rdbms_connection(auto_commit=False, connection=connection) as connection:
            cursor = connection.execute(
                """
                SELECT 
                    iccid,
                    imsi,
                    operator_code,
                    msisdn,
                    ownership,
                    billing_method,
                    billing_frequency,
                    billing_time,
                    payment_method,
                    data_limit,
                    unlimited_data,
                    data_used,
                    data_fee,
                    balance,
                    currency_code,
                    object_status,
                    creation_time,
                    update_time
                  FROM 
                    sim_card
                  WHERE 
                    iccid = %(iccid)s
                """,
                {
                    'iccid': iccid
                })

            row = cursor.fetch_one()
            if row is None:
                raise self.UndefinedObjectException(f"undefined SIM card with ICCID {iccid}")

            sim_card = row.get_object({
                'activation_time': cast.string_to_timestamp,
                'creation_time': cast.string_to_timestamp,
                'billing_frequency': BillingFrequency,
                'billing_method': BillingMethod,
                'billing_time': cast.string_to_timestamp,
                'ownership': Ownership,
                'object_status': ObjectStatus,
                'payment_method': PaymentMethod,
                'update_time': cast.string_to_timestamp
            })

            if check_status:
                if sim_card.object_status == ObjectStatus.deleted:
                    raise self.DeletedObjectException(f"the SIM card with ICCID {iccid} has been banned")
                elif sim_card.object_status == ObjectStatus.disabled:
                    raise self.DisabledObjectException(f"the SIM card with ICCID {iccid} has been disabled")

            if not include_billing_info:
                del sim_card.billing_frequency, \
                    sim_card.billing_method, \
                    sim_card.payment_method, \
                    sim_card.balance

            if not include_data_info:
                del sim_card.data_limit, \
                    sim_card.unlimited_data, \
                    sim_card.data_used, \
                    sim_card.data_fee

            if not (include_billing_info or include_data_info):
                del sim_card.currency_code

            return sim_card

    def register_sim_card(self, app_id, iccid, imsi, connection=None):
        """
        Register a new SIM card.  An administrator of the platform will have
        to complete its properties, such as the billing and data plan
        information, in order to active this SIM card.


        :param app_id: identification of the client application such as a Web,
            a desktop, or a mobile application, that accesses the service.

        :param iccid: Integrated Circuit Card IDentifier (ICCID) stored in the
            SIM card and also engraved or printed on the SIM card body during
            a process called personalization.  The ICCID is defined by the
            ITU-T recommendation E.118 as the Primary Account Number.  It is
            also known as the serial number of the Subscriber Identity Module
            (SIM) card of the mobile phone, or SIMID.

        :param imsi: International Mobile Subscriber Identity (IMSI) as stored
            in the SIM card.

        :param connection: A `RdbmsConnection` object to be used supporting
            the Python clause `with ...:`.


        :return: An object returned by the function `get_sim_card`.
        """
        with self.acquire_rdbms_connection(auto_commit=True, connection=connection) as connection:
            connection.execute(
                """
                INSERT INTO sim_card(
                    iccid,
                    imsi,
                    operator_code,
                    object_status)
                  VALUES 
                    (%(iccid)s,
                     %(imsi)s,
                     %(operator_code)s,
                     %(OBJECT_STATUS_PENDING)s)
                """,
                {
                    'OBJECT_STATUS_PENDING': ObjectStatus.pending,
                    'iccid': iccid,
                    'imsi': imsi,
                    'operator_code': imsi[:5]
                })

        return self.get_sim_card(iccid, connection=connection)

    def set_sim_card(
            self,
            app_id,
            account_id,
            iccid,
            balance=None,
            billing_frequency=None,
            billing_method=None,
            billing_time=None,
            connection=None,
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


        :param app_id: identification of the client application such as a Web,
            a desktop, or a mobile application, that accesses the service.

        :param account_id: identification of the account of the user who is
            defining the properties of this SIM card.

        :param iccid: integrated Circuit Card IDentifier (ICCID) stored in the
            SIM card.

        :param balance: current balance amount of a prepaid SIM card.  This
            parameter is required when the card owner is the service provider
            and when using a prepaid billing method.

        :param billing_frequency: an item of the enumeration
            `BillingFrequency` that indicates the billing frequency for the
            data service.  This parameter is required when data are not
            unlimited.

        :param billing_method: an item of the enumeration `BillingMethod`
            that indicates the billing method of this SIM card.  This
            parameter is required when the card owner is the service provider.

        :param billing_time: the time of the last billing for the data
            service.  Monthly subscription charges generally commence at this
            time.  This parameter is required when data are not unlimited.

        :param connection: A `RdbmsConnection` object to be used supporting
            the Python clause `with ...:`.

        :param ownership: an item of the enumeration `Ownership` that
            indicates who the owner of this SIM card is, and therefore who is
            responsible for paying the SIM card fee to the carrier.  Only an
            administrator of the platform can specified this information,
            otherwise the function raises the exception
            `IllegalAccessException`.

        :param currency_code: ISO 4217 alphabetical code representing the
            currency of the SIM card's balance and data fee.  This alphabetic
            code is based on another ISO standard, ISO 3166, which lists the
            codes for country names.  The first two letters of the ISO 4217
            three-letter code are the same as the code for the country name,
            and where possible the third letter corresponds to the first
            letter of the currency name.  This parameter is required when the
            parameter `data_fee` or `balance` is passed to this function.

        :param data_fee: Fee for the data plan depending on the billing
            frequency.  This parameter is only when the card owner is the
            service provider and when the data are not unlimited.

        :param data_limit: monthly data usage in MB the plan allows.  Once
            data usage exceeds this limit, the customer may be charged a data
            overage rate.  This parameter is required when data are not
            unlimited.

        :param data_used: current amount of data in MB that has been used
            since the last billing time.  This parameter is required if data
            are not unlimited.

        :param payment_method: an item of the enumeration `PaymentMethod`
            that indicates the payment method to be used to increase the
            remaining balance of the SIM card.  This parameter is required
            when the card owner is the service provider and when using a
            prepaid billing method.

        :param unlimited_data: indicate whether the data plan includes
            unlimited data.  The carrier may reduce the bandwidth when data
            usage exceeds the data speed reduction threshold (cf. parameter
            `data_limit`).  This parameter is required when the user on
            behalf of whom this function is an administrator of the platform
            and the parameter `ownership` identifies the service provider,
            or when this user is the customer.


        :raise DeletedObjectException: if the SIM card cannot be used anymore
            (expired, destroyed, lost, etc.).

        :raise DisabledObjectException: if the SIM card is not currently used;
            its properties, such as the billing and data plan information, may
            not be up-to-date.

        :raise IllegalAccessException: if the argument `ownership` has been
            passed to this function while the user is not an administrator of
            the platform.

        :raise InvalidArgumentException: if some arguments have not been
            passed to this function while they are required.

        :raise InvalidOperationException: if the argument `ownership` has
            been passed to this function while the SIM card is active.  It's
            not allowed to change the ownership of a SIM card in that context.

        :raise UndefinedObjectException: if no SIM card has been registered to
            the platform with the specified ICCID.
        """
        # Retrieve the current properties of the SIM card.
        sim_card = self.get_sim_card(iccid, check_status=True, connection=connection)

        # Check that the ownership has been defined or is being defined, which
        # is required to define the other properties of the SIM card.
        if not sim_card.ownership and not ownership:
            raise self.InvalidArgumentException('Card ownership is required')

        # # The owner of the SIM card can be specified only by an administrator
        # # of the platform.
        # from majormode.xeberus.service.xeberus.xeberus_service import \
        #     XeberusService
        #
        # is_administrator = TeamService().is_administrator(account_id, XeberusService.XEBERUS_TEAM.team_id)
        # if ownership:
        #     TeamService()._assert_administrator(account_id, XeberusService.XEBERUS_TEAM.team_id)
        #
        #     if sim_card.object_status == ObjectStatus.enabled:
        #         raise self.InvalidOperationException('It is not possible to change the ownership of an active SIM card')

        # Check that the required parameters have been properly defined.
        if billing_method is None and ownership == Ownership.service:
            raise self.InvalidArgumentException('billing method is required')

        # if unlimited_data is None and (ownership == Ownership.customer or \
        #     (is_administrator and ownership == Ownership.service)):
        #     raise self.InvalidArgumentException('The indicator whether data are unlimited is required')

        if billing_frequency is None and unlimited_data is None:
            raise self.InvalidArgumentException('billing frequency is required')

        if billing_time is None and unlimited_data is None:
            raise self.InvalidArgumentException('last billing time is required')

        if payment_method is None and ownership == Ownership.service and billing_method == BillingMethod.prepaid:
            raise self.InvalidArgumentException('billing method is required')

        if data_limit is None and not unlimited_data:
            raise self.InvalidArgumentException('data limit is required')

        if data_used is None and not unlimited_data:
            raise self.InvalidArgumentException('data used is required')

        if data_fee is None and ownership == Ownership.service:
            raise self.InvalidArgumentException('data fee is required')

        if balance is None and ownership == Ownership.service and billing_method == BillingMethod.prepaid:
            raise self.InvalidArgumentException('balance is required')

        if currency_code is None and (data_fee or balance):
            raise self.InvalidArgumentException('currency code is required')

        # Save the properties of the SIM card that have been specified, i.e.,
        # not null.
        fields = {
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
        }

        defined_fields = dict([
            (name, value)
            for (name, value) in fields.iteritems()
            if value is not None
        ])

        if defined_fields:
            update_set_expression = ','.join([
                '%s = %%(%s)s' % (name, name)
                for name in defined_fields.iterkeys()
            ])

            defined_fields['iccid'] = iccid

            with self.acquire_rdbms_connection(True) as connection:
                connection.execute(
                    """
                    UPDATE 
                        sim_card
                      SET 
                        update_time = current_timestamp,""" + update_set_expression + """
                      WHERE 
                        iccid = %(iccid)s
                    """,
                    defined_fields)
