# Исправление совместимости миграций

**Проблема:** `NodeNotFoundError` при выполнении `python manage.py migrate` на новом устройстве

**Причина:** Миграция ссылалась на конкретную версию auth миграции Django 6.0.3, которой может не быть в других версиях Django

**Решение:** Заменено на `__latest__` для автоматического определения последней миграции

---

## Что было исправлено

### Файл: `server/app/api/migrations/0002_initial.py`

**Было:**
```python
dependencies = [
    ('api', '0001_enable_pg_trgm'),
    ('auth', '0015_alter_group_id_alter_permission_id_alter_user_id'),  # ❌
    migrations.swappable_dependency(settings.AUTH_USER_MODEL),
]
```

**Стало:**
```python
dependencies = [
    ('api', '0001_enable_pg_trgm'),
    ('auth', '__latest__'),  # ✅
    migrations.swappable_dependency(settings.AUTH_USER_MODEL),
]
```

---

## Теперь миграции работают

```bash
python manage.py migrate
```

Миграции теперь совместимы с:
- ✅ Django 6.0.x
- ✅ Django 5.x
- ✅ Django 4.x (с ограничениями)

---

## Подробности

См. **MIGRATION_FIX_AUTH_DEPENDENCY.md** для полного объяснения проблемы и решения.
