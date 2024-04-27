import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from sms import SendSms
import requests,random,string,datetime
import mysql.connector
from concurrent.futures import ThreadPoolExecutor, wait
from datetime import datetime,timedelta
# Bot token
TOKEN = '7111833978:AAF1ndQVeMcinL6VonxdgGgE9Sg1fzv-yDs'  # BOT_TOKEN değerini kendi bot token'ınızla değiştirin
# MySQL bağlantısı oluştur
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="liberal"
)
bot = telebot.TeleBot(TOKEN)
# Kullanıcı ekleme işlemini gerçekleştiren fonksiyon



cursor = conn.cursor(buffered=True)
def add_users(username, ekleyen, k_key):
    try:
        cursor.execute("INSERT INTO sh_kullanici (k_rol, k_adi, k_key, k_ekleyen, k_time, k_verified, k_log, u_time, k_browser, k_os, k_lastlogin, k_cooldown, k_cooldown_bypass, last_login, k_balance, k_image, tg_id) VALUES (%s, %s, %s, %s, '', %s, '', '', '', '', '', '', '', '', '0', '', NULL)", ('0', username, k_key, ekleyen, 'true'))

        conn.commit()
    except Exception as e:
        print("add_users fonksiyonunda bir hata oluştu:", str(e))

@bot.message_handler(commands=['start'])
def start(message):
    global tg_id
    tg_id = message.chat.id
    buttons_page1 = [
        InlineKeyboardButton('Üyeliğini Doğrula ✅', callback_data='doğrula'),
        InlineKeyboardButton('TC Sorgu 🕵️‍♂️', callback_data='tc_sorgu'),
        InlineKeyboardButton('TC=>GSM Sorgu ☎️', callback_data='tcgsm_sorgu'),
        InlineKeyboardButton('GSM=>TC Sorgu ☎️', callback_data='gsmtc_sorgu'),
        InlineKeyboardButton('Detaylı Aile Sorgu 👨‍👩‍👧', callback_data='detayliaile_sorgu'),
        InlineKeyboardButton('Soy Ağacı Sorgu👨‍👩‍👧', callback_data='soyagaci_sorgu'),
        InlineKeyboardButton('»', callback_data='next_page')  # İkinci sayfaya geçmek için buton
    ]

    # İlk sayfa için InlineKeyboardMarkup oluştur
    markup_page1 = InlineKeyboardMarkup(row_width=2)  # Her satırda 2 buton
    markup_page1.add(*buttons_page1)

    bot.reply_to(message, """Theos Panel Bot Satın almak için kayıt olmanız Gerekmektedir.
Kayıt işlemi @emreklasic üzerinden oluyor

Lütfen kaydınızı yapmadan gelip botu yormayın bı açık bulup sorgu atarım demeyin açık yok""",reply_markup=markup_page1)

@bot.callback_query_handler(func=lambda call: call.data == 'next_page')
def next_page(call):
    tg_id=call.message.chat.id
    cursor.execute("SELECT k_rol FROM sh_kullanici WHERE tg_id = %s", (tg_id,))
    user = cursor.fetchone()
    buttons_page2 = [
        InlineKeyboardButton('Tc Pro Sorgu 😈', callback_data='tcpro_sorgu'),
        InlineKeyboardButton('Ad Soyad Sorgu 🤐', callback_data='adsoyad_sorgu'),
        InlineKeyboardButton('GSM=>TC Sorgu (270M) ☎️', callback_data='gsmtcpro_sorgu'),
        InlineKeyboardButton('TC=>GSM Sorgu (270M) ☎️', callback_data='tcgsmpro_sorgu'),
        InlineKeyboardButton('Hane Sorgu 🏡', callback_data='hane_sorgu'),
        InlineKeyboardButton('Adres Sorgu 🏠', callback_data='adres_sorgu'),
        InlineKeyboardButton('SmS Bomber 💣', callback_data='sms_bomber'),
        *([InlineKeyboardButton('Kullanıcı Ekle 👥', callback_data='add_user')] if (user and user[0] == '1') else []),
        *([InlineKeyboardButton('Kullanıcı Düzenle 👥', callback_data='edit_user')] if (user and user[0] == '1') else []),
        InlineKeyboardButton('«', callback_data='previous_page')  # İlk sayfaya geri dönmek için buton
    ]

    # İkinci sayfa için InlineKeyboardMarkup oluştur
    markup_page2 = InlineKeyboardMarkup(row_width=2)  # Her satırda 2 buton
    markup_page2.add(*buttons_page2)

    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup_page2)

