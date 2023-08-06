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

from majormode.perseus.model import wap


class WapService(BaseService):
    def __init__(self, connection):
        super(WapService, self).__init__(connection)

    def delete_wap_configuration(self, bssid,
            team_id=None):
        """
        Forget the security configuration of a Wireless Access Points (WAP)
        that has been shared with the devices of the authenticated user, and
        possibly those of the specified organisation this user belongs to.


        @param bssid: Basic Service Set Identifier (BSSID) that uniquely
            identifies the Wi-Fi network to forget its settings.

        @param team_id: identification of the organisation on behalf of the
            settings of this Wi-Fi network were saved and need to be forgotten.


        @raise IllegalAccessException: if the user on behalf of whom the
            function is called is not a member of the specified organisation.

        @raise UndefinedObjectException: if the specified team doesn't not
            exist, or if the settings of this Wireless Access Point have not
            been saved on behalf of the user or the specified organisation.
        """
        return Object.from_json(
                self.send_request(
                        http_method=self.HttpMethod.DELETE,
                        path='/wap/(bssid)',
                        url_bits={
                            'bssid': bssid
                        },
                        arguments={
                            'team_id': team_id
                        },
                        authentication_required=True,
                        signature_required=True))


    def set_wap_configuration(self, bssid,
            is_public=False,
            preshared_key=None,
            team_id=None):
        """
        Save the security configuration of Wireless Access Point (WAP) that
        will be shared with the devices of the authenticated user, and
        possibly those of the specified organisation this user belongs to.


        @param bssid: Basic Service Set Identifier (BSSID) that uniquely
            identifies the Wi-Fi network to save its security configuration.

        @param is_public: indicate whether this Wi-Fi network publicly shared
            or not.

        @param preshared_key: Passphrase/password to connect to the Wireless
            Access Point.  A pre-shared key (PSK) is a shared secret which was
            previously shared between the two parties using some secure
            channel before it needs to be used.

        @param team_id: identification of the organisation on behalf of the
            security configuration of this Wi-Fi network is saved.


        @raise IllegalAccessException: if the user is not an administrator of
            the specified organisation.

        @raise InvalidOperationException: if the specified Wireless Access
            Point has never been scanned by any device of the user or his
            organisation.
        """
        return Object.from_json(
                self.send_request(
                        http_method=self.HttpMethod.PUT,
                        path='/wap/(bssid)',
                        url_bits={
                            'bssid': bssid
                        },
                        message_body={
                            'is_public': is_public,
                            'preshared_key': preshared_key,
                            'team_id': team_id
                        },
                        authentication_required=True,
                        signature_required=True))
