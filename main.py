import json
from datetime import datetime

DATA_FILE = "hotel_data.json"

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"rooms": {}, "bookings": []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)


def init_rooms():
    data = load_data()
    if not data["rooms"]:
        for i in range(1, 11):
            data["rooms"][str(i)] = {"type": "single" if i <= 5 else "double", "occupied": False}
        save_data(data)
        print("Номера успешно инициализированы!")
    else:
        print("Номера уже инициализированы.")



def book_room():
    data = load_data()
    name = input("Имя клиента: ")
    guests = int(input("Количество гостей: "))
    check_in = input("Дата заезда (ГГГГ-ММ-ДД): ")
    check_out = input("Дата выезда (ГГГГ-ММ-ДД): ")

    room_type = "single" if guests == 1 else "double"
    room_id = None

    for rid, info in data["rooms"].items():
        if not info["occupied"] and info["type"] == room_type:
            room_id = rid
            break

    if room_id:
        data["rooms"][room_id]["occupied"] = True
        data["bookings"].append({
            "name": name,
            "room": room_id,
            "guests": guests,
            "check_in": check_in,
            "check_out": check_out,
            "checked_in": False
        })
        save_data(data)
        print(f"Бронирование успешно! Комната #{room_id} зарезервирована.")
    else:
        print("Свободных номеров подходящего типа нет.")

def check_in_guest():
    data = load_data()
    name = input("Введите имя для заселения: ")
    today = datetime.today().strftime("%Y-%m-%d")

    for booking in data["bookings"]:
        if booking["name"] == name and booking["check_in"] == today and not booking["checked_in"]:
            booking["checked_in"] = True
            save_data(data)
            print(f"Клиент {name} успешно заселён в комнату #{booking['room']}.")
            return

    print("Бронирование не найдено или уже заселён.")


def show_status():
    data = load_data()
    print("\nВсе номера:")
    for rid, info in data["rooms"].items():
        print(f"Комната #{rid}: тип={info['type']}, занята={info['occupied']}")

    print("\nБронирования:")
    for b in data["bookings"]:
        print(f"{b['name']} - комната #{b['room']}, {b['check_in']} to {b['check_out']}, заселён={b['checked_in']}")

def get_dictionary():
    return {
        1: {
            "action": init_rooms,
            "description": "Инициализировать номера"
        },
        2: {
            "action": book_room,
            "description": "Забронировать номер"
        },
        3: {
            "action": check_in_guest,
            "description": "Заселить клиента"
        },
        4: {
            "action": show_status,
            "description": "Показать статус"
        },
        5: {
            "action": exit,
            "description": "Выход из программы"
        }
    }


def menu():
    commands = get_dictionary()
    while True:
        print("\nМеню:")
        for key in sorted(commands):
            print(f"{key}. {commands[key]['description']}")

        choice = input("Выбор: ")

        if not choice.isdigit():
            print("Введите номер команды.")
            continue

        choice = int(choice)

        if choice == 5:
            break

        command = commands.get(choice)
        if command:
            command["action"]()
        else:
            print("Неверный выбор. Попробуйте снова.")



if __name__ == "__main__":
    menu()