@bot.callback_query_handler(func=lambda call: call.data == 'previous_page')
def previous_page(call):
    # İlk sayfa butonları
    buttons_page1 = [
        InlineKeyboardButton('Üyeliğini Doğrula ✅', callback_data='doğrula'),
        InlineKeyboardButton('TC Sorgu 🕵️‍♂️', callback_data='tc_sorgu'),
        InlineKeyboardButton('TC=>GSM Sorgu ☎️', callback_data='tcgsm_sorgu'),
        InlineKeyboardButton('GSM=>TC Sorgu ☎️', callback_data='gsmtc_sorgu'),
        InlineKeyboardButton('Detaylı Aile Sorgu 👨‍👩‍👧', callback_data='detayliaile_sorgu'),
        InlineKeyboardButton('Soy Ağacı Sorgu👨‍👩‍👧', callback_data='soyagaci_sorgu'),
        InlineKeyboardButton('»', callback_data='next_page')  # İkinci sayfaya geçmek için buton
    ]

    # İlk sayfa için InlineKeyboardMarkup oluştur
    markup_page1 = InlineKeyboardMarkup(row_width=2)  # Her satırda 2 buton
    markup_page1.add(*buttons_page1)

    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup_page1)




@bot.callback_query_handler(func=lambda call: call.data == 'doğrula')

def doğrula(call):
    try:
        tg_id = call.message.chat.id
        # MySQL'den kullanıcıyı sorgula
        cursor.execute("SELECT * FROM sh_kullanici WHERE tg_id = %s", (tg_id,))
        kullanici = cursor.fetchone()
       
        if kullanici:
           
                bot.send_message(call.message.chat.id, "Doğrulama zaten yapıldı.")
        else:
            bot.send_message(call.message.chat.id, "Lütfen kullanıcı adınızı ve şifrenizi girin (kullanıcı_adı şifre).")
            bot.register_next_step_handler(call.message, process_kullanici_step)
    except Exception as e:
        bot.reply_to(call.message, 'Üzgünüm, bir hata oluştu: {}'.format(str(e)))
def process_kullanici_step(message):
    try:
        kullanici_bilgileri = message.text.split()
        if len(kullanici_bilgileri) != 2:
            raise Exception("Kullanıcı adı ve şifre girilmedi!")
       
        kullanici_adi, sifre = kullanici_bilgileri
       
        # MySQL'den kullanıcıyı sorgula
        cursor.execute("SELECT * FROM sh_kullanici WHERE k_adi=%s AND k_key=%s", (kullanici_adi, sifre))
        kullanici = cursor.fetchone()
       
        if kullanici:
            tg_id = message.chat.id
            if kullanici[8]=='false':
                bot.send_message(message.chat.id, "Hesabınız Banlı lütfen yetkili ile iletişime geçiniz @emreklasic.")
            elif kullanici[8]=='true':
                if kullanici[17] is None:
                    cursor.execute("UPDATE sh_kullanici SET tg_id = %s WHERE k_adi = %s", (tg_id, kullanici_adi))
                    conn.commit()
                    bot.send_message(message.chat.id, "Doğrulama başarılı! Artık sorguları kullanabilirsiniz.")
                else:
                    bot.send_message(message.chat.id, "Bu hesap zaten başka bir hesaba bağlı.")
        else:
            bot.send_message(message.chat.id, "Doğrulama başarısız! Lütfen doğru kullanıcı adı ve şifreyi girin.")
    except Exception as e:
        bot.reply_to(message, 'Üzgünüm, bir hata oluştu: {}'.format(str(e)))


@bot.callback_query_handler(func=lambda call: call.data == 'add_user')
def add_user(call):
                try:
                    tg_id = call.message.chat.id
                    cursor.execute("SELECT tg_id FROM sh_kullanici WHERE tg_id = %s", (tg_id,))
                    user = cursor.fetchone()
                    if user:
                        bot.send_message(call.message.chat.id, "Lütfen Kullanıcı Adını Girin.")
                        bot.register_next_step_handler(call.message, process_adduser_step)
                    else:
                        bot.send_message(call.message.chat.id, "Lütfen önce üyeliğinizi doğrulayınız. Üyeliğiniz yoksa satın almak için @emreklasic ile iletişime geçiniz.")
                except Exception as e:
                    bot.send_message(call.message.chat.id, "Bir hata oluştu: {}".format(str(e)))
