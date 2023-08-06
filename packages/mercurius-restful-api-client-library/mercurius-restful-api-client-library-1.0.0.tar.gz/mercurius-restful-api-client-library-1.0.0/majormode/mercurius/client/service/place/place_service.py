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
from majormode.perseus.model.locale import DEFAULT_LOCALE


class PlaceService(BaseService):
    BaseService._declare_custom_exceptions({
    })

    # def get_place(
    #         self, place_id,
    #         check_status=True,
    #         include_address=False,
    #         include_contacts=False):
    #     return Object.from_json(
    #         self.send_request(
    #             http_method=self.HttpMethod.GET,
    #             path='/place/(place_id)',
    #             url_bits={'place_id': place_id},
    #             arguments={
    #                 'check_status': check_status,
    #                 'include_address': include_address,
    #                 'include_contacts': include_contacts,
    #             },
    #             authentication_required=False,
    #             signature_required=True))

    def get_places(
            self,
            area_id=None,
            bounds=None,
            category_ids=None,
            location=None,
            include_address=False,
            include_contacts=False,
            include_photos=False,
            limit=None,
            keywords=None,
            locale=DEFAULT_LOCALE,
            offset=0,
            radius=5000,
            remote_ip_address=None,
            sync_time=None,
            team_id=None):
        """
        Return a list of places, worth of extended information, corresponding
        to the specified criteria.


        :param area_id: identification of a geographical area to return the
            list of places.

        :param bounds: a tuple of two instances `GeoPoint` that represent
            the north-east corner and the south-west corners of the rectangle
            area to search places in.

        :param category_ids: a list of identifications of categories that
            indicate the particular use that places to return have been
            designed for.

        :param location: an instance `GeoPoint` of the geographic location
            to search nearby places.

        :param include_address: indicate whether to include address
            information of the places that are returned.

        :param include_contacts: indicate whether to include contacts
            information of the places that are returned.

        :param include_photos: indicate whether to include a limited set of
            photos associated to the places that are returned.

        :param keywords: A list of keywords to search places for.

        :param limit: constrain the number of places to return to the
            specified number.  If not specified, the default value is
            `BaseService.DEFAULT_RESULT_SET_SIZE`.  The maximum value is
            `BaseService.MAXIMUM_RESULT_SET_LIMIT`.

        :param locale: an instance `Locale` to return textual information of
            the places.

        :param offset: require to skip that many records before beginning to
            return records to the client.  Default value is `0`.  If both
            `offset` and `limit` are specified, then `offset` records
            are skipped before starting to count the limit records that are
            returned.

        :param radius: maximal distance in meters of the radius of search for
            places nearby the specified `location`.  If not specified, this
            method returns place within 5000 meters from the specified
            location.

        :param remote_ip_address: remote IP address of the client application.

        :param sync_time: indicate the earliest time to return places based on
            the time of their most recent modification.  If not specified, the
            function returns any available places, sorted by ascending order
            of their modification time.

        :param team_id: identification of an organisation the authenticated
            user belongs to.  The remote method will return places which
            visibility have been restricted to this organisation.


        :return: a list of instances containing the following members:

            * `address` (optional): Postal address of the place.  The address is
              composed of one or more address components. The address components are
              represented with a dictionary, where the key is as an item of the
              enumeration `AddressComponentName` and the value is the textual
              information of this component, written in the specified locale.

            * `category` (required): code name of a category qualifying this
              place.

            * `contacts` (optional): list of properties such as e-mail
              addresses, phone numbers, etc., in respect of the electronic
              business card specification (vCard).  The contact information is
              represented by a list of tuples of the following form::

                 `(name:ContactName, value:string, is_primary:boolean, is_verified:boolean)`

              where:

              * `name`: type of this contact information, which can be one
                of these standard names in respect of the electronic business
                card specification (vCard).

              * `value`: value of this contact information representing by a
                string, such as `+84.01272170781`, the formatted value for a
                telephone number property.

              * `is_primary`: indicate whether this contact information is
                the primary for this place.

              * `is_verified`: indicate whether this contact information has
                been verified, whether it has been grabbed from a trusted
                Social Networking Service (SNS), or whether through a
                challenge/response process.s

            * `location` (required): geographic coordinates of the location
              of the place represented with the following JSON structure::

                    {
                      "accuracy": decimal,
                      "altitude": decimal,
                      "latitude": decimal,
                      "longitude": decimal
                    }

              where:

              * `accuracy` (optional): accuracy of the place's position in
                meters.

              * `altitude` (optional): altitude in meters of the place.

              * `latitude` (required): latitude-angular distance, expressed
                in decimal degrees (WGS84 datum), measured from the center of
                the Earth, of a point north or south of the Equator
                corresponding to the place's location.

              * `longitude` (required): longitude-angular distance,
                expressed in decimal degrees (WGS84 datum), measured from the
                center of the Earth, of a point east or west of the Prime
                Meridian corresponding to the place's location.

            * `photos` (optional): a list of photos attached to this place:

              * `photo_id`: identification of the photo.

              * `photo_url`: Uniform Resource Locator (URL) that specifies
                the location of the photo, if any defined.  The client
                application can use this URL and append the query parameter
                `size` to specify a given pixel resolution of the photo
                picture, such as `thumbnail`, `small`, `medium`, or
                `large`.

            * `place_id` (required): identification of the place.

            * `update_time` (required): time of the last modification of one
              or more attributes of this place.  This time should be used by
              the client application to manage its cache of places and to
              reduce the average time to access data of places.  When the
              client application needs to read places' attributes, it first
              checks whether a copy of these data is in its cache.  If so, the
              client application immediately reads from the cache, which is
              much faster than requesting these data from the server platform.


        :raise InvalidArgumentException: if no geolocation or geographic area
            has been passed to this function.
        """
        return self.send_request(
            http_method=self.HttpMethod.GET,
            path='/place',
            arguments={
                'area_id': area_id,
                'bounds': bounds and f'{bounds[0].latitude},{bounds[0].longitude},{bounds[1].latitude},{bounds[1].longitude}',
                'category_ids': category_ids,
                'include_address': include_address,
                'include_contacts': include_contacts,
                'include_photos': include_photos,
                'keywords': keywords and ','.join(keywords),
                'location': location and f'{location.latitude},{location.longitude}',
                'limit': limit,
                'locale': locale,
                'offset': offset,
                'radius': radius,
                'remote_ip_address': remote_ip_address,
                'sync_time': sync_time,
                'team_id': team_id,
            },
            authentication_required=False,
            signature_required=True)

    # def add_place(
    #         self,
    #         category_id=None,
    #         address=None,
    #         is_address_edited=True,
    #         is_location_edited=False,
    #         locale=None,
    #         location=None):
    #     return self.send_request(
    #             http_method=self.HttpMethod.POST,
    #             path='/place',
    #             message_body={
    #                 'address': address,
    #                 'category_id': category_id,
    #                 'is_address_edited': is_address_edited,
    #                 'is_location_edited': is_location_edited,
    #                 'locale': locale,
    #                 'location': location and '%s,%s' % (location.longitude, location.latitude),
    #             },
    #             authentication_required=True,
    #             signature_required=True)
    #
    # def sync_place(self, place, optimistic_match=True):
    #     return Object.from_json(
    #             self.send_request(
    #                     http_method=self.HttpMethod.PUT,
    #                     path='/place/sync',
    #                     arguments={ 'optimistic_match': optimistic_match },
    #                     message_body=place,
    #                     authentication_required=True,
    #                     signature_required=True))
