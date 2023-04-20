import coloredlogs
import requests
import datetime
import logging
import time
import json
import os

os.system('cls')
os.system('TITLE Fortnite Sections Bot by Liqutch')
coloredlogs.logging.basicConfig(level=coloredlogs.logging.INFO)
log = coloredlogs.logging.getLogger(__name__)
coloredlogs.install(fmt="[%(asctime)s][%(levelname)s] %(message)s", datefmt="%H:%M:%S", logger=log)

if not os.path.isfile('settings.json'):       
  log.error('Ayarlar dosyası bulunamadı, program kapatılıyor...')
  time.sleep(5)
  exit()

with open("settings.json", encoding="utf-8") as f:
  data = json.load(f)
  lastcheck = datetime.datetime.fromisoformat(data["last_check"][:-1])
  checkrate = data["checkrate"]
  lang = data["language"]
  title = data["title"]
  isEmbed = data["embed"]
  embedTitle = data["embed_settings"]["embed_title"]
  footer = data["embed_settings"]["footer"]
  timestamp = data["embed_settings"]["timestamp"]
  webhook = data["webhook_url"]
  account_id = data["account_id"]
  device_id = data["device_id"]
  secret = data["secret"]

now = datetime.datetime.now()
reflesh = False
def refleshToken():
  url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
  body = f"grant_type=device_auth&account_id={account_id}&device_id={device_id}&secret={secret}"
  headers = {
    "Authorization":
    "basic M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU=",
    "Content-Type": "application/x-www-form-urlencoded"
  }
  response = requests.post(url, data=body, headers=headers)
  if response.status_code == 400:
    if reflesh == False:
      log.error("Token oluşturulamadı. Lütfen bilgilerinizi kontrol edin.")
    elif reflesh == True:
      log.error("Token yenilenemedi. Lütfen bilgilerinizi kontrol edin.")
    time.sleep(5)
    exit()
  if response.status_code == 200:
    if reflesh == False:
      log.info("Token başarıyla oluşturuldu.")
    elif reflesh == True:
      log.info("Token başarıyla yenilendi.")
    return response.json()["access_token"]
token = refleshToken()
reflesh = True
tokentime = now
while True:
  with open("settings.json") as f:
    data = json.load(f)
    lastcheck = datetime.datetime.fromisoformat(data["last_check"][:-1])
    checkrate = data["checkrate"]
  now = datetime.datetime.now()
  if (now - tokentime).total_seconds() >= 3600:
    token = refleshToken()
  try:
    calendar = requests.get("https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/calendar/v1/timeline", headers={"Authorization": f"Bearer {token}"})
    sectionIds = calendar.json()["channels"]["client-events"]["states"][1]["state"]["sectionStoreEnds"].keys()
    dailyStoreEnd = calendar.json()["channels"]["client-events"]["states"][1]["state"]["dailyStoreEnd"]
    StoreEnd = datetime.datetime.fromisoformat(dailyStoreEnd[:-1])
    if lastcheck != StoreEnd:
      log.info("Yeni sekmeler algılandı!")
      content = requests.get(f"https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game/shop-sections?lang={lang}")
      sectionList = content.json()["sectionList"]["sections"]
      sections = []
      for key in sectionIds:
        if key in ["Featured2", "Featured3", "Featured4"]:
          key = "Featured"
        if key == "Daily2":
          key = "Daily"
        if key == "Special2":
          key = "Special"
        sections.append(key)

        names = []
        for section in sectionList:
          if section["sectionId"] in sections:
            for item in sections:
              if section["sectionId"] == item:
                names.append(section["sectionDisplayName"])

        counts = {}
        for name in names:
          counts[name] = counts.get(name, 0) + 1

        displayNames = []
        for name, count in counts.items():
          displayNames.append(f"- {name} (x{count})")
      if isEmbed == True:
        body = {
          "content": None,
          "embeds": [
            {
              "title": embedTitle,
              "description": "\n".join(displayNames),
              "footer": {
                "text": footer
              },
              "color": None,
              "timestamp": now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            }
          ],
          "attachments": []
        }
        if embedTitle == None or embedTitle == "":
          del body["embeds"][0]["title"]    
        if footer == None or footer == "":
          del body["embeds"][0]["footer"]       
        if timestamp == False or timestamp == "":
          del body["embeds"][0]["timestamp"] 
      else:
        body = {
          "content": f"{title}\n\n" + "\n".join(displayNames),
          "embeds": None,
          "attachments": []
        }
      request = requests.post(webhook, data=json.dumps(body), headers={"Content-Type": "application/json"})
      if request.status_code == 204:
        log.info("Webhook gönderildi.")
      else:
        log.error("Webhook gönderilirken bir hata oluştu.")
      with open("settings.json", "w") as f:
        data["last_check"] = dailyStoreEnd
        json.dump(data, f, indent=2, ensure_ascii=False)
    else:
      log.info("Yeni sekmeler kontrol ediliyor.")
  except IndexError:
    log.info("Yeni sekmeler kontrol ediliyor.")
  except Exception as e:
    log.error(f"Kontrol edilirken bir hata oluştu: {e}")
    continue
  time.sleep(checkrate)
