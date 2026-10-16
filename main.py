from models import PersonalContact, WorkContact, EmergencyContact, FamilyContact
from logic import print_all, search, sort_contacts, HistoryManager, AddContactCommand, AddPhoneCommand, DeleteContactCommand, EditContactCommand, ToggleFavoriteCommand
from menu import show_menu, choose_sort_menu

TYPES = {
    "1": ("Личный", PersonalContact, [("birthday", "ДР: ")]),
    "2": ("Рабочий", WorkContact, [("company", "Компания: "), ("job_title", "Должность: ")]),
    "3": ("Экстренный", EmergencyContact, [("relationship", "Родство: "), ("priority", "Приоритет (да/нет): ")]),
    "4": ("Семья", FamilyContact, [("family_role", "Роль: ")])
}

def find(lst, name):
    return next((c for c in lst if c.name.lower() == name.strip().lower()), None)

def main():
    contacts = [
        PersonalContact("Анна", "+79001112233", True, birthday="12.05"),
        WorkContact("Борис", "+79002223344", company="Лаб", job_title="дев")
    ]
    hist = HistoryManager()

    while True:
        ch = show_menu()
        if ch == "1":
            print()
            print_all(sort_contacts(contacts, choose_sort_menu()))
        elif ch == "2":
            name = input("Имя: ").strip()
            if not name: continue
            phone = input("Телефон: ").strip()
            exist = find(contacts, name)
            if exist:
                if phone in exist.phones: print("Номер уже есть.")
                else:
                    hist.execute(AddPhoneCommand(exist, phone))
                    print("Номер добавлен к существующему!")
            else:
                print("Тип: 1.Личный 2.Рабочий 3.Экстренный 4.Семья")
                t = input("Выбор: ").strip()
                if t not in TYPES: continue
                _, cls, fields = TYPES[t]
                kw = {}
                try:
                    for fn, prompt in fields:
                        val = input(prompt).strip()
                        if fn == "priority": val = val.lower() in ("да", "true", "1")
                        kw[fn] = val
                    nc = cls(name, phone, **kw)
                    nc.validate()
                    hist.execute(AddContactCommand(contacts, nc))
                    print("Создано!")
                except Exception as e: print(f"Ошибка: {e}")
        elif ch == "3":
            print()
            print_all(search(contacts, input("Поиск: ").strip()))
        elif ch == "4":
            print()
            for i, c in enumerate(contacts, 1): print(f"{i}. {'⭐' if c.is_favorite else ''} {c.name}")
            try:
                hist.execute(ToggleFavoriteCommand(contacts[int(input("Номер: "))-1]))
                print("Статус изменен.")
            except: print("Ошибка.")
        elif ch == "5":
            print()
            for i, c in enumerate(contacts, 1): print(f"{i}. {c.name}")
            try:
                idx = int(input("Номер: ")) - 1
                new_n = input(f"Новое имя [{contacts[idx].name}]: ").strip()
                new_p = input("Доп. телефон: ").strip()
                hist.execute(EditContactCommand(contacts[idx], new_n, new_p))
                print("Изменено.")
            except: print("Ошибка.")
        elif ch == "6":
            print()
            for i, c in enumerate(contacts, 1): print(f"{i}. {c.name}")
            try:
                hist.execute(DeleteContactCommand(contacts, contacts[int(input("Номер: "))-1]))
                print("Удалено.")
            except: print("Ошибка.")
        elif ch == "7":
            hist.undo()
        elif ch == "8":
            hist.redo()
        elif ch == "0":
            break

if __name__ == "__main__":
    main()