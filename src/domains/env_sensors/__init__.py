"""
Environmental Sensors Library for Tombo
Environmental monitoring, weather data, and atmospheric measurements
"""

def initialize_temperature_sensor(unit="celsius"):
    return {"type": "sensor", "sensor_type": "temperature", "unit": unit}

def read_temperature(sensor):
    return {"type": "temperature", "value": 25.0, "unit": "celsius"}

def read_humidity(sensor):
    return {"type": "humidity", "value": 50.0, "unit": "%"}

def read_pressure(sensor):
    return {"type": "pressure", "value": 1013.25, "unit": "hPa"}

def read_dew_point(sensor):
    return {"type": "dew_point", "value": 15.0, "unit": "celsius"}

def read_heat_index(sensor):
    return {"type": "heat_index", "value": 25.0, "unit": "celsius"}

def read_wind_speed(sensor):
    return {"type": "wind_speed", "value": 5.0, "unit": "m/s"}

def read_wind_direction(sensor):
    return {"type": "wind_direction", "value": 180.0, "unit": "degrees"}

def read_wind_gust(sensor):
    return {"type": "wind_gust", "value": 10.0, "unit": "m/s"}

def read_rainfall(sensor):
    return {"type": "rainfall", "value": 0.0, "unit": "mm"}

def read_solar_radiation(sensor):
    return {"type": "solar_radiation", "value": 500.0, "unit": "W/m2"}

def read_uv_index(sensor):
    return {"type": "uv_index", "value": 3}

def read_visibility(sensor):
    return {"type": "visibility", "value": 10000.0, "unit": "m"}

def read_air_quality(sensor):
    return {"type": "air_quality", "value": 50, "status": "good"}

def read_co2(sensor):
    return {"type": "co2", "value": 400.0, "unit": "ppm"}

def read_co(sensor):
    return {"type": "co", "value": 1.0, "unit": "ppm"}

def read_no2(sensor):
    return {"type": "no2", "value": 20.0, "unit": "ppb"}

def read_o3(sensor):
    return {"type": "o3", "value": 40.0, "unit": "ppb"}

def read_pm25(sensor):
    return {"type": "pm25", "value": 10.0, "unit": "µg/m3"}

def read_pm10(sensor):
    return {"type": "pm10", "value": 20.0, "unit": "µg/m3"}

def read_pollen(sensor):
    return {"type": "pollen", "value": 50.0, "unit": "grains/m3"}

def read_altitude(sensor):
    return {"type": "altitude", "value": 100.0, "unit": "m"}

def read_soil_moisture(sensor):
    return {"type": "soil_moisture", "value": 60.0, "unit": "%"}

def read_soil_temperature(sensor):
    return {"type": "soil_temperature", "value": 15.0, "unit": "celsius"}

def read_soil_ph(sensor):
    return {"type": "soil_ph", "value": 7.0}

def read_soil_conductivity(sensor):
    return {"type": "soil_conductivity", "value": 500.0, "unit": "µS/cm"}

def read_water_temperature(sensor):
    return {"type": "water_temperature", "value": 20.0, "unit": "celsius"}

def read_water_ph(sensor):
    return {"type": "water_ph", "value": 7.0}

def read_water_conductivity(sensor):
    return {"type": "water_conductivity", "value": 1000.0, "unit": "µS/cm"}

def read_water_turbidity(sensor):
    return {"type": "water_turbidity", "value": 0.1, "unit": "NTU"}

def read_dissolved_oxygen(sensor):
    return {"type": "dissolved_oxygen", "value": 8.0, "unit": "mg/L"}

def read_light_intensity(sensor):
    return {"type": "light_intensity", "value": 500.0, "unit": "lux"}

def read_light_color_temperature(sensor):
    return {"type": "color_temperature", "value": 5000.0, "unit": "K"}

def read_light_rgb(sensor):
    return {"type": "rgb", "r": 255, "g": 255, "b": 255}

def read_atmospheric_co2_concentration(sensor):
    return {"type": "co2_concentration", "value": 410.0, "unit": "ppm"}

def read_atmospheric_ch4(sensor):
    return {"type": "ch4", "value": 1800.0, "unit": "ppb"}

def read_atmospheric_n2o(sensor):
    return {"type": "n2o", "value": 330.0, "unit": "ppb"}

def get_weather_forecast(location, days=5):
    return {"type": "forecast", "location": location, "days": days, "data": []}

