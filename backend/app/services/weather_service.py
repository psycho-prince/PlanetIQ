import requests

def get_weather(lat,lon):
    url=f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m'
    try:
        c=requests.get(url,timeout=10).json()['current']
        return {'temperature':c['temperature_2m'],'humidity':c['relative_humidity_2m']}
    except Exception:
        return {'temperature':None,'humidity':None}
