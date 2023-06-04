from pydantic import BaseModel,\
    Field, validator


class UnitType(BaseModel):
    value: str | None = Field(alias='Value')
    unit: str | None = Field(alias='Unit')                # TODO(delete): delete this
    unit_type: int | None = Field(alias='UnitType')       # TODO(delete): delete this
    phrase: str | None = Field(alias='Phrase')


class Unit(BaseModel):
    imperial: UnitType | None = Field(alias='Imperial') 
    metric: UnitType | None = Field(alias='Metric')


class WindGust(BaseModel):
    speed: Unit | None = Field(alias='Speed')


# only for wind
class Direction(BaseModel):
    degrees: int | None = Field(alias='Degrees')
    localized: str | None = Field(alias='Localized')
    english: str | None = Field(alias='English')


class Wind(BaseModel):
    direction: Direction | None = Field(alias='Direction')
    speed: Unit | None = Field(alias='Speed')


BASE_MATH_ROUND_FIELDS = (
    'humidity', 'dew_point',
    'temperature', 'wind_speed',
    'cloud_cover', 'wind_gust_speed',
    'visibility', 'uv_index',
    'pressure', 'apparent_temperature',
    # accu
    'feels_like_shade', 'precip1hr',
    # visual
    'solarenergy', 'solarradiation'
)

BASE_TEMP_CONVERT_FIELDS = (
    'dew_point', 'temperature',
    'apparent_temperature',
    # accu
    'feels_like_shade'
)


class BaseWeather(BaseModel):
    # "Weather class designed to work with different weather apis"
    def __init__(cls, **data):
        super().__init__(
            # tomorrow or visual or accu
            temperature=data.pop("temperature", None)
                or data.pop("temp", None) or data.pop("Temperature", None),

            apparent_temperature=data.pop("temperatureApparent", None)
                or data.pop("feelslike", None) or data.pop("ApparentTemperature", None),

            dew_point=data.pop("dewPoint", None)
                or data.pop("dew", None) or data.pop("DewPoint", None),

            wind_speed=data.pop("windSpeed", None) or data.pop("windspeed", None)
                or data.get("Wind"),

            wind_dir=data.pop("windDirection", None) or data.pop("winddir", None)
                or data.pop("Wind", None),

            wind_gust_speed=data.pop("windGust", None)
                or data.pop("windgust", None) or data.pop("WindGust", None),

            cloud_cover=data.pop("cloudCover", None)
                or data.pop("cloudcover", None) or data.pop("CloudCover", None),

            pressure=data.pop("pressureSurfaceLevel", None)
                or data.pop("pressure", None) or data.pop("Pressure", None),

            uv_index=data.pop("uvIndex", None)
                or data.pop("uvindex", None) or data.pop("UVIndex", None),
            humidity=data.pop("humidity", None)
                or data.pop("RelativeHumidity", None),  # (tommorow\visual) and accu

            visibility=data.pop("visibility", None)   # tommorow and visual
                or data.pop("Visibility", None),
            **data,
        )
        print(cls.uv_index, 'uv3')

    temperature: str | Unit | None
    apparent_temperature: str | Unit | None
    dew_point: int | str | Unit | None
    wind_speed: str | Wind | None
    wind_dir: str | Wind | None
    wind_gust_speed: str | WindGust | None
    cloud_cover: str | None
    pressure: str | Unit | None
    uv_index: int | str | None
    humidity: int | str | None
    visibility: str | Unit | None

    @validator(*BASE_MATH_ROUND_FIELDS, check_fields=False)
    def math_round_valid(cls, number: int | str | Unit | WindGust 
                                    | Wind | None) -> str | WindGust | Wind | None:
        print(number, 'pip')
        # if number is None return nothing
        match number:
            case int() | str():
                number = float(number)
                return str(int(number + (0.5 if number > 0 else -0.5)))
            case Unit():
                f_number = float(number.metric.value)
                return str(int(f_number + (0.5 if f_number > 0 else -0.5)))   
            case WindGust() | Wind():
                f_number = float(number.speed.metric.value)
                return str(int(f_number + (0.5 if f_number > 0 else -0.5)))

    @validator(*BASE_TEMP_CONVERT_FIELDS, check_fields=False)
    def temp_convert_valid(cls, temp: str | None) -> str | None:
        print(temp, 'kek')
        if int(temp) > 0:
            temp = '+' + str(temp)
        return str(temp) + ' C°'
    
    @validator('wind_dir', check_fields=False)
    def accu_wind_dir_valid(cls, wind_dir: str | Wind | None) -> str | None:
        match wind_dir:
            case str():
                print(wind_dir, 'wind_dir3')
                wind_dir = float(wind_dir)
                return str(int(wind_dir + (0.5 if wind_dir > 0 else -0.5))) 
            case Wind():
                print('wind123', wind_dir)
                return str(wind_dir.direction.degrees) + '° ' + wind_dir.direction.localized


