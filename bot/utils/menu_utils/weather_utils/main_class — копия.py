from tomorrow import current_weather_tomorrow_api, TOMORROW_IO_API_KEY
#from visual import visual_url
from accu import get_current_weather
import datetime
API_KEY = '42RGKTT7AEZ9E3RWD3S5RYBYV'
location = 'минск'
contentType = "json"
language = "ru"
current_time = str(datetime.datetime.now())
current_time_in_format = datetime.datetime.fromisoformat(current_time).strftime("%Y-%m-%dT%H:%M:%S")
unitGroup = "metric"
period = 'today'
visual_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{current_time_in_format}?maxStations=1&unitGroup={unitGroup}&key={API_KEY}&contentType={contentType}&lang={language}&include=current"

from pprint import pprint
from pydantic import BaseModel, ValidationError,\
    Field, validator
from pydantic.dataclasses import dataclass 


import requests

class UnitType(BaseModel):
    value: str | None = Field(alias = 'Value')
    unit: str | None = Field(alias = 'Unit')                #TODO: delete this
    unit_type: int | None = Field(alias = 'UnitType')       #TODO: delete this
    phrase: str | None = Field(alias = 'Phrase')      
    

class Unit(BaseModel):
    imperial: UnitType | None = Field(alias = 'Imperial')   #TODO: delete this
    metric: UnitType | None = Field(alias = 'Metric')

class WindGust(BaseModel):
    speed: Unit | None = Field(alias = 'Speed')

BASE_MATH_ROUND_FIELDS = (
            'humidity', 'dew_point', 
            'temperature', 'wind_speed',
            'wind_dir', 'cloud_cover',
            'visibility', 'wind_gust',
            'pressure'
    )

BASE_TEMP_CONVERT_FIELDS = (
            'dew_point', 'temperature', 
        
            
)


class BaseWeather(BaseModel):
    #"Класс Weather, предназначенный для работы с разными погодными api"
    def __init__(self, **data):
      super().__init__(
          #tomorrow or visual or accu
          temperature=data.pop("temperature", None) 
                or data.pop("temp", None) or data.pop("Temperature", None),

          apparent_temperature=data.pop("temperatureApparent", None) 
                or data.pop("feelslike", None) or data.pop("ApparentTemperature", None),

          dew_point=data.pop("dewPoint", None) 
                or data.pop("dew", None) or data.pop("DewPoint", None),

          wind_speed=data.pop("windSpeed", None) or data.pop("windspeed", None),
          wind_dir=data.pop("windDirection", None) or data.pop("winddir", None),

          wind_gust=data.pop("windGust", None) 
                or data.pop("windgust", None) or data.pop("WindGust", None),

          cloud_cover=data.pop("cloudCover", None) 
                or data.pop("cloudcover", None) or data.pop("CloudCover", None),
                                
          pressure=data.pop("pressureSeaLevel", None) 
                or data.pop("pressure", None) or data.pop("Pressure", None),

          visibility=data.pop("visibility", None) #tommorow and visual
                or data.pop("Visibility", None),
          **data,
      )
    
    temperature: str | Unit | None
    apparent_temperature: str | Unit | None 
    dew_point: str | Unit | None
    wind_speed: str | None
    wind_dir: str | None
    wind_gust: str | WindGust | None
    cloud_cover: str | None
    pressure: str | Unit | None

    humidity: str | None 
    visibility: str | Unit | None 



    @validator(*BASE_MATH_ROUND_FIELDS)
    def math_round_valid(cls, number: int | float | str\
                                | Unit | WindGust | None) -> int | Unit | WindGust | None:

        #if number is None return nothing
        match number:
            case int() | float() | str():
                number = float(number)
                return int(number + (0.5 if number > 0 else -0.5))
            case Unit():
                #metic
                f_number = float(number.metric.value)
                rounded_value = int(f_number + (0.5 if f_number > 0 else -0.5))
                number.metric.value = rounded_value

                #imperial
                f_number = float(number.imperial.value)
                rounded_value = int(f_number + (0.5 if f_number > 0 else -0.5))
                number.imperial.value = rounded_value
                return number
            case WindGust():
                #metic
                f_number = float(number.speed.metric.value)
                rounded_value = int(f_number + (0.5 if f_number > 0 else -0.5))
                number.speed.metric.value = rounded_value

                #imperial
                f_number = float(number.speed.imperial.value)
                rounded_value = int(f_number + (0.5 if f_number > 0 else -0.5))
                number.speed.imperial.value = rounded_value
                return number

            
      

    
    @validator(*BASE_TEMP_CONVERT_FIELDS)
    def temp_convert_valid(cls, temp: int | Unit | None) -> str | Unit |None:
        match temp:
            case Unit():

                #metic
                i_temp = temp.metric.value
                if i_temp > 0:
                    temp.metric.value = '+' + str(i_temp)
                temp.metric.value = str(i_temp)

                #imperical
                i_temp = temp.imperial.value
                if i_temp > 0:
                    temp.imperial.value = '+' + str(i_temp)
                temp.imperial.value = str(i_temp)
                return temp
            case int():
                if temp > 0:
                    return '+' + str(temp)
                return str(temp)


