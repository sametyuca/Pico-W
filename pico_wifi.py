import rp2
import network
import ubinascii
import machine
import urequests as requests
import time
from sifre import sifre
import socket

# Ülke ayarı
rp2.country('TR')

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Kablosuz ağ bilgilerini sakladığımız sifre.py'den çekiyoruz.
ssid = sifre['ag_adi']
pw = sifre['sifre']

wlan.connect(ssid, pw)

# Bağlantı için 10 sn bekle...
timeout = 10
while timeout > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    timeout -= 1
    print('Baglanti bekleniyor...')
    time.sleep(1)
    
#Eğer bağlantı başarısız olursa bildir.
if wlan.status() != 3:
    raise RuntimeError('Wi-Fi baglantisi basarisiz.')
else:
    led = machine.Pin('LED', machine.Pin.OUT)
    for i in range(wlan.status()):
        led.on()
        time.sleep(.1)
        led.off()
    print('Baglandi')
    status = wlan.ifconfig()
    print('ip = ' + status[0])
    
# HTML sayfasını yükleyecek fonksiyon.  
def get_html(html_name):
    with open(html_name, 'r') as file:
        html = file.read()
        
    return html

# HTTP sunucusu
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('Bekleniyor...', addr)

# Bağlantı için bekle
while True:
    try:
        cl, addr = s.accept()
        print('Istemci bu adresten baglandi:', addr)
        r = cl.recv(1024)
        # print(r)
        
        r = str(r)
        led_on = r.find('?led=on')
        led_off = r.find('?led=off')
        #print('led_on = ', led_on)
        #print('led_off = ', led_off)
        if led_on == 10:
            print('LED Acik')
            led.value(1)
            
        if led_off == 10:
            print('LED Kapali')
            led.value(0)
            
        response = get_html('index.html')
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('Baglanti Sonlandirildi')
