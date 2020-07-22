#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple Bot to reply to Telegram messages.
This is built on the API wrapper, see echobot2.py to see the same example built
on the telegram.ext bot framework.
This program is dedicated to the public domain under the CC0 license.
"""
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
import os
import logging
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
from telegram import ReplyKeyboardMarkup

TOKEN = os.getenv("BOT_TOKEN")

update_id = None


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def main():
     # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

     # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("yardim", start))
    dp.add_handler(CommandHandler("NedenGtu", nedenGtu))
    dp.add_handler(CommandHandler("ArastirmaOlanaklari", arastirmaOlanaklari))
    dp.add_handler(CommandHandler("MuhendisNedir", muhendisNedir))
    dp.add_handler(CommandHandler("MalzemeMuhendisi", malzemeMuhendisi))
    
    dp.add_handler(CommandHandler("KimlerMMOlabilir", kimlerMMOlabilir))
    dp.add_handler(CommandHandler("EgitimSureci", egitimSureci))
    dp.add_handler(CommandHandler("CalismaOrtami", calismaOrtami))
    dp.add_handler(CommandHandler("MMIsImkanlari", isImkanlari))

    dp.add_handler(CommandHandler("EgitimKadrosu", egitimKadrosu))
    dp.add_handler(CommandHandler("Lablar", lablar))
    dp.add_handler(CommandHandler("Burs", burs))
    dp.add_handler(CommandHandler("GTUIsImkanlari", gTUIsImkanlari))
    dp.add_handler(CommandHandler("Ulasim", ulasim))
    dp.add_handler(CommandHandler("Barinma", barinma))
    
    dp.add_handler(CommandHandler("Erasmus", erasmus))
    dp.add_handler(CommandHandler("Kulupler", kulupler))
    dp.add_handler(CommandHandler("OgrenciykenCalisma", ogrenciykenCalisma))
    dp.add_handler(CommandHandler("Basarilar", basarilar))
    dp.add_handler(CommandHandler("CiftveYanDal", ciftveYanDal))
    dp.add_handler(CommandHandler("EgitimDili", egitimDili))
    dp.add_handler(CommandHandler("Akreditasyon", Akreditasyon))
    dp.add_handler(CommandHandler("MetalurjiMalzeme", MetalurjiMalzeme))
    dp.add_handler(CommandHandler("KykYurt", KykYurt))
    dp.add_handler(CommandHandler("YatayGecis", YatayGecis))
    dp.add_handler(CommandHandler("HangiDiller", HangiDiller))
    dp.add_handler(CommandHandler("Siralama", Siralama))
    dp.add_handler(CommandHandler("KacYildaMezun", KacYildaMezun))




    dp.add_handler(CommandHandler("YokAtlas", yokAtlas))
    dp.add_handler(CommandHandler("GirisimciDestekleri", girisimciDestekleri))
    dp.add_handler(CommandHandler("IsBulmaOranlari", isBulmaOranlari))
    dp.add_handler(CommandHandler("KampusFotolari", kampusFotolari))
    dp.add_handler(CommandHandler("HangiBolumuSecmeliyim", hangiBolumuSecmeliyim))
    dp.add_handler(CommandHandler("GrupKurallari", grupKurallari))
    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text, start))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    PORT = int(os.environ.get('PORT', '8443')) 
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN) 
    updater.bot.set_webhook("https://gtumalzeme.herokuapp.com/" + TOKEN) 
    updater.idle()

    # Start the Bot
    # updater.start_polling()
    # updater.idle()
   
def start(bot, update):
    update.message.reply_text(
        "Gebze Teknik Universitesi Malzeme Muhendisligi Botuna Hos Geldiniz.\
        \n /NedenGtu - Neden GTU Malzeme Mühendisliği Secmeliyim?\
        \n /MuhendisNedir - Mühendis Nedir?\
        \n /MalzemeMuhendisi - Malzeme Mühendisi Nedir?\
        \n /KimlerMMOlabilir - Kimler Malzeme Mühendisi Olabilir?\
        \n /EgitimSureci - Eğitim Süreci\
        \n /CalismaOrtami - Çalışma ve İş Ortamları\
        \n /MMIsImkanlari - İş İmkanları\
        \n /EgitimKadrosu - Eğitim Karosu\
        \n /Lablar - Araştıma Labratuarları\
        \n /ArastirmaOlanaklari - Araştırma Olanakları\
        \n /Burs - Burslar\
        \n /Barinma - Yurt Olanakları\
        \n /GTUIsImkanlari - GTU İş İmkanları\
        \n /Ulasim - Ulaşım\
        \n /Erasmus - Erasmus\
        \n /OgrenciykenCalisma - Öğrenciyken Çalışma\
        \n /Kulupler - Okulumuz Öğrenci Kulüpleri Hakkında\
        \n /Basarilar - Başarılarımız\
        \n /CiftveYanDal - Çift Dal ve Yan Dal Olanakları\
        \n /EgitimDili - Eğitim Dili\
        \n /MetalurjiMalzeme - Metalurji ve Malzeme arasındaki fark nedir? \
        \n /Akreditasyon - Akreditasyon ve GTÜ hakkında\
        \n /YatayGecis - Yatay Geçişle İlgili Sorular\
        \n /KykYurt - KYK ve Genel Olarak Barınma için sorulan sorular\
        \n /HangiDiller - Hangi dilleri öğrenmeliyim \
        \n /YokAtlas - YÖK Atlas neden önceki yıllara ait başarı sıranızı göstermiyor? \
        \n /GirisimciDestekleri - Üniversitenin girişimci desteği var mı? \
        \n /IsBulmaOranlari - Mezunlarınızın iş bulma oranları ve süreleri nelerdir?\
        \n /KampusFotolari - Kampüsümüzden görüntüler\
        \n /HangiBolumuSecmeliyim - Malzeme Mühendisliğini mi seçmeliyim, XXXX Mühendisliğini mi seçmeliyim??\
        \n /Siralama - sıralama ile ilgili tahmin aralığı\
        \n /KacYildaMezun - Malzeme Mühendisliğinden mezun olma süresi\
        \n /GrupKurallari - Grubumuzun ufak kuralları \
        \n Adayları Bilgilendirme Grubu - https://t.me/GtuMalzemeMuhBot")
 
def welcome(bot, update):
    for new_user_obj in update.message.new_chat_members:
        chat_id = update.message.chat.id
        new_user = ""
        try:
            new_user = "@" + new_user_obj['username']
        except Exception as e:
            new_user = new_user_obj['first_name'];

        WELCOME_MESSAGE = "Merhaba " + str(new_user) + ", Gebze Teknik Universitesi Malzeme Muhendisligi Grubuna Hos Geldin! Bize kendini tanitmak ister misin? Seni tanimaktan memnuniyet duyariz 🙂. Ayrica merak ettigin konularda bilgi almak icin botumuzu 🤖 buradan @GtuMalzemeMuhBot ziyaret edebilirsin."

        bot.sendMessage(chat_id=chat_id, text=WELCOME_MESSAGE)


def nedenGtu(bot, update):
    
    update.message.reply_text('GTU konumu itibari ile GOSB, TÜBİTAK Serbest Bölge, KOSGEB ve benzeri bir çok AR-GE Merkezi alanında bulunmaktadır. Bu durum staj, mezuniyet öncesi ve sonrası iş olanakları sağlamaktadır. İstanbul’a yakın olması nedeniyle İstanbul’da ikamet etme ve çalışma olanağı sağlamaktadır. Öğrencilere yaptırılan projelerle sadece teorik bilgide kalmayan bunun yanında saha tecrübesi kazandıran bir eğitim verilmektedir. Bölümümüzdeki öğretim üyelerimiz kendi alanlarında yurtdışında saygın üniversitelerde doktora eğitimlerini tamamlamış ve önemli akademik başarılar edinmiştir. Aldıkları iyi eğitimi öğrencilere tüm çabalarıyla aktaran akademisyenlerimiz bir yandan da birçok ulusal ve uluslararası proje yürütmekte, bilimsel makalelerini yayınlamaktadır. Gebze Teknik Üniversitesinin Türkiye’nin en büyük sanayi bölgelerinden birinde bulunması ve sanayi kuruluşları ile birçok iş birliğine sahip olması özellikle mühendislik öğrencileri için gerek staj imkanları gerek üniversite sonrası iş hayatı için büyük bir avantajdır. Bölümümüzdeki öğretim üyelerimiz kendi alanlarında yurtdışında saygın üniversitelerde doktora eğitimlerini tamamlamış ve önemli akademik başarılar edinmiştir. Aldıkları iyi eğitimi öğrencilere tüm çabalarıyla aktaran akademisyenlerimiz bir yandan da birçok ulusal ve uluslararası proje yürütmekte, bilimsel makalelerini yayınlamaktadır. Gebze Teknik Üniversitesinin Türkiye’nin en büyük sanayi bölgelerinden birinde bulunması ve sanayi kuruluşları ile birçok iş birliğine sahip olması özellikle mühendislik öğrencileri için gerek staj imkanları gerek üniversite sonrası iş hayatı için büyük bir avantajdır.')

def Siralama(bot, update):
    
    update.message.reply_text('60k- 150k arasında bölümümüz tercih edilmektedir')

def KacYildaMezun(bot, update):
    
    update.message.reply_text('Tahmini mezun olması süresi 5 yıldır. (Hazırlıkla beraber) ')

def HangiDiller(bot, update):
    
    update.message.reply_text('İyi bir malzeme mühendisi İngilizce bilmelidir. Bunun dışında Almanca, Çince gibi dillere de yönelebilirler. ')

def arastirmaOlanaklari(bot, update):
    
    update.message.reply_text('Malzeme Mühendisliği bölümü olarak 29 adet laboratuvar ile araştırma çalışmalarını sürdürmekteyiz.\
            \n İnce Film Üretim Laboratuvarı - I-II \
            \n İnce Film Elektrik ve Optik Özellikler Ölçüm Laboratuvarı\
            \n Metal Laboratuvarı - I-II-III \
            \n Mühendislik Seramikleri ve Kompozitleri Araştırma Laboratuvarları \
            \n TEM ve SEM labları \
            \n X-Işını Kırınımı Laboratuvarı\
            \n Polimer Karakterizasyonu Laboratuvarı-I-II \
            \n Aygıt Tasarım, Benzetim, Üretim Ve Karakterizasyon Laboratuvarı \
            \n Hidrojen Teknolojileri Araştırma Laboratuvarı \
            \n Katı Oksit Yakıt Hücresi Araştırma Laboratuvarı \
            \n Temiz Oda Ve İnce Film Sentez Laboratuvarı \
            \n Metal Yüzeylerinin Modifikasyonu Laboratuvarı \
            \n Çalışma alanlarımız hakkında detaylı bilgi alabilmek için  : http://www.gtu.edu.tr/kategori/367/0/display.aspx?languageId=1 ')

def muhendisNedir(bot, update):
    
    update.message.reply_text('Mühendis; karmaşık yapıları, makineleri, ürünleri ve sistemleri tasarlayan, üreten ve test eden kişidir. Sistemlerin en verimli şekilde hizmet etmesi için gereksinimleri göz önüne alarak yeni yöntemler geliştirir.')

def malzemeMuhendisi(bot, update):
    
    update.message.reply_text('Malzeme Bilimi ve Mühendisi organik ve inorganik hammaddelerden metaller, seramikler,polimerler ve bunların karışımı olan kompozit malzemeleri hedefe ve amaca yönelik olarak tasarlayan ve üreten kişidir. Her devirde kullanılan teknoloji o devirdeki malzeme bilgisi ile sınırlı olacaktır. Bu nedenle malzeme bilimi ve mühendisleri her dönemde ihtiyaç duyulan kişiler olacaktır.')

def kimlerMMOlabilir(bot, update):
    
    update.message.reply_text('Malzeme Bilimi ve Mühendisi, endüstrinin, teknolojinin ve geleceğin ihtiyaç duyduğu malzemelerin tasarımını yapar. Çok geniş bir alana hakim olan bu mühendislik dalı diğer bütün mühendislik işlerinin yürütülebilmesi için en temel noktada bulunmaktadır. Örneğin bilgisayar teknolojisine yönelik ihtiyacı bilgisayar mühendisi belirliyor ve buna yönelik elektronik tasarımı elektrik-elektronik mühendisi yapıyorken, bu uygulamada kullanılacak malzemenin seçimini, tasarımını ve üretim yöntemini belirlemek malzeme bilimi ve mühendisinin işidir.')

def egitimSureci(bot, update):
    
    update.message.reply_text('Program, öğrencilerine temel Malzeme Bilimi ve Mühendisliği bilgisi ile malzeme tasarım ve özellikleri ile ilgili veriyi analiz edip yorumlayacak, deneyleri tasarlayıp yürütecek, malzeme karakteristik ve özellikleri ile ilgili mühendislik problemlerini tanımlayıp, formüle edecek yetileri kazandırmayı; gerek mühendislik mesleğini icra edebilecek gerekse üst derece programlarına geçiş yapabilecek mezunlar yetiştirmeyi amaçlamaktadır.\
        \n Detaylar için aşağıdaki sayfaları ziyaret edebilirsiniz. \
        \n Uzmanlık alan dersleri icin http://abl.gtu.edu.tr/ects/?duzey=ucuncu&modul=lisans_derskatalogu&bolum=101&tip=lisans \
        \n Tum dersler icin http://abl.gtu.edu.tr/ects/?duzey=ucuncu&menu=lisans_ogretimprogrami&bolum=101&tip=lisans ')


def calismaOrtami(bot, update):
    
    update.message.reply_text('Malzeme bilimi ve mühendisliği geniş bir alanda iş imkanına sahip olduğu için tek bir tanım söz konusu değildir. Bir demir-çelik firmasında yüksek sıcaklık şartları mevcutken, satış mühendisleri genel olarak ofiste çalışmaktadır. Kalite kontrol mühendisleri firmaların laboratuvarlarında çalışırken, üretim mühendisleri üretimin yapıldığı sahalarda çalışmaktadır.')

def isImkanlari(bot, update):
    
    update.message.reply_text('Malzeme bilimi temel olarak 4 ana grupta toplanmaktadır. Bunlar metaller, seramikler, polimerler ve kompozitlerdir. Malzeme Bilimi ve Mühendisi bu malzeme gruplarını içeren bütün noktalarda görev alabilmektedir. Örneğin, çelik parçalar üreten bir demir-çelik fabrikasında üretim mühendisi olarak çalışabileceği gibi pet şişe üreten bir plastik fabrikasında da çalışabilmektedir. Yer karosu üreten bir seramik fabrikasında çalışabileceği gibi cam malzemeler üreten bir kurumda da çalışabilmektedir. Malzeme Bilimi ve Mühendisi sadece üretim noktasında değil öncesi ve sonrasında da çok önemli görevler almaktadır. Bir firmanın yapacağı satın alımlar için malzemeyi bilen kişi olarak satın alma mühendisliği sık çalışılan pozisyonlardan biridir. Bunun yanında üretim sürecinde üretilen malzemelerin belirli kalite standartlarına uyup uymadığını kontrol eden kalite mühendisi pozisyonu da en önemli iş alanlarından biri durumundadır. Kalite mühendisliği pozisyonunda malzeme bilimi ve mühendisine talep olan sektörlerden biri otomotiv sektörüdür. Üretim sonrası çalışma pozisyonu olarak ise üretilen malzemeleri bilen ve bu nedenle satışını yapan satış mühendisi olarak da birçok pozisyon bulunmaktadır. Malzeme Bilimi ve Mühendisi, malzeme tasarlama, üretim yöntemlerini ve malzeme özelliklerini geliştirebilme yeteneklerine sahip olan kişidir. Bu nedenle en önemli iş alanlardan birisi Ar-Ge (Araştırma Geliştirme) ve Ür-Ge (Ürün Geliştirme) pozisyonlarıdır. Ar- Ge mühendisleri çoğunlukla firmaların laboratuvarlarında faaliyet göstermektedir.')

def KykYurt(bot, update):
    
    update.message.reply_text('Kyk yurduna çıkma ihtimali zor mudur? = Değildir KYK yurtlarında yer bulunmaktadır 3 kişilik odalara getirildi kontenjan artırılması için. Kyk Yurtları dışında Şifa mahallesi öğrencie evleri 2+1/3+1 650-750 lira arasındadır.\
            KYK yurdundan devlet otobüsyle ulaşım 45 dakika sürmekte ve aylık 70-80 lira tutmaktadır. Özel servis ile ulaşım 15 dakika sürmekte ve ücreti 150-160 lira arası değişmektedir.')


def egitimKadrosu(bot, update):
    
    update.message.reply_text('Yurtdışında eğitim almış ve farklı ekollerden gelen öğretim üyelerine sahiptir. http://www.gtu.edu.tr/kategori/353/12/display.aspx?languageId=1 linkinde detaylı bir şekilde öğretim üyelerine ait bilgiler verilmektedir.')


def lablar(bot, update):
    
    update.message.reply_text('Malzeme Bölümü bünyesinde 29 farklı alanda araştırmaların yürütüldüğü araştırma laboratuvarları bulunmaktadır.Bölümümüz laboratuvarlar açısından hem kendi bölgesinde hem de Türkiye genelindeki en iyi imkanlardan birine sahiptir. Bu laboratuvarlar hem çeşitli destekler hem de akademisyenlerimizin hazırladığı projeler sayesinde oldukça donanımlıdır. \
   \nAyrıntılı bilgi için http://www.gtu.edu.tr/kategori/367/0/display.aspx?languageId=1')


def burs(bot, update):
    
    update.message.reply_text('Net bir sayı verememekle birlikte çevredeki firmalar tarafından okul yönetiminin belirlediği öğrencilere burs imkânı sağlanmaktadır. \
        Detaylar icin: http://www.gtu.edu.tr/kategori/2460/0/display.aspx?languageId=1')

def barinma(bot, update):
    
    update.message.reply_text('Muallimköy Yerleşkesi’nin batısında Yükseköğrenim Kredi ve Yurtlar Kurumu’na tahsis edilen yerde yurdumuz 320 kız 440 erkek olmak üzere toplam 760 öğrenci kapasitesiyle hizmet vermektedir.\
        \nAyrıca üniversiteye yürüme mesafesinde öğrencilerin ev tutabileceği siteler bulunmaktadır. Aşağıdaki resimde mavi ile çizilmiş yerler İstanbul ve Gebze bölgesinde öğrencilerin yoğunlukla yaşadıkları yerlerdir.\
        \n Detaylar icin: http://www.gtu.edu.tr/kategori/2328/0/barinma-ve-yurtlar.aspx')

def gTUIsImkanlari(bot, update):
    
    update.message.reply_text('Üniversitemiz birçok Teknopark ve ARGE merkezine yakın olduğundan, bu çevredeki firmaların ilgi odağı halindedir. Birçok mezunumuz bu çevredeki firmalarda yarı-zamanlı veya tam-zamanlı olarak çalışmakta, yeni mezunlara da ön ayak olmaktadırlar.')


def ulasim(bot, update):
    
    update.message.reply_text('Ulasim imkanlarini gormek icin: http://www.gtu.edu.tr/icerik/926/629/ulasim-ve-iletisim.aspx')


def erasmus(bot, update):
    
    update.message.reply_text('Üniversitemiz Erasmus öğrenim hareketliliği programına dahildir ve en az 3 ay en fazla 12 ay olacak şekilde öğrencilere yurt dışı deneyimi, çok kültürlü ortamda ders işleme, değişik kültürleri tanıma, Türk kültürünü tanıtma, yeni arkadaşlar edinme, farklı bir okulda öğrenci olabilme ve farklı bir sistem görebilme olanakları kazandırır. GTU Bilgisayar Mühendisliği Fransa, İspanya, Almanya, Belçika, Polonya gibi bir çok farklı ülkedeki üniversitelere bu program ile öğrenciler göndermektedir.\
            Erasmus değişim programı olduğu için bölümün ile ilgili ders alıp 1 dönem veya 2 dönem farklı bir ülkede ve okulda eğitim görme fırsatı buluyorsun. Ülkede kaldığın süre zarfında gittiğin okulun eğitiminin yaninda geziyorsun farkı kültür görüyorsun, o ülkenin dilini ve kulturunu kendine katiyorsun ve büyük tecrübeler edinmiş oluyorsun. \
                    Dil konusunda gideceğin okula göre değişen bir durum oluyor bu. Bazı okullar kendi bulundukları ülkenin dilinde belirli bir seviyede olmanı isteyebiliyorlar ama bazı okullar için eğitim dilleri %100 ingilizce olduğundan dolayı sadece İngilizce yeterli olabiliyor. Benim gideceğim okulda Fransızca zorunluluğu yok mesela ben de bilmiyorum. Bu sayede hem Fransızca öğrenip kendimi geliştireceğim hem de İngilizcemi üst kademeye taşımış olacağım.\
Bunun yanında Erasmus stajı denen bir ayrı durum daha var burada da belirli bir süreliğine farklı bir ülkede stajini yapıyorsun. Bu programların hepsi devlet destekli oluyor. Gittiğin ülkeye göre ve erasmus için gireceğin sıralamana göre belirli bir miktar aylık hesaplama ile hibe aliyorsun. Genelde bizim okulda hibe almayan öğrenci kalmıyor. Bölümümüzün anlaşmalı okullar listesi için : http://www.gtu.edu.tr/kategori/1035/0/display.aspx?languageId=1 ')


def ogrenciykenCalisma(bot, update):
    
    update.message.reply_text('GTU İstanbul-Kocaeli il sınırında bulunan bir üniversite olduğu için hem İstanbul hem de Kocaeli ilinde bulunan şirketlere yakınlığı nedeniyle özellikle 3.sınıftan sonra üniversite de öğrenilen bilgileri iş hayatında uygulamaya koymak isteyen öğrencilere avantaj sağlamaktadır. Bu kapsamda bölümümüz TAİ, TEİ gibi firmalarda ücretli uzun dönem staj yapabilmektedirler. Öğrenciler için ders programında boş gün ve saatler ayarlanarak kısa zamanlı çalışmak isteyen öğrencilere kolaylıklar sunulmaktadır. Ayrıca bölümün dış destekli araştırma projelerinde öğrencilere çalışma fırsatları verilmektedir. Aynı zamanda hocalarımız lisans seviyesindeki öğrencileri projelerinde uygun pozisyonlara alıp onların teorik bilgilerini bir yandan da pratik olarak uygulamalarını sağlamakta, gelecek yıllar için bilimsel çalışma pratiğini kazandırmaktadır. ')

def kulupler(bot, update):
    
    update.message.reply_text('Üniversite içinde ki kulüpler teknik kulüpler ve sosyal kulüpler olmak üzere iki alanda çalışmalarını sürdürmektedirler. \
            \n Her bölümün kendine ait topluluğu bulunmakla beraber Robotik ve Otomasyon, Havacılık ve Uzay, SEDS Uzay ve Fizik , Savunma Teknolojileri, IEEE,Sosyal Yaşam ve Medya, Latin Dans Topluluğu, Fotoğrafçılık ve Kısa Film, Siber Güvenlik,Malzeme Mühendisliği Kulübü gibi kulüpler ile üyelerine ders dışı vakitlerini değerlendirme olanağı sağlamaktadır.\
            \n Kulüplerin kendi içlerinde oluşturduğu topluluklar sayesinde uluslarası yarışmalara katılım ve uluslararası TEKNOFEST,TUBITAK yarışmalarına katılım sağlanmaktadır. Aynı zamanda çeşitli seminer ve etkinlikler düzenlemektedirler. \
            \n Havacılık ve Uzay kulübü  ve Robotik kulüpleri içerisinde oluşan Model Uydu Takımları 2018 yılından beri NASA dahil olmak üzere Amerikan ve Avrupa yarışlarına katılmaktadır. Havacılık kulübünün IHA , Model Uçak takımları 2013 yılından beri çeşitli yarışmalarda sayısız ödül kazanmıştır.  Robotik otomasyon kulübü her sene değişik alanlarda eğitimler düzenlemek ve nisan aylarında geleneksel Robot olimpiyatları düzenlemektedir. Okul içerisinde GTU Roket kulübü adlı model roketçilik kulübü bulunmakta ve Türkiye Tayyare Derneği tarafından desteklenmektedir. Otonom Araç geliştirmek üzerine kurulan GTU HAZINE OTONOM araç takımı ise birebir boyut otonom araç tasarlamak ve bu konular üzerine çalışmaktadır. IEEE olarak sosyal yardımlaşma amaçlı robotlar tasarlanmaktadır. Ayrıca bu etkinlikler yanı sıra haftalık latin dans geceleri ve fotoğrafçılık gezileri olmaktadır. ')

def basarilar(bot, update):
    
    update.message.reply_text('Basarilarimi gormek icin: http://www.gtu.edu.tr/icerik/8/4200/display.aspx?languageId=1')

def MetalurjiMalzeme(bot, update):
    
    update.message.reply_text('Metalurji, malzeme biliminin içerisinde bulunan metaller dalına verilen addır ve metal bilimi anlamına gelmektedir. Malzeme bilimi bütün malzeme gruplarını ve dolayısıyla metalurjiyi de kapsamaktadır. Ülkemizde birçok demir-çelik firması bulunmaktadır ve bazı okullar bu nedenle metalurji mühendisliği adını kullanmaktadır. Dünya genelinde ise bu meslek “Malzeme Bilimi ve Mühendisliği” olarak tanımlanmıştır. Ülkemiz şartlarında, "metalurji  ve malzeme mühendisleri" ile "malzeme bilimi ve mühendisleri", hem devlette hem de özel sektörde aynı hak, şart ve vasıflarda çalışabilmektedir.')


def ciftveYanDal(bot, update):
    
    update.message.reply_text('Üniversitemiz belirli not ortalamasını sağlayan öğrencilere çift anadal ve yandal programları ile ikinci bir diploma veya sertifika olanağı sağlanmaktadır. Öğrenciler ilan edilen (Elektronik Mühendisliği, Malzeme Bilimi ve Mühendisliği gibi) yandal ve çiftanadal programına anadal lisans programının 3. ve 5. döneminde başvurabilir.')

def egitimDili(bot, update):
    
    update.message.reply_text('Malzeme Mühendisliğinde eğitim dili en az %30 İngilizcedir. Öğrenciler eğitime başlamadan önce 1 yıl İngilizce hazırlık kursu görmektedirler. İngilizceleri yeterli olan öğrenciler kursa başlamadan önce İngilizce hazırlık geçiş sınavına girerek, bu kurstan muaf olarak eğitime başlama hakkına sahiptir.')

def Akreditasyon(bot, update):
    
    update.message.reply_text('Akreditasyon çalışmaları başlamış bulunmaktadır. Önümüzdeki birkaç sene içerisinde ABET akreditasyonu alınması planlanmaktadır.')

def YatayGecis(bot, update):
    
    update.message.reply_text('Merhabalar ben yatay geçiş süreciyle yerleşen bir arkadaşım , merkezi yerleştirme puanı ile yatay geçiş yapacaklar için yaşadığım süreçten ve Gtü malzemeyi neden tercih ettiğimden kısaca bahsedeceğim. Benim zamanımda Lys ve Ygs olduğu için puan türü farklı olabilir ancak MF-4 ile geçiş yapmıştım, okulun açtığı kontenjan kadar kişi puan sıralaması doğrultusunda kabul ediliyor. Benimle beraber 2015 senesinde 3 kişi daha geçiş yapmıştı yani kontenjan 4 diye düşünüyorum. Hazırlık okuma durumu-Eğer okulunuzdan geçerli bir yabancı dil belgeniz var ise yani daha önce hazırlık okuyup başarı ile geçtiyseniz burada hazırlık okumanıza gerek kalmıyor. Ancak Türkçe bir bölümden geçiyorsanız, maalesef GTÜ’de hazırlık sınavını geçmelisiniz. Ders saydırma - Okulunuzun size verdiği havuz derslerinin(Mat,Fizik,Türkçe vb.) CC ve daha üstü olanlarını geçiş yaptığınızda saydırabilirsiniz.\
    \n Yatay geçiş yaparken istenen belgeler içerisinde, önceki okulunuzdan başarı ile geçtiğiniz derslerin dökümünü çıkartmanız istenmektedir. Bölüm dersleri için ise tavsiyem, tamamını GTÜ’den almanızdır. İki üniversite görmüş biri olarak söylemeliyim ki, ders içerikleri ve niteliği çok farklı oluyor. Neden GTÜ bilgisayar -Eğitiminiz sadece derste kalmıyor, verilen ödevler ve projeler ile hem derste işlenen konu pekişmiş oluyor hem de sizi iş hayatının yoğunluğuna hazırlanmış oluyorsunuz. Belki okul eğitiminde ağırlıklı olarak console eğitimi verilse de, öğrencilerin çoğu yaz tatillerinde ya da mezun olduktan sonra web, mobil gibi popüler alanlara kolaylıkla kayabilecek yeterlilikte ve özgüvende oluyorlar.\
    \n Ayrıca öğrenciler çok rahat bir biçimde 3. ve 4. sınıfta okurken çalışabilecekleri gibi, mezun olur olmaz rahatlıkla iş bulabiliyorlar. Kötü yanları peki? -Gerçekten vaktinizin çoğunu okul alacak, bunu göze almalısınız. Ben çok hafta biliyorum, 4 ödev teslim ettiğim oldu bu da neredeyse hiçbir günün bana kalmaması anlamına geliyordu. Ayrıca okulun Gebze’de olması da bir dezavantaj olarak görülebilir ancak şanslısınız ki Marmaray açıldı :) . Nasıl Girebiliriz - \
    \n Arkadaşlar yatay geçiş her üniversiteden yapılabilir fakat 2 çeşit yatay geçiş var biri önceki seneler puanı tuttuğu halde yazmayıp sonradan geçmeyi düşünenler için(merkezi yatay geçiş) diğeri ortalama ile yatay geçiş bunun içinde belli bir ortalamanın üstünde olup başvuruyorsunuz tabi başka kriterlere de bakılabilir o dönem başvuranlar arasında listeye alınıyorsunuz eğer şartları(yaptığınız GNO,girdiğiniz sene ki sınav puanı gibi katmanların belli katsayılarla çarpılıp size puan çıkarılması) sağlarsanız ve kontenjana girerseniz geçebilirsiniz . Tüm üniversitelerde böyle bu olay , ders denklik olayı ayrı bir olay tabi')


def yokAtlas(bot, update):
    
    update.message.reply_text('Bölümümüz 2018 yılında Ingilizce eğitime başladığı için daha önceki yıllarda elde edilen başarı sıralamaları tercih kılavuzunda yer almamaktadır. Bölümümüz başarı sıralamaları için http://www.gtu.edu.tr/kategori/1730/0/display.aspx?languageId=1 adresindeki yıllara göre başarı sıralamaları grafiğini inceleyebilirsiniz.')

def girisimciDestekleri(bot, update):
    
    update.message.reply_text('GTÜ Teknoloji Transfer Merkezi bu konuda hizmet vermektedir http://gebzettm.com/birimler/girisimcilik-ve-kulucka Ilgili haber için http://www.sanayigazetesi.com.tr/ar-ge/tirtil-girisimci-kelebege-donusuyor-h17468.html')

def isBulmaOranlari(bot, update):
    
    update.message.reply_text('Gebze Teknik Üniversitesi Malzeme Bilimi ve Mühendisliği Bölümü mezunlarımızın, mezun olduktan sonraki ilk 1 sene içerisinde istihdam edilme oranı %75 tir.Bu konuda yapılmış bazı anketlere göre Türkiye\'nin en iyileri arasındayız. Ilgili bağlantı http://calibre.kyyd.org.tr/EniyiUniversiteler.aspx')



def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def grupKurallari(bot, update):
     update.message.reply_text('1) İlk olarak kendinizi lütfen tanıtınız. Aday iseniz, isim sıralama bizim için yeterlidir.\
                                \n2) Üniversite öğrencisi/görevlisi iseniz, isim sınıf veya göreviniz vs. (esktralar sizden 🙂)\
                                \n3) Üniversite mezunu iseniz, çalıştığınız kurum ve pozisyon (ekstralar sizden 🙂)\
                                \n4) Mesajlarımızı yazarken lütfen bir metin halinde gönderelim. Bir kaç kelime yazıp "enter" basmak gruptaki çalışanları düşününce çok hoş bir durum olmuyor, grubun sessize alınmasını istemeyiz 🙂\
                                \n5) Grupta profesöründen bölüm öğrencisine kadar insanlar olduğunu unutmayıp saygı ve sevgi çerçevesini bozmayalım. (Bozanlar gruptan 1. uyarıdan sonra nazikçe çıkarılacaktır.)\
                                \n6) Grupta sizleri bilgilendirmek için varız. Grup kurulduğu günden itibaren mesajları görmeniz mümkündür. Bu yüzden aratma opsiyonunu kullanarak tek kelimelik aramalar ile sorunuzun cevabına ulaşabilirsiniz. Bulamazsanız cevaplamak için buradayız zaten 🙂')

def kampusFotolari(bot,update):
    update.message.reply_text('Kampus fotolarını sitemizden görmek icin: http://www.gtu.edu.tr/kategori/2362/0/display.aspx?languageId=1 \n')

def hangiBolumuSecmeliyim(bot,update):

    update.message.reply_text("Bu soru bana çok soruluyor ve cevaplaması gerçekten çok zor. İyi bir eğitim almış malzeme mühendisinin hem Türkiye'de hem de yurt dışında iyi iş bulacağı herkes tarafından kabul ediliyor. Bu konuda yapılan istatistikler hep bu yönde. \
        \nFakat bu herkes malzeme mühendisi olmalıdır manasına gelmiyor tabi ki, eğer yetenekleriniz ve planlarınınız XXXX mühendisliği yönünde ise tabi ki XXXX mühendisi olun derim. Ancak kararınız bilinçli olmalı, iyi bir araştırmaya dayalı olmalı. Üniversite tercih aşamasında bu türlü bir kararı vermek hiç te kolay değil, bunu herkes biliyor. O nedenle bu ikilemde kalan adaylara şunu öneriyorum. Eğer malzeme mühendisliği ve XXXX mühendisliği arasında ikilemdeyseniz, GTÜ Malzeme Mühendisliği bölümünü tercih edin. \
        \nİlk yıl okuyun, size çok iyi temel mühendislik ve alan dersi vereceğiz. Bu arada bir malzeme mühendisinin ne yaptığını yavaş yavaş anlamış olacaksınız. Eğer yıl sonunda hala XXXX mühendisi olmak istiyorsanız, o zaman hemen dilekçenizi vererek merkezi yatay geçiş (http://www.yok.gov.tr/documents/7701936/7719456/yataygeci%C5%9Fpdf.pdf/) kontenjanlarından Türkiye'de istediğiniz üniversiteye yatay geçiş yapabilirsiniz, tabi ki tercih yaptığınız dönemde o bölüme YKS puanınızın yetmesi gerekiyor. \
        \nBu şekilde eğer bilgisayar mühendisi olmak isterseniz bir kaybınız olmaz, eğer XXXX olmak isterseniz, temel bilim dersleriniz yeni bölümünüzde saydırırsınız, yıl kaybınız olmaz. \
        \nMerkezi yatay geçiş için herhangi bir sınırlama yok (ortalama, not ve devam durumu, sınıf, kontenjan, fakülte farkı vb.) Sadece söylediğim gibi tercih yaptığınız dönemde o bölüme YKS puanınızın yetmesi gerekiyor. Bölümüze her sene çok sayıda merkezi yatay geçiş öğrencisi geliyor ve aynı zamanda çok sayıda öğrenci de ayrılıyor. Merkezi yatay geçiş bence YÖK'ün son yıllarda devreye aldığı en güzel uygulama. Başlangıçta yapılan tercih yanlışlıklarının büyük kısmını gideriyor.")


if __name__ == '__main__':
    main()