class TommorowWeather(BaseWeather):
    cloud_base: float | None = Field(alias = "cloudBase", default_factory=None)
    cloud_ceiling: float | None = Field(alias = 'cloudCeiling')
 
    fire_index: int | None = Field(alias = 'fireIndex')
    flood_index: int | None = Field(alias = 'floodIndex')

    precipitation_type: int | None = Field(alias = 'precipitationType')
    pressure_surface_level: float | None = Field(alias = 'pressureSurfaceLevel')
    snow_intensity: int | None = Field(alias = 'snowIntensity')
    stream_flow: float | None = Field(alias = 'streamFlow')

    tree_index: int | None = Field(alias = 'treeIndex')
    uv_index: int | None = Field(alias = 'uvIndex')
    visibility: float | None = Field(alias = 'visibility')
    



class VisualWeather(BaseWeather):
    conditions: str | None = Field(alias = "conditions", default_factory=None)
    #icon: str | None = Field(alias = "icon", default_factory=None) TODO: visual icon

    
    sunrise: str | None = Field(alias = "sunrise", default_factory=None)
    sunset: str | None = Field(alias = "sunset", default_factory=None)
    moonphase: str | None = Field(alias = "moonphase", default_factory=None)
    precip: str | None = Field(alias = "precip", default_factory=None)
    uv_index: float | None = Field(alias = "uvindex", default_factory=None)
    snow: str | None = Field(alias = "snow", default_factory=None)
    snowdepth: float | None = Field(alias = "snowdepth", default_factory=None)
    solarenergy: float | None = Field(alias = "solarenergy", default_factory=None)
    solarradiation: float | None = Field(alias = "solarradiation", default_factory=None)
 


#only for wind
class Direction(BaseModel):
    degrees: int | None = Field(alias = 'Degrees')   
    localized: str | None = Field(alias = 'Localized')
    english: str | None = Field(alias = 'English')


class Wind(BaseModel):
    direction: Direction | None = Field(alias = 'Direction')
    speed: Unit | None = Field(alias = 'Speed')

    



#only for  PressureTendency
class PressureTendency(BaseModel):
    localized_text: int | None = Field(alias = 'LocalizedText')   
    code: str | None = Field(alias = 'Code')

    
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

    local_obs_datetime: str | None = Field(alias = 'LocalObservationDateTime', default_factory=None)
    weather_text: str | None = Field(alias = 'WeatherText', default_factory=None)
    has_precipitation: bool | None = Field(alias = 'HasPrecipitation', default_factory=None)
    precipitation_type: str | None = Field(alias = 'PrecipitationType', default_factory=None)
      
    feels_like: Unit | None = Field(alias = 'RealFeelTemperature', default_factory=None)
    feels_like_shade: Unit | None = Field(alias = 'RealFeelTemperatureShade', default_factory=None)
    relative_humidity: str | None = Field(alias = 'RelativeHumidity', default_factory=None)
    indoor_relative_humidity: str | None = Field(alias = 'IndoorRelativeHumidity', default_factory=None)
    uv_index: int | None = Field(alias = 'UVIndex', default_factory=None)
    uv_index_text: str | None = Field(alias = 'UVIndexText', default_factory=None)
    indoor_relative_humidity: str | None = Field(alias = 'IndoorRelativeHumidity', default_factory=None)
    cloud_ceil: Unit | None = Field(alias = 'Ceiling', default_factory=None)
    Pressure_tendency: PressureTendency | None = Field(alias = 'PressureTendency', default_factory=None)

    wind_сhill_temperature: Unit | None = Field(alias = 'WindChillTemperature', default_factory=None)
    precip1hr: Unit | None = Field(alias = 'Precip1hr', default_factory=None)
    wind: Wind | None = Field(alias = 'Wind', default_factory=None)

    link: str | None = Field(alias = 'Link', default_factory=None)

    

    
if __name__ == '__main__':
 
   
    lat = 53.893009
    lon = 27.567444
    
   
    weather_json = get_current_weather('minsk')
    print(weather_json)
  
    
    #weather_json = current_weather_tomorrow_api(TOMORROW_IO_API_KEY, lat, lon)
   
    #weather_json = requests.get(url = visual_url).json().get('currentConditions')
    #print(weather_json)
    try:
        #weather = TommorowWeather(**weather_json)
        #weather = VisualWeather(**weather_json)

        weather = AccuWeather(**weather_json)

        print(weather)


    except ValidationError as e:
        print(e.json())

    
   