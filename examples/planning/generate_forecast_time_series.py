#!/usr/bin/env python
# Copyright 2019 Google LLC
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
"""This example generates forecast time series for a keyword plan.

To create a keyword plan, run the add_keyword_plan.py example.
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


# [START generate_forecast_time_series]
def main(client, customer_id, keyword_plan_id):
    keyword_plan_service = client.get_service("KeywordPlanService")
    resource_name = keyword_plan_service.keyword_plan_path(
        customer_id, keyword_plan_id
    )


    response = keyword_plan_service.generate_forecast_time_series(
        keyword_plan=resource_name
    )

    # group by week
    for i, forecast in enumerate(response.weekly_time_series_forecasts):
        # the resource name of keyword_plan_campaign
        print(f"#{i+1} Keyword Plan Campaign: {forecast.keyword_plan_campaign}\n")

        for j, weekly_forecast in enumerate(forecast.weekly_forecasts):
            # list a forecast in the form of a time series for the
            # Keyword Plan over the next 52 weeks
            print(f"    Week#{j + 1} start_date:{weekly_forecast.start_date}")
            metrics = weekly_forecast.forecast

            imp_val = metrics.impressions
            impressions = f"{imp_val:.2f}" if imp_val else "unspecified"
            print(f"    Estimated daily impressions: {impressions}")

            ctr_val = metrics.ctr
            ctr = f"{ctr_val:.2f}" if ctr_val else "unspecified"
            print(f"    Estimated average ctr: {ctr}")

            cpc_val = metrics.average_cpc
            cpc = f"{cpc_val:.2f}" if cpc_val else "unspecified"
            print(f"    Estimated average cpc: {cpc}")

            click_val = metrics.clicks # double
            clicks = f"{click_val:.2f}" if click_val else "unspecified"
            print(f"    Estimated daily clicks: {clicks}\n")

    # [END generate_forecast_time_series]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Generates forecast time series for a keyword plan."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    parser.add_argument(
        "-k",
        "--keyword_plan_id",
        type=str,
        required=True,
        help="A Keyword Plan ID.",
    )
    args = parser.parse_args()

    try:
        main(googleads_client, args.customer_id, args.keyword_plan_id)
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