@bot.callback_query_handler(func=lambda call: call.data == 'edit_user')
def edit_user(call):
                try:
                    tg_id = call.message.chat.id
                    cursor.execute("SELECT tg_id FROM sh_kullanici WHERE tg_id = %s", (tg_id,))
                    user = cursor.fetchone()
                    if user:
                        bot.send_message(call.message.chat.id, "Lütfen Kullanıcı Adını Girin.")
                        bot.register_next_step_handler(call.message, process_edituser_step)
                    else:
                        bot.send_message(call.message.chat.id, "Lütfen önce üyeliğinizi doğrulayınız. Üyeliğiniz yoksa satın almak için @emreklasic ile iletişime geçiniz.")
                except Exception as e:
                    bot.send_message(call.message.chat.id, "Bir hata oluştu: {}".format(str(e)))

@bot.callback_query_handler(func=lambda call: call.data == 'hane_sorgu')
def hane_sorgu(call):
    try:
        tg_id = call.message.chat.id
       
        cursor.execute("SELECT tg_id FROM sh_kullanici WHERE tg_id = %s", (tg_id,))
        user = cursor.fetchone()
       
        if user:
            bot.send_message(call.message.chat.id, "Lütfen TC değerini girin.")
            bot.register_next_step_handler(call.message, process_hane_step)
        else:
            bot.send_message(call.message.chat.id, "Lütfen önce üyeliğinizi doğrulayınız. Üyeliğiniz yoksa satın almak için @emreklasic ile iletişime geçiniz.")
    except Exception as e:
        bot.send_message(call.message.chat.id, "Bir hata oluştu: {}".format(str(e)))

@bot.callback_query_handler(func=lambda call: call.data == 'adres_sorgu')
def adres_sorgu(call):
    try:
        tg_id = call.message.chat.id
       
        cursor.execute("SELECT tg_id FROM sh_kullanici WHERE tg_id = %s", (tg_id,))
        user = cursor.fetchone()
       
        if user:
            bot.send_message(call.message.chat.id, "Lütfen TC değerini girin.")
            bot.register_next_step_handler(call.message, process_adres_step)
        else:
            bot.send_message(call.message.chat.id, "Lütfen önce üyeliğinizi doğrulayınız. Üyeliğiniz yoksa satın almak için @emreklasic ile iletişime geçiniz.")
    except Exception as e:
        bot.send_message(call.message.chat.id, "Bir hata oluştu: {}".format(str(e)))

@bot.callback_query_handler(func=lambda call: call.data == 'tcgsmpro_sorgu')
def tcgsmpro_sorgu(call):
    try:
        tg_id = call.message.chat.id
       
        cursor.execute("SELECT tg_id, k_balance FROM sh_kullanici WHERE tg_id = %s", (tg_id,))
        user = cursor.fetchone()
        if user:
            k_balance = user[1]
            if k_balance < 20:
                bot.send_message(call.message.chat.id, "Bakiye yetersiz. Lütfen bakiyenizi yükseltin.")
            else:
                bot.send_message(call.message.chat.id, "Lütfen TC değerini girin.")
               
                bot.register_next_step_handler(call.message, process_tcgsmpro_step)
        else:
            bot.send_message(call.message.chat.id, "Lütfen önce üyeliğinizi doğrulayınız. Üyeliğiniz yoksa satın almak için @emreklasic ile iletişime geçiniz.")
    except Exception as e:
        bot.send_message(call.message.chat.id, "Bir hata oluştu: {}".format(str(e)))

           
@bot.callback_query_handler(func=lambda call: call.data == 'tcgsm_sorgu')
def tcgsm_sorgu(call):
    try:
        tg_id = call.message.chat.id
       
        cursor.execute("SELECT tg_id FROM sh_kullanici WHERE tg_id = %s", (tg_id,))
        user = cursor.fetchone()
       
        if user:
            bot.send_message(call.message.chat.id, "Lütfen TC değerini girin.")
            bot.register_next_step_handler(call.message, process_tcgsm_step)
        else:
            bot.send_message(call.message.chat.id, "Lütfen önce üyeliğinizi doğrulayınız. Üyeliğiniz yoksa satın almak için @emreklasic ile iletişime geçiniz.")
    except Exception as e:
        bot.send_message(call.message.chat.id, "Bir hata oluştu: {}".format(str(e)))
   
