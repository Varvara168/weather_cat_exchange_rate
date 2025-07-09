from t import *
def main():
    while True:
        print("\n📋 Выберите действие:")
        print("[1] Посмотреть погоду")
        print("[2] Получить котика")
        print("[3] Курс валют")
        print("[0] Выйти")

        choice = input("👉 Ваш выбор: ")

        if choice == "1":
            get_weather()
        elif choice == "2":
            get_cat()
        elif choice == "3":
            get_exchange_rate()
        elif choice == "0":
            print("👋 Пока!")
            break
        else:
            print("❗ Неверный выбор")

main()