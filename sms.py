from colorama import Fore, Style
from time import sleep
from os import system
from sms import SendSms
import threading

# Servisleri otomatik topla
servisler_sms = []
for attribute in dir(SendSms):
    attribute_value = getattr(SendSms, attribute)
    if callable(attribute_value) and not attribute.startswith('__'):
        servisler_sms.append(attribute)

while 1:
    system("cls||clear")
    print(f"""{Fore.LIGHTCYAN_EX}
██████╗  ███████╗████████╗███████╗██╗  ██╗███████╗
██╔══██╗██╔════╝╚══██╔══╝╚══███╔╝██║ ██╔╝╚══███╔╝
██████╔╝█████╗     ██║     ███╔╝ █████╔╝   ███╔╝ 
██╔══██╗██╔══╝     ██║    ███╔╝  ██╔═██╗  ███╔╝  
██║  ██║███████╗   ██║   ███████╗██║  ██╗███████╗
╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝

    Sms: {len(servisler_sms)}           {Style.RESET_ALL}by {Fore.LIGHTRED_EX}@ReTeKZ{Style.RESET_ALL}\n  
""")

    try:
        menu = input(f"{Fore.LIGHTMAGENTA_EX} 1- SMS Gönder (Normal)\n\n 2- SMS Gönder (Turbo)\n\n 3- Çıkış\n\n{Fore.LIGHTYELLOW_EX} Seçim: ")
        if menu == "":
            continue
        menu = int(menu)
    except ValueError:
        system("cls||clear")
        print(f"{Fore.LIGHTRED_EX}Hatalı giriş yaptın. Tekrar deneyiniz.{Style.RESET_ALL}")
        sleep(3)
        continue

    if menu == 1:
        system("cls||clear")
        print(f"{Fore.LIGHTYELLOW_EX}Telefon numarasını başında '+90' olmadan yazınız (Birden çoksa 'enter' tuşuna basınız): {Fore.LIGHTGREEN_EX}", end="")
        tel_no = input()
        tel_liste = []
        
        if tel_no == "":
            system("cls||clear")
            print(f"{Fore.LIGHTYELLOW_EX}Telefon numaralarının kayıtlı olduğu dosyanın dizinini yazınız: {Fore.LIGHTGREEN_EX}", end="")
            dizin = input()
            try:
                with open(dizin, "r", encoding="utf-8") as f:
                    for i in f.read().strip().split("\n"):
                        if len(i) == 10 and i.isdigit():
                            tel_liste.append(i)
            except FileNotFoundError:
                system("cls||clear")
                print(f"{Fore.LIGHTRED_EX}Hatalı dosya dizini. Tekrar deneyiniz.{Style.RESET_ALL}")
                sleep(3)
                continue
        else:
            try:
                int(tel_no)
                if len(tel_no) != 10:
                    raise ValueError
                tel_liste.append(tel_no)
            except ValueError:
                system("cls||clear")
                print(f"{Fore.LIGHTRED_EX}Hatalı telefon numarası. Tekrar deneyiniz.{Style.RESET_ALL}")
                sleep(3)
                continue

        system("cls||clear")
        print(f"{Fore.LIGHTYELLOW_EX}Mail adresi (Bilmiyorsanız 'enter' tuşuna basın): {Fore.LIGHTGREEN_EX}", end="")
        mail = input()
        if mail and ("@" not in mail or ".com" not in mail):
            system("cls||clear")
            print(f"{Fore.LIGHTRED_EX}Hatalı mail adresi. Tekrar deneyiniz.{Style.RESET_ALL}")
            sleep(3)
            continue

        system("cls||clear")
        print(f"{Fore.LIGHTYELLOW_EX}Kaç saniye aralıkla göndermek istiyorsun: {Fore.LIGHTGREEN_EX}", end="")
        try:
            aralik = int(input())
        except ValueError:
            system("cls||clear")
            print(f"{Fore.LIGHTRED_EX}Hatalı giriş yaptın. Tekrar deneyiniz.{Style.RESET_ALL}")
            sleep(3)
            continue

        system("cls||clear")
        
        for phone in tel_liste:
            sms = SendSms(phone, mail)
            for method_name in servisler_sms:
                getattr(sms, method_name)()
                sleep(aralik)

        print(f"{Fore.LIGHTRED_EX}\nMenüye dönmek için 'enter' tuşuna basınız..{Style.RESET_ALL}")
        input()

    elif menu == 2:
        system("cls||clear")
        print(f"{Fore.LIGHTYELLOW_EX}Telefon numarasını başında '+90' olmadan yazınız: {Fore.LIGHTGREEN_EX}", end="")
        tel_no = input()
        try:
            int(tel_no)
            if len(tel_no) != 10:
                raise ValueError
        except ValueError:
            system("cls||clear")
            print(f"{Fore.LIGHTRED_EX}Hatalı telefon numarası. Tekrar deneyiniz.{Style.RESET_ALL}")
            sleep(3)
            continue

        system("cls||clear")
        print(f"{Fore.LIGHTYELLOW_EX}Mail adresi (Bilmiyorsanız 'enter' tuşuna basın): {Fore.LIGHTGREEN_EX}", end="")
        mail = input()
        if mail and ("@" not in mail or ".com" not in mail):
            system("cls||clear")
            print(f"{Fore.LIGHTRED_EX}Hatalı mail adresi. Tekrar deneyiniz.{Style.RESET_ALL}")
            sleep(3)
            continue

        system("cls||clear")
        send_sms = SendSms(tel_no, mail)
        dur = threading.Event()

        def Turbo():
            while not dur.is_set():
                thread = []
                for fonk in servisler_sms:
                    t = threading.Thread(target=getattr(send_sms, fonk), daemon=True)
                    thread.append(t)
                    t.start()
                for t in thread:
                    t.join()

        try:
            Turbo()
        except KeyboardInterrupt:
            dur.set()
            system("cls||clear")
            print(f"\n{Fore.LIGHTRED_EX}Ctrl+C tuş kombinasyonu algılandı. Menüye dönülüyor..{Style.RESET_ALL}")
            sleep(2)

    elif menu == 3:
        system("cls||clear")
        print(f"{Fore.LIGHTRED_EX}Çıkış yapılıyor...{Style.RESET_ALL}")
        break
