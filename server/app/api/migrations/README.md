# Миграции API приложения

Эта директория содержит миграции базы данных для приложения `api`.

## Структура миграций

### 0001_enable_pg_trgm.py
**Назначение:** Включение расширения PostgreSQL для триграммного поиска.

**Содержимое:**
- `TrigramExtension()` - создает расширение `pg_trgm` в PostgreSQL

**Важно:** Эта миграция должна быть первой, так как следующая миграция создает GIN-индекс, который требует это расширение.

**Зависимости:** Нет (initial=True)

---

### 0002_initial.py
**Назначение:** Создание всех моделей базы данных.

**Содержимое:**
- 11 моделей Django
- Все поля, связи и ограничения
- GIN-индекс на поле `Product.name`

**Зависимости:**
- `api.0001_enable_pg_trgm` (требует расширение pg_trgm)
- `auth.0015_alter_group_id_alter_permission_id_alter_user_id`
- `settings.AUTH_USER_MODEL`

**Модели:**
1. **AuthenticationToken** - токены для Telegram-авторизации
2. **AuthenticationRequest** - запросы аутентификации через Telegram
3. **Product** - товары магазина (с полем `remaining` для учета остатков)
4. **ProductImage** - изображения товаров
5. **Tag** - теги для товаров
6. **ProductTag** - промежуточная модель Product ↔ Tag (с полями `added_at`, `priority`)
7. **Cart** - корзина покупок (с ограничением уникальности user+product)
8. **Order** - заказы пользователей
9. **OrderProduct** - промежуточная модель Order ↔ Product
10. **UserImage** - изображения профилей пользователей
11. **ProductReport** - PDF-отчеты по товарам

---

## Применение миграций на новом устройстве

### Предварительные требования
1. PostgreSQL 13+ установлен и запущен
2. База данных создана
3. Виртуальное окружение активировано
4. Зависимости установлены из `requirements.txt`

### Команда
```bash
python manage.py migrate
```

### Ожидаемый результат
```
Operations to perform:
  Apply all migrations: admin, api, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying api.0001_enable_pg_trgm... OK
  Applying api.0002_initial... OK
```

---

## Проверка миграций

### Просмотр статуса миграций
```bash
python manage.py showmigrations api
```

**Ожидаемый вывод:**
```
api
 [X] 0001_enable_pg_trgm
 [X] 0002_initial
```

### Запуск тестов
```bash
# Windows
set TESTING=1
python manage.py test api.tests

# Linux/macOS
export TESTING=1
python manage.py test api.tests
```

**Ожидаемый результат:** 33 теста пройдены ✅

---

## Решение проблем

### Ошибка: "extension pg_trgm does not exist"

**Решение:** Создайте расширение вручную
```sql
psql -U postgres -d your_database_name
CREATE EXTENSION IF NOT EXISTS pg_trgm;
\q
```

### Ошибка: "operator class gin_trgm_ops does not exist"

**Причина:** Миграции применены в неправильном порядке.

**Решение:** Пересоздайте базу данных или примените миграции заново:
```bash
python manage.py migrate api zero --fake
python manage.py migrate api --fake
```

### Ошибка: "relation already exists"

**Причина:** Таблицы уже существуют в базе данных.

**Решение:** Удалите и пересоздайте базу данных:
```sql
DROP DATABASE your_database_name;
CREATE DATABASE your_database_name;
```

Затем примените миграции:
```bash
python manage.py migrate
```

---

## История изменений

**11 мая 2026** - Пересоздание миграций
- Удалены 20 старых миграций (0001-0020)
- Созданы 2 чистые миграции для переноса проекта
- Все тесты проходят успешно (33/33)

---

## Дополнительная документация

- **DEPLOYMENT_GUIDE.md** - полное руководство по развертыванию проекта
- **MIGRATION_RESET_REPORT.md** - отчет о пересоздании миграций
- **STOCK_MANAGEMENT.md** - документация по управлению остатками товаров

---

## Важные замечания

⚠️ **Не изменяйте эти миграции вручную!** Они созданы автоматически Django и отражают текущее состояние моделей.

⚠️ **Порядок миграций важен!** Миграция `0001_enable_pg_trgm` должна быть применена ДО `0002_initial`.

✅ **Для новых изменений** используйте команду `python manage.py makemigrations`, которая создаст новые миграции (0003, 0004 и т.д.).

✅ **Перед применением миграций** на production всегда делайте резервную копию базы данных!
