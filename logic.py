def print_all(lst):
    if not lst:
        print("Список пуст.")
        return
    for c in lst:
        print(c.display())

def search(lst, t):
    return [c for c in lst if c.matches(t)]

def sort_contacts(lst, by="name"):
    favs = sorted([c for c in lst if c.is_favorite], key=lambda x: (getattr(x, by) if by in ["name", "phone"] else x.name).lower())
    others = sorted([c for c in lst if not c.is_favorite], key=lambda x: (getattr(x, by) if by in ["name", "phone"] else x.name).lower())
    return favs + others

class Command:
    def execute(self): pass
    def undo(self): pass

class AddContactCommand(Command):
    def __init__(self, lst, c): self.lst, self.c = lst, c
    def execute(self): self.lst.append(self.c)
    def undo(self):
        if self.c in self.lst: self.lst.remove(self.c)

class AddPhoneCommand(Command):
    def __init__(self, c, p): self.c, self.p = c, p
    def execute(self):
        if self.p not in self.c.phones: self.c.phones.append(self.p)
    def undo(self):
        if self.p in self.c.phones and len(self.c.phones) > 1: self.c.phones.remove(self.p)

class DeleteContactCommand(Command):
    def __init__(self, lst, c): self.lst, self.c = lst, c; self.idx = lst.index(c) if c in lst else 0
    def execute(self):
        if self.c in self.lst: self.idx = self.lst.index(self.c); self.lst.remove(self.c)
    def undo(self):
        if self.c not in self.lst: self.lst.insert(self.idx, self.c)

class EditContactCommand(Command):
    def __init__(self, c, name, phone):
        self.c, self.new_name, self.new_phone = c, name, phone
        self.old_name, self.old_phones = c.name, list(c.phones)
    def execute(self):
        if self.new_name: self.c.name = self.new_name
        if self.new_phone and self.new_phone not in self.c.phones: self.c.phones.append(self.new_phone)
    def undo(self):
        self.c.name, self.c.phones = self.old_name, list(self.old_phones)

class ToggleFavoriteCommand(Command):
    def __init__(self, c): self.c, self.old = c, c.is_favorite
    def execute(self): self.c.is_favorite = not self.old
    def undo(self): self.c.is_favorite = self.old

class HistoryManager:
    def __init__(self): self.undo_s, self.redo_s = [], []
    def execute(self, cmd): cmd.execute(); self.undo_s.append(cmd); self.redo_s.clear()
    def undo(self):
        if not self.undo_s: print("Нечего отменять."); return
        cmd = self.undo_s.pop(); cmd.undo(); self.redo_s.append(cmd); print("Действие отменено.")
    def redo(self):
        if not self.redo_s: print("Нечего повторять."); return
        cmd = self.redo_s.pop(); cmd.execute(); self.undo_s.append(cmd); print("Действие повторено.")
