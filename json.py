import network
import time
import urequests

# Ağa bağlan
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('Ornek', 'Ornek')

# Urequest'i kullanarak JSON verisi çek
astronauts = urequests.get("http://api.open-notify.org/astros.json").json()

# Astronauts bir liste ve bu liste içinde birçok kategori bar. Bunlardan birisi de number.
# Bu number listesinin içindeki sayıyı tutması için aynı isimde bir değişken oluşturuyoruz.
number = astronauts['number']

#Daha sonra 'number' içindeki sayı kadar astronot ismi listeliyoruz.
for i in range(number):
     print(astronauts['people'][i]['name'])