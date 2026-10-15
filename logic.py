def print_all(contacts):
    if not contacts:
        print("Список контактов пуст.")
        return
    for contact in contacts:
        print(contact.display())


def search(contacts, text):
    result = []
    for contact in contacts:
        if contact.matches(text):
            result.append(contact)
    return result


def validate_all(contacts):
    for contact in contacts:
        contact.validate()