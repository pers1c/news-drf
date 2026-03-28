# API Documentation

Base URL: `http://localhost:8000/api/v1`

---

## Аутентификация

Все защищённые эндпоинты требуют заголовок:
```
Authorization: Bearer <access_token>
```

---

## Accounts `/api/v1/auth/`

### POST `/api/v1/auth/register/`
Регистрация нового пользователя.

**Доступ:** Публичный

**Тело запроса:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "StrongPass123!",
  "password_confirm": "StrongPass123!",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Ответ `201 Created`:**
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "avatar": null,
    "bio": "",
    "created_at": "2026-03-22T10:00:00Z",
    "updated_at": "2026-03-22T10:00:00Z",
    "post_count": 0,
    "comment_count": 0
  },
  "refresh": "<refresh_token>",
  "access": "<access_token>",
  "message": "User regirstered successfully!"
}
```

**Ошибки:**
- `400` — пароли не совпадают, email/username уже занят, пароль не прошёл валидацию

---

### POST `/api/v1/auth/login/`
Вход пользователя по email и паролю.

**Доступ:** Публичный

**Тело запроса:**
```json
{
  "email": "john@example.com",
  "password": "StrongPass123!"
}
```

**Ответ `200 OK`:**
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "avatar": null,
    "bio": "",
    "post_count": 5,
    "comment_count": 12
  },
  "refresh": "<refresh_token>",
  "access": "<access_token>",
  "message": "User login successfully!"
}
```

**Ошибки:**
- `400` — неверные учётные данные или пользователь неактивен

---

### POST `/api/v1/auth/logout/`
Выход пользователя (инвалидация refresh-токена).

**Доступ:** Требует авторизации

**Тело запроса:**
```json
{
  "refresh_token": "<refresh_token>"
}
```

**Ответ `200 OK`:**
```json
{
  "message": "User logged out successfully!"
}
```

**Ошибки:**
- `400` — невалидный токен
- `401` — не авторизован

---

### POST `/api/v1/auth/token/refresh/`
Обновление access-токена. При `ROTATE_REFRESH_TOKENS: True` также возвращается новый refresh-токен.

**Доступ:** Публичный

**Тело запроса:**
```json
{
  "refresh": "<refresh_token>"
}
```

**Ответ `200 OK`:**
```json
{
  "access": "<new_access_token>",
  "refresh": "<new_refresh_token>"
}
```

**Ошибки:**
- `401` — токен истёк или невалиден

---

### GET `/api/v1/auth/profile/`
Получение профиля текущего пользователя.

**Доступ:** Требует авторизации