@bot.callback_query_handler(func=lambda call: call.data == 'gsmtcpro_sorgu')
def gsmtcpro_sorgu(call):
        tg_id = call.message.chat.id
       
        cursor.execute("SELECT tg_id, k_balance FROM sh_kullanici WHERE tg_id = %s", (tg_id,))
        user = cursor.fetchone()
        if user:
            k_balance = user[1]
            if k_balance < 20:
                bot.send_message(call.message.chat.id, "Bakiye yetersiz. Lütfen bakiyenizi yükseltin.")
            else:
                bot.send_message(call.message.chat.id, "Lütfen Telefon Numarası değerini girin. (Başında 0 olmasın example: 5555555555)")
                bot.register_next_step_handler(call.message, process_gsmtcpro_step)
        else:
            bot.send_message(call.message.chat.id, "Lütfen önce üyeliğinizi doğrulayınız. Üyeliğiniz yoksa satın almak için @emreklasic ile iletişime geçiniz.")

@bot.callback_query_handler(func=lambda call: call.data == 'sms_bomber')
def sms_bomber(call):
      tg_id = call.message.chat.id
       
      cursor.execute("SELECT tg_id FROM sh_kullanici WHERE tg_id = %s", (tg_id,))
      user = cursor.fetchone()
       
      if user:
        bot.send_message(call.message.chat.id, "Lütfen Telefon Numarası değerini girin. (Başında 0 olmasın example: 5555555555)")
        bot.register_next_step_handler(call.message, process_smsbomber_step)
      else:
            bot.send_message(call.message.chat.id, "Lütfen önce üyeliğinizi doğrulayınız. Üyeliğiniz yoksa satın almak için @emreklasic ile iletişime geçiniz.")

@bot.callback_query_handler(func=lambda call: call.data == 'gsmtc_sorgu')
def gsmtc_sorgu(call):
      tg_id = call.message.chat.id
       
      cursor.execute("SELECT tg_id FROM sh_kullanici WHERE tg_id = %s", (tg_id,))
      user = cursor.fetchone()
       
      if user:
        bot.send_message(call.message.chat.id, "Lütfen Telefon Numarası değerini girin. (Başında 0 olmasın example: 5555555555)")
        bot.register_next_step_handler(call.message, process_gsmtc_step)
      else:
            bot.send_message(call.message.chat.id, "Lütfen önce üyeliğinizi doğrulayınız. Üyeliğiniz yoksa satın almak için @emreklasic ile iletişime geçiniz.")
           

   
@bot.callback_query_handler(func=lambda call: call.data == 'detayliaile_sorgu')
def detayliaile_sorgu(call):
    tg_id = call.message.chat.id
       
    cursor.execute("SELECT tg_id FROM sh_kullanici WHERE tg_id = %s", (tg_id,))
    user = cursor.fetchone()
       
    if user:
        bot.send_message(call.message.chat.id, "Lütfen TC değerini girin.")
        bot.register_next_step_handler(call.message, process_detayliaile_step)
    else:
            bot.send_message(call.message.chat.id, "Lütfen önce üyeliğinizi doğrulayınız. Üyeliğiniz yoksa satın almak için @emreklasic ile iletişime geçiniz.")

@bot.callback_query_handler(func=lambda call: call.data == 'soyagaci_sorgu')
def soyagaci_sorgu(call):
    tg_id = call.message.chat.id
       
    cursor.execute("SELECT tg_id FROM sh_kullanici WHERE tg_id = %s", (tg_id,))
    user = cursor.fetchone()
       
    if user:
        bot.send_message(call.message.chat.id, "Lütfen TC değerini girin.")
        bot.register_next_step_handler(call.message, process_soyagaci_step)
    else:
            bot.send_message(call.message.chat.id, "Lütfen önce üyeliğinizi doğrulayınız. Üyeliğiniz yoksa satın almak için @emreklasic ile iletişime geçiniz.")

@bot.callback_query_handler(func=lambda call: call.data == 'tcpro_sorgu')
def tcpro_sorgu(call):
    tg_id = call.message.chat.id
       
    cursor.execute("SELECT tg_id FROM sh_kullanici WHERE tg_id = %s", (tg_id,))
    user = cursor.fetchone()
       
    if user:
        bot.send_message(call.message.chat.id, "Lütfen TC değerini girin.")
        bot.register_next_step_handler(call.message, process_tcpro_step)
    else:
            bot.send_message(call.message.chat.id, "Lütfen önce üyeliğinizi doğrulayınız. Üyeliğiniz yoksa satın almak için @emreklasic ile iletişime geçiniz.")
       
