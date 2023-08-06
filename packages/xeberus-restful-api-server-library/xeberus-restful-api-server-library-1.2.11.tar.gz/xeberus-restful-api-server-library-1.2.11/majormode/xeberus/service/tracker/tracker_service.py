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

import base64
import datetime
import hashlib
import hmac
import uuid

# import collections
# import json
# import os

from majormode.perseus.constant.obj import ObjectStatus
from majormode.perseus.constant.sort_order import SortOrder
from majormode.perseus.model.enum import Enum
from majormode.perseus.model.geolocation import GeoPoint
from majormode.perseus.model.obj import Object
from majormode.perseus.model.version import Version
from majormode.perseus.service.account.account_service import AccountService
from majormode.perseus.service.base_rdbms_service import BaseRdbmsService
from majormode.perseus.service.team.team_service import TeamService
from majormode.perseus.utils import cast
from majormode.perseus.utils.date_util import ISO8601DateTime
from majormode.xeberus.constant.tracker import BatteryPlugMode
from majormode.xeberus.constant.tracker import BatteryStateEventType
from majormode.xeberus.constant.tracker import SecurityLevel


class TrackerService(BaseRdbmsService):
    # Cryptographic function to use for hashing security information.
    CRYPTOGRAPHIC_HASH_FUNCTION = hashlib.sha1

    # Default duration expressed in seconds of a code generated to activate
    # a tracker mobile device before this code expires.
    DEFAULT_ACTIVATION_CODE_DURATION = 10

    # Default minimum remaining time of a activation code before it expires
    # in order to be able to recycle it.
    DEFAULT_ACTIVATION_CODE_REMAINING_TIME_FOR_RECYCLING = 2

    # Maximum fix age of a location to be considered as a recent location
    # of a tracker mobile device.
    MAXIMUM_FIX_AGE = 5 * 60



    # # Define the name of the Content Delivery Network (CDN) bucket that
    # # groups pictures of devices.
    # CDN_BUCKET_NAME_DEVICE = 'device'
    #
    # CRYPTOGRAPHIC_HASH_FUNCTION = hashlib.sha1
    #
    # # Default fix age of a location to be considered as a recent location
    # # of a vehicle.
    # DEFAULT_FIX_AGE = 2 * 60
    #
    # MAXIMUM_DEVICE_LOCATION_LIMIT = 1000
    #
    # # Default number of venues to return in one single call.
    # DEFAULT_VENUE_LIMIT = 20
    #
    # # Maximum default number of registered devices allowed per user.  This
    # # prevents freight companies from using this service, which is
    # # dedicated to end-users only.
    # MAXIMUM_REGISTERED_DEVICES_PER_USER = 3

    # # Maximal number of venues to return in one single call.
    # MAXIMAL_VENUE_LIMIT = 100
    #
    # # Length of time, expressed in seconds, the device alert state changed
    # # notification lives before it is deleted.
    # NOTIFICATION_LIFESPAN_BATTERY_STATE_CHANGED = 60 * 60 * 24
    #
    # # Length of time, expressed in seconds, the device alert state changed
    # # notification lives before it is deleted.
    # NOTIFICATION_LIFESPAN_DEVICE_ALERT_STATE_CHANGED = 60
    #
    # # Length of time, expressed in seconds, the start playback
    # # notification lives before it is deleted.
    # NOTIFICATION_LIFESPAN_START_PLAYBACK = 40
    #
    # # Length of time, expressed in seconds, of the lifespan of the
    # # notification that informs when a vehicle enters or exits a venue.
    # NOTIFICATION_LIFESPAN_VENUE_COMINGS_AND_GOINGS_ACTIVITY_DETECTED_VENUE = 60 * 5
    #
    # # Indicate that the alarm system of the device is active, which is
    # # an alarm that the user manually arms when he leaves his vehicle.
    # # The user will be urgently alerted of any movement of his
    # # vehicle.
    # SECURITY_LEVEL_ACTIVE = 1
    #
    # # Indicate that the alarm system of the device is passive, which
    # # is an alarm that doesn't need to be manually armed when the user
    # # leaves his vehicle.  Instead, the alarm is automatically
    # # activated when the vehicle doesn't move anymore after a few
    # # seconds.  The user will be gently notified of any movement of
    # # his vehicle.
    # SECURITY_LEVEL_PASSIVE = 0
    #
    # # Maximal speed in m/s of a vehicle that is considered as entering the
    # # location of a venue.  Higher speed would be considered as just
    # # cruising nearby this venue.
    # VENUE_ENTRANCE_MAXIMAL_SPEED = 10 / 3.6
    #
    # # Minimal accuracy in meters of the location reported by the tracker
    # # attached to a vehicle, to detect when this vehicle exits a venue.
    # #
    # # When the vehicle is parked for a while, the GPS is not active
    # # anymore. When the vehicle starts to move, the first GPS fixes are
    # # quite approximate, especially if the vehicle was parked in a garage.
    # # The vehicle's location reported by the tracker can be far from the
    # # real location. Therefore the platform wrongly detects that the
    # # vehicle has exited the venue where the vehicle was parked at.
    # VENUE_EXIT_DETECTION_MINIMAL_ACCURACY = 20
    #
    # # Search distance in meters of a venue nearby the location of a
    # # vehicle.  This distance corresponds to a radius from the location of
    # # a venue.
    # VENUE_SEARCH_DISTANCE = 100
    #
    # # Define the name of the package that groups the Xeberus mobile
    # # applications under a same family, whatever their business message
    # # (lite-free, full-paid) and their mobile platform (Android, iOS).
    # # This Xeberus service delivers push notifications to users that
    # # have installed one or more applications of this family.
    # XEBERUS_MOBILE_APPLICATION_PACKAGE = 'com.majormode.tracker.mobile'
    #
    # # Define the name of the Xeberus team that MUST have been registered
    # # against the platform before this module is loaded.
    # XEBERUS_TEAM_NAME = 'Xeberus'
    #
    # # Retrieve the Xeberus team information that will be used by the
    # # methods of this class to verify whether the user on behalf of whom
    # # these methods are called are granted access to Xeberus resources.
    # #
    # # If a team is not already registered, just create a new with the
    # # botnet account.  The members of this team will be added by an
    # # administrator of the platform, who can then pass the administrator
    # # role of the botnet account to one of these new members.
    # try:
    #     XEBERUS_TEAM = TeamService().get_team_by_name(XEBERUS_TEAM_NAME, check_status=True)
    #
    # except BaseRdbmsService.UndefinedObjectException:
    #     XEBERUS_TEAM = TeamService().create_team(
    #             settings.PLATFORM_SERVER_APP_ID,
    #             settings.PLATFORM_BOTNET_ACCOUNT_ID,
    #             XEBERUS_TEAM_NAME)


    GoingsAndCommingsEventType = Enum(
        'vehicle_enter_venue',
        'vehicle_exit_venue'
    )

    ThreatLevel = Enum(
        'Critical',    # Red
        'Severe',      # Orange
        'Substantial', # Yellow
        'Moderate',    # Green
        'Low'          # Blue
    )

    XeberusNotification = Enum(
        # Indicate that the alert state of a vehicle has changed as reported
        # by the a device mounted on this vehicle.
        'on_alert_state_changed',

        # Indicate that the state of a tracker device's battery has changed.
        # This device has been connected to or disconnected from an external
        # power source.
        'on_battery_state_changed',

        # Indicate that a device has been activated by an administrator of the
        # Xeberus team.
        'on_device_activated',

        # Indicate that a device sent a handshake while it was not yet
        # registered against the platform.  Its activation stays pending until
        # an administrator of the Xeberus team decides to activate it.
        'on_device_activation_requested',

        # Indicate that the properties of a tracker device have been updated.
        # This notification includes the list of properties that have been
        # updated, and their new respective values.
        'on_device_properties_updated',

        # Indicate that the geographical location of a vehicle has changed.
        'on_location_changed',

        # Indicate that the user requested one of his device to start the
        # playback of a sound effect.
        'on_playback_start_requested',
        'on_playback_started',

        # Indicate that the user requested one of his device to stop the
        # playback of a sound effect.
        'on_playback_stop_requested',

        'on_playback_stopped',

        # Request a Xeberus agent application, running on a device, to
        # recharge the credit of the Subscriber Identification Module (SIM)
        # card currently installed on this device. The agent application needs
        # to send a  Unstructured Supplementary Service Data (USSD) message to
        # the telephony operator of the SIM card with the magic code of a top
        # up card.  The amount of money to credit the SIM card of the device
        # corresponds to the value of a top up card.
        #
        # @deprecated
        'on_sim_recharge_requested',

        # Indicate that a stop-over, which is a brief stay in the course of a
        # journey of a particular vehicle, has been detected.
        'on_stopover_added',

        # Indicate that a stopover of a particular vehicle has been updated.
        # This stop-over was already detected, but not yet reviewed by the
        # owner of the vehicle, or a member of his organization, while a the
        # background job detects this stop-over from a recent journey of this
        # vehicle, updating the size and the radius of the corresponding
        # centroid-cluster.
        'on_stopover_updated',

        # Indicate that the platforms has detected new possible venues, based
        # on the activity analysis of the vehicles of an organization.
        'on_new_venue_suggested',

        # Indicate that a vehicle started to move.
        'on_vehicle_started_moving'

        # Indicate that a vehicle stopped to move at a given location.  It
        # could be a simple stopover, or an arrival to a destination at a
        # venue.
        'on_vehicle_stopped_moving',

        # Indicate that the platform has detected a comings and goings
        # activity at a registered venue.  The exact event is provided by an
        # item of the enumeration `GoingsAndComingsEventType`.
        'on_venue_comings_and_goings_activity_detected',
    )

    # class MaximumRegisteredDevicesReachedException(BaseService.BaseServiceException):
    #     """
    #     Signal that the maximum number of registered devices for the specified
    #     user reached and as such this user is not allowed not register anymore
    #     devices.
    #     """
    #     pass


    # @classmethod
    # def __assert_valid_device_id(cls, device_id, imei, mac_address):
    #     """
    #     :deprecated: Mobile application is not granted access to IMEI anymore!
    #
    #
    #     Assert that the identification of a tracker mobile device provided by
    #     a client application is valid.
    #
    #
    #     :param device_id: Identification of a tracker mobile device.
    #
    #
    #     :param imei: International Mobile Equipment Identity that uniquely
    #         identifies a tracker mobile device.  It is composed of 15 decimal
    #         digits.
    #
    #     :param mac_address: Media Access Control (MAC) address of the tracker
    #         mobile device. It is composed of 12 decimal digits (48 bits).
    #
    #
    #     :raise InvalidArgumentException: If one or more location updates
    #         identify a tracker mobile device different from the argument
    #         `device_id`.
    #     """
    #     if device_id != cls.__build_device_id(imei, mac_address):
    #         raise cls.InvalidArgumentException(
    #             "invalid device identification",
    #             payload={'device_id': device_id})

    @classmethod
    def __assert_location_updates_from_same_device(cls, reports, device_id):
        """
        Assert that a list of location updates are provided by the same
        tracker mobile device.


        :param reports: A list of `LocationUpdate` object.

        :param device_id: identification of the tracker mobile device that
            reported these geographical location changes.


        :raise InvalidArgumentException: If one or more location updates
            identify a tracker mobile device different from the argument
            `device_id`.
        """
        device_ids = list(set([
            report.device_id
            for report in reports
            if report.device_id is not None
        ]))

        if device_ids:
            if len(device_ids) > 1:
                raise cls.InvalidArgumentException(
                    "These location updates don't come from the same tracker",
                    payload={'device_ids': device_ids})

            device_id_ = device_ids[0]
            if device_id_ != device_id:
                raise cls.InvalidArgumentException(
                    "These location updates come from another tracker that the one specified",
                    payload={
                        'location_update_device_id': device_id_,
                        'specified_device_id': device_id
                    })

    # @staticmethod
    # def __build_device_id(imei, mac_address):
    #     """
    #     :deprecated: Mobile application is not granted access to IMEI anymore!
    #

    #     Build the identification of a tracker mobile device.
    #
    #     The function removes hardware information that would allow to identify
    #     a specific device.
    #
    #
    #     :param imei: International Mobile Equipment Identity that uniquely
    #         identifies a tracker mobile device.  It is composed of 15 decimal
    #         digits.
    #
    #     :param mac_address: Media Access Control (MAC) address of the tracker
    #         mobile device. It is composed of 12 decimal digits (48 bits).
    #
    #
    #     :return: An alphanumeric string that uniquely identifies the tracker
    #         mobile device.
    #     """
    #     mixed_id = ''.join([a + b for a, b in zip(imei, mac_address)])
    #     return hashlib.md5(mixed_id.encode()) \
    #         .hexdigest()

    @staticmethod
    def __build_device_time_filters(device_ids):
        """
        Build the list of tracker mobile device identifications and time
        constraints to filter location updates.


        :param device_ids: Identification of one or more tracker mobile
            devices.  The following types are supported:

            * `device_id:str`: Identification of a single tracker mobile device.

            * `[device_id:str, ...]`: Collection of the identifications of one or
              more tracker mobile devices.  List, set, and tuple are supported.

            * `(device_id:str, start_time:datetime, end_time:datetime)`:
              Identification of a tracker mobile device and start and end times to
              filter its location updates:

              * `start_time`: Earliest non-inclusive time to filter location updates
                of the tracker mobile device based on their fix time. This item can
                be `None`.

              * `end_time`: Latest inclusive time to filter location updates of the
                tracker mobile device based on their fix time.  This item can be `None`.

            * `[(device_id:str, start_time:datetime, end_time:datetime), ...]`:
              Collection of tuples representing one or more tracker mobile devices
              and their respective start and end times to filter their location
              updates.


        :return: A list of tuples `(device_id, start_time, end_time)`.


        :raise ValueError: If the argument 'device_ids' is null or empty, or
            if it is not of the expected format.
        """
        if not device_ids:
            raise ValueError("The argument 'device_ids' must not be null or empty")

        if isinstance(device_ids, str):
            # Convert the single tracker mobile device identification to a list of
            # the single identification with null start and end times.
            device_filters = [(device_ids, None, None), ]

        elif isinstance(device_ids, (list, set, tuple)):
            if all([isinstance(device_id, str) for device_id in device_ids]):
                # Convert the simple list of tracker mobile device identifications to a
                # list of identifications with null start and end times.
                device_filters = [(device_id, None, None) for device_id in device_ids]

            elif isinstance(device_ids, tuple) and len(device_ids) == 3:
                # Convert the identification of a tracker mobile device and start and
                # end times to a list of one element:
                device_filters = [device_ids]

            else:
                if not all(isinstance(item, tuple) and len(item) == 3 for item in device_ids):
                    raise ValueError("The argument 'device_ids' must not contain mixed item types")
                device_filters = device_ids

        else:
            raise ValueError("Unsupported type of argument 'device_ids'")

        # Check that each element of the list has the right type.
        if any([
            not (isinstance(device_id, str)
                 and (start_time is None or isinstance(start_time, datetime.datetime))
                 and (end_time is None or isinstance(end_time, datetime.datetime)))
            for device_id, start_time, end_time in device_filters
        ]):
            raise ValueError("Unsupported format of the argument 'device_ids'")

        return device_filters

    # def __deactivate_device(self, device, connection=None):
    #     """
    #     Set the device to pending mode.  This requires an administrator of the
    #     platform to review its properties and to activate it.
    #
    #
    #     :param device: An object representing the device to deactivate.
    #
    #     :param connection: A `RdbmsConnection` object to be used supporting
    #         the Python clause `with ...:`.
    #     """
    #     with self.acquire_rdbms_connection(auto_commit=True, connection=connection) as connection:
    #         cursor = connection.execute(
    #             """
    #             UPDATE
    #                 tracker
    #               SET
    #                 object_status = %(OBJECT_STATUS_PENDING)s,
    #                 update_time = current_timestamp
    #               WHERE
    #                 device_id = %(device_id)s
    #                 AND object_status = %(OBJECT_STATUS_ENABLED)s
    #               RETURNING
    #                 true
    #             """,
    #             {
    #                 'OBJECT_STATUS_ENABLED': ObjectStatus.enabled,
    #                 'OBJECT_STATUS_PENDING': ObjectStatus.pending,
    #                 'device_id': device.device_id
    #             })
    #
    #         if cursor.get_row_count() > 0:
    #             # @todo: Send a notification to the owner or the administrators of the
    #             #     organization officially responsible for managing this device.
    #             pass

    def __find_device_with_iccid(self, iccid, connection=None):
        """
        Return the device with the specified SIM card inserted in.


        :param iccid: Integrated Circuit Card IDentifier (ICCID) stored in a
            SIM card.

        :param connection: A `RdbmsConnection` object to be used supporting
            the Python clause `with ...:`.


        :return: An object returned by the function `__get_device`.
        """
        with self.acquire_rdbms_connection(auto_commit=False, connection=connection) as connection:
            cursor = connection.execute(
                """
                SELECT
                    device_id
                  FROM 
                    tracker
                  WHERE 
                  icci = %(iccid)s""",
                {
                    'iccid': iccid
                })

            row = cursor.fetch_one()
            return row and self.get_device(
                row.get_value('device_id', cast.string_to_uuid))

    def __generate_new_activation_code(
            self,
            account_id,
            team_id,
            activation_code_duration,
            connection=None):
        """
        Generate a new code to activate a tracker mobile device.


        This activation code needs to be used before it expires.  A tracker
        mobile device needs to scan this activation code (for instance, as a
        QR code) and to send it to the platform in order this device to be
        activated on behalf the organization that manages this device.


        :param account_id: Identification of an administrator of the
            organization that requests to activate a new tracker mobile device.

        :param team_id: Identification of the organization that is responsible
            for managing this tracker mobile device.

        :param activation_code_duration: Duration in seconds for which the
            generated activation code is valid.

        :param connection: A `RdbmsConnection` object to be used supporting
            the Python clause `with ...:`.


        :return: An object containing the following attributes:

            * `activation_code`: A string representing an activation code that a
              tracker mobile device needs to scan and to send back to the platform
              in order to be activated on behalf the organization that manages this
              device.

            * `expiration_time`: Time when this activation code expires.
        """
        with self.acquire_rdbms_connection(auto_commit=True, connection=connection) as connection:
            activation_id = uuid.uuid1()

            activation_code = hmac.new(
                f'{account_id}{team_id}'.encode(),
                msg=activation_id.hex.encode(),
                digestmod=self.CRYPTOGRAPHIC_HASH_FUNCTION) \
                .hexdigest()

            expiration_time = ISO8601DateTime.now() + datetime.timedelta(
                seconds=activation_code_duration or self.DEVICE_ACTIVATION_CODE_DURATION)

            connection.execute(
                """
                INSERT INTO tracker_activation(
                    activation_code,
                    expiration_time,
                    account_id,
                    team_id)
                  VALUES
                    (%(activation_code)s,
                     %(expiration_time)s,
                     %(account_id)s,
                     %(team_id)s)
                """,
                {
                    'account_id': account_id,
                    'activation_code': activation_code,
                    'expiration_time': expiration_time,
                    'team_id': team_id
                })

            activation = Object(
                activation_code=activation_code,
                expiration_time=expiration_time)

            return activation

    def __get_device(
            self,
            device_id,
            check_status=False,
            connection=None,
            include_extended_info=False,
            strict_status=True):
        """
        Return extended information of the specified tracker mobile device.


        @warning: this function is for internal usage only; it MUST not be
            surfaced to client applications.


        :param device_id: Identification of the tracker mobile device.

        :param check_status: Indicate whether to check the current status of
            the tracker mobile device and raise an exception if this device is
            not enabled or pending.

        :param connection: A `RdbmsConnection` object to be used supporting
            the Python clause `with ...:`.

        :param include_extended_info: Indicate whether to return extended
            information about the tracker mobile device.  This includes the
            following attributes:

            * `device_model`
            * `is_battery_plugged`
            * `mac_address`
            * `os_name`
            * `os_version`
            * `product_name`
            * `product_version`

        :param strict_status: `True` indicates that the device MUST be enabled
            (i.e., activated); `False` indicates that its activation can be
             still pending.


        :return: An object containing the following attributes:

            * `account_id` (optional): Identification of the account of the user
              this tracker mobile device is registered to.

            * `activation_time` (required): Time when this tracker mobile device has
              been activated by an individual or an organization.

            * `battery_level` (optional): Current level in percentage of the battery
              of the tracker mobile device.

            * `device_id` (required): International Mobile Equipment Identity of the
              tracker mobile device.

            * `fix_age` (required): Difference, expressed in seconds, between the
              time when the tracker mobile device calculated the last knwon location
              fix and the current time on the platform.  This duration corresponds
              to the current age of the last known location fix.

            * `keepalive_time` (required): Time of the last keep-alive (KA) message
              sent by the tracker mobile device to the platform to check the link
              between the device and the platform is operation properly, and to
              notify the platform that the device is still in operation as expected.

            * `location` (required): An object `GeoPont` representing the last known
              location of the tracker mobile device.

            * `mileage` (required): Total distance travelled by the tracker mobile
              device since the tracker application has been installed and executed
              on this device.  This mileage is calculated by the device itself based
              on the location changes its internal GPS determined over the time.

              This mileage might not correspond to the mileage displayed by the
              odometer of the vehicle this tracker device is mounted on.

              @todo: What is this information calculated for?

            * `name` (optional): Human-readable name given to tracker mobile device.

              A portable tracker mobile device may be attached to multiple vehicles
              over the time, after each trip.  This name should not represent the
              vehicle that the device is currently attached to.

            * `object_status` (required): Current registration status of this tracker
              mobile device.

            * `picture_id` (optional): Identification of the picture of the tracker
              mobile device.

              A portable tracker mobile device may be attached to multiple vehicles
              over the time, after each trip.  This picture should not represent the
              vehicle that the device is currently attached to.

            * `picture_url` (optional): Uniform Resource Locator (URL) that
              specifies the location of the picture representing the tracker mobile
              device.  The client application can use this URL and append the query
              parameter `size` to specify a given pixel resolution of this picture.

            * `provider` (required): Name of the location provider that reported the
              last known location of the tracker mobile device.

            * `security_level` (required): An item of the enumeration `SecurityLevel`
              representing the current level of security of the tracker mobile
              device.

            * `team_id` (optional): Identification of the organization this tracker
              mobile device is registered to.

            * `update_time` (required): Time of the most recent modification of one
              or more attributes of this tracker mobile device.


        :raise DeletedObjectException: if the device has been deleted while
            the argument `check_status` has been set to `True`.

        :raise DisabledObjectException: if the device has been disabled while
            the argument `check_status` has been set to `True`.

        :raise InvalidOperationException: If the tracker mobile device has not
            been activated by the user or an administrator of the organization
            officially responsible for this device.

        :raise UndefinedObjectException: if the specified identification
            doesn't refer to a device registered against the platform.
        """
        with self.acquire_rdbms_connection(auto_commit=False, connection=connection) as connection:
            cursor = connection.execute(
                """
                SELECT
                    account_id,
                    accuracy,
                    activation_time,
                    bearing,
                    ST_Z(location) AS altitude,
                    battery_level,
                    battery_plug_mode,
                    device_id,
                    device_model,
                    EXTRACT(EPOCH FROM current_timestamp - fix_time) AS fix_age,
                    fix_time,
                    is_battery_plugged,
                    keepalive_time,
                    ST_Y(location) AS latitude,
                    ST_X(location) AS longitude,
                    mac_address,
                    mileage,
                    name,
                    object_status,
                    os_name,
                    os_version,
                    picture_id,
                    product_name,
                    product_version,
                    security_level,
                    speed,
                    team_id,
                    update_time
                  FROM 
                    tracker
                  WHERE
                    device_id = %(device_id)s
                """,
                {
                    'device_id': device_id
                })

            row = cursor.fetch_one()
            if row is None:
                raise self.UndefinedObjectException(f"the device {device_id} is not registered")

            device = row.get_object({
                'account_id': cast.string_to_uuid,
                'activation_time': cast.string_to_timestamp,
                'battery_plug_mode': BatteryPlugMode,
                'fix_time': cast.string_to_timestamp,
                'keepalive_time': cast.string_to_timestamp,
                'object_status': ObjectStatus,
                'os_version': Version,
                'picture_id': cast.string_to_uuid,
                'product_version': Version,
                'security_level': SecurityLevel,
                'team_id': cast.string_to_uuid,
                'update_time': cast.string_to_timestamp
            })

            # If required, raise an exception if the device is disabled or banned.
            if check_status:
                if device.object_status == ObjectStatus.disabled:
                    raise self.DisabledObjectException(f"the device {device_id} has been deactivated")
                elif device.object_status == ObjectStatus.deleted:
                    raise self.DeletedObjectException(f"the device {device_id} has been suspended")
                elif device.object_status == ObjectStatus.pending and strict_status:
                    raise self.InvalidOperationException(f"the device {device_id} has not been activated")

            # Build the object representing the last known location of the device.
            device.location = device.longitude and device.latitude and \
                GeoPoint.objectify_attributes(device)

            # Remove extended information if not requested.
            if not include_extended_info:
                del device.activation_time
                del device.product_name
                del device.product_version
                del device.device_model
                del device.is_battery_plugged
                del device.mac_address
                del device.os_name
                del device.os_version

            return device

    def __get_device_activation_request(
            self,
            activation_code,
            check_status=False,
            connection=None):
        """
        Return extended information about a tracker mobile device activation
        request.


        :param activation_code: A code that have been generated by an
            administrator of an organization to activate an tracker mobile
            device of this organization.

        :param check_status: Indicate whether to check the current status of
            this activation request.

        :param connection: A `RdbmsConnection` object to be used supporting
            the Python clause `with ...:`.


        :return: An object containing the following attributes:

            * `account_id` (required): Identification of the account of the
              administrator of the organization who requested the generation of this
              this activation code.

            * `creation_time` (required): Time when this activation code has been
              generated.

            * `expiration_time` (required): Time when the activation code expires.

            * `object_status` (required): Current status of this activation
              request.

            * `team_id` (required): Identification of the organization on behalf
              of which this activation code has been generated.

            * `update_time` (required): Time of the most recent modification of
              attributes of this activation request.


        :raise DeletedObjectException: If the specified activation has expired,
            while the argument `check_status` is `True`.

        :raise DisabledObjectException: If the specified activation code has
            been already used to activate a tracker mobile device, while the
            argument `check_status` is `True`.

            An activation code is generally reused to activate multiple tracker
            mobile device while this code has not expired, but a particular
            business logic may require that an activation can be only used once.

        :raise UndefinedObjectException: If the specified code doesn't refer
            to any tracker mobile device activation request registered to the
            platform.
        """
        with self.acquire_rdbms_connection(auto_commit=True, connection=connection) as connection:
            # Retrieve the information of this activation code.
            cursor = connection.execute(
                """
                SELECT
                    team_id,
                    account_id,
                    expiration_time,
                    object_status,
                    creation_time,
                    update_time
                  FROM 
                    tracker_activation
                  WHERE 
                    activation_code = %(activation_code)s
                """,
                {
                    'activation_code': activation_code
                })

            row = cursor.fetch_one()
            if row is None:
                raise self.UndefinedObjectException(f"undefined activation code {activation_code}")

            activation_request = row.get_object({
                'account_id': cast.string_to_uuid,
                'creation_time': cast.string_to_timestamp,
                'expiration_time': cast.string_to_timestamp,
                'object_status': ObjectStatus,
                'team_id': cast.string_to_uuid,
                'update_time': cast.string_to_timestamp})

            # Automatically change the status of this activation code to 'deleted',
            # if this activation code has expired.
            if activation_request.object_status == ObjectStatus.enabled and activation_request.expiration_time < ISO8601DateTime.now():
                activation_request.object_status = ObjectStatus.deleted

            # When required, check that the activation is still enabled.
            if check_status:
                if activation_request.object_status == ObjectStatus.disabled:
                    raise self.DisabledObjectException(f"the activation code {activation_code} has been already used")
                elif activation_request.object_status == ObjectStatus.deleted:
                    raise self.DeletedObjectException(f"the activation code {activation_code } has expired")

            return activation_request

    def __get_device_security_key(self, device_id, connection=None):
        """
        Return the security key of a tracker mobile device.


        :param device_id: Identification of a tracker mobile device.

        :param connection: A `RdbmsConnection` object to be used supporting
            the Python clause `with ...:`.


        :return: The security key that the tracker mobile device has shared
            with the platform.


        :raise InvalidOperationException: If the tracker mobile device hasn't
            initially shared its security key with the platform.
        """
        with self.acquire_rdbms_connection(auto_commit=False, connection=connection) as connection:
            cursor = connection.execute(
                """
                SELECT 
                    mac_address
                  FROM 
                    tracker
                  WHERE 
                    device_id = %(device_id)s
                """,
                {
                    'device_id': device_id
                })

            row = cursor.fetch_one()
            if row is None:
                raise self.InvalidOperationException(f"device {device_id} hasn't shared encryption key yet")

            return row.get_value('mac_address')

    # def __get_or_register_sim_card(self, app_id, iccid, imsi, connection=None):
    #     """
    #     :deprecated: mobile application has no more granted access to the
    #         ICCID and IMSI information of the mobile device.
    #
    #     Return the information of a SIM card or register it if necessary.
    #
    #
    #     :param app_id: identification of the client application such as a Web,
    #         a desktop, or a mobile application, that accesses the service.
    #
    #     :param iccid: Integrated Circuit Card IDentifier (ICCID) stored in the
    #         SIM card and also engraved or printed on the SIM card body during
    #         a process called personalization.  The ICCID is defined by the
    #         ITU-T recommendation E.118 as the Primary Account Number.  It is
    #         also known as the serial number of the Subscriber Identity Module
    #         (SIM) card of the mobile phone, or SIMID.
    #
    #     :param imsi: International Mobile Subscriber Identity (IMSI) as stored
    #         in the SIM card.
    #
    #     :param connection: A `RdbmsConnection` object to be used supporting
    #         the Python clause `with ...:`.
    #
    #
    #     :return: An object containing the following attributes:
    #
    #         * `balance` (optional): Current balance amount of a prepaid SIM card.
    #           This information is defined when the card owner is the service
    #           provider and when using a prepaid billing method.  This attribute is
    #           provided only if the argument `include_billing_info` is `true`.
    #
    #         * `billing_frequency` (optional): An item of the enumeration
    #           `BillingFrequency` that indicates the billing frequency for the data
    #           service.  This information is defined when the card owner is the
    #           service provider.  This attribute is provided only if the argument
    #           `include_billing_info` is `true`.
    #
    #         * `billing_method` (optional): An item of the enumeration
    #           `BillingMethod` that indicates the billing method of this SIM card.
    #           This attribute is provided only if the argument
    #           `include_billing_info` is `true`.
    #
    #         * `billing_time` (optional): Time of the last billing for the data
    #           service.  Monthly subscription charges generally commence at this
    #           time. This attribute is provided only if the argument
    #           `include_billing_info` is `true`.
    #
    #         * `ownership` (required): An item of the enumeration `Ownership`
    #           that indicates who the owner of this SIM card is, and therefore who is
    #           responsible for paying the SIM card fee to the carrier
    #
    #         * `creation_time` (required): Time when this SIM card has been
    #           registered to the platform.
    #
    #         * `currency_code` (optional): ISO 4217 alphabetical code representing
    #           the currency of the SIM card's balance and data fee.  This alphabetic
    #           code is based on another ISO standard, ISO 3166, which lists the codes
    #           for country names.  The first two letters of the ISO 4217 three-letter
    #           code are the same as the code for the country name, and where possible
    #           the third letter corresponds to the first letter of the currency name.
    #           This attribute is provided only if at least one of the arguments
    #           `include_billing_info` and `include_data_info` is `true`.
    #
    #         * `data_fee` (optional): Fee for the data plan depending on the
    #           billing frequency.  This information is defined when the card owner is
    #           the service provider and when using a prepaid billing method.  This
    #           attribute is provided only if the argument `include_data_info` is
    #           `true`.
    #
    #         * `data_limit` (optional): Monthly data usage in MB the plan allows,
    #           or `None` if unlimited.  Once data usage exceeds this limit, the
    #           customer may be charged a data overage rate.  This attribute is
    #           provided only if the argument `include_data_info` is `true`.
    #
    #         * `data_used` (optional): Current amount of data in MB that has been
    #           used since the last top-up.  This attribute is provided only if the
    #           argument `include_data_info` is `true`.
    #
    #         * `iccid` (required): Integrated Circuit Card IDentifier (ICCID)
    #           stored in the SIM card and also engraved or printed on the SIM card
    #           body during a process called personalization.  The ICCID is defined by
    #           the ITU-T recommendation E.118 as the Primary Account Number.  It is
    #           also known as the serial number of the Subscriber Identity Module
    #           (SIM) card of the mobile phone, or SIMID.
    #
    #         * `imsi` (required): International Mobile Subscriber Identity (IMSI)
    #           as stored in the SIM card.  The first 3 digits are the mobile country
    #           code (MCC), which are followed by the mobile network code (MNC),
    #           either 2 digits (European standard) or 3 digits (North American
    #           standard).
    #
    #         * `msisdn` (required): Mobile Subscriber Integrated Services Digital
    #           Network Number (MSISDN) currently associated to the SIM card.
    #
    #         * `object_status` (required): An item of the enumeration
    #           `ObjectStatus` that indicates the current status of this SIM card.
    #
    #         * `operator_code` (required): Identification of the mobile network
    #           operator (carrier) that provides the SIM card.  This identification is
    #           composed of the mobile country code (MCC) used in combination with the
    #           mobile network code (MNC) of this carrier.
    #
    #           The mobile country code consists of 3 decimal digits and the mobile
    #           network code consists of 2 or 3 decimal digits.  The first digit of
    #           the mobile country code identifies the geographic region as follows
    #           (the digits 1 and 8 are not used):
    #
    #           * `0`: Test networks
    #
    #           * `2`: Europe
    #
    #           * `3`: North America and the Caribbean
    #
    #           * `4`: Asia and the Middle East
    #
    #           * `5`: Oceania
    #
    #           * `6`: Africa
    #
    #           * `7`: South and Central America
    #
    #           * `9`: Worldwide (Satellite, Air - aboard aircraft, Maritime -
    #             aboard ships, Antarctica)
    #
    #         * `payment_method (optional): An item of the enumeration
    #           `PaymentMethod` that indicates the payment method to be used to
    #           increase the remaining balance of the SIM card.  This information is
    #            defined when the card owner is the service provider and when using a
    #            prepaid billing method.  This attribute is provided only if the
    #            argument `include_billing_info` is `true`.
    #
    #         * `unlimited_data` (optional): Indicate whether the data plan includes
    #           unlimited data.  The carrier may reduce the bandwidth when data usage
    #           exceeds the data speed reduction threshold (cf. `data_limit`).
    #           This attribute is provided only if the argument `include_data_info`
    #           is `true`.
    #
    #         * `update_time` (required): Time of the most recent modification of
    #           any variable attribute of this SIM card, such as its status, the most
    #           recent top-up of the SIM balance.
    #     """
    #     try:
    #         sim_card = SimCardService().get_sim_card(
    #             iccid,
    #             check_status=True,
    #             connection=connection,
    #             include_billing_info=True,
    #             include_data_info=True)
    #
    #         # Check that the SIM card has the same IMSI that previously registered.
    #         if sim_card.imsi != imsi:
    #             raise self.InvalidOperationException(
    #                 "the SIM card has been already registered with another IMSI",
    #                 payload={'iccid': iccid, 'imsi': imsi})
    #
    #     except SimCardService.UndefinedObjectException:
    #         sim_card = SimCardService().register_sim_card(app_id, iccid, imsi, connection=connection)
    #
    #     return sim_card

    def __preregister_device(
            self,
            device_id,
            mac_address,
            agent_application,
            is_battery_present,
            is_battery_plugged,
            battery_level,
            connection=None,
            location=None):
        """
        Preregister a tracker mobile device when handshaking for the first
        time.

        An individual user or an administrator of the organization officially
        responsible for managing this device will need to acquire and activate
        this device.


        :param device_id: Identification of the tracker mobile device.

        :param mac_address: Media Access Control (MAC) address of the network
            interface of the device.  This information is immutable.

        :param: agent_application: A `ClientApplication` object representing
            the agent application installed on the tracker mobile device.

        :param is_battery_present: Indicate whether the device is equipped
            with an internal battery.  A device not equipped with an internal
            battery is less secure as it is not able to send any notification
            when it is disconnected from the power source of the vehicle this
            device is mounted on; the device is immediately shutdown.

        :param is_battery_plugged: Indicate if the internal battery of the
            tracker mobile device is plugged to a power source.

        :param battery_level: Current level in percentage of the internal
            battery of the tracker mobile device.

        :param location: a `GeoPoint` object representing the last known
            location of the device.

        :param connection: An object `RdbmsConnection` that supports the
            Python clause `with ...:`.


        :return: An object returned by the function `__get_device`.
        """
        with self.acquire_rdbms_connection(auto_commit=True, connection=connection) as connection:
            connection.execute(
                """
                INSERT INTO tracker(
                    accuracy,
                    battery_level,
                    bearing,
                    device_id,
                    device_model,
                    fix_time,
                    is_battery_plugged,
                    is_battery_present,
                    location,
                    mac_address,
                    object_status,
                    os_name,
                    os_version,
                    product_name,
                    product_version,
                    provider,
                    speed)
                  VALUES 
                    (%(accuracy)s,
                     %(battery_level)s,
                     %(bearing)s,
                     %(device_id)s,
                     %(device_model)s,
                     %(fix_time)s,
                     %(is_battery_plugged)s,
                     %(is_battery_present)s,
                     ST_SetSRID(ST_MakePoint(%(longitude)s, %(latitude)s, %(altitude)s), 4326),
                     %(mac_address)s,
                     %(OBJECT_STATUS_PENDING)s,
                     %(os_name)s,
                     %(os_version)s,
                     %(product_name)s,
                     %(product_version)s,
                     %(provider)s,
                     %(speed)s)
                """,
                {
                    'OBJECT_STATUS_PENDING': ObjectStatus.pending,
                    'accuracy': location and location.accuracy,
                    'altitude': location and location.altitude,
                    'battery_level': battery_level,
                    'bearing': location and location.bearing,
                    'device_id': device_id,
                    'device_model': agent_application.device_model,
                    'fix_time': location and location.fix_time,
                    'is_battery_plugged': is_battery_plugged,
                    'is_battery_present': is_battery_present,
                    'latitude': location and location.latitude,
                    'longitude': location and location.longitude,
                    'mac_address': mac_address,
                    'os_name': agent_application.os_name,
                    'os_version': str(agent_application.os_version),
                    'product_name': agent_application.product_name,
                    'product_version': str(agent_application.product_version),
                    'provider': location and location.provider,
                    'speed': location and location.speed
                })

            return self.__get_device(
                device_id,
                check_status=False,
                connection=connection,
                include_extended_info=True)

            # # Send a notification to the administrators of the platform to inform
            # # them from the pending registration of this device.
            # NotificationService().send_notification(
            #         settings.PLATFORM_SERVER_APP_ID,
            #         XeberusService.XeberusNotification.on_device_activation_requested,
            #         TeamService()._get_team_administrators(XeberusService.XEBERUS_TEAM.team_id),
            #         payload=Object(
            #                 creation_time=device.creation_time,
            #                 device_id=device_id,
            #                 location=location))
            #
            # return device

    def __recycle_previous_activation_code(
            self,
            account_id,
            team_id,
            minimal_expiration_time,
            connection=None):
        """
        Recycle a previous activation code that is not yet expired.

        An activation code can be recycled for the same user and the
        organization it has been initially generated.

        An activation code can be recycled if and only if its remaining time
        is more than a few seconds, otherwise a new activation code needs to
        be generated.  This prevents providing a recycled activation code that
        is going to expire meanwhile it is scanned by tracker mobile device.
        The tracker mobile device would not have the time to send it back to
        the platform before this activation code expires.


        :param account_id: Identification of an administrator of the
            organization that requests to activate a new tracker mobile device.

        :param team_id: Identification of the organization that is responsible
            for managing this tracker mobile device.

        :param minimal_expiration_time: Minimal expiration time of an
            activation code to be recycled.

        :param connection: A `RdbmsConnection` object to be used supporting
            the Python clause `with ...:`.


        :return: A recycled activation code, if any; `None` otherwise.

            A recycled activation code is represented with an object containing
            the following attributes:

            * `activation_code`: A string representing an activation code that a
              tracker mobile device needs to scan and to send back to the platform
              in order to be activated on behalf the organization that manages this
              device.

            * `expiration_time`: Time when this activation code is going to expire.
        """
        with self.acquire_rdbms_connection(auto_commit=True, connection=connection) as connection:
            cursor = connection.execute(
                """
                SELECT 
                    activation_code,
                    expiration_time
                  FROM 
                    tracker_activation
                  WHERE 
                    account_id = %(account_id)s
                    AND team_id = %(team_id)s
                    AND object_status = %(OBJECT_STATUS_ENABLED)s
                    AND expiration_time >= %(minimal_expiration_time)s
                  ORDER BY
                    creation_time ASC
                  LIMIT 1
                """,
                {
                    'OBJECT_STATUS_ENABLED': ObjectStatus.enabled,
                    'account_id': account_id,
                    'minimal_expiration_time': minimal_expiration_time,
                    'team_id': team_id
                })

            row = cursor.fetch_one()
            return row and row.get_object({
                'expiration_time': cast.string_to_timestamp
            })

    # def __register_device(
    #         self,
    #         app_id,
    #         device_id,
    #         mac_address,
    #         team_id,
    #         account_id,
    #         agent_application,
    #         battery_level,
    #         is_battery_plugged,
    #         location,
    #         connection=None,
    #         security_key=None):
    #     """
    #     Register a tracker mobile device on behalf of an individual or an
    #     organization.
    #
    #
    #     :param app_id: Identification of the client application running on the
    #         tracker mobile device.
    #
    #     :param device_id: Identification of the tracker mobile device.  It
    #         corresponds to a hashed version of its International Mobile
    #         Equipment Identity (IMEI) number.
    #
    #     :param mac_address: Media Access Control (MAC) address of the network
    #         interface of the device.  This information is immutable.
    #
    #     :param team_id: Identification of the organization on behalf of which
    #         this device is registered.
    #
    #     :param account_id: Identification of the account of the user on behalf
    #         of whom this device is registered.
    #
    #     :param agent_application: An object `ClientApplication` representing
    #         the agent application installed on the tracker mobile device.
    #
    #     :param battery_level: Current level in percentage of the battery of
    #         the tracker mobile device.
    #
    #     :param is_battery_plugged: Indicate whether the battery of the tracker
    #         mobile device is currently plugged to a power source.
    #
    #     :param location: Last known geographical location of the tracker
    #         mobile device.
    #
    #     :param connection: A `RdbmsConnection` object to be used supporting
    #         the Python clause `with ...:`.
    #
    #     :param security_key: A key shared between the server platform and the
    #         tracker mobile application to secure the communication.
    #
    #
    #     :return: An object containing the following attributes:
    #
    #         * `creation_time` (required): Time when this tracker mobile device has
    #           been registered to the platform.
    #
    #         * `object_status` (required): Current status of the tracker mobile
    #           device.
    #     """
    #     with self.acquire_rdbms_connection(auto_commit=True, connection=connection) as connection:
    #         cursor = connection.execute(
    #             """
    #             INSERT INTO tracker(
    #                 account_id,
    #                 accuracy,
    #                 battery_level,
    #                 device_id,
    #                 device_model,
    #                 fix_time,
    #                 is_battery_plugged,
    #                 location,
    #                 mac_address,
    #                 os_version,
    #                 product_version,
    #                 security_key,
    #                 team_id)
    #               VALUES
    #                 (%(account_id)s,
    #                  %(accuracy)s,
    #                  %(battery_level)s,
    #                  %(device_id)s,
    #                  %(device_model)s,
    #                  %(fix_time)s,
    #                  %(is_battery_plugged)s,
    #                  ST_SetSRID(ST_MakePoint(%(longitude)s, %(latitude)s, %(altitude)s), 4326),
    #                  %(mac_address)s,
    #                  %(os_version)s,
    #                  %(product_version)s,
    #                  %(security_key)s,
    #                  %(team_id)s)
    #               RETURNING
    #                 object_status,
    #                 creation_time
    #             """,
    #             {
    #                 'accuracy': location.accuracy,
    #                 'account_id': account_id,
    #                 'product_version': str(agent_application.product_version),
    #                 'altitude': location.altitude,
    #                 'battery_level': battery_level,
    #                 'device_id': device_id,
    #                 'device_model': agent_application.device_model,
    #                 'fix_time': location.fix_time,
    #                 'is_battery_plugged': is_battery_plugged,
    #                 'latitude': location.latitude,
    #                 'longitude': location.longitude,
    #                 'mac_address': ':'.join(mac_address),
    #                 'os_version': str(agent_application.os_version),
    #                 'security_key': security_key,
    #                 'team_id': team_id
    #             })
    #
    #         row = cursor.fetch_one()
    #         device = row.get_object({
    #             'creation_time': cast.string_to_timestamp,
    #             'object_status': ObjectStatus
    #         })
    #
    #         return device

    def __update_device_battery_state(self, app_id, device, events, connection=None):
        """
        Update the current battery state of a tracker mobile device.

        The function checks whether one of the specified battery states is
        more recent than the last known battery stated already stored for this
        device.


        :param app_id: Identification of the client application such as a Web,
            a desktop, or a mobile application, that accesses the service.

        :param device: An object representing a tracker mobile device.

        :param events: A list of `BatteryStateChangeEvent` objects related to
            this device.

        :param connection: A `RdbmsConnection` object to be used supporting
            the Python clause `with ...:`.
        """
        with self.acquire_rdbms_connection(auto_commit=True, connection=connection) as connection:
            # Sort battery state change events by their descending order of time and
            # retrieve the most recent event from this list.
            sorted_events = sorted(events, key=lambda event: event.event_time, reverse=True)
            most_recent_event = sorted_events[0]

            is_battery_plugged = True if most_recent_event.event_type == BatteryStateEventType.battery_plugged \
                else False if most_recent_event.event_type == BatteryStateEventType.battery_unplugged \
                else device.is_battery_plugged

            connection.execute(
                """
                UPDATE
                    tracker
                  SET 
                    battery_level = %(battery_level)s,
                    is_battery_plugged = %(is_battery_plugged)s,
                    keepalive_time = current_timestamp,
                    update_time = current_timestamp
                  WHERE
                    device_id = %(device_id)s
                """,
                {
                    'battery_level': most_recent_event.battery_level,
                    'device_id': device.device_id,
                    'is_battery_plugged': is_battery_plugged
                })

            # # Send a notification to the mobile devices of the user who owns the
            # # tracker device that reported these alerts.
            # #
            # # Only send the most recent alert event, which overrides all the
            # # previous events that were not yet sent.
            # most_recent_event.device_id = device_id

            # NotificationService().send_notification(app_id,
            #         XeberusService.XeberusNotification.on_battery_state_changed,
            #         recipient_ids=account_id,
            #         team_id=device.team_id,
            #         lifespan=XeberusService.NOTIFICATION_LIFESPAN_state_changeD,
            #         notification_mode=NotificationService.NotificationMode.push,
            #         package=XeberusService.XEBERUS_MOBILE_APPLICATION_PACKAGE,
            #         payload=most_recent_state_change)

    def __update_device_last_known_location(self, app_id, device, reports, accuracy=20, connection=None):
        """
        Update the last known location of a tracker mobile device.

        The function checks whether one of the specified locations is more
        recent than the last known location already stored for this device.


        :param app_id: Identification of the client application such as a Web,
            a desktop, or a mobile application, that accesses the service.

        :param device: An object representing a tracker mobile device.

        :param reports: A list of `LocationUpdate` objects related to this
            device.

        :param accuracy: The minimal accuracy accepted in meters to filter the
            most precise location possible.  Location updates with an accuracy
            worse than this value are ignored.

        :param connection: A `RdbmsConnection` object to be used supporting
            the Python clause `with ...:`.
        """
        accurate_reports = [
            report
            for report in reports
            if report.location.accuracy <= accuracy
        ]

        if accurate_reports:
            with self.acquire_rdbms_connection(auto_commit=True, connection=connection) as connection:
                # Sort location update by their descending order of fix time and
                # retrieve the last known location of the device from this list.
                most_recent_report = sorted(
                    accurate_reports,
                    key=lambda report: report.location.fix_time, reverse=True)[0]

                last_known_location = most_recent_report.location

                connection.execute(
                    """
                    UPDATE tracker
                      SET
                        location = ST_SetSRID(ST_MakePoint(%(longitude)s, %(latitude)s, %(altitude)s), 4326),
                        accuracy = %(accuracy)s,
                        bearing = %(bearing)s,
                        speed = %(speed)s,
                        fix_time = %(fix_time)s,
                        provider = %(provider)s,
                        keepalive_time = current_timestamp,
                        update_time = current_timestamp
                      WHERE
                        device_id = %(device_id)s
                        AND (fix_time IS NULL OR fix_time < %(fix_time)s)
                      RETURNING true""",
                    {
                        'accuracy': last_known_location.accuracy,
                        'altitude': last_known_location.altitude,
                        'bearing': last_known_location.bearing,
                        'fix_time': last_known_location.fix_time,
                        'device_id': device.device_id,
                        'latitude': last_known_location.latitude,
                        'longitude': last_known_location.longitude,
                        'provider': last_known_location.provider,
                        'speed': last_known_location.speed
                    })

            # Send a notification to the owner of the device or the members of the
            # organization responsible for managing this device, to inform about the
            # new location of this device.
            # NotificationService().send_notifications(
            #     app_id,
            #     TrackerService.XeberusNotification.on_device_location_changed,
            #     account_id=device.account_id,
            #     payload=most_recent_report,
            #     team_id=device.team_id)

    # def __update_device_sim_card(self, device, sim_card, connection=None):
    #     """
    #     :deprecated:  Mobile application is not granted access to SIM card
    #         information anymore!
    #
    #
    #     Update the SIM card information of a tracker mobile device.
    #
    #
    #     :param device: An object representing a tracker mobile device.
    #
    #     :param sim_card: An object representing a SIM card inserted in the
    #         device.
    #
    #     :param connection: A `RdbmsConnection` object to be used supporting
    #         the Python clause `with ...:`.
    #     """
    #     # If the SIM card has not been reviewed by the owner or the organization
    #     # officially responsible for managing this device, deactivate the device
    #     # until the complete information of the SIM card (e.g., data plan), is
    #     # defined.
    #     if sim_card.object_status == ObjectStatus.pending:
    #         self.__deactivate_device(device, connection=connection)
    #
    #     # If the SIM card has been moved from a device to another, the device
    #     # which the SIM card was previously inserted in needs to be deactivated
    #     # (pending mode) until it sends a new handshake providing the new SIM
    #     # card inserted.  The owner or the organization officially responsible
    #     # for managing this device will review this information and activate the
    #     # device
    #     elif device.iccid != sim_card.iccid:
    #         previous_device = self.__find_device_with_iccid(sim_card.iccid, connection=connection)
    #         if previous_device:  # Record of this device manually removed from database?!
    #             self.__deactivate_device(previous_device, connection=connection)
    #
    #         self.__update_device_iccid(device, sim_card.iccid, connection=connection)

    def __update_device_sys_info(self, device, agent_application, connection=None):
        """
        Update the system information of a tracker mobile device when
        necessary.


        :param device: An object representing a tracker mobile device extended
            of its system information.

        :param agent_application: An object `ClientApplication` representing
            the agent application installed on the tracker mobile device.

        :param connection: An object `RdbmsConnection` that supports the
            Python clause `with ...:`.
        """
        if device.product_version != agent_application.product_version \
           or device.os_version != agent_application.os_version:
            with self.acquire_rdbms_connection(auto_commit=True, connection=connection) as connection:
                connection.execute(
                    """
                    UPDATE 
                        tracker
                      SET 
                        os_version = %(os_version)s,
                        product_version = %(product_version)s,
                        update_time = current_timestamp
                      WHERE 
                        device_id = %(device_id)s
                    """,
                    {
                        'device_id': device.device_id,
                        'os_version': str(agent_application.os_version),
                        'product_version': str(agent_application.product_version),
                    })

    def __verify_digest(self, device, seed):
        """
        Verify that the given seed has been generated by the specified
        tracker mobile device.


        :param device: An object representing the extended information of a
            tracker mobile device.

        :param seed: A "number used once" (nonce) -- also known as pseudo-
            random number -- encrypted with keys shared with the platform.
            This seed is used to verify the authentication of the tracker
            mobile device in order to prevent spoofing attack.


        :raise IllegalAccessException: If the given seed has not been
            successfully verified, meaning that someone or a program tries to
            masquerade as the specified tracker mobile device (spoofing attack).

        :raise InvalidOperationException: If the specified tracker mobile
            device didn't initially share any encryption keys with the
            platform.
        """
        security_key = device.mac_address

        # Retrieve the nonce (8 characters) and its encrypted value.
        nonce = seed[0:8]
        encrypted_nonce = seed[8:]

        # Check that the nonce has been correctly encrypted with the security
        # key of the tracker mobile device.
        hashed_nonce = hmac.new(
            security_key.encode(),
            msg=nonce.encode(),
            digestmod=self.CRYPTOGRAPHIC_HASH_FUNCTION)

        valid_encrypted_nonce = hashed_nonce.digest().hex()

        if encrypted_nonce != valid_encrypted_nonce:
            self.log_warning(f'Invalid encrypted capsule: expected "{valid_encrypted_nonce}", but received "{encrypted_nonce}"')
            raise self.IllegalAccessException('The given seed has not been successfully verified')

    # def activate_device(
    #         self,
    #         app_id,
    #         device_id,
    #         imei,
    #         activation_code,
    #         mac_address,
    #         agent_application,
    #         battery_level,
    #         is_battery_plugged,
    #         location):
    #     """
    #     Activate a tracker mobile device providing an activation code.
    #
    #     If the tracker mobile device has been already activated on behalf of
    #     the organization that has generated the activation code, the function
    #     simply returns the information about this organization.  It does not
    #     raise an exception.
    #
    #     The function doesn't disable the activation code once the function has
    #     activated the device.  This activation code can be still reused to
    #     activate other tracker mobile device of the organization, before this
    #     code expires.
    #
    #
    #     :param app_id: Identification of the client application running on the
    #         tracker mobile device.
    #
    #     :param device_id: Identification of the tracker mobile device.  It
    #         corresponds to a hashed version of its International Mobile
    #         Equipment Identity (IMEI) number.
    #
    #     :param imei: International Mobile Equipment Identity (IMEI) number of
    #         the tracker mobile device.
    #
    #     :param activation_code: A code that has been generated by an
    #         administrator of an organization to activate a tracker mobile
    #         device.
    #
    #     :param mac_address: Media Access Control (MAC) address of the network
    #         interface of the device.  This information is immutable.
    #
    #     :param agent_application: An object `ClientApplication` representing
    #         the agent application installed on the tracker mobile device.
    #
    #     :param battery_level: Current level in percentage of the battery of
    #         the tracker mobile device.
    #
    #     :param is_battery_plugged: Indicate whether the battery of the tracker
    #         mobile device is currently plugged to a power source.
    #
    #     :param location: Last known geographical location of the tracker
    #         mobile device.
    #
    #
    #     :return: An object containing the following attributes:
    #
    #         * `team` (required): information about the organization that manages
    #           this tracker mobile device.
    #
    #           * `name` (required): Name of the organization.
    #
    #           * `team_id` (required): Identification of the organization.
    #
    #           * `picture_id` (optional): Identification of the picture that visually
    #             represents the organization, such as its logo.
    #
    #           * `picture_url` (optional): Uniform Resource Locator (URL) that
    #             specifies the location of the picture representing the organization.
    #
    #
    #     :raise DeletedObjectException: If the specified activation has expired.
    #
    #     :raise DisabledObjectException: If the specified activation code has
    #         been already used to activate an tracker mobile device.
    #
    #     :raise IllegalAccessException: If the tracker mobile device has been
    #         already activated by another organization.
    #
    #     :raise InvalidOperationException: If this tracker mobile device has
    #         been disabled or banned from the organization.
    #
    #     :raise UndefinedObjectException: If the specified code doesn't refer
    #         to any tracker mobile device activation request registered to the
    #         platform.
    #     """
    #     with self.acquire_rdbms_connection(auto_commit=True) as connection:
    #         # Retrieve the activation request corresponding to the specified
    #         # activation code.
    #         activation_request = self.__get_device_activation_request(
    #             activation_code,
    #             check_status=True,
    #             connection=connection)
    #
    #         # Check that the specified tracker mobile device has not been already
    #         # activated, which should never occur unless the tracker mobile got its
    #         # internal data cleared and it lost the reference of the organization
    #         # it belongs to.
    #         try:
    #             device = self.__get_device(
    #                 device_id,
    #                 check_status=True,
    #                 connection=connection)
    #
    #             if device.team_id != activation_request.team_id:
    #                 raise self.IllegalAccessException(f"the tracker mobile device {device_id} has been already activated by another organization")
    #
    #         except (self.DeletedObjectException, self.DisabledObjectException):
    #             raise self.InvalidOperationException(f"the tracker mobile device {device_id} is disabled or banned ")
    #
    #         # The tracker mobile device is not registered to the platform yet, which
    #         # is the expected behaviour; register this device.
    #         except self.UndefinedObjectException:
    #             device = self.__register_device(
    #                 app_id,
    #                 device_id,
    #                 imei,
    #                 mac_address,
    #                 activation_request.team_id,
    #                 activation_request.account_id,
    #                 agent_application,
    #                 battery_level,
    #                 is_battery_plugged,
    #                 location,
    #                 connection=connection)
    #
    #         # Return information about the organization on behalf of which the
    #         # tracker mobile device is activated.
    #         return Object(
    #             team=TeamService().get_team(
    #                 activation_request.team_id,
    #                 check_status=True,
    #                 connection=connection,
    #                 extended_info=False,
    #                 include_contacts=False))

    def get_tracker_locations_by_device_ids(
            self,
            device_ids,
            connection=None,
            end_time=None,
            limit=None,
            max_fix_age=None,
            provider=None,
            sort_order=None,
            start_time=None):
        """
        Return a list of locations reported by the specified tracker mobile
        devices.


        >>> get_tracker_locations_by_device_ids(
        ...     '869044038077499',
        ...     start_time=datetime.datetime(2020, 7, 10, 4, 13, 49),
        ...     end_time=datetime.datetime(2020, 7, 10, 4, 14, 0),
        ...     provider='gps')

        >>> get_tracker_locations_by_device_ids(
        ...     ['869044038077499', '100702457943371'],
        ...     start_time=datetime.datetime(2020, 7, 10, 4, 13, 49, 273627),
        ...     end_time=datetime.datetime(2020, 7, 10, 4, 15, 0),
        ...     max_fix_age=60)

        >>> get_tracker_locations_by_device_ids(
        ...     [
        ...         ('869044038077499',
        ...          datetime.datetime(2020, 7, 10, 4, 13, 49, 273627),
        ...          datetime.datetime(2020, 7, 10, 4, 15, 0)),
        ...         ('100702457943371',
        ...          datetime.datetime(2020, 7, 2, 0, 0, 0),
        ...          None)
        ...     ],
        ...     max_fix_age=60)


        :param device_ids: Identification of one or more tracker mobile
            devices.  The following types are supported:

            * `device_id:str`: Identification of a single tracker mobile device.

            * `[device_id:str, ...]`: Collection of the identifications of one or
              more tracker mobile devices.  List, set, and tuple are supported.

            * `[(device_id:str, start_time:datetime, end_time:datetime), ...]`:
              Collection of tuples representing one or more tracker mobile devices
              and their respective start and end times to filter their location
              updates:

              * `start_time`: Earliest non-inclusive time to filter location updates
                of the tracker mobile device based on their fix time. This item can
                be `None`.

              * `end_time`: Latest inclusive time to filter location updates of the
                tracker mobile device based on their fix time.  This item can be `None`.



        :param connection: An object `RdbmsConnection` that supports the
            Python clause `with ...:`.

        :param end_time: Latest inclusive time to filter location updates
            based on their fix time.

        :param limit: Constrain the number of locations per tracker mobile
            device to return to the specified number.  The default value is
            `TrackerService.DEFAULT_LIMIT`.  The maximum value is
            `TrackerService.MAXIMUM_LIMIT`.

        :param max_fix_age: Maximum difference, expressed in seconds, between
            the time when a tracker mobile device calculated the location fix
            and the current time on the server platform.  This duration
            corresponds to the current age of the location fix.

        :param provider: Filter the locations with the provider that
            calculated these locations:

            * ``gps``: This provider determines locations using satellites (Global
              Positioning System (GPS)).

            * ``network``: This provider determines locations based on
              availability of cell towers and Wi-Fi access points.  Results are
              retrieved by means of a network lookup.

            * ``passive``: A special location provider for receiving locations
              without actually initiating a location fix.  This provider can be
              used to passively receive location updates when other applications
              or services request them without actually requesting the locations
              yourself.  This provider will return locations generated by other
              providers.

        :param sort_order: An item of the enumeration `SortOrder` that
            indicates the order to sort location updates:

            * `SortOrder.ascending` (default): The location updates of a tracker
              mobile device are sorted by ascending order of their fix time.

            * `SortOrder.descending`: The location updates of a tracker mobile
              device are sorted by descending order of their fix time.

        :param start_time: Earliest non-inclusive time to filter location
            updates based on their fix time.


        :return: A list of object containing the following attributes:

            * `accuracy` (required): Accuracy in meters of the location.

            * `altitude` (optional): Altitude in meters of the location.

            * `bearing` (optional): Bearing in degrees. Bearing is the horizontal
              direction of travel of the tracker mobile device, and is not related
              to the device orientation. It is guaranteed to be in the range `[0.0,
              360.0]`.

            * `fix_time` (required): Time when the tracker mobile device determined
              the information of this fix.

            * `latitude` (required): Latitude-angular distance, expressed in
              decimal degrees (WGS84 datum), measured from the center of the Earth,
              of a point north or south of the Equator corresponding to the
              location.

            * `longitude` (required): Longitude-angular distance, expressed in
              decimal degrees (WGS84 datum), measured from the center of the Earth,
              of a point east or west of the Prime Meridian corresponding to the
              location.

            * `speed` (optional): Speed in meters/second over the ground.


        :raise ValueError: If the argument 'device_ids' is null or empty, or
            if it is not of the expected format.
        """
        if sort_order is None:
            sort_order = SortOrder.ascending

        device_filters = self.__build_device_time_filters(device_ids)

        with self.acquire_rdbms_connection(auto_commit=False, connection=connection) as connection:
            cursor = connection.execute(
                """
                SELECT
                    accuracy,
                    ST_Z(location) AS altitude,
                    bearing,
                    device_id,
                    fix_time,
                    ST_Y(location) AS latitude,
                    ST_X(location) AS longitude,
                    speed
                  FROM (
                    SELECT
                        device_id,
                        location,
                        accuracy,
                        bearing,
                        speed,
                        EXTRACT(EPOCH FROM current_timestamp - fix_time) AS fix_age,
                        fix_time,
                        row_number() OVER (
                          PARTITION BY 
                            device_id 
                          ORDER BY 
                            fix_time %(sort_order)s
                        ) AS position
                      FROM
                        tracker_location
                      INNER JOIN (VALUES %[device_filters]s) AS device_filter(device_id, start_time, end_time)
                        USING (device_id)
                      WHERE
                        (device_filter.start_time IS NULL OR fix_time > device_filter.start_time::timestamptz(3))
                        AND (device_filter.end_time IS NULL or fix_time <= device_filter.end_time::timestamptz(3))
                        AND (%(provider)s IS NULL OR provider = %(provider)s)
                        AND (%(max_fix_age)s IS NULL OR fix_time >= current_timestamp - %(max_fix_age)s::interval) 
                        AND (%(start_time)s IS NULL OR fix_time > %(start_time)s)
                        AND (%(end_time)s IS NULL OR fix_time <= %(end_time)s)
                  ) AS foo
                  WHERE
                    position <= %(limit)s
                  ORDER BY
                    fix_time %(sort_order)s
                """,
                {
                    'device_filters': device_filters,
                    'end_time': end_time,
                    'limit': min(limit or self.DEFAULT_LIMIT, self.MAXIMUM_LIMIT),
                    'max_fix_age': max_fix_age and '%d seconds' % min(max_fix_age, self.MAXIMUM_FIX_AGE),
                    'provider': provider,
                    'start_time': start_time,
                    'sort_order': ('ASC' if sort_order == SortOrder.ascending else 'DESC',)
                }
            )

            locations = [
                row.get_object({
                  'fix_time': cast.string_to_timestamp
                })
                for row in cursor.fetch_all()
            ]

            return locations

    def get_tracker_locations_by_team_id(
            self,
            team_id,
            connection=None,
            end_time=None,
            limit=None,
            max_fix_age=None,
            provider=None,
            sort_order=None,
            start_time=None):
        """
        Return a list of locations reported by the tracker mobile devices of
        an organization.


        :param team_id: Identification of an organization to fetch location
            updates of tracker mobile devices belonging to this organization.

        :param connection: An object `RdbmsConnection` that supports the
            Python clause `with ...:`.

        :param end_time: Latest inclusive time to filter location updates
            based on their fix time.

        :param limit: Constrain the number of locations per tracker mobile
            device to return to the specified number.  The default value is
            `TrackerService.DEFAULT_LIMIT`.  The maximum value is
            `TrackerService.MAXIMUM_LIMIT`.

        :param max_fix_age: Maximum difference, expressed in seconds, between
            the time when a tracker mobile device calculated the location fix
            and the current time on the server platform.  This duration
            corresponds to the current age of the location fix.

        :param provider: Filter the locations with the provider that
            calculated these locations:

            * ``gps``: This provider determines locations using satellites (Global
              Positioning System (GPS)).

            * ``network``: This provider determines locations based on
              availability of cell towers and Wi-Fi access points.  Results are
              retrieved by means of a network lookup.

            * ``passive``: A special location provider for receiving locations
              without actually initiating a location fix.  This provider can be
              used to passively receive location updates when other applications
              or services request them without actually requesting the locations
              yourself.  This provider will return locations generated by other
              providers.

        :param sort_order: An item of the enumeration `SortOrder` that
            indicates the order to sort location updates:

            * `SortOrder.ascending` (default): The location updates of a tracker
              mobile device are sorted by ascending order of their fix time.

            * `SortOrder.descending`: The location updates of a tracker mobile
              device are sorted by descending order of their fix time.

        :param start_time: Earliest non-inclusive time to filter location
            updates based on their fix time.


        :return: A list of object containing the following attributes:

            * `accuracy` (required): Accuracy in meters of the location.

            * `altitude` (optional): Altitude in meters of the location.

            * `bearing` (optional): Bearing in degrees. Bearing is the horizontal
              direction of travel of the tracker mobile device, and is not related
              to the device orientation. It is guaranteed to be in the range `[0.0,
              360.0]`.

            * `fix_time` (required): Time when the tracker mobile device determined
              the information of this fix.

            * `latitude` (required): Latitude-angular distance, expressed in
              decimal degrees (WGS84 datum), measured from the center of the Earth,
              of a point north or south of the Equator corresponding to the
              location.

            * `longitude` (required): Longitude-angular distance, expressed in
              decimal degrees (WGS84 datum), measured from the center of the Earth,
              of a point east or west of the Prime Meridian corresponding to the
              location.

            * `speed` (optional): Speed in meters/second over the ground.
        """
        if sort_order is None:
            sort_order = SortOrder.ascending

        with self.acquire_rdbms_connection(auto_commit=False, connection=connection) as connection:
            cursor = connection.execute(
                """
                SELECT
                    accuracy,
                    ST_Z(location) AS altitude,
                    bearing,
                    device_id,
                    fix_time,
                    ST_Y(location) AS latitude,
                    ST_X(location) AS longitude,
                    speed
                  FROM (
                    SELECT
                        device_id,
                        location,
                        accuracy,
                        bearing,
                        speed,
                        EXTRACT(EPOCH FROM current_timestamp - fix_time) AS fix_age,
                        fix_time,
                        row_number() OVER (
                          PARTITION BY 
                            device_id 
                          ORDER BY 
                            fix_time %(sort_order)s
                        ) AS position
                      FROM
                        tracker_location
                      WHERE
                        team_id = %(team_id)s
                        AND (%(provider)s IS NULL OR provider = %(provider)s)
                        AND (%(max_fix_age)s IS NULL OR fix_time >= current_timestamp - %(max_fix_age)s::interval) 
                        AND (%(start_time)s IS NULL OR fix_time > %(start_time)s)
                        AND (%(end_time)s IS NULL OR fix_time <= %(end_time)s)
                  ) AS foo
                  WHERE
                    position <= %(limit)s
                  ORDER BY
                    fix_time %(sort_order)s
                """,
                {
                    'end_time': end_time,
                    'limit': min(limit or self.DEFAULT_LIMIT, self.MAXIMUM_LIMIT),
                    'max_fix_age': max_fix_age and '%d seconds' % min(max_fix_age, self.MAXIMUM_FIX_AGE),
                    'provider': provider,
                    'start_time': start_time,
                    'sort_order': ('ASC' if sort_order == SortOrder.ascending else 'DESC',),
                    'team_id': team_id
                }
            )

            locations = [
                row.get_object({
                  'fix_time': cast.string_to_timestamp
                })
                for row in cursor.fetch_all()
            ]

            return locations

    def request_activation_code(
            self,
            app_id,
            account_id,
            team_id,
            activation_code_duration=None,
            remaining_time_for_recycling=None):
        """
        Request a code on behalf of an organization to activate a tracker
        mobile device.

        The function tries to recycle a previous activation code that may have
        been recently generated and not yet expired.  This allows reusing this
        code for consecutively activating several tracker mobile devices
        without having to generate a series of activation codes.


        :param app_id: Identification of the client application such as a Web,
            a desktop, or a mobile application, that accesses the service.

        :param account_id: Identification of an administrator of the
            organization that requests to activate a new tracker mobile device.

        :param team_id: Identification of the organization that is responsible
            for managing this tracker mobile device.

        :param activation_code_duration: Duration in seconds for which the
            generated activation code is valid.

        :param remaining_time_for_recycling: Minimal remaining time in seconds
            of an activation code before it expires in order to be able to be
            recycled.


        :return: An object containing the following attributes:

            * `activation_code` (required): A code that a tracker mobile device
              needs to send to the server platform in order to be activated on
              behalf the organization that manages this device.

            * `expiration_time` (required): Time when this activation code is
              going to expire.


        :raise IllegalAccessException: If the specified account is not an
            administrator of the given organization.
        """
        with self.acquire_rdbms_connection(auto_commit=True) as connection:
            # Retrieve the account of the specified user and check its status.
            account = AccountService().get_account(
                account_id,
                check_status=True,
                connection=connection,
                include_contacts=False)

            # Retrieve the specified organization and check its status.
            team = TeamService().get_team(
                team_id,
                check_status=True,
                connection=connection,
                extended_info=False,
                include_contacts=False)

            # Check whether the specified user is an administrator of the
            # organization on behalf of which a tracker mobile device needs to be
            # activated.
            TeamService().assert_administrator(account_id, team_id)

            # Recycle a previous activation code if possible, or generate a new one.
            expiration_time = ISO8601DateTime.now() + datetime.timedelta(
                seconds=abs(  # @patch: Prevent bug of activation duration less than remaining time
                    activation_code_duration
                    - (remaining_time_for_recycling or self.DEFAULT_ACTIVATION_CODE_REMAINING_TIME_FOR_RECYCLING)))

            return self.__recycle_previous_activation_code(account_id, team_id, expiration_time) or \
                self.__generate_new_activation_code(account_id, team_id, activation_code_duration)

    def report_battery_events(
            self,
            app_id,
            device_id,
            events,
            account_id=None,
            seed=None):
        """
        Report one or more battery state changes of a tracker mobile device:

        * the device is connected to or disconnected from a power source (such
          as the battery of the vehicle this device is mounted on);

        * the level of the device's battery increases or decreases.

        Only devices equipped with an internal battery can broadcast this
        notification.  A device not equipped with an internal battery is
        indeed less secure as it is not able to send any notification when it
        is disconnected from the power source of the vehicle this device is
        mounted on; the device is immediately shutdown.


        :param app_id: Identification of the client application such as a Web,
            a desktop, or a mobile application, that accesses the service.

        :param device_id: Identification of the tracker mobile device that
            reports these geographical location changes.

        :param events: A list of `BatteryStateChangeEvent` objects.

        :param account_id: Identification of the account of a user who has
            logged in the mobile tracker device.

        :param seed: A "number used once" (nonce) -- also known as pseudo-
            random number -- encrypted with keys shared with the platform.
            This seed is used to verify the authentication of the tracker
            mobile device in order to prevent spoofing attack.


        :return: A list of identifications of the battery state updates that
            have been stored.  The function ignores those that were already
            stored.


        :raise DisabledObjectException: If the tracker mobile device has been
            disabled.

        :raise IllegalAccessException: If the given seed is invalid.

        :raise InvalidArgumentException: If both arguments `account_id` and
            `seed` are not defined.

        :raise InvalidOperationException:If the tracker mobile device has not
            been activated by the user or an administrator of the organization
            officially responsible for this device.

        :raise UndefinedObjectException: if the argument `device_id` doesn't
            refer to a device registered to the platform.
        """
        if account_id is None and seed is None:
            raise self.InvalidArgumentException("The argument 'account_id' or 'seed' MUST be defined")

        if seed:
            # Retrieve the information of the tracker mobile device.  Require the
            # extended information to get the security key of this device.
            device = self.__get_device(device_id, check_status=True, include_extended_info=True)

            # Check whether the seed has been correctly encrypted with the security
            # key of the tracker mobile device.
            self.__verify_seed(device, seed)

        with self.acquire_rdbms_connection(auto_commit=True) as connection:
            # Filter out battery state changes that would have been already reported
            # in a previous call.
            #
            # This may happen when network outage occurs after the client
            # application reported successfully a batch of battery state changes, but
            # the transaction timeout before the client application had the chance
            # to receive the acknowledgement from the server platform.  The client
            # application reattempts to report one more time these locations.
            cursor = connection.execute(
                """
                SELECT 
                    event_id
                  FROM 
                    tracker_battery_event
                  WHERE 
                    event_id IN (%[event_ids]s)
                """,
                {
                    'event_ids': [state_change.event_id for state_change in events]
                })

            duplicated_event_ids = [
                row.get_value('event_id', cast.string_to_uuid)
                for row in cursor.fetch_all()
            ]

            if duplicated_event_ids:
                events = [
                    event
                    for event in events
                    if event.event_id not in duplicated_event_ids
                ]

            # Store the battery state changes that have not been already stored.
            if events:
                connection.execute(
                    """
                    INSERT INTO tracker_battery_event(
                        event_id,
                        device_id,
                        app_id,
                        account_id,
                        event_type,
                        event_time,
                        battery_level,
                        location,
                        accuracy,
                        bearing,
                        speed,
                        fix_time,
                        provider)
                      VALUES 
                        %[values]s
                    """,
                    {
                        'values': [
                            (event.event_id,
                             device_id,
                             app_id,
                             account_id or device.account_id,
                             event.event_type,
                             event.event_time,
                             event.battery_level,
                             event.location and (f'ST_SetSRID(ST_MakePoint({event.location.longitude}, {event.location.latitude}, {event.location.altitude}), 4326)',),
                             event.location and event.location.accuracy,
                             event.location and event.location.bearing,
                             event.location and event.location.speed,
                             event.location and event.location.fix_time,
                             event.location and event.location.provider)
                            for event in events
                        ]
                    })

                # Update the last update of the battery state of the tracker mobile
                # device, if updates more recent than the current batter state of this
                # device.
                if seed:  # @todo: Should be able to update this information even with logged-in used.
                    self.__update_device_battery_state(app_id, device, events, connection=connection)

            return [event.event_id for event in events]

    def report_location_updates(
            self,
            app_id,
            device_id,
            events,
            account_id=None,
            seed=None,
            team_id=None):
        """
        Report geographical location updates on behalf of a tracker mobile
        device.


        :param app_id: Identification of the client application such as a Web,
            a desktop, or a mobile application, that accesses the service.

        :param device_id: Identification of the tracker mobile device that
            reports these geographical location changes.

        :param events: A list of `LocationUpdate` objects.

        :param account_id: Identification of the account of a user who has
            logged in to the server platform with the mobile tracker device.

        :param seed: A "number used once" (nonce) -- also known as pseudo-
            random number -- encrypted with keys shared with the platform.
            This seed is used to verify the authentication of the tracker
            mobile device in order to prevent spoofing attack.

        :param team_id: Identification of the organization who owns this
            tracker mobile device.


        :return: A list of identifications of the reports that have been
            stored.  The function ignores those that were already stored.


        :raise DeletedObjectException: If the tracker mobile device has been
            deleted.

        :raise DisabledObjectException: If the tracker mobile device has been
            disabled.

        :raise IllegalAccessException: If the given seed is invalid.

        :raise InvalidArgumentException: If one or more reports identify a
            tracker mobile device different from the argument `device_id`.

        :raise InvalidOperationException: If the tracker mobile device has not
            been activated by the user or an administrator of the organization
            officially responsible for this device.

        :raise UndefinedObjectException: if the argument `device_id` doesn't
            refer to a device registered to the platform.
        """
        # Check whether the location events are provided by the same tracker
        # mobile device.
        self.__assert_location_updates_from_same_device(events, device_id)

        # if seed:
        # Retrieve the information of the tracker mobile device.  Require the
        # extended information to get the security key of this device.
        device = self.__get_device(device_id, check_status=True, include_extended_info=True)

            # # Check whether the seed has been correctly encrypted with the security
            # # key of the tracker mobile device.
            # self.__verify_seed(device, seed)

        with self.acquire_rdbms_connection(auto_commit=True) as connection:
            # Filter out locations that would have been already reported in a
            # previous call.
            #
            # This may happen when a network outage occurs after the client
            # application reported successfully a batch of locations, but the
            # transaction timeout before the client application had the chance
            # to receive the acknowledgement from the server platform; the client
            # application reattempts to report one more time these locations.
            cursor = connection.execute(
                """
                SELECT
                    event_id
                  FROM 
                    tracker_location
                  WHERE
                    event_id IN (%[event_ids]s)
                """,
                {
                    'event_ids': [event.event_id for event in events]
                })

            duplicated_event_ids = [
                row.get_value('event_id', cast.string_to_uuid)
                for row in cursor.fetch_all()
            ]

            if duplicated_event_ids:
                events = [
                    event
                    for event in events
                    if event.event_id not in duplicated_event_ids
                ]

            # Store location updates that have not been already stored.
            if events:
                connection.execute(
                    """
                    INSERT INTO tracker_location(
                        event_id,
                        device_id,
                        app_id,
                        account_id,
                        team_id,
                        location,
                        accuracy,
                        bearing,
                        speed,
                        fix_time,
                        provider,
                        network_type,
                        satellites)
                      VALUES 
                        %[values]s
                      RETURNING 
                        event_id
                    """,
                    {
                        'values': [
                            (event.event_id,
                             device_id,
                             app_id,
                             account_id or device.account_id,
                             team_id or device.team_id,
                             (f'ST_SetSRID(ST_MakePoint({event.location.longitude}, {event.location.latitude}, {event.location.altitude}), 4326)',),
                             event.location.accuracy,
                             event.location.bearing,
                             event.location.speed,
                             event.location.fix_time,
                             event.location.provider,
                             event.network_type,
                             event.satellites)
                            for event in events]
                    })

                # Update the last known location of the tracker mobile device if any
                # location updates more recent than the current last known location of
                # this device.
                # if seed:
                self.__update_device_last_known_location(app_id, device, events, connection=connection)

            return [event.event_id for event in events]

    def shake_hands(
            self,
            app_id,
            device_id,
            mac_address,
            agent_application,
            is_battery_present,
            is_battery_plugged,
            battery_level,
            location=None):
        """
        Establish the connection between a tracker mobile device and the
        server platform before normal communication begins.

        The function registers the device if not already registered.

        The registration of the device is pending until an individual user or
        an administrator of an organization responsible for this device
        reviews the information provided.  The device may not be able to
        access all the services supported by the server platform until the
        device has been activated.


        :param app_id: Identification of the client application such as a Web,
            a desktop, or a mobile application, that accesses the service.

        :param device_id: Identification of the device.

        :param mac_address: Media Access Control (MAC) address of the device.
            A MAC address is a unique identifier assigned to a network
            interface for communications at the data link layer of a network
            segment.

        :param agent_application: A `ClientApplication` object representing
            the agent application installed on the tracker mobile device.

        :param is_battery_present: Indicate whether the device is equipped
            with an internal battery.

        :param is_battery_plugged: Indicate whether the battery of the tracker
            mobile device is currently plugged to a power source.

        :param battery_level: Current level in percentage of the battery of
            the tracker mobile device.

        :param location: An object `GeoPoint` representing the last known
            location of the device.


:return: An object containing the following attributes:

    * `object_status` (required): An item of the enumeration `ObjectStatus`
      corresponding to the current status of the tracker mobile device.


        """
        with self.acquire_rdbms_connection(auto_commit=True) as connection:
            try:
                # Retrieve the information of the tracker mobile device.  This raises
                # the exception `UndefinedObjectException` if this device is not
                # registered yet.
                device = self.__get_device(
                    device_id,
                    check_status=True,
                    strict_status=False,
                    connection=connection,
                    include_extended_info=True)

                # Update the system information of this device when necessary.
                self.__update_device_sys_info(device, agent_application, connection=connection)

            except self.UndefinedObjectException:
                device = self.__preregister_device(
                    device_id,
                    mac_address,
                    agent_application,
                    is_battery_present,
                    is_battery_plugged,
                    battery_level,
                    connection=connection,
                    location=location)

        # Return the necessary information only.
        device = Object(object_status=device.object_status)

        return device



    # def get_tracker_locations_by_account_ids(
    #         self,
    #         account_ids,
    #         connection=None,
    #         end_time=None,
    #         limit=None,
    #         max_fix_age=None,
    #         provider=None,
    #         sort_order=None,
    #         start_time=None):
    #     """
    #
    #     >>> get_tracker_locations(
    #     ...     uuid.UUID('e58a3c00-b52f-11ea-8e0d-0008a20c190f'),
    #     ...     start_time=datetime.datetime(2020, 7, 10, 4, 13, 49),
    #     ...     end_time=datetime.datetime(2020, 7, 10, 4, 14, 0),
    #     ...     provider='gps')
    #
    #     >>> get_tracker_locations(
    #     ...     accounts_ids=(
    #     ...         uuid.UUID('e58a3c00-b52f-11ea-8e0d-0008a20c190f'),
    #     ...         datetime.datetime(2020, 7, 10, 4, 13, 49, 273627),
    #     ...         datetime.datetime(2020, 7, 10, 4, 15, 0)
    #     ...     ),
    #     ...     max_fix_age=60)
    #
    #
    #     >>> get_tracker_locations(
    #     ...     accounts_ids=[
    #     ...         uuid.UUID('e58a3c00-b52f-11ea-8e0d-0008a20c190f'),
    #     ...         uuid.UUID('15e0e0a6-b5d1-11ea-8e0d-0008a20c190f')
    #     ...     ],
    #     ...     start_time=datetime.datetime(2020, 7, 10, 4, 13, 49),
    #     ...     end_time=datetime.datetime(2020, 7, 10, 4, 14, 0))
    #
    #
    #     >>> get_tracker_locations(
    #     ...     accounts_ids=[
    #     ...         (uuid.UUID('e58a3c00-b52f-11ea-8e0d-0008a20c190f'),
    #     ...          datetime.datetime(2020, 7, 10, 4, 13, 49, 273627),
    #     ...          datetime.datetime(2020, 7, 10, 4, 15, 0)),
    #     ...         (uuid.UUID('15e0e0a6-b5d1-11ea-8e0d-0008a20c190f'),
    #     ...          datetime.datetime(2020, 7, 2, 0, 0, 0),
    #     ...          None)
    #     ...     ],
    #     ...     max_fix_age=60)
    #
    #     :param account_ids:
    #
    #
    #     :param connection:
    #     :param end_time:
    #     :param limit:
    #     :param max_fix_age:
    #     :param provider:
    #     :param sort_order:
    #     :param start_time:
    #     :return:
    #     """
    #
    #
    #     with self.acquire_rdbms_connection(auto_commit=False, connection=connection) as connection:
    #         cursor = connection.execute(
    #             """
    #             """,
    #             {
    #                 "account_ids": account_ids
    #                 'end_time': end_time,
    #                 'limit': min(limit or self.DEFAULT_LIMIT, self.MAXIMUM_LIMIT),
    #                 'max_fix_age': max_fix_age and '%d seconds' % min(max_fix_age, self.MAXIMUM_FIX_AGE),
    #                 'provider': provider,
    #                 'start_time': start_time,
    #                 'sort_order': ('ASC' if sort_order == SortOrder.ascending else 'DESC',)
    #             }
    #         )
    #
    #         locations = [
    #             row.get_object({
    #               'fix_time': cast.string_to_timestamp
    #             })
    #             for row in cursor.fetch_all()
    #         ]
    #
    #         return locations


    # def get_tracker_locations(self,
    #         account_ids=None,
    #         connection=None,
    #         end_time=None,
    #         device_ids=None,
    #         limit=None,
    #         max_fix_age=None,
    #         offset=None,
    #         provider=None,
    #         sort_order=None,
    #         start_time=None,
    #         team_id=None):
    #     """
    #
    #     >>> get_tracker_locations(
    #     ...     team_id=uuid.UUID('2249b140-6d80-11ea-8e0d-0008a20c190f'),
    #     ...     start_time=datetime.datetime(2020, 7, 10, 4, 13, 49),
    #     ...     max_fix_age=60)
    #
    #
    #     >>> get_tracker_locations(
    #     ...     device_ids='869044038077499',
    #     ...     start_time=datetime.datetime(2020, 7, 10, 4, 13, 49),
    #     ...     end_time=datetime.datetime(2020, 7, 10, 4, 14, 0),
    #     ...     provider='gps')
    #
    #
    #     >>> get_tracker_locations(
    #     ...     device_ids=['869044038077499', '100702457943371'],
    #     ...     max_fix_age=30)
    #
    #
    #     >>> get_tracker_locations(
    #     ...     accounts_ids=[
    #     ...         UUID('e58a3c00-b52f-11ea-8e0d-0008a20c190f'),
    #     ...         uuid.UUID('15e0e0a6-b5d1-11ea-8e0d-0008a20c190f')
    #     ...     ],
    #     ...     start_time=datetime.datetime(2020, 7, 10, 4, 13, 49),
    #     ...     end_time=datetime.datetime(2020, 7, 10, 4, 14, 0))
    #
    #
    #     >>> get_tracker_locations(
    #     ...     accounts_ids=[
    #     ...         (uuid.UUID('e58a3c00-b52f-11ea-8e0d-0008a20c190f'),
    #     ...          datetime.datetime(2020, 7, 10, 4, 13, 49, 273627),
    #     ...          datetime.datetime(2020, 7, 10, 4, 15, 0)),
    #     ...         (uuid.UUID('15e0e0a6-b5d1-11ea-8e0d-0008a20c190f'),
    #     ...          datetime.datetime(2020, 7, 2, 0, 0, 0),
    #     ...          None)
    #     ...     ])
    #
    #
    #     :param account_ids: List of identification of accounts of users to
    #         fetch location updates of tracker mobile devices that those users
    #         were logged in.
    #
    #     :param connection: An object `RdbmsConnection` that supports the
    #         Python clause `with ...:`.
    #
    #     :param end_time: Latest inclusive time to filter location updates
    #         based on their fix time.
    #
    #     :param device_ids: List of identifications of tracker mobile devices
    #         to fetch location updates.
    #
    #     :param limit: Constrain the number of locations per tracker mobile
    #         device to return to the specified number.  The default value is
    #         `TrackerService.DEFAULT_LIMIT`.  The maximum value is
    #         `TrackerService.MAXIMUM_LIMIT`.
    #
    #     :param max_fix_age: Maximum difference, expressed in seconds, between
    #         the time when a tracker mobile device calculated the location fix
    #         and the current time on the server platform.  This duration
    #         corresponds to the current age of the location fix.
    #
    #     :param sort_order: An item of the enumeration `SortOrder` that
    #         indicates the order to sort location updates:
    #
    #         * `SortOrder.ascending` (default): The location updates of a tracker
    #           mobile device are sorted by ascending order of their fix time.
    #
    #         * `SortOrder.descending`: The location updates of a tracker mobile
    #           device are sorted by descending order of their fix time.
    #
    #     :param start_time: Earliest non-inclusive time to filter location
    #         updates based on their fix time.
    #
    #     :param team_id: Identification of an organization to fetch location
    #         updates of tracker mobile devices belonging to this organization.
    #
    #     :return:
    #     """
    #     if not account_ids and not device_ids and not team_id:
    #         raise ValueError("Missing argument one of the arguments 'account_ids', 'devices_id', 'team_id'")
    #
    #     if account_ids and device_ids:
    #         raise ValueError("Conflicting arguments 'account_ids' and 'devices_ids'")
    #
    #     if max_fix_age and (start_time or end_time):
    #         raise ValueError("Conflicting arguments 'max_fix_age' with 'start_time' or 'end_time'")
    #
    #
    #
    #     filter_with_account_id = account_ids is not None
    #
    #     with self.acquire_rdbms_connection(auto_commit=False, connection=connection) as connection:
    #         cursor = connection.execute(
    #             """
    #             SELECT
    #                 accuracy,
    #                 ST_Z(location) AS altitude,
    #                 bearing,
    #                 device_id,
    #                 fix_time,
    #                 ST_Y(location) AS latitude,
    #                 ST_X(location) AS longitude,
    #                 speed
    #               FROM (
    #                 SELECT
    #                     account_id,
    #                     device_id,
    #                     team_id,
    #                     location,
    #                     accuracy,
    #                     bearing,
    #                     speed,
    #                     fix_time
    #                     row_number() OVER (
    #                       PARTITION BY
    #                         device_id
    #                       ORDER BY fix_time %(sort_order)s
    #                     ) AS position
    #                   FROM
    #                     tracker_location
    #                   INNER JOIN (VALUES %[values]s)
    #                     AS device(
    #                         device_id,
    #                         start_time,
    #                         end_time)
    #                     USING (device_id)
    #                   WHERE
    #                     ((%(device_ids)s) IS NULL OR device_id IN (%(device_ids)s))
    #                     AND ((%(account_id)s) IS NULL OR account_id IN (%(account_id)s))
    #                     AND (%(team_id)s IS NULL OR team_id = %(team_id)s)
    #                     AND (%(provider)S IS NULL OR provider = %(provider)s)
    #                     AND (device.start_time IS NULL OR fix_time > device.start_time::timestamptz(3))
    #                     AND (device.end_time IS NULL OR fix_time <= device.end_time::timestamptz(3))
    #               ) AS foo
    #
    #
    #
    #               WHERE
    #               ORDER BY
    #                 fix_time %(sort_order)s
    #               LIMIT %(limit)s
    #               OFFSET %(offset)s
    #             """,
    #             {
    #                 'account_ids': account_ids,
    #                 'device_ids': device_ids,
    #                 'end_time': end_time,
    #                 'limit': min(limit or self.DEFAULT_LIMIT, self.MAXIMUM_LIMIT),
    #                 'offset': offset or 0,
    #                 'provider': provider,
    #                 'start_time': start_time,
    #                 'sort_order': (True, sort_order or SortOrder.ascending),
    #                 'team_id': team_id
    #             }
    #         )