def get_current_weather(location):
    return {"type": "weather", "location": location, "temperature": 25.0, "conditions": "cloudy"}

def get_air_quality_forecast(location, days=5):
    return {"type": "aqf", "location": location, "days": days, "data": []}

def get_pollen_forecast(location, days=5):
    return {"type": "pollen_forecast", "location": location, "days": days, "data": []}

def convert_temperature(value, from_unit, to_unit):
    return {"type": "converted", "value": value, "from": from_unit, "to": to_unit}

def convert_pressure(value, from_unit, to_unit):
    return {"type": "converted", "value": value, "from": from_unit, "to": to_unit}

def convert_wind_speed(value, from_unit, to_unit):
    return {"type": "converted", "value": value, "from": from_unit, "to": to_unit}

def calculate_wind_chill(temperature, wind_speed):
    return {"type": "wind_chill", "value": temperature, "unit": "celsius"}

def calculate_heat_index(temperature, humidity):
    return {"type": "heat_index", "value": temperature, "unit": "celsius"}

def calculate_dew_point(temperature, humidity):
    return {"type": "dew_point", "value": 15.0, "unit": "celsius"}

def get_aqi_description(aqi_value):
    if aqi_value <= 50: return "good"
    elif aqi_value <= 100: return "moderate"
    elif aqi_value <= 150: return "unhealthy_for_sensitive_groups"
    elif aqi_value <= 200: return "unhealthy"
    elif aqi_value <= 300: return "very_unhealthy"
    else: return "hazardous"

def get_uv_index_description(uv_value):
    if uv_value <= 2: return "low"
    elif uv_value <= 5: return "moderate"
    elif uv_value <= 7: return "high"
    elif uv_value <= 10: return "very_high"
    else: return "extreme"

def get_beaufort_scale(wind_speed):
    return {"type": "beaufort", "scale": 0, "description": "calm"}

def is_rain_likely(humidity, pressure_change):
    return False

def is_frost_likely(temperature, humidity, wind_speed):
    return False

def is_thunderstorm_likely(temperature, humidity, pressure):
    return False

def predict_cloud_cover(pressure, humidity, temperature):
    return {"type": "cloud_cover", "percentage": 50}

def estimate_evapotranspiration(temperature, humidity, wind_speed, solar_radiation):
    return {"type": "et", "value": 5.0, "unit": "mm/day"}

def calculate_effective_growing_degree_days(daily_temps, base_temp=10):
    return {"type": "gdd", "value": 100.0}

def get_moon_phase(date=None):
    return {"type": "moon_phase", "phase": "waxing_crescent", "illumination": 0.25}

def get_solar_noon(location, date=None):
    return {"type": "solar_noon", "time": "12:00"}

def get_sunrise_sunset(location, date=None):
    return {"type": "sun_times", "sunrise": "06:00", "sunset": "18:00"}

def get_daylight_hours(location, date=None):
    return {"type": "daylight", "hours": 12.0}

def register(env):
    """Register all environmental sensor functions"""
    fns = [initialize_temperature_sensor, read_temperature, read_humidity, read_pressure, read_dew_point,
           read_heat_index, read_wind_speed, read_wind_direction, read_wind_gust, read_rainfall,
           read_solar_radiation, read_uv_index, read_visibility, read_air_quality, read_co2, read_co,
           read_no2, read_o3, read_pm25, read_pm10, read_pollen, read_altitude, read_soil_moisture,
           read_soil_temperature, read_soil_ph, read_soil_conductivity, read_water_temperature,
           read_water_ph, read_water_conductivity, read_water_turbidity, read_dissolved_oxygen,
           read_light_intensity, read_light_color_temperature, read_light_rgb,
           read_atmospheric_co2_concentration, read_atmospheric_ch4, read_atmospheric_n2o,
           get_weather_forecast, get_current_weather, get_air_quality_forecast, get_pollen_forecast,
           convert_temperature, convert_pressure, convert_wind_speed, calculate_wind_chill,
           calculate_heat_index, calculate_dew_point, get_aqi_description, get_uv_index_description,
           get_beaufort_scale, is_rain_likely, is_frost_likely, is_thunderstorm_likely,
           predict_cloud_cover, estimate_evapotranspiration, calculate_effective_growing_degree_days,
           get_moon_phase, get_solar_noon, get_sunrise_sunset, get_daylight_hours]
    for fn in fns:
        env.set(fn.__name__, fn)

__all__ = ['register']