# only for  PressureTendency
class PressureTendency(BaseModel):
    localized_text: str | None = Field(alias='LocalizedText')
    code: str | None = Field(alias='Code')

    @validator('code')
    def pressure_valid(cls, code: str | None) -> str | None:
        match code:
            case "S":
                return "Давление устойчиво"
            case "F":
                return "Давление падает"
            case "R":
                return "Давление растет"


class AccuWeather(BaseWeather):

    local_obs_datetime: str | None = Field(alias='LocalObservationDateTime', default_factory=None)
    weather_text: str | None = Field(alias='WeatherText', default_factory=None)
    has_precipitation: bool | None = Field(alias='HasPrecipitation', default_factory=None)
    precipitation_type: str | None = Field(alias='PrecipitationType', default_factory=None)

    feels_like: Unit | None = Field(alias='RealFeelTemperature', default_factory=None)
    feels_like_shade: Unit | None = Field(alias='RealFeelTemperatureShade', default_factory=None)
    relative_humidity: str | None = Field(alias='RelativeHumidity', default_factory=None)
    indoor_relative_humidity: str | None = Field(alias='IndoorRelativeHumidity', default_factory=None)
    uv_index_text: str | None = Field(alias='UVIndexText', default_factory=None)
    cloud_ceil: Unit | None = Field(alias='Ceiling', default_factory=None)
    pressure_tendency: PressureTendency | None = Field(alias='PressureTendency', default_factory=None)

    wind_сhill_temperature: Unit | None = Field(alias='WindChillTemperature', default_factory=None)
    precip1hr: Unit | None = Field(alias='Precip1hr', default_factory=None)
    link: str | None = Field(alias='Link', default_factory=None)


class VisualWeather(BaseWeather):
    conditions: str | None = Field(alias="conditions", default_factory=None)
    icon: str | None = Field(alias="icon", default_factory=None)

    sunrise: str | None = Field(alias="sunrise", default_factory=None)
    sunset: str | None = Field(alias="sunset", default_factory=None)
    moonphase: str | None = Field(alias="moonphase", default_factory=None)
    precip: str | None = Field(alias="precip", default_factory=None)
    snow: str | None = Field(alias="snow", default_factory=None)
    snowdepth: float | None = Field(alias="snowdepth", default_factory=None)
    solarenergy: float | None = Field(alias="solarenergy", default_factory=None)
    solarradiation: float | None = Field(alias="solarradiation", default_factory=None)


class TommorowWeather(BaseWeather):
    cloud_base: float | None = Field(alias="cloudBase", default_factory=None)
    cloud_ceiling: float | None = Field(alias='cloudCeiling')

    fire_index: int | None = Field(alias='fireIndex')
    flood_index: int | None = Field(alias='floodIndex')

    precipitation_type: int | None = Field(alias='precipitationType')
    pressure_surface_level: float | None = Field(alias='pressureSurfaceLevel')
    snow_intensity: int | None = Field(alias='snowIntensity')
    stream_flow: float | None = Field(alias='streamFlow')

    tree_index: int | None = Field(alias='treeIndex')
    visibility: float | None = Field(alias='visibility')
