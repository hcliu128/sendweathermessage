import requests
import bs4
import time
# import keepalive

place_list = {
  "台中":
  'https://weather.com/zh-TW/weather/today/l/e7629778659a8bcc50e38c2a4f5c02582dc4eef7a29f116b3616bb4e7a39412b',
  "新竹":
  'https://weather.com/zh-TW/weather/today/l/9d98eb3f97a83330c0599a7548c3c7b47163615858673cfee2406e208ce20604',
  "台北":
  'https://weather.com/zh-TW/weather/today/l/6b221b26e046a442e03dc46fbe91d5874c6461afde61187dd4126bddeea1e2aa'
}

wakeuptime = {
  "Mon": "8",
  "Tue": "9",
  "Wed": "10",
  "Thu": "8",
  "Fri": "10",
  "Sat": "8",
}


def get_date():
  timestamp = time.ctime()
  t1 = timestamp.split(":")[0]
  t2 = t1.split(" ")[0]
  return t2


def get_hour():
  timestamp = time.ctime()
  t1 = timestamp.split(":")[0]
  t2 = t1.split(" ")[-1]
  return t2


def get_data(url):
  detail = {}
  rawdata = requests.get(url)
  soup = bs4.BeautifulSoup(rawdata.text, 'html.parser')
  place = soup.find('span', attrs={"class": "styles--locationName--1R6PN"})
  temp = soup.find('span', attrs={"class": "styles--temperature--3YaGV"})
  rain = soup.find('span',
                   attrs={
                     "class": "Accessibility--visuallyHidden--H7O4p"
                   }).parent
  highandlow = soup.find('div', attrs={"class": "CurrentConditions--tempHiLoValue--3T1DG"})

  detail["place"] = place.text
  detail["temparture"] = temp.text
  detail["rainy_possibility"] = rain.text
  detail["highandlow"] = highandlow.text
  detail = "地點:" + detail["place"] + " 現在溫度:" + detail[
    "temparture"] + detail["rainy_possibility"] + detail["highandlow"]
  return detail


def send_line(detail):
  token = 'AnPJWB64a7gdcskk2zw9E4h2FKrTOrPk3tXaAjheGn4'
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/x-www-form-urlencoded"
  }
  payload = {'message': detail}
  send_data = requests.post("https://notify-api.line.me/api/notify",
                            headers=headers,
                            params=payload)


if __name__ == "__main__":
#   keepalive.keep_alive()
  print(time.ctime())
  city = "台北"
  city_url = ""
  # city = input("請輸入您所在的城市\n")
  while (True):
    if city in place_list:
      city_url = place_list[city]
    # if int(get_hour()) + 8 == int(wakeuptime[get_date()]):
      send_line(get_data(city_url))
      time.sleep(3600)
