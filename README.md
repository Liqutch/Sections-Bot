# Fortnite Sections Bot
Fortnite'da günlük içerik mağazası sekmelerini tespit eden ve bunları otomatik olarak bir Discord webhook'u aracılığıyla paylaşan bir bot.

# Gereksinimler
- [Python](https://www.python.org/downloads/) 3.6 ve üstü bir sürümün yüklü ve PATH'e eklenmiş olduğundan emin olun.
- `packages.bat` adlı dosyayı çalıştırarak gerekli modülleri yükleyin veya aşağıdaki satırları komut istemcisine yazın.
```
pip install coloredlogs
pip install requests
pip install logging
```
# Yapılandırma
- Sekmeleri bir Discord sunucunuzda paylaşmak için seçtiğiniz kanalda, entegrasyonlar üzerinden bir webhook oluşturun ve bu webhook URL'sini kopyalayıp, `setting.json` içerisindeki "webhook_url" anahtarına giriniz.
- `settings.json` dosyası içerisinde, girmeniz gereken "Account ID", "Device ID" ve "Secret" gibi hesabınıza dair bilgiler girmeniz istenecektir.
Bu bilgiler, Fortnite'ın içerik mağazası sekmelerinin bulunduğu Calendar program arayüzüne erişmeniz için gereklidir.
Bu bilgileri elde etmek için [xMistt](https://github.com/xMistt) tarafından yapılan [DeviceAuthGenerator](https://github.com/xMistt/DeviceAuthGenerator) projesine göz atabilirsiniz.
- "language", "title" gibi özelleştirilebilir değerleri düzenleyebilirsiniz. Eğer paylaşımın bir embed içerisinde yapılmasını isterseniz, "embed" değerini `true` olarak değiştirin.
- Not: "checkrate" değeri, kontrol sıklığını saniye cinsinden ayarlamaktadır. 10 saniyeden düşük bir değer girmemelisiniz!
## Örnek
```json
{
  "last_check": "2023-04-21T00:00:00Z",
  "checkrate": 30,
  "webhook_url": "WEBHOOK_URL",
  "account_id": "ACCOUNT_ID",
  "device_id": "DEVICE_ID",
  "secret": "SECRET",
  "language": "tr",
  "title": "İçerik Mağazası Sekmeleri",
  "embed": true,
  "embed_settings": {
    "embed_title": "İçerik Mağazası Sekmeleri",
    "footer": "Bot - Liqutch#7777",
    "timestamp": true
  }
}
```
# Yardım
Eğer bir problemle karşılaşıyorsanız, aşağıdaki bağlantılardan yardım alabilirsiniz.
- [Twitter](https://twitter.com/Liqutch)
- [Discord](https://discord.gg/nNPrQeqCyf)
- [İletişim](https://liqutch.dev/)
