#  Copyright 2019 Michael Kemna.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

from enum import Enum

from sqlalchemy import text


class Query(Enum):
    """
    This Enum is used to create a framework to store the queries that are used by the application.
    Of course, you can also create your own Query Enum in your own module.

    source to execute raw sql with sqlalchemy:
    https://chartio.com/resources/tutorials/how-to-execute-raw-sql-in-sqlalchemy/
    """
    select_forecast_24h = text("""
        SELECT r.id, lat, lng
        FROM resort as r
        LEFT JOIN (SELECT id, resort_id
                   FROM forecast
                   WHERE date = current_date
                   and timepoint = 0
                   ) as f on r.id = f.resort_id
        WHERE f.id is NULL
    """)

    select_weather_3h = text("""
        SELECT r.id, lat, lng
        FROM resort as r
        LEFT JOIN (SELECT id, resort_id 
                   FROM weather 
                   WHERE date_request > current_timestamp - 3 * interval '1 hour'
                   ) as w on r.id = w.resort_id
        WHERE w.id is NULL
    """)
