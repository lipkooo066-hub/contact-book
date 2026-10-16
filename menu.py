def show_menu():
    print("\n=== КНИГА КОНТАКТОВ ===")
    print("1. Показать список\n2. Добавить контакт\n3. Найти\n4. Избранное вкл/выкл\n5. Изменить\n6. Удалить\n7. Undo\n8. Redo\n0. Выход")
    return input("Выбор: ").strip()

def choose_sort_menu():
    return "phone" if input("Сортировка (1-Имя, 2-Телефон): ").strip() == "2" else "name"