**Ответ `200 OK`:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "full_name": "John Doe",
  "avatar": "/media/avatars/photo.jpg",
  "bio": "About me",
  "created_at": "2026-03-22T10:00:00Z",
  "updated_at": "2026-03-22T10:00:00Z",
  "post_count": 5,
  "comment_count": 12
}
```

---

### PUT/PATCH `/api/v1/auth/profile/`
Обновление профиля текущего пользователя.

**Доступ:** Требует авторизации

**Тело запроса (PATCH — все поля опциональны):**
```json
{
  "first_name": "Johnny",
  "last_name": "Doe",
  "bio": "Updated bio",
  "avatar": "<multipart file>"
}
```

**Ответ `200 OK`:** Обновлённый объект профиля (аналогично GET `/profile/`)

---

### PUT/PATCH `/api/v1/auth/change_password/`
Смена пароля текущего пользователя.

**Доступ:** Требует авторизации

**Тело запроса:**
```json
{
  "old_password": "OldPass123!",
  "new_password": "NewPass456!",
  "new_password_confirmation": "NewPass456!"
}
```

**Ответ `200 OK`:**
```json
{
  "message": "Password updated successfully!"
}
```

**Ошибки:**
- `400` — старый пароль неверен, новые пароли не совпадают, не прошла валидация
- `401` — не авторизован

---

## Main (Posts & Categories) `/api/v1/posts/`

### GET `/api/v1/posts/`
Список постов. Неавторизованным возвращаются только опубликованные посты. Авторизованные видят свои черновики в дополнение к опубликованным.

**Доступ:** Публичный (чтение) / Требует авторизации (создание)

**Query-параметры:**

| Параметр | Тип | Описание |
|----------|-----|----------|
| `search` | string | Поиск по `title`, `content` |
| `category` | integer | Фильтр по ID категории |
| `author` | integer | Фильтр по ID автора |
| `status` | string | `draft` или `published` |
| `ordering` | string | `created_at`, `updated_at`, `views_count`, `title` (префикс `-` для DESC) |
| `page` | integer | Номер страницы (размер: 20) |

**Ответ `200 OK`:**
```json
{
  "count": 42,
  "next": "http://localhost:8000/api/v1/posts/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "My First Post",
      "slug": "my-first-post",
      "content": "Preview of content up to 200 chars...",
      "image": "/media/posts/image.jpg",
      "category": "Technology",
      "author": "john_doe",
      "status": "published",
      "created_at": "2026-03-22T10:00:00Z",
      "updated_at": "2026-03-22T10:00:00Z",
      "views_count": 150,
      "comments_count": 8
    }
  ]
}
```

---

### POST `/api/v1/posts/`
Создание нового поста. Поле `author` и `slug` устанавливаются автоматически.

**Доступ:** Требует авторизации

**Тело запроса:**
```json
{
  "title": "New Post Title",
  "content": "Full post content here...",
  "category": 2,
  "status": "published",
  "image": "<multipart file — опционально>"
}
```

**Ответ `201 Created`:**
```json
{
  "title": "New Post Title",
  "content": "Full post content here...",
  "image": null,
  "category": 2,
  "status": "published"
}
```

---

### GET `/api/v1/posts/<slug>/`
Детальная информация о посте. При каждом GET-запросе увеличивает `views_count` на 1.

**Доступ:** Публичный

**Ответ `200 OK`:**
```json
{
  "id": 1,
  "title": "My First Post",
  "slug": "my-first-post",
  "content": "Full content...",
  "image": "/media/posts/image.jpg",
  "category": 2,
  "category_info": {
    "id": 2,
    "name": "Technology",
    "slug": "technology"
  },
  "author": 1,
  "author_info": {
    "id": 1,
    "username": "john_doe",
    "full_name": "John Doe",
    "avatar": "/media/avatars/photo.jpg"
  },
  "status": "published",
  "created_at": "2026-03-22T10:00:00Z",
  "updated_at": "2026-03-22T10:00:00Z",
  "views_count": 151,
  "comments_count": 8
}
```

**Ошибки:**
- `404` — пост не найден

---

### PUT/PATCH `/api/v1/posts/<slug>/`
Обновление поста. При изменении `title` slug пересчитывается автоматически.

**Доступ:** Только автор поста

**Тело запроса (PATCH — все поля опциональны):**
```json
{
  "title": "Updated Title",
  "content": "Updated content...",
  "status": "draft"
}
```

**Ответ `200 OK`:** Обновлённый объект поста

**Ошибки:**
- `403` — не является автором
- `404` — пост не найден

---

### DELETE `/api/v1/posts/<slug>/`
Удаление поста.

**Доступ:** Только автор поста

**Ответ `204 No Content`**

**Ошибки:**
- `403` — не является автором
- `404` — пост не найден

---

### GET `/api/v1/posts/my-posts/`
Все посты текущего пользователя, включая черновики.

**Доступ:** Требует авторизации

**Query-параметры:** `search`, `category`, `status`, `ordering`, `page` (аналогично GET `/posts/`)

**Ответ `200 OK`:** Пагинированный список постов (аналогично GET `/posts/`)

---

### GET `/api/v1/posts/popular/`
Топ-10 постов по количеству просмотров.

**Доступ:** Публичный

**Ответ `200 OK`:** Список из 10 постов без пагинации

> ⚠️ **Баг:** сортировка использует `-view_count` вместо `-views_count` — порядок постов будет случайным.

---

### GET `/api/v1/posts/recent/`
Последние 10 опубликованных постов по дате создания.

**Доступ:** Публичный

**Ответ `200 OK`:** Список из 10 постов без пагинации

---

### GET `/api/v1/posts/featured/`
> ⚠️ Маршрут объявлен в `urls.py`, но обработчик `featured_posts` **не реализован** в `views.py`. Вернёт `500`.

---

### GET `/api/v1/posts/pinned/`
> ⚠️ Маршрут объявлен в `urls.py`, но обработчик `pinned_posts_only` **не реализован** в `views.py`. Поле `is_pinned` также отсутствует в модели `Post`. Вернёт `500`.

---

### GET `/api/v1/posts/categories/`
Список всех категорий с количеством опубликованных постов в каждой.

**Доступ:** Публичный

**Query-параметры:**

| Параметр | Тип | Описание |
|----------|-----|----------|
| `search` | string | Поиск по `name`, `description` |
| `ordering` | string | `name`, `created_at` (префикс `-` для DESC) |

**Ответ `200 OK`:**
```json
[
  {
    "id": 1,
    "name": "Technology",
    "slug": "technology",
    "description": "Tech articles",
    "posts_count": 15,
    "created_at": "2026-01-01T00:00:00Z"
  }
]
```

---

### POST `/api/v1/posts/categories/`
Создание новой категории. `slug` генерируется автоматически из `name`.

**Доступ:** Требует авторизации

**Тело запроса:**
```json
{
  "name": "Science",
  "description": "Science articles"
}
```

**Ответ `201 Created`:** Созданный объект категории

**Ошибки:**
- `400` — категория с таким именем уже существует
- `401` — не авторизован

> ⚠️ **Баг:** в `CategorySerializer.create` используется `validated_data.get['name']` вместо `validated_data.get('name')` — упадёт с `TypeError`. Проще всего удалить метод `create` целиком, так как slug генерируется в `Category.save()`.

---

### GET `/api/v1/posts/categories/<slug>/`
Детальная информация о категории.

**Доступ:** Публичный

**Ответ `200 OK`:** Объект категории (аналогично списку)

**Ошибки:**
- `404` — категория не найдена

---

### PUT/PATCH `/api/v1/posts/categories/<slug>/`
Обновление категории.

**Доступ:** Требует авторизации

**Тело запроса (PATCH — все поля опциональны):**
```json
{
  "name": "Updated Name",
  "description": "Updated description"
}
```

**Ответ `200 OK`:** Обновлённый объект категории

---

### DELETE `/api/v1/posts/categories/<slug>/`
Удаление категории. Связанные посты получают `category = null`.

**Доступ:** Требует авторизации

**Ответ `204 No Content`**

---

### GET `/api/v1/posts/categories/<category_slug>/posts/`
Все опубликованные посты конкретной категории, без пагинации.

**Доступ:** Публичный

**Ответ `200 OK`:**
```json
{
  "category": {
    "id": 1,
    "name": "Technology",
    "slug": "technology",
    "description": "Tech articles",
    "posts_count": 15,
    "created_at": "2026-01-01T00:00:00Z"
  },
  "posts": []
}
```

**Ошибки:**
- `404` — категория не найдена

---

## Оставшиеся баги

| # | Файл | Описание |
|---|------|----------|
| 1 | `main/serializers.py` | `CategorySerializer.create`: `validated_data.get['name']` → нужны круглые скобки `get('name')`. Либо удалить метод — slug генерируется в `Category.save()` |
| 2 | `main/serializers.py` | `PostListSerializer`: поля `is_pinned`, `pinned_info` отсутствуют в модели `Post` — сериализатор упадёт при обращении к данным |
| 3 | `main/views.py` | `popular_posts`: сортировка по `-view_count` вместо `-views_count` |
| 4 | `main/views.py` | `PostListCreateView.get_queryset`: `filter(status=Q(...) \| Q(...))` — лишний именованный аргумент `status=`, нужно `filter(Q(...) \| Q(...))` |
| 5 | `main/urls.py` | Маршруты `pinned/` и `featured/` объявлены, но обработчики не реализованы в `views.py` |