#
#
#     def on_device_alert_message(self, app_id, device_id, seed, alert_events):
#         """
#         Signal the platform that a device reports events related to one or
#         more alerts.  An alert starts whenever the device detects a movement
#         based on the values read from a built-in motion sensor, such as a
#         gyroscope or an accelerometer.  An alert stops when no movement is
#         etected after a few seconds.
#
#         Depending on the current alert mode of the device, an alert event is
#         considered either as a serious threat (active mode), either as
#         expected (passive mode).
#
#
#         :param app_id: identification of the client application such as a Web,
#             a desktop, or a mobile application, that accesses the service.
#
#         :param device_id: identification of the device that reported these
#             alert changes.
#
#         :param seed: a seed, which is a "number used once" (nonce) -- also
#             known as pseudo-random number -- encrypted with keys shared with
#             the platform.  This seed is used to verify the authentication of
#             the device in order to prevent spoofing attack.
#
#         :param alert_events: a list of instances `AlertEvent` each indicates
#             whether an alert starts or ends.
#
#
#         :return: a list of identifications of alerts that ended while they
#             weren't previously registered against the platform.
#
#
#         :raise DeletedObjectException: if the device has been deleted.
#
#         :raise DisabledObjectException: if the device has been disabled.
#
#         :raise InvalidOperationException: if the device is not linked to any
#             account or team.
#
#         :raise UndefinedObjectException: if the specified device_id doesn't refer
#             to a device registered against the platform.
#         """
#         self.verify_seed(device_id, seed)
#         device = XeberusService().get_device(device_id)
#
#         with self.acquire_rdbms_connection(True) as connection:
#             # Register all the events that correspond to starting alerts.
#             started_alerts = [ (alert_event.alert_id, alert_event.event_time)
#                     for alert_event in alert_events
#                         if alert_event.event_type == XeberusService.AlertEventType.alert_start ]
#             if len(started_alerts) > 0:
#                 cursor = connection.execute("""
#                     INSERT INTO xeberus_alert(
#                             alert_id,
#                             device_id,
#                             account_id,
#                             team_id,
#                             start_time)
#                       SELECT alert_id::uuid,
#                              %(device_id)s,
#                              %(account_id)s,
#                              %(team_id)s,
#                              start_time::timestamptz(3)
#                         FROM (VALUES %[values]s) AS foo(alert_id, start_time)
#                         WHERE NOT EXISTS (
#                           SELECT true
#                             FROM xeberus_alert
#                             WHERE xeberus_alert.alert_id = foo.alert_id::uuid)""",
#                     { 'account_id': device.account_id,
#                       'device_id': device_id,
#                       'team_id': device.team_id,
#                       'values': started_alerts })
#
#             # Register all the events that correspond to ending alerts.
#             mismatched_alerts = []
#
#             ended_alerts = [
#                     (alert_event.alert_id,
#                      alert_event.event_time,
#                      alert_event.location and alert_event.location.longitude,
#                      alert_event.location and alert_event.location.latitude,
#                      alert_event.location and alert_event.location.altitude,
#                      alert_event.location and alert_event.location.accuracy,
#                      alert_event.location and alert_event.location.provider,
#                      alert_event.location and alert_event.location.fix_time)
#                 for alert_event in alert_events
#                     if alert_event.event_type == XeberusService.AlertEventType.alert_end ]
#
#             if len(ended_alerts) > 0:
#                 cursor = connection.execute("""
#                     UPDATE xeberus_alert
#                       SET end_time = foo.end_time::timestamptz(3),
#                           update_time = current_timestamp::timestamptz(3),
#                           location = ST_SetSRID(ST_MakePoint(foo.longitude::float, foo.latitude::float, foo.altitude), 4326),
#                           accuracy = foo.accuracy::float,
#                           provider = foo.provider,
#                           fix_time = foo.fix_time::timestamptz(3)
#                       FROM (VALUES %[values]s) AS foo (alert_id, end_time, longitude, latitude, altitude, accuracy, provider, fix_time)
#                       WHERE xeberus_alert.alert_id = foo.alert_id::uuid
#                         AND xeberus_alert.device_id = %(device_id)s
#                       RETURNING foo.alert_id""",
#                     { 'device_id': device_id,
#                       'values': ended_alerts })
#                 mismatched_alerts = set([ alert_id for (alert_id, _, _, _, _, _, _, _) in ended_alerts ]) \
#                         - set([ row.get_value('alert_id', cast.string_to_uuid) for row in cursor.fetch_all() ])
#
#             # Send a notification to the mobile devices of the user who owns the
#             # tracker device that reported these alerts.  Only send the most
#             # recent alert event, which overrides all the previous events that
#             # were not yet sent.
#             if len(alert_events) > 0:
#                 alert_events.sort(key=lambda alert_event: alert_event.event_time, reverse=True)
#                 most_recent_alert_event = alert_events[0]
#                 most_recent_alert_event.device_id = device_id
#
#                 NotificationService().send_notification(app_id,
#                         XeberusService.XeberusNotification.on_alert_state_changed,
#                         recipient_ids=account_id,
#                         team_id=device.team_id,
#                         lifespan=XeberusService.NOTIFICATION_LIFESPAN_DEVICE_ALERT_STATE_CHANGED,
#                         notification_mode=NotificationService.NotificationMode.push,
#                         package=XeberusService.XEBERUS_MOBILE_APPLICATION_PACKAGE,
#                         payload=most_recent_alert_event)
#
#             return mismatched_alerts
#
#


