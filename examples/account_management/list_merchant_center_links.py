#!/usr/bin/env python
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Demonstrates how to list Merchant Center links.

Prerequisite: You need to have access to a Merchant Center account. You can find instructions to create a Merchant Center account here:
https://support.google.com/merchants/answer/188924.

To run this code example, you must use the Merchant Center UI or the Content API for Shopping to send a link request between your Merchant Center and Google Ads accounts.
"""

import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.api_core import protobuf_helpers


def main(client, customer_id):
    """Demonstrates how to approve a Merchant Center link request.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The client customer ID string.
        merchant_center_account_id: ID of the Merchant center whose link request
        is to be approved.
    """
    merchant_center_link_service = client.get_service(
        "MerchantCenterLinkService"
    )

    # [START retrieve all the existing merchant]
    # Retrieve all the existing Merchant Center links.
    response = merchant_center_link_service.list_merchant_center_links(
        customer_id=customer_id
    )
    print(
        f"{len(response.merchant_center_links)} Merchant Center link(s) "
        "found with the following details:"
    )
    # [END retrieve all the existing merchant]

    merchant_center_link_status_enum = client.enums.MerchantCenterLinkStatusEnum

    # Iterate through the results and filter for links with pending statuses.
    for merchant_center_link in response.merchant_center_links:
        # [START print merchant_certer_link status]
        print(
            f"Link '{merchant_center_link.resource_name}' has status "
            f"'{merchant_center_link.status.name}'."
        )
        # [END print merchant_certer_link status]
    print("------end of merchant center links------")
if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description=("Approves a Merchant Center link request.")
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    args = parser.parse_args()

    try:
        main(
            googleads_client, args.customer_id
        )
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status'
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
