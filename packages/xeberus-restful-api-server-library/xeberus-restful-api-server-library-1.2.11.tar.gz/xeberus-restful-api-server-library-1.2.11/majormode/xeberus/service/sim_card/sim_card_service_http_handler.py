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

from majormode.perseus.constant.http import HttpMethod
from majormode.perseus.service.base_http_handler import HttpRequest
from majormode.perseus.service.base_http_handler import HttpRequestHandler
from majormode.perseus.service.base_http_handler import http_request
from majormode.xeberus.constant.sim import BillingFrequency
from majormode.xeberus.constant.sim import BillingMethod
from majormode.xeberus.constant.sim import Ownership
from majormode.xeberus.constant.sim import PaymentMethod

from majormode.xeberus.service.sim_card.sim_card_service import SimCardService


class SimCardServiceHttpRequestHandler(HttpRequestHandler):
    @http_request(r'^/sim_card$',
                  http_method=HttpMethod.GET,
                  authentication_required=True,
                  signature_required=True)
    def get_sim_cards(self, request):
        limit = request.get_argument(
            'limit',
            data_type=HttpRequest.ArgumentDataType.integer,
            is_required=False,
            default_value=SimCardService.DEFAULT_LIMIT)

        offset = request.get_argument(
            'offset',
            data_type=HttpRequest.ArgumentDataType.integer,
            is_required=False,
            default_value=0)

        sync_time = request.get_argument(
            'sync_time',
            data_type=HttpRequest.ArgumentDataType.timestamp,
            is_required=False)

        return SimCardService().get_sim_cards(
            request.app_id,
            request.account_id,
            limit=limit,
            offset=offset,
            sync_time=sync_time)

    @http_request(r'^/sim_card/(iccid)$',
                  http_method=HttpMethod.PUT,
                  authentication_required=True,
                  signature_required=True)
    def set_sim_card(self, request, iccid):
        balance = request.get_argument(
            'balance',
            data_type=HttpRequest.ArgumentDataType.decimal,
            is_required=False)

        billing_frequency = request.get_argument(
            'billing_frequency',
            data_type=HttpRequest.ArgumentDataType.enumeration,
            enumeration=BillingFrequency,
            is_required=False)

        billing_method = request.get_argument(
            'billing_method',
            data_type=HttpRequest.ArgumentDataType.enumeration,
            enumeration=BillingMethod,
            is_required=False)

        billing_time = request.get_argument(
            'billing_time',
            data_type = HttpRequest.ArgumentDataType.timestamp,
            is_required=False)

        ownership = request.get_argument(
            'ownership',
            data_type=HttpRequest.ArgumentDataType.enumeration,
            enumeration=Ownership,
            is_required=False)

        currency_code = request.get_argument(
            'currency_code',
            data_type=HttpRequest.ArgumentDataType.string,
            is_required=False)

        data_fee = request.get_argument(
            'data_fee',
            data_type=HttpRequest.ArgumentDataType.decimal,
            is_required=False)

        data_limit = request.get_argument(
            'data_limit',
            data_type=HttpRequest.ArgumentDataType.integer,
            is_required=False)

        data_used = request.get_argument(
            'data_used',
            data_type=HttpRequest.ArgumentDataType.integer,
            is_required=False)

        payment_method = request.get_argument(
            'payment_method',
            data_type=HttpRequest.ArgumentDataType.enumeration,
            enumeration=PaymentMethod,
            is_required=False)

        unlimited_data = request.get_argument(
            'unlimited_data',
            data_type = HttpRequest.ArgumentDataType.boolean,
            is_required = False)

        return SimCardService().set_sim_card(
            request.app_id,
            request.account_id,
            iccid,
            balance=balance,
            billing_frequency=billing_frequency,
            billing_method=billing_method,
            billing_time=billing_time,
            ownership=ownership,
            currency_code=currency_code,
            data_fee=data_fee,
            data_limit=data_limit,
            data_used=data_used,
            payment_method=payment_method,
            unlimited_data=unlimited_data)
