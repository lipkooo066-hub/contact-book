class Contact:
    validation_rules = {}
    def __init__(self, name, phone, is_favorite=False, **kw):
        self.name = name.strip()
        self.phones = [phone] if isinstance(phone, str) else list(phone)
        self.is_favorite = bool(is_favorite)
        for f in getattr(self, "extra_fields", ()): setattr(self, f, kw.get(f))

    @property
    def phone(self): return self.phones[0] if self.phones else ""

    def matches(self, t):
        return t.lower() in self.name.lower() or any(t.lower() in p for p in self.phones)

    def validate(self):
        if not self.name or not self.phones: raise ValueError("Пустое имя или телефон")
        for f, r in self.validation_rules.items():
            if not r(getattr(self, f, None)): raise ValueError(f"Ошибка в поле {f}")
        return True

    def display(self): raise NotImplementedError
    def summary(self): raise NotImplementedError

class PersonalContact(Contact):
    extra_fields = ("birthday",)
    validation_rules = {"birthday": lambda v: bool(v and isinstance(v, str))}
    def display(self): return f"{'⭐ ' if self.is_favorite else ''}{self.name} — {', '.join(self.phones)} | ДР: {self.birthday}"
    def summary(self): return f"{'⭐ ' if self.is_favorite else ''}Личный: {self.name} ({self.phone})"

class WorkContact(Contact):
    extra_fields = ("company", "job_title")
    validation_rules = {"company": lambda v: bool(v and isinstance(v, str)), "job_title": lambda v: bool(v and isinstance(v, str))}
    def display(self): return f"{'⭐ ' if self.is_favorite else ''}{self.name} — {', '.join(self.phones)} | Работа: {self.company} ({self.job_title})"
    def summary(self): return f"{'⭐ ' if self.is_favorite else ''}Рабочий: {self.name} — {self.company}"

class EmergencyContact(Contact):
    extra_fields = ("relationship", "priority")
    validation_rules = {"relationship": lambda v: bool(v and isinstance(v, str)), "priority": lambda v: isinstance(v, bool)}
    def display(self): return f"{'⭐ ' if self.is_favorite else ''}{self.name} — {', '.join(self.phones)} | Родство: {self.relationship} | Приоритет: {'Высокий' if self.priority else 'Обычный'}"
    def summary(self): return f"{'⭐ ' if self.is_favorite else ''}ЭКСТРЕННЫЙ [{self.relationship}]: {self.name} ({self.phone})"

class FamilyContact(Contact):
    extra_fields = ("family_role",)
    validation_rules = {"family_role": lambda v: bool(v and isinstance(v, str))}
    def display(self): return f"{'⭐ ' if self.is_favorite else ''}{self.name} — {', '.join(self.phones)} | Роль в семье: {self.family_role}"
    def summary(self): return f"{'⭐ ' if self.is_favorite else ''}Семья ({self.family_role}): {self.name}"