@bot.callback_query_handler(func=lambda call: call.data == 'adsoyad_sorgu')
def adsoyad_sorgu(call):
    tg_id = call.message.chat.id
       
    cursor.execute("SELECT tg_id FROM sh_kullanici WHERE tg_id = %s", (tg_id,))
    user = cursor.fetchone()
       
    if user:
        bot.send_message(call.message.chat.id, "Lütfen adınızı girin.")
        bot.register_next_step_handler(call.message, process_ad_step)
    else:
            bot.send_message(call.message.chat.id, "Lütfen önce üyeliğinizi doğrulayınız. Üyeliğiniz yoksa satın almak için @emreklasic ile iletişime geçiniz.")
def process_tc_step(message):
    try:
       
        tc = message.text
        tcsorgu = requests.get("http://185.148.241.133/test2.php?tc=" + tc).json()
        total_peoples = tcsorgu["number"]
        formatted_data = (
            f"╔══════════════╗\n"
            f"║ Toplam:  {total_peoples} veri.\n"
            f"╠══════════════╣\n"
        )
        if total_peoples > 0:
            person = tcsorgu["data"][0]
            formatted_data += (
                f"║ TC: {person.get('TC', 'YOK')}\n"
                f"║ Ad: {person.get('ADI', 'YOK')}\n"
                f"║ Soyad: {person.get('SOYADI', 'YOK')}\n"
                f"║ Doğum Tarihi: {person.get('DOGUMTARIHI', 'YOK')}\n"
                f"║ Nüfus İl: {person.get('NUFUSIL', 'YOK')}\n"
                f"║ Nüfus İlçe: {person.get('NUFUSILCE', 'YOK')}\n"
                f"║ Anne Adı: {person.get('ANNEADI', 'YOK')}\n"
                f"║ Anne TC: {person.get('ANNETC', 'YOK')}\n"
                f"║ Baba Adı: {person.get('BABAADI', 'YOK')}\n"
                f"║ Baba TC: {person.get('BABATC', 'YOK')}\n"
                f"║ Uyruk: {person.get('UYRUK', 'YOK')}\n"
                f"╠══════════════╣\n"
            )
        bot.send_message(message.chat.id, formatted_data)
    except Exception as e:
        bot.reply_to(message, 'Üzgünüm, bir hata oluştu.')

def process_tcgsm_step(message):
    try:
       
        tc = message.text
        tcgsmsorgu = requests.get("http://185.148.241.133/test.php?tc=" + tc).json()
        formatted_data = ""
        total_peoples = tcgsmsorgu["number"]
        formatted_data = (
            f"╔══════════════╗\n"
            f"║ Toplam:  {total_peoples} veri.\n"
            f"╠══════════════╣\n"
        )
        for person in tcgsmsorgu["data"]:
                formatted_data += (
                f"║ TC: {person.get('TC', 'YOK')}\n"
                f"║ GSM: {person.get('GSM', 'YOK')}\n"
                f"╠══════════════╣\n"
            )
        bot.send_message(message.chat.id, formatted_data)
    except Exception as e:
        bot.reply_to(message, 'Üzgünüm, bir hata oluştu.')


def process_adduser_step(message):
    try:
       
        username = message.text
        k_key = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        tg_id = message.chat.id
        cursor.execute("SELECT k_adi FROM sh_kullanici WHERE tg_id = %s", (tg_id,))
        ekleyen= cursor.fetchone()
       
       
        add_users(username, ekleyen[0], k_key)
        formatted_data1 = (
            f"╔══════════════╗\n"
            f"║Kullanıcı Başarıyla Oluşturuldu\n"
            f"║Bot: @TheosPanelBot\n"
            f"╠══════════════╣\n"
        )
        formatted_data2= (
                f"║ Kullanıcı Adı: {username}\n"
                f"║ Şifre: {k_key}\n"
                f"╠══════════════╣\n"
            )
        bot.send_message(message.chat.id,formatted_data1+formatted_data2)
    except Exception as e:
        bot.reply_to(message, 'Üzgünüm, bir hata oluştu.{}'.format(str(e)))

#(1, '1', '85.106.128.232', '1', 'Handheld Browser', 'Android Device', '2022-06-01 18:56:19', 'p7XiO5Z0HxGJ1mylo6pgNplv4uaHribu', 'true', 'emre', 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36', 'emre', '', '', '2024-02-19 17:22:58', 4920, 'theos.png', '5307220102')
def process_edituser_step(message):
    try:
        global usernamess
        usernamess = message.text
        tg_id = message.chat.id
        cursor.execute("SELECT * FROM sh_kullanici WHERE k_adi = 
