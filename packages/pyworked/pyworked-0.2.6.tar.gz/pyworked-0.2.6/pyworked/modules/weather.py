import requests

class Weather:
    
    def __init__(self, q, typed, units, appid):
        res = requests.get("http://api.openweathermap.org/data/2.5/find", 
        params={
            'q': q,
            'type': typed,
            'units': units,
            'APPID': appid
        })
        self.data = res.json()

    def get_id(self):
        return(self.data['list'][0]['id'])

    def get_request_name(self):
        return(self.data['list'][0]['name'])
    
    def get_coord_lat(self):
        return(self.data['list'][0]['coord']['lat'])

    def get_coord_lon(self):
        return(self.data['list'][0]['coord']['lon'])

    def get_country(self):
        return(self.data['list'][0]['sys']['country'])

    def get_rain(self):
        return(self.data['list'][0]['rain'])

    def get_snow(self):
        return(self.data['list'][0]['snow'])

    def get_clouds(self):
        return(self.data['list'][0]['clouds']['all'])

    def get_description(self):
        return(self.data['list'][0]['weather'][0]['description'])

    def get_temp(self):
        return(self.data['list'][0]['main']['temp'])

    def get_temp_min(self):
        return(self.data['list'][0]['main']['temp_min'])

    def get_temp_max(self):
        return(self.data['list'][0]['main']['temp_max'])
    
    def get_wind_speed(self):
        return(self.data['list'][0]['wind']['speed'])

    def get_wind_deg(self):
        return(self.data['list'][0]['wind']['deg'])

    def get_pressure(self):
        return(self.data['list'][0]['main']['pressure'])
    
    def get_humidity(self):
        return(self.data['list'][0]['main']['humidity'])

    def get_feels_like(self):
        return(self.data['list'][0]['main']['feels_like'])