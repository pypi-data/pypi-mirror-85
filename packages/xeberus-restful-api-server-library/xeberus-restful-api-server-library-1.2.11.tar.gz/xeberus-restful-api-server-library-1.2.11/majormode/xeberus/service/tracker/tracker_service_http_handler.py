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
from majormode.perseus.model.geolocation import GeoPoint
from majormode.perseus.service.base_http_handler import HttpRequest
from majormode.perseus.service.base_http_handler import HttpRequestHandler
from majormode.perseus.service.base_http_handler import http_request
from majormode.xeberus.model.tracker import BatteryStateChangeEvent
from majormode.xeberus.model.tracker import LocationUpdate

from majormode.xeberus.service.tracker.tracker_service import TrackerService


class TrackerServiceHttpRequestHandler(HttpRequestHandler):
    @http_request(r'^/tracker/(device_id)/activation/(activation_code)$',
                  http_method=HttpMethod.POST,
                  authentication_required=False,
                  signature_required=True)
    def activate_device(self, request, device_id, activation_code):
        # Check whether the information of the agent application has been
        # correctly passed.
        if not request.client_application:
            raise TrackerService.InvalidOperationException(
                "the information of the tracker agent application has not be given (cf. User-Agent HTTP header)")

        imei = request.get_argument(
            'imei',
            data_type=HttpRequest.ArgumentDataType.string,
            is_required=True)

        mac_address = request.get_argument(
            'mac_address',
            data_type=HttpRequest.ArgumentDataType.macaddr,
            is_required=True)

        battery_level = request.get_argument(
            'battery_level',
            data_type=HttpRequest.ArgumentDataType.decimal,
            is_required=True)

        is_battery_plugged = request.get_argument(
            'is_battery_plugged',
            data_type=HttpRequest.ArgumentDataType.boolean,
            is_required=True)

        location = request.get_argument(
            'location',
            data_type=HttpRequest.ArgumentDataType.object,
            object_class=GeoPoint,
            is_required=False)

        return TrackerService().activate_device(
            request.app_id,
            device_id,
            imei,
            activation_code,
            mac_address,
            request.client_application,
            battery_level,
            is_battery_plugged,
            location)

    @http_request(r'^/tracker/activation/request$',
                  http_method=HttpMethod.POST,
                  authentication_required=True,
                  signature_required=True)
    def request_activation_code(self, request):
        activation_code_duration = request.get_argument(
            'duration',
            data_type=HttpRequest.ArgumentDataType.integer,
            is_required=False)

        team_id = request.get_argument(
            'team_id',
            data_type=HttpRequest.ArgumentDataType.uuid,
            is_required=True)

        return TrackerService().request_activation_code(
            request.app_id,
            request.account_id,
            team_id,
            activation_code_duration=activation_code_duration)

    @http_request(r'^/tracker/(device_id)/battery/event$',
                  http_method=HttpMethod.POST,
                  authentication_required=False,
                  signature_required=True)
    def report_battery_events(self, request, device_id):
        if not isinstance(request.body, list):
            raise TrackerService.InvalidArgumentException("The message body MUST be a list of battery events")

        seed = request.get_argument(
            's',
            data_type=HttpRequest.ArgumentDataType.string,
            argument_passing=HttpRequest.ArgumentPassing.query_string,
            is_required=False)

        events = [
            BatteryStateChangeEvent.from_json(payload)
            for payload in request.body
        ]

        return TrackerService().report_battery_events(
            request.app_id,
            device_id,
            events,
            account_id=request.session and request.session.account_id,
            seed=seed)

    @http_request(r'^/tracker/(device_id)/location$',
                  http_method=HttpMethod.POST,
                  authentication_required=False,
                  signature_required=True)
    def report_location_updates(self, request, device_id):
        if not isinstance(request.body, list):
            raise TrackerService.InvalidArgumentException("The message body MUST be a list of location updates")

        seed = request.get_argument(
            's',
            data_type=HttpRequest.ArgumentDataType.string,
            argument_passing=HttpRequest.ArgumentPassing.query_string,
            is_required=False)

        team_id = request.get_argument(
            'team_id',
            data_type=HttpRequest.ArgumentDataType.string,
            argument_passing=HttpRequest.ArgumentPassing.query_string,
            is_required=False)

        events = [
            LocationUpdate.from_json(payload, device_id)
            for payload in request.body
        ]

        return TrackerService().report_location_updates(
            request.app_id,
            device_id,
            events,
            account_id=request.session and request.session.account_id,
            seed=seed,
            team_id=team_id)

    @http_request(r'^/tracker/(device_id)/handshake$',
                  http_method=HttpMethod.POST,
                  authentication_required=False,
                  signature_required=True)
    def shake_hands(self, request, device_id):
        # Check whether the information of the agent application has been
        # correctly passed.
        if not request.client_application:
            raise TrackerService.InvalidOperationException(
                "the information of the tracker agent application has not be given (cf. User-Agent HTTP header)")

        battery_level = request.get_argument(
            'battery_level',
            data_type=HttpRequest.ArgumentDataType.decimal,
            is_required=True)

        is_battery_plugged = request.get_argument(
            'is_battery_plugged',
            data_type=HttpRequest.ArgumentDataType.boolean,
            is_required=True)

        is_battery_present = request.get_argument(
            'is_battery_present',
            data_type=HttpRequest.ArgumentDataType.boolean,
            is_required=True)

        location = request.get_argument(
            'location',
            data_type=HttpRequest.ArgumentDataType.object,
            object_class=GeoPoint,
            is_required=False)

        mac_address = request.get_argument(
            'mac_address',
            data_type=HttpRequest.ArgumentDataType.string,
            is_required=True)

        return TrackerService().shake_hands(
            request.app_id,
            device_id,
            mac_address,
            request.client_application,
            is_battery_present,
            is_battery_plugged,
            battery_level,
            location=location)

































    # @http_request(r'^/device/(device_id)/alert_message$',
    #               http_method=HttpRequest.HttpMethod.POST,
    #               authentication_required=False,
    #               signature_required=True)
    # def on_device_alert_message(self, request, device_id):
    #     seed = request.get_argument('s',
    #         data_type=HttpRequest.ArgumentDataType.string,
    #         argument_passing=HttpRequest.ArgumentPassing.query_string,
    #         is_required=True)
    #
    #     if not isinstance(request.body, list):
    #         raise XeberusService.InvalidArgumentException()
    #
    #     state_changes = [ AlertStateChangeEvent.from_json(payload)
    #             for payload in request.body ]
    #
    #     return XeberusService().on_device_alert_message(request.app_id, device_id, seed, state_changes)
    #
    #
    #
    #

    #
    # @http_request(r'^/device/(device_id)/keepalive_message$',
    #               http_method=HttpRequest.HttpMethod.POST,
    #               authentication_required=False,
    #               signature_required=True)
    # def on_device_keepalive_message(self, request, device_id):
    #     seed = request.get_argument('s',
    #             data_type=HttpRequest.ArgumentDataType.string,
    #             argument_passing=HttpRequest.ArgumentPassing.query_string,
    #             is_required=True)
    #
    #     battery_level = request.get_argument('battery_level',
    #             data_type=HttpRequest.ArgumentDataType.decimal,
    #             is_required=False)
    #
    #     is_battery_plugged = request.get_argument('is_battery_plugged',
    #             data_type=HttpRequest.ArgumentDataType.boolean,
    #             is_required=False)
    #
    #     location = request.get_argument('location',
    #             data_type=HttpRequest.ArgumentDataType.object,
    #             object_class=GeoPoint,
    #             is_required=False)
    #
    #     return XeberusService().on_device_keepalive_message(request.app_id, device_id, seed,
    #             battery_level=battery_level,
    #             is_battery_plugged=is_battery_plugged,
    #             location=location)
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    # @http_request(r'/device/(device_id)/allocation$',
    #               http_method=HttpRequest.HttpMethod.POST,
    #               authentication_required=True,
    #               signature_required=True)
    # def acquire_device(self, request, device_id):
    #     return XeberusService().acquire_device(request.app_id, request.account_id, device_id)
    #
    #
    # @http_request(r'^/device$',
    #               http_method=HttpRequest.HttpMethod.GET,
    #               authentication_required=True,
    #               signature_required=True)
    # def get_devices(self, request):
    #     """
    #     @deprecated: to be replaced with get_devices_ex
    #     """
    #     limit = request.get_argument('limit',
    #             data_type=HttpRequest.ArgumentDataType.integer,
    #             is_required=False,
    #             default_value=XeberusService.DEFAULT_LIMIT)
    #
    #     offset = request.get_argument('offset',
    #             data_type=HttpRequest.ArgumentDataType.integer,
    #             is_required=False,
    #             default_value=0)
    #
    #     sync_time = request.get_argument('sync_time',
    #             data_type=HttpRequest.ArgumentDataType.timestamp,
    #             is_required=False)
    #
    #     return XeberusService().get_devices(request.app_id, request.account_id,
    #             limit=limit,
    #             offset=offset,
    #             sync_time=sync_time)
    #
    #
    # @http_request(r'^/device_ex$',
    #               http_method=HttpRequest.HttpMethod.GET,
    #               authentication_required=True,
    #               signature_required=True)
    # def get_devices_ex(self, request):
    #     limit = request.get_argument('limit',
    #             data_type=HttpRequest.ArgumentDataType.integer,
    #             is_required=False,
    #             default_value=XeberusService.DEFAULT_LIMIT)
    #
    #     offset = request.get_argument('offset',
    #             data_type=HttpRequest.ArgumentDataType.integer,
    #             is_required=False,
    #             default_value=0)
    #
    #     sync_time = request.get_argument('sync_time',
    #             data_type=HttpRequest.ArgumentDataType.timestamp,
    #             is_required=False)
    #
    #     return XeberusService().get_devices_ex(request.app_id, request.account_id,
    #             limit=limit,
    #             offset=offset,
    #             sync_time=sync_time)
    #
    #
    #
    # # @http_request(r'^/venue/(venue_id:uuid)/confirmation$',
    # #               http_method=HttpRequest.HttpMethod.POST,
    # #               authentication_required=True,
    # #               signature_required=True)
    # # def confirm_suggested_venue(self, request, venue_id):
    # #     return XeberusService().confirm_suggested_venue(request.app_id, request.account_id, venue_id)
    #
    #
    # # @http_request(r'^/venue/(venue_id:uuid)',
    # #               http_method=HttpRequest.HttpMethod.DELETE,
    # #               authentication_required=True,
    # #               signature_required=True)
    # # def delete_venue(self, request, venue_id):
    # #     return XeberusService().delete_venue(request.app_id, request.account_id, venue_id)
    #
    #
    # # @http_request(r'/route')
    # # def add_route(self, request, ):
    # #     name = request.get_argument('name',
    # #             )
    # #
    # #     path = request.get_argument('path',
    # #             data_type=HttpRequest.ArgumentDataType.list,
    # #             item_data_type=HttpRequest.ArgumentDataType.object,
    # #             object_class=GeoPoint,
    # #             is_required=True)
    # #
    # #     waypoints = request.get_argument('waypoints',
    # #             data_type=HttpRequest.ArgumentDataType.list,
    # #             item_data_type=HttpRequest.ArgumentDataType.object,
    # #             object_class=GeoPoint,
    # #             is_required=True)
    # #
    # #     return XeberusService().add_route(request.app_id, request.account_id, path,
    # #             waypoints=waypoints)
    #
    #
    # @http_request(r'^/device/(device_id)/notification$',
    #               http_method=HttpRequest.HttpMethod.GET,
    #               authentication_required=False,
    #               signature_required=True)
    # def get_device_notifications(self, request, device_id):
    #     seed = request.get_argument('s',
    #             data_type=HttpRequest.ArgumentDataType.string,
    #             is_required=True)
    #
    #     start_time = request.get_argument('start_time',
    #             data_type=HttpRequest.ArgumentDataType.timestamp,
    #             is_required=False)
    #     end_time = request.get_argument('end_time',
    #             data_type=HttpRequest.ArgumentDataType.timestamp,
    #             is_required=False)
    #     offset = request.get_argument('offset',
    #             data_type=HttpRequest.ArgumentDataType.integer,
    #             is_required=False,
    #             default_value=0)
    #     limit = request.get_argument('limit',
    #             data_type=HttpRequest.ArgumentDataType.integer,
    #             is_required=False,
    #             default_value=XeberusService.DEFAULT_LIMIT)
    #     include_read = request.get_argument('include_read',
    #             data_type=HttpRequest.ArgumentDataType.boolean,
    #             is_required=False,
    #             default_value=False)
    #     mark_read = request.get_argument('mark_read',
    #             data_type=HttpRequest.ArgumentDataType.boolean,
    #             is_required=False,
    #             default_value=True)
    #
    #     return XeberusService().get_device_notifications(request.app_id, device_id, seed,
    #         start_time=start_time, end_time=end_time,
    #         offset=offset, limit=limit,
    #         include_read=include_read, mark_read=mark_read)
    #
    #
    # @http_request(r'^/device/registration$',
    #               http_method=HttpRequest.HttpMethod.GET,
    #               authentication_required=True,
    #               signature_required=True)
    # def get_device_registrations(self, request):
    #     limit = request.get_argument('limit',
    #         data_type=HttpRequest.ArgumentDataType.integer,
    #         is_required=False,
    #         default_value=XeberusService.DEFAULT_LIMIT)
    #     offset = request.get_argument('offset',
    #         data_type=HttpRequest.ArgumentDataType.integer,
    #         is_required=False,
    #         default_value=0)
    #
    #     return XeberusService().get_device_registrations(request.app_id, request.account_id,
    #         limit=limit, offset=offset)
    #
    #
    # @http_request(r'^/device/alert$',
    #               http_method=HttpRequest.HttpMethod.GET,
    #               authentication_required=True,
    #               signature_required=True)
    # def get_devices_alerts(self, request):
    #     device_id = request.get_argument('device_id',
    #         data_type=HttpRequest.ArgumentDataType.list)
    #     limit = request.get_argument('limit',
    #         data_type=HttpRequest.ArgumentDataType.integer,
    #         is_required=False,
    #         default_value=XeFuryService.DEFAULT_LIMIT)
    #     offset = request.get_argument('offset',
    #         data_type=HttpRequest.ArgumentDataType.integer,
    #         is_required=False,
    #         default_value=0)
    #     start_time = request.get_argument('start_time',
    #         data_type=HttpRequest.ArgumentDataType.timestamp,
    #         is_required=False)
    #     return XeberusService().get_devices_alerts(request.app_id, request.account_id, device_id,
    #             start_time=start_time, limit=limit, offset=offset)
    #
    #
    # @http_request(r'^/device/(device_id)/location$',
    #               http_method=HttpRequest.HttpMethod.GET,
    #               authentication_required=True,
    #               signature_required=True)
    # def get_device_locations(self, request, device_id):
    #     start_time = request.get_argument('start_time',
    #             data_type=HttpRequest.ArgumentDataType.timestamp,
    #             is_required=True)
    #
    #     end_time = request.get_argument('end_time',
    #             data_type=HttpRequest.ArgumentDataType.timestamp,
    #             is_required=True)
    #
    #     limit = request.get_argument('limit',
    #             data_type=HttpRequest.ArgumentDataType.integer,
    #             is_required=False,
    #             default_value=XeberusService.DEFAULT_LIMIT)
    #
    #     offset = request.get_argument('offset',
    #             data_type=HttpRequest.ArgumentDataType.integer,
    #             is_required=False,
    #             default_value=0)
    #
    #     return XeberusService().get_device_locations(request.app_id, request.account_id,
    #             device_id, start_time, end_time,
    #             limit=limit,
    #             offset=offset)
    #
    #
    # @http_request(r'^/device/location/recent$',
    #               http_method=HttpRequest.HttpMethod.GET,
    #               authentication_required=True,
    #               signature_required=True)
    # def get_devices_recent_locations(self, request):
    #     devices = dict([ (device_id, cast.string_to_timestamp(timestamp))
    #             for (device_id, timestamp) in [ device.split('@')
    #                 for device in request.get_argument('devices',
    #                         data_type=HttpRequest.ArgumentDataType.list,
    #                         item_data_type=HttpRequest.ArgumentDataType.string,
    #                         is_required=True) ] ])
    #
    #     fix_age = request.get_argument('fix_age',
    #             data_type=HttpRequest.ArgumentDataType.integer,
    #             is_required=False,
    #             default_value=XeberusService.DEFAULT_FIX_AGE)
    #
    #     limit = request.get_argument('limit',
    #             data_type=HttpRequest.ArgumentDataType.integer,
    #             is_required=False,
    #             default_value=XeberusService.DEFAULT_LIMIT)
    #
    #     return XeberusService().get_devices_recent_locations(request.app_id, request.account_id, devices,
    #             fix_age=fix_age,
    #             limit=limit)
    #
    #
    # @http_request(r'^/vehicle/message$',
    #               http_method=HttpRequest.HttpMethod.GET,
    #               authentication_required=False,
    #               signature_required=True)
    # def get_vehicle_models(self, request):
    #     make = request.get_argument('make',
    #         data_type=HttpRequest.ArgumentDataType.string,
    #         is_required=False)
    #     year = request.get_argument('year',
    #         data_type=HttpRequest.ArgumentDataType.integer,
    #         is_required=False)
    #     sync_time = request.get_argument('sync_time',
    #         data_type=HttpRequest.ArgumentDataType.timestamp,
    #         is_required=False)
    #
    #     return XeberusService().get_vehicle_models(request.app_id,
    #             make=make, year=year, sync_time=sync_time)
    #
    #
    # # @http_request(r'^/venue$',
    # #               http_method=HttpRequest.HttpMethod.GET,
    # #               authentication_required=False,
    # #               signature_required=True)
    # # def get_venues(self, request):
    # #     include_address = request.get_argument('include_address',
    # #             data_type=HttpRequest.ArgumentDataType.boolean,
    # #             is_required=False,
    # #             default_value=False)
    # #
    # #     include_contacts = request.get_argument('include_contacts',
    # #             data_type=HttpRequest.ArgumentDataType.boolean,
    # #             is_required=False,
    # #             default_value=False)
    # #
    # #     include_stopovers = request.get_argument('include_stopovers',
    # #             data_type=HttpRequest.ArgumentDataType.boolean,
    # #             is_required=False,
    # #             default_value=False)
    # #
    # #     limit = request.get_argument('limit',
    # #             data_type=HttpRequest.ArgumentDataType.integer,
    # #             is_required=False,
    # #             default_value=XeberusService.DEFAULT_VENUE_LIMIT)
    # #
    # #     locale = request.get_argument('locale',
    # #             data_type=HttpRequest.ArgumentDataType.locale,
    # #             is_required=False,
    # #             default_value=DEFAULT_LOCALE)
    # #
    # #     statuses = request.get_argument('statuses',
    # #             data_type=HttpRequest.ArgumentDataType.list,
    # #             item_data_type=HttpRequest.ArgumentDataType.integer,
    # #             is_required=False)
    # #
    # #     sync_time = request.get_argument('sync_time',
    # #         data_type=HttpRequest.ArgumentDataType.timestamp,
    # #         is_required=False)
    # #
    # #     team_id = request.get_argument('team_id',
    # #         data_type=HttpRequest.ArgumentDataType.uuid,
    # #         is_required=False)
    # #
    # #     return XeberusService().get_venues(request.app_id, request.account_id,
    # #             include_address=include_address,
    # #             include_contacts=include_contacts,
    # #             #include_stopovers=include_stopovers,
    # #             statuses=statuses,
    # #             limit=limit,
    # #             locale=locale,
    # #             sync_time=sync_time,
    # #             team_id=team_id)
    #
    #
    #
    #
    #
    #
    #
    # @http_request(r'^/device/(device_id)/error$',
    #               http_method=HttpRequest.HttpMethod.POST,
    #               authentication_required=False,
    #               signature_required=True)
    # def on_error_raised(self, request, device_id):
    #     if not isinstance(request.body, list):
    #         raise XeberusService.InvalidArgumentException()
    #
    #     seed = request.get_argument('s',
    #         data_type=HttpRequest.ArgumentDataType.string,
    #         argument_passing=HttpRequest.ArgumentPassing.query_string,
    #         is_required=False)
    #
    #     return XeberusService().on_error_raised(request.app_id, device_id, seed,
    #             [ ErrorReport.from_json(payload, device_id) for payload in request.body ])
    #
    #
    #
    # @http_request(r'^/payment/cash$',
    #               http_method=HttpRequest.HttpMethod.POST,
    #               authentication_required=True,
    #               signature_required=True)
    # def register_cash_payment(self, request):
    #     customer_account_id = request.get_argument('account_id',
    #         data_type=HttpRequest.ArgumentDataType.uuid,
    #         is_required=True)
    #     amount = request.get_argument('amount',
    #         data_type=HttpRequest.ArgumentDataType.decimal,
    #         is_required=True)
    #     currency = request.get_argument('currency',
    #         data_type=HttpRequest.ArgumentDataType.string,
    #         is_required=True)
    #
    #     return XeberusService().register_cash_payment(request.app_id, request.account_id,
    #         customer_account_id, amount, currency)
    #
    #
    # @http_request(r'^/prospect/vehicle/registration$',
    #               http_method=HttpRequest.HttpMethod.POST,
    #               authentication_required=False,
    #               signature_required=True)
    # def _register_prospect_vehicle_model(self, request):
    #     email_address = request.get_argument('email_address',
    #         data_type=HttpRequest.ArgumentDataType.string,
    #         is_required=True)
    #     model_id = request.get_argument('model_id',
    #         data_type=HttpRequest.ArgumentDataType.uuid,
    #         is_required=False)
    #
    #     make = None if model_id else request.get_argument('make',
    #         data_type=HttpRequest.ArgumentDataType.string,
    #         is_required=True)
    #     model = None if model_id else request.get_argument('message',
    #         data_type=HttpRequest.ArgumentDataType.string,
    #         is_required=False)
    #
    #     return XeberusService()._register_prospect_vehicle_model(request.app_id, email_address,
    #             model_id=model_id,
    #             make=make,
    #             model=model)
    #
    #
    # @http_request(r'^/topup-card$',
    #               http_method=HttpRequest.HttpMethod.POST,
    #               authentication_required=True,
    #               signature_required=True)
    # def register_topup_cards(self, request):
    #     topup_cards = [
    #             Object(credit_amount=payload['credit_amount'],
    #                    currency_code=payload['currency_code'],
    #                    expiration_time=cast.string_to_timestamp(payload.get('expiration_time')),
    #                    magic_code=payload['magic_code'],
    #                    operator_code=payload['operator_code'],
    #                    serial_number=payload['serial_number'])
    #             for payload in request.body ]
    #
    #     return XeberusService().register_topup_cards(request.app_id, request.account_id,
    #                 topup_cards)
    #
    #
    # @http_request(r'^/device/(device_id)/mileage/(mileage:integer)$',
    #               http_method=HttpRequest.HttpMethod.PUT,
    #               authentication_required=True,
    #               signature_required=True)
    # def set_device_mileage(self, request, device_id, mileage):
    #     return XeberusService().set_device_mileage(request.app_id, request.account_id, device_id, mileage)
    #
    #
    # @http_request(r'^/device/(device_id)/picture$',
    #               http_method=HttpRequest.HttpMethod.PUT,
    #               authentication_required=True,
    #               signature_required=True)
    # def set_device_picture(self, request, device_id):
    #     if len(request.uploaded_files) != 1:
    #         raise XeberusService.InvalidOperationException('One and one only picture file MUST be uploaded')
    #
    #     return XeberusService().set_device_picture(request.app_id, request.account_id, device_id, request.uploaded_files[0])
    #
    #
    # @http_request(r'/sim/(imsi)/plan$',
    #               http_method=HttpRequest.HttpMethod.PUT,
    #               authentication_required=True,
    #               signature_required=True)
    # def set_sim_plan(self, request, imsi):
    #     data_amount = request.get_argument('data_amount',
    #             data_type=HttpRequest.ArgumentDataType.integer,
    #             is_required=True)
    #
    #     activation_time = request.get_argument('activation_time',
    #             data_type=HttpRequest.ArgumentDataType.timestamp,
    #             is_required=True)
    #
    #     return XeberusService().set_sim_plan(request.app_id, request.account_id,
    #             imsi, data_amount, activation_time)
    #
    # @http_request(r'^/device/(device_id)/playback/(slot:integer)$',
    #               http_method=HttpRequest.HttpMethod.POST,
    #               authentication_required=True,
    #               signature_required=True)
    # def start_playback(self, request, device_id, slot):
    #     return XeberusService().start_playback(request.app_id, request.account_id, device_id, slot)
    #
    #
    # @http_request(r'^/device/(device_id)/playback$',
    #               http_method=HttpRequest.HttpMethod.DELETE,
    #               authentication_required=True,
    #               signature_required=True)
    # def stop_playback(self, request, device_id):
    #     return XeberusService().stop_playback(request.app_id, request.account_id, device_id)
    #
    #
    # # @http_request(r'^/device/(device_id)/stopover',
    # #               http_method=HttpRequest.HttpMethod.POST,
    # #               authentication_required=True,
    # #               signature_required=True)
    # # def submit_stop_overs(self, request, device_id):
    # #     if not isinstance(request.body, list):
    # #         raise XeberusService.InvalidArgumentException()
    # #
    # #     seed = request.get_argument('s',
    # #         data_type=HttpRequest.ArgumentDataType.string,
    # #         argument_passing=HttpRequest.ArgumentPassing.query_string,
    # #         is_required=False)
    # #
    # #     return XeberusService().submit_stop_overs(request.app_id, request.account_id, device_id,
    # #             [ Stopover.from_json(payload) for payload in request.body ])
    #
    #
    # @http_request(r'^/device/(device_id)$',
    #               http_method=HttpRequest.HttpMethod.PUT,
    #               authentication_required=True,
    #               signature_required=True)
    # def update_device(self, request, device_id):
    #     is_battery_alarm_muted = request.get_argument('is_battery_alarm_muted',
    #         data_type=HttpRequest.ArgumentDataType.boolean,
    #         is_required=False)
    #     is_device_alarm_muted = request.get_argument('is_device_alarm_muted',
    #         data_type=HttpRequest.ArgumentDataType.boolean,
    #         is_required=False)
    #     is_security_alarm_muted = request.get_argument('is_security_alarm_muted',
    #         data_type=HttpRequest.ArgumentDataType.boolean,
    #         is_required=False)
    #     security_level = request.get_argument('security_level',
    #         data_type=HttpRequest.ArgumentDataType.integer,
    #         is_required=False)
    #
    #     return XeberusService().update_device(request.app_id, request.account_id, device_id,
    #             is_battery_alarm_muted=is_battery_alarm_muted,
    #             is_device_alarm_muted=is_device_alarm_muted,
    #             is_security_alarm_muted=is_security_alarm_muted,
    #             security_level=security_level)
