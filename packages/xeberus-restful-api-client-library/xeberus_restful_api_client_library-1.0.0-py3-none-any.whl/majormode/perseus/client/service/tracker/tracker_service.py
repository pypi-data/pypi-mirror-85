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

from majormode.perseus.constant.sort_order import SortOrder
from majormode.perseus.client.service.base_service import BaseService
from majormode.perseus.client.service.account.account_service import AccountService
from majormode.perseus.model.locale import DEFAULT_LOCALE
from majormode.perseus.model.obj import Object


class XeberusService(BaseService):
    """
    Proxy class that surfaces the methods that the Xeberus RESTful API
    supports.
    """

    # Default fix age of a location to be considered as a recent location
    # of a vehicle.
    DEFAULT_FIX_AGE = 2 * 60

    # Default number of venues to return in one single call.
    DEFAULT_VENUE_LIMIT = 20,

    BaseService._declare_custom_exceptions({
        'AuthenticationFailureException': AccountService.AuthenticationFailureException,
    })


    def __init__(self, connection):
        super(XeberusService, self).__init__(connection)


    def activate_account(self, fullname, password, phone_number):
        """
        Activate the account of the user by providing his fullname, his 
        password, and his mobile phone number.

        
        @param fullname: complete full name of the user.

        @param password: password of the user account.
 
        @param phone_number: phone number of the user provided in E.164
            numbering plan, an ITU-T recommendation which defines the
            international public telecommunication numbering plan used in the
            Public Switched Telephone Network (PSTN).
        """
        return Object.from_json(
                self.send_request(
                        http_method=self.HttpMethod.POST,
                        path='/account/activation',
                        message_body={
                            'fullname': fullname,
                            'password': password,
                            'phone_number': phone_number
                        },
                        authentication_required=True,
                        signature_required=True))


    def confirm_contact(self, verification_code):
        """
        Validate a contact information that a user has been requested to
        confirm through a challenge/response verification process.


        @param verification_code: a "number used once", a pseudo-random number
               issued when requesting the user to confirm his contact
               information.


        @return: a session instance containing the following members:

            * ``account_id`` (required): identification of the account of the
              user.

            * ``expiration_time`` (required): time when the login session will
              expire.

            * ``fullname`` (required): complete full name of the user as given by
                the user himself, i.e., untrusted information, or as determined
                from his email address as for a ghost account.

            * ``session_id`` (required): identification of the login session of the
                user.
        """
        return Object.from_json(
                self.send_request(
                        http_method=self.HttpMethod.POST,
                        path='/account/contact/confirmation/(verification_code)',
                        url_bits={
                            'verification_code': verification_code
                        },
                        authentication_required=False,
                        signature_required=True))


    def sign_in(self, email_address, password):
        """
        Sign-in the user against the platform providing his email address and
        his password.


        @param email_address: email address of the user.

        @param password: password of the user.


        @return: a session instance containing the following members:

            * ``account_id`` (required): identification of the account of the
              user.

            * ``contacts`` (required): a list of contact information that can be
              used as primary contact information for this user account.  A
              contact information corresponds to the following tuples::

                   ``(name, value, is_verified)``

                where:

                * ``name``: an item of the enumeration ``ContactPropertyName``.

                * ``value``: value of the property representing by a string.

                * ``is_verified``: indicate whether this contact information has been
                  verified.

            * ``expiration_time``: time when the login session will expire.

            * ``fullname``: complete full name of the user as given by the user
              himself, i.e., untrusted information, or as determined from his
              email address as for a ghost account.

            * ``session_id``: identification of the login session of the user.
        """
        payload = Object.from_json(
                self.send_request(
                        http_method=self.HttpMethod.POST,
                        path='/account/session',
                        message_body={
                            'email_address': email_address,
                            'password': password
                        },
                        authentication_required=False,
                        signature_required=True))

        self.set_session(self.session.connection.build_authenticated_session(payload))

        return self.session


    def sign_up(self, email_address, locale, client_ip_adress):
        session_payload = Object.from_json(
                self.send_request(
                        http_method=self.HttpMethod.POST,
                        path='/account',
                        message_body={
                            'client_ip_address': client_ip_adress,
                            'email_address': email_address,
                            'locale': locale
                        },
                        authentication_required=False,
                        signature_required=True))

        self.set_session(self.session.connection.build_authenticated_session(session_payload))

        return session_payload









    def confirm_suggested_venue(self, venue_id):
        """
        Confirm on behalf of a user that a new venue has been wisely suggested
        by the platform.

        This venue will be then monitored by the platform.  When a vehicle of
        the user and his organisation enters or exits this venue, the platform
        will send a notification to this user and any member of his
        organisation.


        @param venue_id: identification of the venue that the user confirms as
            a valid venue.


        @raise DeletedObjectException: if the venue has been deleted.

        @raise DisabledObjectException: if the venue has been disabled.

        @raise IllegalAccessException: if the account on behalf of whom this
            venue is confirmed is not the account who or a member of the
            organisation that registered this venue.

        @raise UndefinedObjectException: if the specified identification
            doesn't correspond to a venue registered on behalf of this account
            or one of the organisations this user belongs to.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.POST,
                path='/venue/(venue_id)/confirmation',
                url_bits={
                    'venue_id': venue_id
                },
                authentication_required=True,
                signature_required=True))


    def delete_venue(self, venue_id):
        """
        Soft delete the specified venue to prevent the platform to trigger
        events that would occur at the same location of this venue.  The
        venue is then removed from the list of venues that the platform is
        actively monitoring.

        A soft delete also prevents the platform from detecting this location,
        based on future stopovers of vehicles, as a possible new venue to be
        suggested to the organisation that manages these vehicles.


        @param venue_id: identification of the venue to ignore.


        @raise DeletedObjectException: if the venue has been deleted.

        @raise DisabledObjectException: if the venue has been disabled.

        @raise IllegalAccessException: if the account on behalf of whom this
            venue is ignored is not the account who or an administrator of the
            organisation that registered this venue.

        @raise UndefinedObjectException: if the specified identification
            doesn't correspond to a venue registered on behalf of this account
            or one of the organisations this user belongs to.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.DELETE,
                path='/venue/(venue_id)',
                url_bits={
                    'venue_id': venue_id
                },
                authentication_required=True,
                signature_required=True))


    def get_device_locations(self, device_id, start_time, end_time,
            limit=BaseService.DEFAULT_RESULT_SET_SIZE,
            offset=0):
        """
Return a list of geographical locations of the specified device for
the given time period.


@param device_id: identification of the device.

@param start_time: indicate the earliest time to return locations of
    this device.

@param end_time: indicate the latest time to return locations of this
    device.

@param limit:  constrain the number of records that are returned to
    the specified number.

@param offset: require to skip that many records before beginning to
    return records to the client.  If both ``offset`` and ``limit``
    are specified, then ``offset`` records are skipped before starting
    to count the limit records that are returned.


@return:
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/device/(device_id)/location',
                url_bits={
                    'device_id': device_id
                },
                arguments={
                    'end_time': end_time,
                    'limit': limit,
                    'offset': offset,
                    'start_time': start_time
                },
                authentication_required=True,
                signature_required=True))


    def get_device_registrations(self,
            limit=BaseService.DEFAULT_RESULT_SET_SIZE,
            offset=0):
        """
        Return up to 100 device registrations that are still pending, worth of
        extended information.

        The application installed in a mobile tracker device MUST
        automatically send a request registration of the device every time
        its starts running.

        The first registration ever of the device requires an administrator of
        the platform to complete the registration.  Meanwhile, the device's
        registration is pending; the device cannot access all the services
        supported by the platform until the registration is fully completed
        and the device is enabled.

        The authenticated user MUST be an administrator of the platform,
        otherwise the exception ``IllegalAccessException`` is raised.


        @param limit: constrain the number of device registrations that are
            returned to the specified number.  If not specified, the default
            value is ``20``.  The maximum value is ``100``.

        @param offset: require to skip that many device registrations before
            beginning to return device registrations.  Default value is ``0``.
            If both ``offset`` and ``limit`` are specified, then ``offset``
            device registrations are skipped before starting to count the
            ``limit`` device registrations that are returned.


        @return: a list of instances containing the following members:

            * ``accuracy`` (optional): accuracy in meters of the last known
              location of the device.

            * ``altitude`` (optional): altitude in meters of the last known
              location location of the device.

            * ``fix_time`` (optional): time when the device has determined the
              information of the fix of the last known location.

            * ``imei`` (required): International Mobile Equipment Identity
              (IMEI) that uniquely identifies the device.

            * ``latitude`` (optional): latitude-angular distance, expressed in
              decimal degrees (WGS84 datum), measured from the center of the
              Earth, of a point north or south of the Equator corresponding to
              the last known location of the device.

            * ``longitude`` (optional): longitude-angular distance, expressed in
              decimal degrees (WGS84 datum), measured from the center of the
              Earth, of a point east or west of the Prime Meridian corresponding
              to the last known location of the device.

            * ``provider`` (optional): code name of the location provider that
              reported the last known location of the device:

              * ``gps``: indicate that the location has been provided by a
                Global Positioning System (GPS).

              * ``network``: indicate that the location has been provided by
                an hybrid positioning system, which uses different positioning
                technologies, such as Global Positioning System (GPS), Wi-Fi
                hotspots, cell tower signals.

            * ``registration_time`` (required): time when the device has been
              registered.

        @raise DeletedObjectException: if the user account has been deleted.

        @raise DisabledObjectException: if the user account has been disabled.

        @raise IllegalAccessException: if the authenticated user is not an
            administrator of the platform.

        @raise UndefinedObjectException: if the specified identification
            doesn't refer to a user account registered against the platform.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/device/registration',
                arguments={
                    'limit': limit,
                    'offset': offset,
                },
                authentication_required=True,
                signature_required=True))


    def get_devices(self,
            sync_time=None,
            limit=BaseService.DEFAULT_RESULT_SET_SIZE, offset=0):
        """
        Return a list of devices that the authenticated user currently owns.


        @param app_id: identification of the client application such as a Web,
            a desktop, or a mobile application, that accesses the service.

        @param account_id: identification of the account of the user to return
            the list of devices he currently owns.

        @param sync_time: indicate the earliest non-inclusive time to filter
            the devices of this user based on the update time of their
            properties.  If not specified, no time as lower bounding filter is
            applied, meaning that all the devices could possibly be returned.

        @param limit: constrain the number of records that are returned to the
            specified number.  Default value is ``20``. Maximum value is
            ``100``.

        @param offset: require to skip that many records before beginning to
            return records to the client.  Default value is ``0``.  If both
            ``offset`` and ``limit`` are specified, then ``offset`` records
            are skipped before starting to count the limit records that are
            returned.


        @return: a list of instances containing the following members:

            * ``accuracy``: accuracy in meters of the last known location of
              the device.

            * ``acquire_time``: time when the user acquires this device.

            * ``altitude``: altitude in meters of the last known location of
              the device.

            * ``battery_level``: current level in percentage of the battery of
              the device.

            * ``bearing``: bearing in degrees.  Bearing is the horizontal
              direction of travel of the device, and is not related to the
              device orientation.  It is guaranteed to be in the range
              ``[0.0, 360.0]``, or ``None`` if the bearing of the device at
              its last known location is not provided.

            * ``fix_time``: time when the device calculated the fix of the
              last known location of the device.

            * ``imei``: International Mobile Equipment Identity (IMEI) number
              of a device.

            * ``is_battery_alarm_muted``: indicate whether the user muted the
              alarm that was triggered when the battery has been unplugged or
              when the level of the battery went down below a critical
              threshold.

            * ``is_battery_plugged``: indicate if the battery of the device is
              plugged in a power source.

            * ``is_device_alarm_muted``: indicate whether the user muted the
              alarm that was triggered when the device is not responding
              anymore.

            * ``is_security_alarm_muted``: indicate whether the user muted the
              alarm system that was triggered when the device has detected a
              movement or a location change while the security level is set to
              ``+security-level-active+``.

            * ``keepalive_time``: time of the last keep-alive (KA) message
              sent by this device to the platform to check that the link
              between the device and the platform is operating, and to notify
              the  platform that the device is still in operation as expected.

            * ``latitude``: latitude-angular distance, expressed in decimal
              degrees (WGS84 datum), measured from the center of the Earth, of
              a point north or south of the Equator, of the last known
              location of the device.

            * ``longitude``: longitude-angular distance, expressed in decimal
              degrees (WGS84 datum), measured from the center of the Earth, of
              a point east or west of the Prime Meridian, of the last known
              location of the device.

            * ``name``: humanely readable name of the vehicle this device is
              attached to.

            * ``picture_id``: identification of the graphical representation
              of this device, or more likely by extension the vehicle where
              this device is installed in, if any defined.

            * ``picture_url``: Uniform Resource Locator (URL) that specifies
              the location of the graphical representation of the vehicle this
              device is attached to, if any defined.  The client application
              can use this URL and append the query parameter ``size`` to
              specify a given pixel resolution of the device's picture:

              * ``thumbnail``

              * ``small``

              * ``medium``

              * ``large``

            * ``provider``: name of the location provider that reported the
              geographical location.

            * ``security_level``: the current level of security of this device
              (cf. ``XeberusService.SecurityLevel``).

            * ``speed``: speed in meters/second over the ground, or ``None``
              if the speed of the device at its last known location is not
              provided.

            * ``update_time``: time of the most recent modification of at
              least one properties of this device, such as its security level,
              its name, etc.  This time should be used as the cache time
              reference for this device.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/device',
                arguments={
                    'limit': limit,
                    'offset': offset,
                    'sync_time': sync_time
                },
                authentication_required=True,
                signature_required=True))


    def get_devices_recent_locations(self, devices,
            limit=BaseService.DEFAULT_RESULT_SET_SIZE,
            fix_age=DEFAULT_FIX_AGE):
        """
        Return a list of recent geographical locations of the specified
        devices.


        @param devices: a dictionary of devices specification, where the key
            corresponds to the International Mobile Equipment Identity (IMEI)
            of a device, and the value a possible timestamp that indicates the
            earliest time to return locations of this device, based on their
            time of fix.  If the specified timestamp is ``None``, the platform
            returns any available prior recent locations of this device,
            sorted by ascending order.

        @param limit: constrain the number of locations that are returned per
            device to the specified number.  Maximum value is ``100``.  The
            default value is ``20``.

        @param fix_age: maximal age in seconds of the location fixes to be
            returned.


        @return: a list of instance containing the following members:

            * ``imei`` (required): International Mobile Equipment Identity
              (IMEI) of a device.

            * ``locations`` (required): a list of geographical locations of
              the device sorted with the requested order.  Each location
              contains the following attributes:

              * ``accuracy`` (required): accuracy in meters of the device's
                location.

              * ``altitude`` (required): altitude in meters of the device's
                location.

              * ``bearing`` (optional): bearing in degrees.  Bearing is the
                horizontal direction of travel of the device, and is not
                related to the device orientation.  It is guaranteed to be in
                the range ``[0.0, 360.0]``, or it is not provided if this
                location does not have a bearing.

              * ``fix_time`` (required): time when the device determined the
                information of this fix.

              * ``latitude`` (required): latitude-angular distance, expressed
                in decimal degrees (WGS84 datum), measured from the center of
                the Earth, of a point north or south of the Equator
                corresponding to the location.

              * ``longitude`` (required): longitude-angular distance,
                expressed in decimal degrees (WGS84 datum), measured from the
                center of the Earth, of a point east or west of the Prime
                Meridian corresponding to the location.

              * ``provider`` (required): code name of the location provider
                that reported the geographical location.

                * ``gps``: indicate that the location has been provided by a
                  Global Positioning System (GPS).

                * ``network``: indicate that the location has been provided
                  by an hybrid positioning system, which uses different
                  positioning technologies, such as Global Positioning System
                  (GPS), Wi-Fi hotspots, cell tower signals.

              * ``speed`` (optional): speed in meters/second over the ground,
                or it is not provided if this location does not have a speed.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/device/location/recent',
                arguments={
                    'devices': [ '%s@%s' % (imei, fix_time if fix_time else '')
                            for (imei, fix_time) in devices.iteritems() ],
                    'limit': limit,
                    'fix_age': fix_age
                },
                authentication_required=True,
                signature_required=True))


    def get_vehicle_models(self, app_id,
            make=None,
            year=None,
            sync_time=None):
        """
        Return the list of vehicle models currently supported by the platform.


        @param app_id: identification of the client application such as a Web,
            a desktop, or a mobile application, that accesses the service.

        @param make: the name of a particular manufacturer that builds
            vehicles.

        @param year: describe approximately when vehicles were built, and
            usually indicates the coinciding base specification (design
            revision number) of vehicles.  This is done for the simple reason
            of making the vehicles more easily distinguished.

        @param sync_time: indicate the time of the last version of the list of
            vehicle models cached by the client application. If this time
            corresponds to the most recent version of the list of vehicle models
            registered, the platform returns an empty list, otherwise the
            platform returns the most recent version of the list of vehicle
            models. If this parameter is not provided, the platform always
            returns the most recent version of the list of vehicle models.


        @return: an instance containing the following attributes:

            * ``models`` (required): a list of instances containing the
               following attributes.

              * ``make``: name of the manufacturer that built this vehicle
                model.

              * ``model`` (required): commercial name of the model of this
                vehicle.

              * ``model_id`` (required): identification of this particular
                vehicle model.

              * ``year`` (optional): describe approximately when this vehicle
                model was built.

            * ``update_time`` (required):  time of the most recent
              modification of one or more vehicle models of this list.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/vehicle/model',
                arguments={
                    'make': make,
                    'sync_time': sync_time,
                    'year': year,
                },
                authentication_required=False,
                signature_required=True))


    def get_venues(self,
            include_address=False,
            include_contacts=False,
            include_stopovers=False,
            statuses=None,
            limit=DEFAULT_VENUE_LIMIT,
            locale=DEFAULT_LOCALE,
            sync_time=None,
            team_id=None):
        """
        Return a list of venues that have been registered by the user on
        behalf this request is sent, or by the organization(s) this user
        belongs to.

        The platform can also include not yet defined venues that the platform
        has detected based on stop-overs of the vehicle(s) that this user, or
        the organization(s) he belongs to, has registered.


        @param include_address: indicate whether to include address
            information of the venues returned.  By default, address
            information is not included.

        @param include_contacts: indicate whether to include contact
            information of the venues returned.  By default, contact
            information is not included.

        @param include_stopovers: indicate whether to include brief stays in
            the course of a journey of vehicles.  Stop-overs are determined
            from the locations reported by tracker devices mounted on
            vehicles.  A background job filters all those locations to, and
            groups them into centroid-based clusters such that the squared
            distances from the cluster are minimized.  By default, stop-overs
            are not included.

        @param statuses: indicate the statuses of the venues to return.

        @param limit: constrain the number of venues that are returned to the
            specified number.  Maximum value is ``100``. The default value is
            ``20``.

        @param locale: an instance ``Locale`` denoting the locale to use for
            any textual information that is returned.  If no locale is
            specified, the function returns textual information in all the
            available translated versions.  If there is textual information
            not available in the specified locale, the function returns all
            the translated versions of this particular textual information.

        @param sync_time: indicate the earliest time to return venues based on
            the time of their most recent modification.  If not specified, the
            function returns any available venues, sorted by ascending order
            of their modification time.

        @param team_id: the identification of an organization the
            authenticated user belongs to.  If defined, the function returns
            the venues registered by any member who belongs to this
            organization.


        @return: a list of instances that contains the following members:

            * ``address`` (optional): postal address of the venue, composed of
              one or more address components, which textual information is
              written in the specified locale.  An address component is defined
              with a component type and its value.  The component type of an
              address is an instance ``AddressComponentType``.

            * ``category`` (optional): code name of category qualifying this
              venue.

            * ``contacts`` (optional): list of properties such as e-mail
              addresses, phone numbers, etc., in respect of the electronic
              business card specification (vCard).  The contact information is
              a list of instances containing the following members:

              * ``name``: type of this contact information, which can be one
                of these standard names in respect of the electronic business
                card specification (vCard):

              * ``value``: value of this contact information representing by a
                string, such as ``+84.01272170781``, the formatted value for a
                telephone number property.

              * ``is_primary``: indicate whether this contact information is
                the primary for this venue.

               * ``is_verified``: indicate whether this contact information
                 has been verified, whether it has been grabbed from a trusted
                 Social Networking Service (SNS), or whether through a
                 challenge/response process.

            * ``is_business_related`` (optional): indicate whether this venue
              is connected to the business of the user or his organization.

            * ``location`` (required): an instance ``GeoPoint`` corresponding
              to geographical coordinates of the venue's location.

            * ``object_status`` (required): current status of this venue.

              * ``OBJECT_STATUS_ENABLED``: this venue has already been
                identified as a venue by the user or a member of his
                organization.

              * ``OBJECT_STATUS_DISABLED``: this venue has already been
                disabled by the user or a member of his organization, as this
                location is not of interest.  The platform doesn't delete this
                record to remind that this venue should not be suggested to
                the user and his organization anymore.

              * ``OBJECT_STATUS_PENDING``: this venue has been suggested to the
                user, but not yet reviewed by him, nor by any member of his
                organization.

            * ``creation_time`` (required): time when this venue has been
              registered to the platform.

            * ``update_time`` (required): time of the last modification of one
              or more attributes of this venue.

            * ``venue_id`` (required): identification of the venue.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/venue',
                arguments={
                    'include_address': include_address,
                    'include_contacts': include_contacts,
                    'include_stopevers': include_stopovers,
                    'limit': limit,
                    'locale': locale,
                    'statuses': statuses,
                    'sync_time': sync_time,
                    'team_id': team_id
                },
                authentication_required=True,
                signature_required=True))


    def _register_prospect_vehicle_model(self, app_id, email_address,
            model_id=None,
            make=None,
            model=None):
        """
        Register the email address of a prospect who signed-up online to the
        Explorer Program and save the vehicle model of this prospect.

        The Explorer Program is designed for people who want to get involved
        early and help shape the future of the service.  This program is
        expanding little by little, and experimenting with different ways of
        bringing new Explorers into the program.

        If a prospect is a Vietnam resident and is interested in joining, he
        can sign up here and the administrators of the online service let him
        know if a spot opens up.


        @note: this function will be deprecated as soon as the service will be
            fully opened to all the users.

        @note: either ``model_id`` needs to be provided, either ``make`` and
            optionally ``model`` needs to be provided.


        @param app_id: identification of the client application such as a Web,
            a desktop, or a mobile application, that accesses the service.

        @param email_address: email address of the prospect.

        @param model_id: identification of the prospect's vehicle as
            registered on the platform.

        @param make: name of a manufacturer that builds vehicles.

        @param model: commercial name of the model of the prospect's vehicle.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.POST,
                path='/prospect/vehicle/registration',
                message_body={
                    'email_address': email_address,
                    'make': make,
                    'model': model,
                    'model_id': model_id
                },
                authentication_required=False,
                signature_required=True))
