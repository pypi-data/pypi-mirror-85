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
from sqlalchemy import Table, Column, Integer, Float, Date, DateTime, String, Sequence, MetaData, \
    ForeignKey, UniqueConstraint


def model_resort(metadata: MetaData) -> Table:
    return Table('resort', metadata,
                 Column('id', Integer, Sequence('resort_id_seq'), primary_key=True,
                        comment='The identifier of the resort'),
                 Column('continent', String, comment='The continent where the resort is located'),
                 Column('name', String, comment='The shorthand name of the resort'),
                 Column('fullname', String, comment='The full name of the resort'),
                 Column('country', String, comment='The country where the resort is located'),
                 Column('village', String, comment='The village where the resort is located'),
                 Column('lat', Float, comment='The latitudinal coordinate of the geolocation of the resort'),
                 Column('lng', Float, comment='The longitudinal coordinate of the geolocation of the resort'),
                 Column('altitude_min_m', Integer, comment='The lowest altitude of the resort (in metres)'),
                 Column('altitude_max_m', Integer, comment='The highest altitude of the resort (in metres)'),
                 Column('lifts', Integer, comment='The amount of lifts in the resort'),
                 Column('slopes_total_km', Integer, comment='The length of all slopes in the resort (in kilometres)'),
                 Column('slopes_blue_km', Integer, comment='The length of blue slopes in the resort (in kilometres)'),
                 Column('slopes_red_km', Integer, comment='The length of red slopes in the resort (in kilometres)'),
                 Column('slopes_black_km', Integer, comment='The length of black slopes in the resort (in kilometres)'),
                 UniqueConstraint('village', 'country'),
                 )


def model_weather(metadata: MetaData) -> Table:
    return Table('weather', metadata,
                 Column('id', Integer, Sequence('weather_id_seq'), primary_key=True,
                        comment='The identifier of the weather report'),
                 Column('resort_id', Integer, ForeignKey('resort.id', onupdate='CASCADE', ondelete='CASCADE'),
                        comment='Foreign key to the related resort'),
                 Column('date_request', DateTime, comment='The date on which the weather was requested by the scraper'),
                 Column('dt', DateTime, comment='The datetime as given by the scraped api'),
                 Column('date', Date, comment='The date derived from dt'),
                 Column('timepoint', Integer, default=-1,
                        comment='Ordinal timepoint of the day, categorized every 3 hours (range 0-7)'),
                 Column('temperature_c', Float, comment='The temperature in Celsius'),
                 Column('wind_speed_kmh', Float, comment='The wind speed in kilometres per hour'),
                 Column('wind_direction_deg', Float, comment='The wind direction in degrees'),
                 Column('visibility_km', Float, comment='The visibility in kilometres'),
                 Column('clouds_pct', Float, comment='The amount of clouds in percentage'),
                 Column('snow_3h_mm', Float, comment='The amount of snow in the last 3 hours in millimetres'),
                 Column('rain_3h_mm', Float, comment='The amount of rain in the last 3 hours in millimetres'),
                 UniqueConstraint('date', 'timepoint', 'resort_id'),
                 )


def model_forecast(metadata: MetaData) -> Table:
    return Table('forecast', metadata,
                 Column('id', Integer, Sequence('forecast_id_seq'), primary_key=True),
                 Column('resort_id', Integer, ForeignKey('resort.id', onupdate="CASCADE", ondelete="CASCADE")),
                 Column('date_request', DateTime),
                 Column('date', Date),
                 Column('timepoint', Integer),
                 Column('temperature_max_c', Float),
                 Column('temperature_min_c', Float),
                 Column('rain_total_mm', Float),
                 Column('snow_total_mm', Float),
                 Column('prob_precip_pct', Float),
                 Column('wind_speed_max_kmh', Float),
                 Column('windgst_max_kmh', Float),
                 UniqueConstraint('date', 'timepoint', 'resort_id'),
                 )


def model_forecast_week(metadata: MetaData) -> Table:
    return Table('forecast_week', metadata,
                 Column('id', Integer, Sequence('forecast_week_id_seq'), primary_key=True),
                 Column('resort_id', Integer, ForeignKey('resort.id', onupdate="CASCADE", ondelete="CASCADE")),
                 Column('date_request', DateTime),
                 Column('date', Date),
                 Column('rain_week_mm', Float),
                 Column('snow_week_mm', Float),
                 UniqueConstraint('date', 'resort_id'),
                 )