#
#
#
#     def on_device_keepalive_message(self, app_id, device_id, seed,
#             battery_level=None,
#             is_battery_plugged=None,
#             location=None):
#         """
#         Keepalive (KA) sent by one device to the platform to check that the
#         link between the two is operating, or to informm the platform that the
#         device is running properly.
#
#
#         :param app_id: identification of the client application such as a Web,
#             a desktop, or a mobile application, that accesses the service.
#
#         :param device_id: identification of the device.
#
#         :param seed: a seed, which is a "number used once" (nonce) -- also
#             known as pseudo-random number -- encrypted with keys shared with
#             the platform.  This seed is used to verify the authentication of
#             the device in order to prevent spoofing attack.
#
#         :param battery_level: current level in percentage of the battery of
#             the mobile device.
#
#         :param is_battery_plugged: indicate if the battery of the mobile
#             device is plugged in a power source .
#
#         :param last_known_location: an instance `GeoPoint` representing the
#             last known location of the device.
#
#
#         :raise DeletedObjectException: if the device has been deleted.
#
#         :raise DisabledObjectException: if the device has been disabled.
#
#         :raise UndefinedObjectException: if the specified device_id doesn't refer
#             to a device registered against the platform.
#         """
#         # Check whether this device is enabled.
#         device = self.get_device(device_id, check_status=True)
#
#         # Verify that this keepalive message is really sent by the specified
#         # device.
#         self.verify_seed(device_id, seed)
#
#         # Update the last time keep-alive sent by the device.
#         with self.acquire_rdbms_connection(True) as connection:
#             cursor = connection.execute("""
#                 UPDATE xeberus_device
#                   SET keepalive_time = current_timestamp,
#                       is_battery_plugged = %(is_battery_plugged)s,
#                       battery_level = %(battery_level)s,
#                       update_time = current_timestamp::timestamptz(3)
#                   WHERE device_id = %(device_id)s
#                   RETURNING fix_time""",
#                 { 'battery_level': battery_level,
#                   'device_id': device_id,
#                   'is_battery_plugged': is_battery_plugged })
#
#             # Update the last known location of the device if most recent than the
#             # last already stored.
#             if last_known_location:
#                 fix_time = cursor.fetch_one().get_value('fix_time', cast.string_to_timestamp)
#                 if fix_time is None or fix_time < last_known_location.fix_time:
#                     connection.execute("""
#                         UPDATE xeberus_device
#                           SET location = ST_SetSRID(ST_MakePoint(%(longitude)s, %(latitude)s, %(altitude)s), 4326),
#                               accuracy = %(accuracy)s,
#                               bearing = %(bearing)s,
#                               speed = %(speed)s,
#                               fix_time = %(fix_time)s
#                               provider = %(provider)s
#                           WHERE device_id = %(device_id)s""",
#                         { 'accuracy': location and location.accuracy,
#                           'altitude': location and location.altitude,
#                           'bearing': location and location.bearing,
#                           'fix_time': location and location.fix_time,
#                           'latitude': location and location.latitude,
#                           'longitude': location and location.longitude,
#                           'provider': location and location.provider,
#                           'speed': location and location.speed })
#
#             # Send a notification to indicate that the battery power increases
#             # (charging) or decreases (discharging) by a quarter (25%), or when
#             # the battery power reaches a critical level (1%).
#             if device.battery_level and battery_level:
#                 previous_battery_status_index = int(device.battery_level * 100) / 25
#                 current_battery_status_index = int(battery_level * 100) / 25
#
#                 if current_battery_status_index != previous_battery_status_index or \
#                    battery_level == 0.01 and device.battery_level > 0.01:
#                     NotificationService().send_notification(app_id,
#                             XeberusService.XeberusNotification.on_battery_state_changed,
#                             recipient_ids=device.account_id,
#                             team_id=device.team_id,
#                             lifespan=XeberusService.NOTIFICATION_LIFESPAN_BATTERY_STATE_CHANGED,
#                             notification_mode=NotificationService.NotificationMode.push,
#                             package=XeberusService.XEBERUS_MOBILE_APPLICATION_PACKAGE,
#                             payload={
#                                 "battery_level": battery_level,
#                                 "device_id": device_id,
#                                 "event_time": date_util.ISO8601DateTime.now(),
#                                 "event_type": BatteryStateChange.BatteryStateEventType.battery_level_changed,
#                                 "is_battery_plugged": is_battery_plugged })
#
#
#     def acquire_device(self, app_id, account_id, device_id):
#         """
#         Allocate a registered device to a user account providing this device
#         is not already acquired by another user.
#
#         :param app_id: identification of the client application such as a Web,
#             a desktop, or a mobile application, that accesses the service.
#
#         :param account_id: identification of the account of the user who
#             requests the specified device.
#
#         :param device_id: International Mobile Equipment Identity (device_id) number of
#             the device to allocate to the user account.
#
#         :return: the object returned by the function `get_device`.
#
#         :raise DeletedObjectException: if the device has been deleted while
#             the argument `check_status` has been set to `True`.
#
#         :raise DisabledObjectException: if the device has been disabled while
#             the argument `check_status` has been set to `True`.
#
#         :raise InvalidOperationException: if the specified device is already
#             acquired by another user account.
#
#         :raise MaximumRegisteredDevicesReachedException: if the maximum number
#             of registered devices for the specified user reached and as such
#             this user is not allowed not register anymore devices.
#
#         :raise UndefinedObjectException: if the specified identification
#             doesn't refer to a device registered against the platform.
#         """
#         device = self.get_device(device_id, check_status=True)
#
#         # Check whether the specified device is available:
#         #
#         # * if the device is not attached to a user account
#         # * if the device belongs to a team, and the account on behalf of whom
#         #   the function is called is a member of this team.
#         if device.account_id:
#             if device.account_id != account_id and (device.team_id is None or not TeamService().is_member(account_id, device.team_id)):
#                 raise self.InvalidOperationException('This device is alread acquired by another user')
#
#         # Allocate this device to the specified user, providing this user has
#         # not reached the maximum number of device already registered.
#         else:
#             with self.acquire_rdbms_connection(True) as connection:
#                 cursor = connection.execute("""
#                     SELECT COUNT(*) AS device_count
#                       FROM xeberus_device
#                       WHERE account_id = %(account_id)s""",
#                     { 'account_id': account_id })
#                 if cursor.fetch_one().get_value('device_count') > XeberusService.MAXIMUM_REGISTERED_DEVICES_PER_USER:
#                     raise self.MaximumRegisteredDevicesReachedException()
#
#                 connection.execute("""
#                     UPDATE xeberus_device
#                       SET account_id = %(account_id)s,
#                           update_time = current_timestamp::timestamptz(3)
#                       WHERE device_id = %(device_id)s""",
#                     { 'account_id': account_id,
#                       'device_id': device_id })
#
#         return device
#
#
#     def activate_device(self, app_id, admin_account_id, device_id, customer_account_id, team_id=None):
#         """
#         Activate a device which registration is still pending.
#
#         :param app_id: identification of the client application such as a Web,
#             a desktop, or a mobile application, that accesses the service.
#
#         :param admin_account_id: identification of the account of an
#             administrator of the Xeberus team.
#
#         :param device_id: International Mobile Equipment Identity (device_id) number
#             of the device to activate and allocate to the specified user
#             account.
#
#         :param customer_account_id: identification of the account of the user
#            to allocate the device to.
#
#         :param team_id: identification of a team to allocate the device to.
#             The specified customer user account MUST belong to this team.
#
#         :raise DeletedObjectException: if the device has been deleted.
#
#         :raise DisabledObjectException: if the device has been disabled.
#
#         :raise IllegalAccessException: if the function is called on behalf of
#             a user account that is not an administrator of the Xeberus team.
#
#         :raise InvalidOperationException: if the specified device is already
#             activated.
#
#         :raise UndefinedObjectException: if the specified identification
#             doesn't refer to a device registered against the platform.
#         """
#         customer_account = AccountService().get_account(customer_account_id, check_status=True)
#
#         admin_account = AccountService().get_account(admin_account_id, check_status=True)
#         TeamService()._assert_administrator(admin_account_id, XeberusService.XEBERUS_TEAM.team_id)
#
#         device = self.get_device(device_id, check_status=True)
#         if device.object_status != OBJECT_STATUS_PENDING:
#             raise self.InvalidOperationException()
#
#         if team_id:
#             team = TeamService().get_team(team_id, check_status=True)
#             TeamService()._assert_member(customer_account_id, team_id)
#
#         with self.acquire_rdbms_connection(True) as connection:
#             cursor = connection.execute("""
#                 UPDATE xeberus_device
#                   SET account_id = %(account_id)s,
#                       team_id = %(team_id)s,
#                       object_status = %(OBJECT_STATUS_ENABLED)s,
#                       update_time = current_timestamp
#                   WHERE device_id = %(device_id)s""",
#                 { 'OBJECT_STATUS_ENABLED': OBJECT_STATUS_ENABLED,
#                   'account_id': customer_account_id,
#                   'device_id': device_id,
#                   'team_id': team_id })
#
#
#     def get_devices(self, app_id, account_id,
#             limit=BaseRdbmsService.DEFAULT_LIMIT,
#             offset=0,
#             sync_time=None):
#         """
#         @deprecated: replaced by get_devices_ex
#
#
#         Return a list of devices that the specified user currently owns.
#
#
#         :param app_id: identification of the client application such as a Web,
#             a desktop, or a mobile application, that accesses the service.
#
#         :param account_id: identification of the account of the user to return
#             the list of devices he currently owns.
#
#         :param offset: require to skip that many records before beginning to
#             return records to the client.  Default value is `0`.  If both
#             `offset` and `limit` are specified, then `offset` records
#             are skipped before starting to count the limit records that are
#             returned.
#
#         :param limit: constrain the number of records that are returned to the
#             specified number.  Default value is `20`. Maximum value is
#             `100`.
#         :param sync_time: indicate the earliest non-inclusive time to filter
#             the devices of this user based on the update time of their
#             properties.  If not specified, no time as lower bounding filter is
#             applied, meaning that all the devices could possibly be returned.
#
#
#         :return: a list of instances containing the following members:
#
#             * `accuracy`: accuracy in meters of the last known location of
#               the device.
#
#             * `activation_time`: time when the user acquires this device.
#
#             * `altitude`: altitude in meters of the last known location of
#               the device.
#
#             * `battery_level`: current level in percentage of the battery of
#               the device.
#
#             * `bearing`: bearing in degrees.  Bearing is the horizontal
#               direction of travel of the device, and is not related to the
#               device orientation.  It is guaranteed to be in the range
#               `[0.0, 360.0]`, or `None` if the bearing of the device at
#               its last known location is not provided.
#
#             * `fix_time`: time when the device calculated the fix of the
#               last known location of the device.
#
#             * `fix_age`: difference, expressed in seconds, between the
#               time when the device calculated the location fix and the current
#               time on the platform.  This duration corresponds to the current
#               age of the location fix.
#
#             * `device_id`: International Mobile Equipment Identity (device_id) number
#               of a device.
#
#             * `is_battery_alarm_muted`: indicate whether the user muted the
#               alarm that was triggered when the battery has been unplugged or
#               when the level of the battery went down below a critical
#               threshold.
#
#             * `is_battery_plugged`: indicate if the battery of the device is
#               plugged in a power source.
#
#             * `is_device_alarm_muted`: indicate whether the user muted the
#               alarm that was triggered when the device is not responding
#               anymore.
#
#             * `is_security_alarm_muted`: indicate whether the user muted the
#               alarm system that was triggered when the device has detected a
#               movement or a location change while the security level is set to
#               `+security-level-active+`.
#
#             * `keepalive_time`: time of the last keep-alive (KA) message
#               sent by this device to the platform to check that the link
#               between the device and the platform is operating, and to notify
#               the  platform that the device is still in operation as expected.
#
#             * `latitude`: latitude-angular distance, expressed in decimal
#               degrees (WGS84 datum), measured from the center of the Earth, of
#               a point north or south of the Equator, of the last known
#               location of the device.
#
#             * `longitude`: longitude-angular distance, expressed in decimal
#               degrees (WGS84 datum), measured from the center of the Earth, of
#               a point east or west of the Prime Meridian, of the last known
#               location of the device.
#
#             * `name`: humanely readable name of the vehicle this device is
#               attached to.
#
#             * `picture_id`: identification of the graphical representation
#               of this device, or more likely by extension the vehicle where
#               this device is installed in, if any defined.
#
#             * `picture_url`: Uniform Resource Locator (URL) that specifies
#               the location of the graphical representation of the vehicle this
#               device is attached to, if any defined.  The client application
#               can use this URL and append the query parameter `size` to
#               specify a given pixel resolution of the device's picture:
#
#               * `thumbnail`
#
#               * `small`
#
#               * `medium`
#
#               * `large`
#
#             * `provider`: name of the location provider that reported the
#               geographical location.
#
#             * `security_level`: the current level of security of this device
#               (cf. `XeberusService.SecurityLevel`).
#
#             * `speed`: speed in meters/second over the ground, or `None`
#               if the speed of the device at its last known location is not
#               provided.
#
#             * `update_time`: time of the most recent modification of at
#               least one properties of this device, such as its security level,
#               its name, etc.  This time should be used as the cache time
#               reference for this device.
#         """
#         with self.acquire_rdbms_connection() as connection:
#             cursor = connection.execute("""
#                 SELECT device_id,
#                        name,
#                        picture_id,
#                        security_level,
#                        COALESCE(is_security_alarm_muted, false) AS is_security_alarm_muted,
#                        activation_time,
#                        keepalive_time,
#                        ST_X(location) AS longitude,
#                        ST_Y(location) AS latitude,
#                        ST_Z(location) AS altitude,
#                        accuracy,
#                        fix_time,
#                        EXTRACT(EPOCH FROM current_timestamp - fix_time) AS fix_age,
#                        speed,
#                        bearing,
#                        is_battery_plugged,
#                        battery_level,
#                        --COALESCE(is_battery_alarm_muted, false) AS is_battery_alarm_muted,
#                        --COALESCE(is_device_alarm_muted, false) AS is_device_alarm_muted,
#                        object_status,
#                        update_time
#                   FROM xeberus_device
#                   WHERE ((account_id = %(account_id)s) OR
#                          (team_id IS NOT NULL AND team_is_member(%(account_id)s, team_id)))
#                     AND ((%(sync_time)s IS NOT NULL AND update_time > %(sync_time)s) OR
#                          (%(sync_time)s IS NULL AND object_status = %(OBJECT_STATUS_ENABLED)s))""",
#                 { 'OBJECT_STATUS_ENABLED': ObjectStatus.enabled,
#                   'account_id': account_id,
#                   'sync_time': sync_time })
#             devices = [ row.get_object({
#                     'activation_time': cast.string_to_timestamp,
#                     'fix_time': cast.string_to_timestamp,
#                     'keepalive_time': cast.string_to_timestamp,
#                     'picture_id': cast.string_to_uuid,
#                     'update_time': cast.string_to_timestamp })
#                 for row in cursor.fetch_all() ]
#
#             for device in [ d for d in devices if d.picture_id is not None ]:
#                 device.picture_url =  os.path.join(settings.CDN_URL_ROOT_PATH,
#                     self.CDN_BUCKET_NAME_DEVICE, str(device.picture_id))
#
#             return devices
#
#
#     def get_devices_ex(self, app_id, account_id,
#             limit=BaseRdbmsService.DEFAULT_LIMIT,
#             offset=0,
#             sync_time=None):
#         """
#         Return a list of devices that the specified user currently owns.
#
#
#         :param app_id: identification of the client application such as a Web,
#             a desktop, or a mobile application, that accesses the service.
#
#         :param account_id: identification of the account of the user to return
#             the list of devices he currently owns.
#
#         :param offset: require to skip that many records before beginning to
#             return records to the client.  Default value is `0`.  If both
#             `offset` and `limit` are specified, then `offset` records
#             are skipped before starting to count the limit records that are
#             returned.
#
#         :param limit: constrain the number of records that are returned to the
#             specified number.  Default value is `20`. Maximum value is
#             `100`.
#         :param sync_time: indicate the earliest non-inclusive time to filter
#             the devices of this user based on the update time of their
#             properties.  If not specified, no time as lower bounding filter is
#             applied, meaning that all the devices could possibly be returned.
#
#
#         :return: a list of instances containing the following members:
#
#             * `accuracy`: accuracy in meters of the last known location of
#               the device.
#
#             * `activation_time`: time when the user acquires this device.
#
#             * `altitude`: altitude in meters of the last known location of
#               the device.
#
#             * `battery_level`: current level in percentage of the battery of
#               the device.
#
#             * `bearing`: bearing in degrees.  Bearing is the horizontal
#               direction of travel of the device, and is not related to the
#               device orientation.  It is guaranteed to be in the range
#               `[0.0, 360.0]`, or `None` if the bearing of the device at
#               its last known location is not provided.
#
#             * `fix_time`: time when the device calculated the fix of the
#               last known location of the device.
#
#             * `fix_age`: difference, expressed in seconds, between the
#               time when the device calculated the location fix and the current
#               time on the platform.  This duration corresponds to the current
#               age of the location fix.
#
#             * `device_id`: International Mobile Equipment Identity (device_id) number
#               of a device.
#
#             * `is_battery_alarm_muted`: indicate whether the user muted the
#               alarm that was triggered when the battery has been unplugged or
#               when the level of the battery went down below a critical
#               threshold.
#
#             * `is_battery_plugged`: indicate if the battery of the device is
#               plugged in a power source.
#
#             * `is_device_alarm_muted`: indicate whether the user muted the
#               alarm that was triggered when the device is not responding
#               anymore.
#
#             * `is_security_alarm_muted`: indicate whether the user muted the
#               alarm system that was triggered when the device has detected a
#               movement or a location change while the security level is set to
#               `+security-level-active+`.
#
#             * `keepalive_time`: time of the last keep-alive (KA) message
#               sent by this device to the platform to check that the link
#               between the device and the platform is operating, and to notify
#               the  platform that the device is still in operation as expected.
#
#             * `latitude`: latitude-angular distance, expressed in decimal
#               degrees (WGS84 datum), measured from the center of the Earth, of
#               a point north or south of the Equator, of the last known
#               location of the device.
#
#             * `longitude`: longitude-angular distance, expressed in decimal
#               degrees (WGS84 datum), measured from the center of the Earth, of
#               a point east or west of the Prime Meridian, of the last known
#               location of the device.
#
#             * `name`: humanely readable name of the vehicle this device is
#               attached to.
#
#             * `picture_id`: identification of the graphical representation
#               of this device, or more likely by extension the vehicle where
#               this device is installed in, if any defined.
#
#             * `picture_url`: Uniform Resource Locator (URL) that specifies
#               the location of the graphical representation of the vehicle this
#               device is attached to, if any defined.  The client application
#               can use this URL and append the query parameter `size` to
#               specify a given pixel resolution of the device's picture:
#
#               * `thumbnail`
#
#               * `small`
#
#               * `medium`
#
#               * `large`
#
#             * `provider`: name of the location provider that reported the
#               geographical location.
#
#             * `security_level`: the current level of security of this device
#               (cf. `XeberusService.SecurityLevel`).
#
#             * `speed`: speed in meters/second over the ground, or `None`
#               if the speed of the device at its last known location is not
#               provided.
#
#             * `update_time`: time of the most recent modification of at
#               least one properties of this device, such as its security level,
#               its name, etc.  This time should be used as the cache time
#               reference for this device.
#         """
#         with self.acquire_rdbms_connection() as connection:
#             cursor = connection.execute("""
#                 SELECT device_id,
#                        name,
#                        picture_id,
#                        security_level,
#                        COALESCE(is_security_alarm_muted, false) AS is_security_alarm_muted,
#                        activation_time,
#                        keepalive_time,
#                        ST_X(location) AS longitude,
#                        ST_Y(location) AS latitude,
#                        ST_Z(location) AS altitude,
#                        accuracy,
#                        fix_time,
#                        EXTRACT(EPOCH FROM current_timestamp - fix_time) AS fix_age,
#                        speed,
#                        bearing,
#                        is_battery_plugged,
#                        battery_level,
#                        battery_plug_mode,
#                        COALESCE(is_battery_alarm_muted, false) AS is_battery_alarm_muted,
#                        COALESCE(is_device_alarm_muted, false) AS is_device_alarm_muted,
#                        object_status,
#                        update_time
#                   FROM xeberus_device
#                   WHERE ((account_id = %(account_id)s) OR
#                          (team_id IS NOT NULL AND team_is_member(%(account_id)s, team_id)))
#                     AND ((%(sync_time)s IS NOT NULL AND update_time > %(sync_time)s) OR
#                          (%(sync_time)s IS NULL AND object_status = %(OBJECT_STATUS_ENABLED)s))""",
#                 { 'OBJECT_STATUS_ENABLED': OBJECT_STATUS_ENABLED,
#                   'account_id': account_id,
#                   'sync_time': sync_time })
#
#             devices = [ row.get_object({
#                     'activation_time': cast.string_to_timestamp,
#                     'battery_plug_mode': BatteryPlugMode,
#                     'fix_time': cast.string_to_timestamp,
#                     'keepalive_time': cast.string_to_timestamp,
#                     'object_status': ObjectStatus,
#                     'picture_id': cast.string_to_uuid,
#                     'update_time': cast.string_to_timestamp })
#                 for row in cursor.fetch_all() ]
#
#
#             for device in devices:
#                 if device.longitude and device.latitude:
#                     device.location = GeoPoint(device.longitude, device.latitude,
#                              accuracy=device.accuracy,
#                              altitude=device.altitude,
#                              bearing=device.bearing,
#                              fix_time=device.fix_time,
#                              provider=device.provider,
#                              speed=device.speed)
#
#                     device.location.fix_age = device.fix_age
#
#                     del device.accuracy, \
#                         device.altitude, \
#                         device.bearing, \
#                         device.fix_age, \
#                         device.fix_time, \
#                         device.latitude, \
#                         device.longitude, \
#                         device.provider, \
#                         device.speed
#
#             for device in [ d for d in devices if d.picture_id is not None ]:
#                 device.picture_url =  os.path.join(settings.CDN_URL_ROOT_PATH,
#                     self.CDN_BUCKET_NAME_DEVICE, str(device.picture_id))
#
#             return devices
#
#
#     def get_device_locations(self, app_id, account_id, device_id, start_time, end_time,
#             limit=BaseRdbmsService.DEFAULT_LIMIT,
#             offset=0):
#         device = self.get_device(device_id, check_status=True)
#         if account_id != device.account_id \
#            and (device.team_id and not TeamService().is_member(account_id, device.team_id)):
#             raise self.IllegalAccessException(payload={ 'device_id': device_id })
#
#         with self.acquire_rdbms_connection(False) as connection:
#             cursor = connection.execute("""
#                 SELECT ST_X(location) AS longitude,
#                        ST_Y(location) AS latitude,
#                        accuracy,
#                        fix_time,
#                        speed,
#                        bearing
#                   FROM xeberus_location
#                   WHERE device_id = %(device_id)s
#                     AND provider = 'gps'
#                     AND fix_time >= %(start_time)s
#                     AND fix_time < %(end_time)s
#                   ORDER BY fix_time ASC
#                   LIMIT %(limit)s
#                   OFFSET %(offset)s""",
#                 { 'device_id': device_id,
#                   'end_time': end_time,
#                   'limit': min(self.MAXIMUM_DEVICE_LOCATION_LIMIT, limit),
#                   'offset': offset,
#                   'start_time': start_time })
#             return [ row.get_object({ 'fix_time': cast.string_to_timestamp })
#                     for row in cursor.fetch_all() ]
#
#
#     def get_devices_recent_locations(self, app_id, account_id, devices,
#             limit=BaseRdbmsService.DEFAULT_LIMIT,
#             fix_age=DEFAULT_FIX_AGE):
#         """
#         """
#         with self.acquire_rdbms_connection(False) as connection:
#             # Filter out device_ids that the user doesn't have access to.
#             cursor = connection.execute("""
#                 SELECT device_id
#                   FROM xeberus_device
#                   WHERE device_id IN (%[device_ids]s)
#                     AND object_status = %(OBJECT_STATUS_ENABLED)s
#                     AND (account_id = %(account_id)s OR team_is_member(%(account_id)s::uuid, team_id))""",
#                 { 'OBJECT_STATUS_ENABLED': OBJECT_STATUS_ENABLED,
#                   'account_id': account_id,
#                   'device_ids': devices.keys() })
#             if cursor.get_row_count() == 0:
#                 return []
#
#             device_ids = [ row.get_value('device_id') for row in cursor.fetch_all() ]
#
#             # Retrieve the locations of the specified devices corresponding to the
#             # given criteria.
#             cursor = connection.execute("""
#                 SELECT device_id,
#                        ST_X(location) AS longitude,
#                        ST_Y(location) AS latitude,
#                        ST_Z(location) AS altitude,
#                        accuracy,
#                        fix_time,
#                        EXTRACT(EPOCH FROM current_timestamp - fix_time) AS fix_age,
#                        speed,
#                        bearing
#                   FROM (
#                     SELECT device_id,
#                            location,
#                            accuracy,
#                            fix_time,
#                            speed,
#                            bearing,
#                            row_number() OVER (PARTITION BY device_id ORDER BY fix_time DESC) AS position
#                     FROM xeberus_location
#                     INNER JOIN (VALUES %[values]s) AS foo(device_id, recent_fix_time)
#                       USING (device_id)
#                     WHERE (foo.recent_fix_time IS NULL OR fix_time > foo.recent_fix_time::timestamptz(3))
#                       AND provider = 'gps'
#                       AND fix_time >= current_timestamp - %(fix_age)s::interval) AS foo
#                   WHERE position <= %(limit)s
#                   ORDER BY fix_time DESC""",
#                 { 'fix_age': '%d seconds' % min(fix_age, self.MAXIMUM_FIX_AGE),
#                   'limit': limit,
#                   'values': devices.items() })
#
#             devices_locations = collections.defaultdict(list)
#             for location in [ row.get_object({ 'fix_time': cast.string_to_timestamp })
#                     for row in cursor.fetch_all() ]:
#                 if len(devices_locations[location.device_id]) <= limit:
#                     devices_locations[location.device_id].append(location)
#                     del location.device_id
#
#             return [ Object(device_id=device_id, locations=locations)
#                     for (device_id, locations) in devices_locations.iteritems() ]
#
#
#     def get_device_notifications(self, app_id, device_id, seed,
#             start_time=None, end_time=None,
#             limit=BaseRdbmsService.DEFAULT_LIMIT, offset=0,
#             include_read=False, mark_read=True):
#         """
#         Return a list of notifications that have been sent to the specified
#         device.
#
#         :param app_id: identification of the client application such as a Web,
#             a desktop, or a mobile application, that accesses the service.
#
#         :param device_id: International Mobile Equipment Identity (device_id) of the
#             device on behalf of which notifications are requested.
#
#         :param seed: nonce encrypted with some identifications of the device
#             on behalf of which this function is called.
#
#         :param start_time: indicate the earliest time to return a
#             notification.  If not specified, the function returns all
#             available prior notifications.
#
#         :param end_time: indicate the latest time to return a notification.
#
#         :param limit: constrain the number of records that are returned to the
#             specified number.  Default value is `20`. Maximum value is
#             `100`.
#
#         :param offset: require to skip that many records before beginning to
#             return records to the client.  Default value is `0`.  If both
#             `offset` and `limit` are specified, then `offset` records
#             are skipped before starting to count the limit records that are
#             returned.
#
#         :param include_read: indicate whether to include notifications that
#             have already been read.  By default, notifications a device has
#             read are not included.
#
#         :param mark_read: indicate whether to mark read every notification
#             this functions returns.  By default, the function marks as read
#             notifications that are returned.
#
#         :return: a list of instances containing the following members:
#
#             * `notification_id` (required): identification of the
#               notification.
#
#             * `notification_type` (required): string representation of the
#               type of the notification, as defined by the client application
#               or the service that posted this notification to the user.
#
#             * `account_id` (optional): the identification of the account of
#               the user who initiates the notification.
#
#             * `payload` (optional): JSON string representation of additional
#               information specific to this particular notification.
#
#             * `is_unread` (required): indicate whether the notification has
#               been marked as read.
#
#             * `creation_time` (required): the time the notification was
#               originally sent.
#
#             * `update_time` (required): the time the notification was
#               originally sent, or the most recent time an attribute of the
#               notification, such as its read status, was updated.
#         """
#         account_id = self.verify_seed(device_id, seed)
#
#         with self.acquire_rdbms_connection(True) as connection:
#             if mark_read:
#                 cursor = connection.execute("""
#                     UPDATE xeberus_notification
#                       SET is_unread = false
#                       WHERE notification_id IN (
#                         SELECT notification_id
#                           FROM xeberus_notification
#                           WHERE device_id = %(device_id)s
#                             AND (%(start_time)s IS NULL OR creation_time > %(start_time)s)
#                             AND (%(end_time)s IS NULL OR creation_time < %(end_time)s)
#                             AND (%(include_read)s OR is_unread)
#                             AND object_status = %(OBJECT_STATUS_ENABLED)s
#                           ORDER BY creation_time ASC
#                           OFFSET %(offset)s
#                           LIMIT %(limit)s)
#                       RETURNING notification_id,
#                                 notification_type,
#                                 is_unread,
#                                 payload,
#                                 creation_time,
#                                 update_time""",
#                     { 'OBJECT_STATUS_ENABLED': OBJECT_STATUS_ENABLED,
#                       'end_time': end_time,
#                       'device_id': device_id,
#                       'include_read': include_read,
#                       'limit': min(limit, self.MAXIMUM_LIMIT),
#                       'offset': offset,
#                       'start_time': start_time })
#             else:
#                 cursor = connection.execute("""
#                     SELECT notification_id,
#                            notification_type,
#                            is_unread,
#                            payload,
#                            creation_time,
#                            update_time
#                       FROM xeberus_notification
#                       WHERE device_id = %(device_id)s
#                         AND (%(start_time)s IS NULL OR creation_time > %(start_time)s)
#                         AND (%(end_time)s IS NULL OR creation_time < %(end_time)s)
#                         AND (%(include_read)s OR is_unread)
#                         AND object_status = %(OBJECT_STATUS_ENABLED)s
#                       ORDER BY creation_time ASC
#                       OFFSET %(offset)s
#                       LIMIT %(limit)s""",
#                     { 'OBJECT_STATUS_ENABLED': OBJECT_STATUS_ENABLED,
#                       'end_time': end_time,
#                       'device_id': device_id,
#                       'include_read': include_read,
#                       'limit': min(limit, self.MAXIMUM_LIMIT),
#                       'offset': offset,
#                       'start_time': start_time })
#
#             notifications = [ row.get_object({
#                 'creation_time': cast.string_to_timestamp,
#                 'notification_id': cast.string_to_uuid,
#                 'payload': cast.string_to_json,
#                 'account_id': cast.string_to_uuid,
#                 'update_time': cast.string_to_timestamp
#             }) for row in cursor.fetch_all() ]
#
#             return notifications
#
#
#     def get_activation_requests(self, app_id, account_id,
#             limit=BaseRdbmsService.DEFAULT_LIMIT, offset=0):
#         """
#         Return up to 100 device activation requests that are still pending,
#         worth of extended information.
#
#         The application installed in a mobile tracker device MUST
#         automatically send a handshake to the platform every time
#         its starts running.
#
#         The first handshake ever of the device requests the platform to
#         activate the device.  Meanwhile, the device's activation is pending;
#         the device cannot access all the services supported by the platform
#         until its activation is fully completed and the device is enabled.
#
#         :param app_id: identification of the client application such as a Web,
#             a desktop, or a mobile application, that accesses the service.
#
#         :param account_id: identification of the account of the user on behalf
#             of whom the list of device activation request is retrieved.  This
#             user MUST be an administrator of the Xeberus team.
#
#         :param limit: constrain the number of device activation requests that
#             are returned to the specified number.  If not specified, the
#             default value is `20`.  The maximum value is `100`.
#
#         :param offset: require to skip that many device activation requests
#             before beginning to return device activation requests.  Default
#             value is `0`. If both `offset` and `limit` are specified,
#             then `offset` device activation requests are skipped before
#             starting to count the `limit` device activation requests that
#             are returned.
#
#         :return: a list of instances containing the following members:
#
#             * `accuracy` (optional): accuracy in meters of the last known
#               location of the device.
#
#             * `altitude` (optional): altitude in meters of the last known
#               location location of the device.
#
#             * `fix_time` (optional): time when the device has determined the
#               information of the fix of the last known location.
#
#             * `device_id` (required): International Mobile Equipment Identity
#               (device_id) that uniquely identifies the device.
#
#             * `imsi` (required): International Mobile Subscriber Identity
#               (IMSI) of the SIM card attached to the device.
#
#             * `latitude` (optional): latitude-angular distance, expressed in
#               decimal degrees (WGS84 datum), measured from the center of the
#               Earth, of a point north or south of the Equator corresponding to
#               the last known location of the device.
#
#             * `longitude` (optional): longitude-angular distance, expressed in
#               decimal degrees (WGS84 datum), measured from the center of the
#               Earth, of a point east or west of the Prime Meridian corresponding
#               to the last known location of the device.
#
#             * `provider` (optional): code name of the location provider that
#               reported the last known location of the device:
#
#               * `gps`: indicate that the location has been provided by a
#                 Global Positioning System (GPS).
#
#               * `network`: indicate that the location has been provided by
#                 an hybrid positioning system, which uses different positioning
#                 technologies, such as Global Positioning System (GPS), Wi-Fi
#                 hotspots, cell tower signals.
#
#             * `creation_time` (required): time when the device has been
#               registered.
#
#         :raise DeletedObjectException: if the user account has been deleted.
#
#         :raise DisabledObjectException: if the user account has been disabled.
#
#         :raise IllegalAccessException: if the authenticated user is not an
#             administrator of the platform.
#
#         :raise UndefinedObjectException: if the specified identification
#             doesn't refer to a user account registered against the platform.
#         """
#         account = AccountService().get_account(account_id, check_status=True)
#         if account.account_type not in [
#                     AccountService.AccountType.administrator,
#                     AccountService.AccountType.botnet] \
#            and not TeamService().is_member(account_id, XeberusService.XEBERUS_TEAM.team_id):
#             raise self.IllegalAccessException()
#
#         with self.acquire_rdbms_connection() as connection:
#             cursor = connection.execute("""
#                 SELECT device_id,
#                        imsi,
#                        ST_X(location) AS longitude,
#                        ST_Y(location) AS latitude,
#                        ST_Z(location) AS altitude,
#                        accuracy,
#                        fix_time,
#                        provider,
#                        xeberus_device.creation_time
#                   FROM xeberus_device
#                   INNER JOIN xeberus_sim
#                     USING (device_id)
#                   WHERE xeberus_device.object_status = %(OBJECT_STATUS_PENDING)s
#                     AND xeberus_sim.object_status = %(OBJECT_STATUS_ENABLED)s
#                   ORDER BY xeberus_device.creation_time ASC
#                   LIMIT %(limit)s
#                   OFFSET %(offset)s""",
#                 { 'OBJECT_STATUS_ENABLED': OBJECT_STATUS_ENABLED,
#                   'OBJECT_STATUS_PENDING': OBJECT_STATUS_PENDING,
#                   'limit': limit,
#                   'offset': offset })
#             return [ row.get_object({
#                             'fix_time': cast.string_to_timestamp,
#                             'creation_time': cast.string_to_timestamp })
#                 for row in cursor.fetch_all() ]
#
#
#
#
#     def on_error_raised(self, app_id, device_id, seed, reports):
#         # Check that all the error reports are tagged with the same device_id
#         # than the one specified.
#         if len([ report for report in reports if report.device_id and report.device_id != device_id ]) > 0:
#             raise self.InvalidArgumentException('Some reports are tagged with another device_id that the one specified')
#
#         account_id = self.verify_seed(device_id, seed)
#
#         with self.acquire_rdbms_connection(True) as connection:
#             connection.execute("""
#                 INSERT INTO xeberus_error(
#                                 report_id,
#                                 device_id,
#                                 error_time,
#                                 class_name,
#                                 message,
#                                 stack_trace)
#                   VALUES %[values]s
#                   RETURNING report_id""",
#                 { 'values': [
#                       (report.report_id,
#                        device_id,
#                        report.error_time,
#                        report.class_name,
#                        report.message,
#                        report.stack_trace)
#                     for report in reports ] })
#
#         return [ report.report_id for report in reports ]
#
#
#
#
#
#     def set_device_mileage(self, app_id, account_id, device_id, mileage):
#         """
#         Set the current mileage of the specified tracker device.
#
#         :note: only the owner of this tracker device, or an administrator of
#             his organization, or an administrator of the platform, is allowed
#             to change the mileage of this device.
#
#         :note: the mileage of the tracker device CANNOT be updated if the
#             device is moving.
#
#         :param app_id: identification of the client application such as a Web,
#             a desktop, or a mobile application, that accesses the service.
#
#         :param account_id: identification of the account of the user who
#             requests to change the mileage of the specified tracker's device.
#
#         :param device_id: identification of the tracker's device to set its
#             mileage.
#
#         :param mileage: new mileage to set for this tracker device as the
#             total distance travelled by the vehicle this tracker device is
#             mounted on.
#
#         :raise InvalidAccessException: if the authenticated user is not the
#             owner of this tracker device, nor an administrator of his
#             organization, nor an administrator of the platform.
#
#         :raise InvalidOperationException: if the vehicle, which the tracker
#             device is mounted on, is moving.
#
#         :raise `UndefinedObjectException`: if the specified identification
#             doesn't refer to any tracker device registered against the
#             platform.
#         """
#         device = self.get_device(device_id, check_status=True)
#
#         if account_id != device.account_id \
#            and (device.team_id and not TeamService().is_administrator(account_id, device.team_id)) \
#            and AccountService().get_account(account_id).account_type != AccountService.AccountType.administrator:
#             self.IllegalAccessException('This user is not allowed to update the mileage of the specified device')
#
#         if device.speed and device.speed > 0:
#             self.InvalidOperationException('The mileage of the device cannot be set while the vehicle is moving')
#
#         with self.acquire_rdbms_connection(True) as connection:
#             cursor = connection.execute("""
#                 UPDATE xeberus_device
#                   SET mileage = %(mileage)s,
#                       update_time = current_timestamp
#                   WHERE device_id = %(device_id)s
#                   RETURNING team_id""",
#                 { 'device_id': device_id,
#                   'mileage': mileage })
#             team_id = cursor.fetch_one().get_value('team_id', cast.string_to_uuid)
#
#         # NotificationService().send_notification(app_id,
#         #         XeberusService.XeberusNotification.on_device_properties_updated,
#         #         team_id=team_id,
#         #         payload={
#         #             'account_id': account_id,
#         #             'device_id': device_id,
#         #             'properties': {
#         #                 'mileage': mileage
#         #             }
#         #         },
#         #         sender_id=account_id)
#
#
#     def set_device_picture(self, app_id, account_id, device_id, uploaded_file):
#         """
#         Update the picture representing the specified device.
#
#         :param app_id: identification of the client application such as a Web,
#             a desktop, or a mobile application, that accesses the service.
#
#         :param account_id: identification of the account of the user on behalf
#             of whom the picture of the device is updated.  This account MUST
#             be the current owner of this device, or an administrator of the
#             platform.
#
#         :param device_id: the International Mobile Equipment Identity (device_id) number
#             of the device to update its picture.
#
#         :param uploaded_file: an instance `HttpRequest.HttpRequestUploadedFile`.
#
#         :return: an instance containing the following member.
#
#         :raise IllegalAccessException: if the account of the user on behalf
#             of whom this function is called is not allowed to update the
#             properties of this device, i.e., nor the owner of this device, nor
#             nor an administrator of the team this device belongs to, nor an
#             administrator of the platform.
#
#         :raise UndefinedObjectException: if the specified International Mobile
#             Equipment Identity (device_id) doesn't refer to a device registered
#             against the platform.
#         """
#         device = self.get_device(device_id, check_status=True)
#
#         if account_id != device.account_id \
#            and (device.team_id and not TeamService().is_member(account_id, device.team_id)) \
#            and AccountService().get_account(account_id).account_type != AccountService.AccountType.administrator:
#             self.IllegalAccessException('This user is not allowed to update the properties of the specified device')
#
#         # Determine the MD5 signature and the size of the data of the uploaded
#         # picture, and check whether this picture is not already defined for
#         # this device, in which case ignore the current request.
#         file_checksum = hashlib.md5(uploaded_file.data).hexdigest()
#         file_size = len(uploaded_file.data)
#
#         if device.picture_id and \
#            device.picture_file_size == uploaded_file_size and \
#            device.picture_file_checksum == uploaded_file_checksum:
#             return device.picture_id
#
#         # Check whether this picture has been already defined for another
#         # device, in which case simply reuse this picture.
#         with self.acquire_rdbms_connection(True) as connection:
#             cursor = connection.execute("""
#                 SELECT picture_id
#                   FROM xeberus_device
#                   WHERE picture_file_checksum = %(file_checksum)s
#                     AND picture_file_size = %(file_size)s""",
#                 { 'file_checksum': file_checksum,
#                   'file_size': file_size })
#             row = cursor.fetch_one()
#             if row is not None:
#                 picture_id = row.get_value('picture_id', cast.string_to_uuid)
#
#             else:
#                 # Generate the multiple pixel resolutions of the uploaded image, and
#                 # store them in the Network File System (NFS) of the platform's
#                 # Content Delivery Network (CDN).
#                 (_, picture_id) = cdn_util.store_image_multiple_pixel_resolutions(uploaded_file.data,
#                     settings.IMAGE_PIXEL_RESOLUTIONS['device'],
#                     settings.CDN_NFS_ROOT_PATH, self.CDN_BUCKET_NAME_DEVICE,
#                     filter=image_util.Filter.AntiAlias,
#                     image_format='JPEG',
#                     must_be_squared=True)
#
#                 # If a picture was already associated to this device, determine
#                 # whether another device also references this previous picture, and if
#                 # not garbage collect this picture, including all the multiple pixel
#                 # resolution files.
#                 if device.picture_id:
#                     cursor = connection.execute("""
#                         SELECT COUNT(*) AS reference_count
#                           FROM xeberus_device
#                           WHERE picture_id = %(picture_id)s""",
#                         { 'picture_id': device.picture_id })
#                     if cursor.fetch_one().get_value('reference_count') <= 1:
#                         for file_path_name in glob.glob(os.path.join(settings.CDN_NFS_ROOT_PATH, self.CDN_BUCKET_NAME_DEVICE,
#                                 file_util.build_tree_pathname(str(device.picture_id)),
#                                 '%s*' % device.picture_id)):
#                             os.remove(file_path_name)
#
#             # Associate the picture to the device.
#             connection.execute("""
#                 UPDATE xeberus_device
#                   SET picture_id = %(picture_id)s,
#                       update_time = current_timestamp
#                   WHERE device_id = %(device_id)s""",
#                 { 'device_id': device_id,
#                   'picture_id': picture_id })
#
#         device = Object()
#         device.picture_id = picture_id
#         device.picture_url = os.path.join(settings.CDN_URL_ROOT_PATH,
#             self.CDN_BUCKET_NAME_DEVICE, str(picture_id))
#
#         return device
#
#
#
#
#     def update_device_settings(self, app_id, account_id, device_id,
#             is_battery_alarm_muted=None,
#             is_device_alarm_muted=None,
#             is_security_alarm_muted=None,
#             security_level=None):
#         """
#         Update one or more properties of the specified device on behalf of the
#         user that currently owns this device.
#
#         :param app_id: identification of the client application such as a Web,
#             a desktop, or a mobile application, that accesses the service.
#         :param account_id: identification of the account of the user on behalf
#             of whom the properties of the device are updated.  This account
#             MUST be the current owner of this device, or an administrator of
#             the platform.
#         :param device_id: the International Mobile Equipment Identity (device_id) number
#             of the device to update its properties.
#         :param is_battery_alarm_muted: indicate whether the user muted the
#             alarm that was triggered when the battery has been unplugged or
#             when the level of the battery went down below a critical
#             threshold.
#         :param is_device_alarm_muted: indicate whether the user muted the
#             alarm that alerts the user whenever the device is not
#             responding.
#         :param is_security_alarm_muted: indicate whether the user muted the
#             alarm that was triggered when the device is not responding
#             anymore.
#         :param security_level: indicate the current level of security of this
#             device:
#             * `XeberusService.SECURITY_LEVEL_ACTIVE`: indicate that the
#               alarm system of the device is active, which is an alarm that the
#               user manually arms when he leaves his vehicle.  The user will
#               be urgently alerted of any movement of his vehicle.
#             * `XeberusService.SECURITY_LEVEL_PASSIVE`: indicate that the
#               alarm system of the device is passive, which is an alarm that
#               doesn't need to be manually armed when the user leaves his
#               vehicle.  Instead, the alarm  is automatically activated when
#               the vehicle doesn't move anymore after a few seconds.  The user
#               will be gently notified of any movement of his vehicle.
#
#         :return: an instance containing the following members, but only if
#             the properties of the device have been updated, :
#             * `device_id`: the International Mobile Equipment Identity (device_id)
#               number of the device which one or more properties have been
#               updated.
#             * `update_time`: time of the most recent change of one or more
#               properties of this device.
#
#         :raise UndefinedObjectException: if the specified International Mobile
#                Equipment Identity (device_id) number doesn't correspond to any
#                device registered against the platform.
#         """
#         device = self.get_device(device_id, check_status=True)
#
#         # Check whether at least one property has been specified for update,
#         # or simply return.
#         properties = {
#             'is_battery_alarm_muted': is_battery_alarm_muted,
#             'is_device_alarm_muted': is_device_alarm_muted,
#             'is_security_alarm_muted': is_security_alarm_muted,
#             'security_level': security_level
#         }
#
#         new_values = dict([ (name, value) for (name, value) in properties.iteritems()
#                 if value is not None ])
#         if len(new_values) == 0:
#             return
#
#         with self.acquire_rdbms_connection(True) as connection:
#             # Check whether at least one property has been modified.
#             cursor = connection.execute("""
#                 SELECT """ + ','.join(new_values.iterkeys()) + """
#                   FROM xeberus_device
#                   WHERE device_id = %(device_id)s""",
#                 { 'device_id': device_id })
#             old_values = cursor.fetch_one().get_object()
#             updated_values = dict([ (name, value) for (name, value) in new_values.iteritems()
#                     if getattr(old_values, name) != value ])
#             if len(updated_values) == 0:
#                 return
#
#             # Update the properties that have been modified.
#             update_set_statement = [ "%s = %%(%s)s" % (name, name)
#                 for (name, value) in updated_values.iteritems() ]
#
#             updated_values['device_id'] = device_id
#
#             cursor = connection.execute("""
#                 UPDATE xeberus_device
#                   SET """ + ','.join(update_set_statement) + """,
#                       update_time = current_timestamp
#                   WHERE device_id = %(device_id)s
#                   RETURNING device_id,
#                             update_time""",
#                 updated_values)
#
#             return cursor.fetch_one().get_object({ 'update_time': cast.string_to_timestamp })
