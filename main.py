from models import PersonalContact, WorkContact, EmergencyContact, FamilyContact
from logic import print_all, search, validate_all
from menu import show_menu

# Реестр доступных типов для динамического добавления (Требование 13 со слайдов)
CONTACT_TYPES = {
    "1": ("Личный", PersonalContact, [("birthday", "Дата рождения (например, 12.05): ")]),
    "2": ("Рабочий", WorkContact, [("company", "Компания: "), ("job_title", "Должность: ")]),
    "3": ("Экстренный", EmergencyContact,
          [("relationship", "Степень родства: "), ("priority", "Высокий приоритет (да/нет): ")]),
    "4": ("Семья", FamilyContact, [("family_role", "Роль в семье: ")])
}


def main():
    contacts = [
        PersonalContact("Анна", "+7 900 111-22-33", birthday="12.05"),
        WorkContact("Борис", "+7 900 222-33-44", company="Лаб", job_title="аналитик"),
        EmergencyContact("Вера", "+7 900 333-44-55", relationship="сестра", priority=True),
        FamilyContact("Дмитрий", "+7 900 444-55-66", family_role="отец")
    ]

    while True:
        choice = show_menu()

        if choice == "1":
            print("\n--- ПОЛНЫЙ СПИСОК КОНТАКТОВ ---")
            print_all(contacts)

        elif choice == "2":
            print("\n--- КРАТКАЯ СВОДКА (summary) ---")
            if not contacts:
                print("Список пуст.")
            else:
                for i, c in enumerate(contacts, 1):
                    print(f"{i}. {c.summary()}")

        elif choice == "3":
            print("\n--- ДОБАВЛЕНИЕ КОНТАКТА ---")
            print("Выберите тип контакта:")
            for key, (name_type, _, _) in CONTACT_TYPES.items():
                print(f"{key}. {name_type}")

            t_choice = input("Ваш выбор: ").strip()
            if t_choice not in CONTACT_TYPES:
                print("Неверный тип контакта!")
                continue

            type_name, cls, fields_config = CONTACT_TYPES[t_choice]
            name = input("Введите имя: ").strip()
            phone = input("Введите телефон: ").strip()

            kwargs = {}
            try:
                for field_name, prompt in fields_config:
                    val = input(prompt).strip()
                    if field_name == "priority":
                        val = val.lower() in ("да", "true", "1", "yes")
                    kwargs[field_name] = val

                new_contact = cls(name, phone, **kwargs)
                new_contact.validate()  # Проверяем перед добавлением
                contacts.append(new_contact)
                print(f"Контакт '{name}' успешно добавлен!")
            except Exception as e:
                print(f"Ошибка при добавлении: {e}")

        elif choice == "4":
            query = input("\nВведите текст для поиска: ").strip()
            found = search(contacts, query)
            print(f"\n--- РЕЗУЛЬТАТЫ ПОИСКА ('{query}') ---")
            if not found:
                print("Ничего не найдено.")
            else:
                for c in found:
                    print(c.display())

        elif choice == "5":
            print("\n--- ИЗМЕНЕНИЕ КОНТАКТА ---")
            if not contacts:
                print("Список пуст.")
                continue
            for i, c in enumerate(contacts, 1):
                print(f"{i}. {c.summary()}")
            try:
                idx = int(input("Введите номер контакта для изменения: ")) - 1
                if 0 <= idx < len(contacts):
                    target = contacts[idx]
                    print(f"Редактируем: {target.name}")
                    new_name = input(f"Новое имя [{target.name}]: ").strip()
                    new_phone = input(f"Новый телефон [{target.phone}]: ").strip()
                    if new_name: target.name = new_name
                    if new_phone: target.phone = new_phone
                    print("Контакт успешно обновлен!")
                else:
                    print("Неверный номер.")
            except ValueError:
                print("Введите число.")

        elif choice == "6":
            print("\n--- УДАЛЕНИЕ КОНТАКТА ---")
            if not contacts:
                print("Список пуст.")
                continue
            for i, c in enumerate(contacts, 1):
                print(f"{i}. {c.summary()}")
            try:
                idx = int(input("Введите номер контакта для удаления: ")) - 1
                if 0 <= idx < len(contacts):
                    removed = contacts.pop(idx)
                    print(f"Контакт '{removed.name}' удален.")
                else:
                    print("Неверный номер.")
            except ValueError:
                print("Введите число.")

        elif choice == "7":
            print("\n--- ПРОВЕРКА ВАЛИДАЦИИ ---")
            try:
                validate_all(contacts)
                print("Все контакты прошли проверку успешно!")
            except ValueError as e:
                print(f"Ошибка валидации: {e}")

        elif choice == "0":
            print("\nВыход из программы. До свидания!")
            break
        else:
            print("Неверный пункт меню. Попробуйте снова.")


if __name__ == "__main__":
    main()