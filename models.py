class Contact:
    validation_rules = {}

    def __init__(self, name, phone, **specific_fields):
        self.name = name
        self.phone = phone
        for field in getattr(self, "extra_fields", ()):
            setattr(self, field, specific_fields.get(field))

    def matches(self, text):
        text_lower = text.lower()
        return text_lower in self.name.lower() or text_lower in self.phone

    def validate(self):
        for field, rule in self.validation_rules.items():
            value = getattr(self, field, None)
            if not rule(value):
                raise ValueError(f"Ошибка валидации поля '{field}' со значением '{value}'")
        return True

    def display(self):
        raise NotImplementedError

    def summary(self):
        raise NotImplementedError


class PersonalContact(Contact):
    extra_fields = ("birthday",)
    validation_rules = {"birthday": lambda v: bool(v and isinstance(v, str))}

    def display(self):
        return f"{self.name} — {self.phone} | ДР: {self.birthday}"

    def summary(self):
        return f"Личный: {self.name} ({self.phone})"


class WorkContact(Contact):
    extra_fields = ("company", "job_title")
    validation_rules = {
        "company": lambda v: bool(v and isinstance(v, str)),
        "job_title": lambda v: bool(v and isinstance(v, str))
    }

    def display(self):
        return f"{self.name} — {self.phone} | Работа: {self.company} ({self.job_title})"

    def summary(self):
        return f"Рабочий: {self.name} — {self.company}"


class EmergencyContact(Contact):
    extra_fields = ("relationship", "priority")
    validation_rules = {
        "relationship": lambda v: bool(v and isinstance(v, str)),
        "priority": lambda v: isinstance(v, bool)
    }

    def display(self):
        priority_str = "Высокий" if self.priority else "Обычный"
        return f"{self.name} — {self.phone} | Родство: {self.relationship} | Приоритет: {priority_str}"

    def summary(self):
        return f"ЭКСТРЕННЫЙ [{self.relationship}]: {self.name} ({self.phone})"


class FamilyContact(Contact):
    extra_fields = ("family_role",)
    validation_rules = {"family_role": lambda v: bool(v and isinstance(v, str))}

    def display(self):
        return f"{self.name} — {self.phone} | Роль в семье: {self.family_role}"

    def summary(self):
        return f"Семья ({self.family_role}): {self.name}"