# Get latitude, longitude from a name
from geopy.geocoders import Nominatim

geolocator = Nominatim()
location = geolocator.geocode("175 5th Avenue NYC")
print((location.latitude, location.longitude))