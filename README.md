# TattooAI Studio

## Опис проєкту (Бізнес-логіка)

TattooAI (ТатуАЙ) --- це інноваційна вебплатформа для студії кастомного татуювання. Головна мета сайту --- спростити комунікацію між клієнтом та майстром, а також допомогти клієнтам краще візуалізувати свої ідеї.

На платформі клієнти можуть переглядати портфоліо майстрів та каталог готових ескізів студії. Основна унікальна функція сайту --- це інтеграція зі штучним інтелектом. Користувач може описати бажане татуювання словами (наприклад, "щільний чорно-білий ескіз морди собаки, стиль blackwork"), а ШІ згенерує візуальний концепт. Усі згенеровані концепти та вподобані готові ескізи клієнт може зберігати у своєму особистому кабінеті, щоб згодом прикріпити їх до заявки під час бронювання сеансу у обраного майстра.

> У поточній роботі реалізовано CRUD для основних ресурсів: ескізи (`designs`) та майстри (`masters`).

## Як запустити проєкт

```bash
python -m venv .venv
.venv\Scripts\activate          # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Сервер буде доступний за адресою **http://127.0.0.1:8000**.

Колекція Postman: `postman/TattooAI.postman_collection.json` (базова адреса винесена у змінну `{{base_url}}` = `http://127.0.0.1:8000`).

## Архітектура REST API

Дані передаються у форматі `JSON`. Архітектура побудована за принципами REST, де кожен ендпоінт відповідає за певний ресурс. Версія API вказана в URL (`/api/v1/`). Для оновлення використовується `PUT` (повна заміна об'єкта), `DELETE` повертає видалений об'єкт.

### 1. Каталог ескізів (Designs)

#### Список ескізів

**Опис:** Отримання переліку готових ескізів студії з можливістю фільтрації за стилем.

* Request Method: `GET`
* Endpoint: `/api/v1/designs`
* Request Body: `?style=blackwork` (Query-параметр, необов'язковий)
* Response Status: `200 OK`
* Response Body:

```json
[
  {
    "id": 1,
    "title": "Орнаментальна мандала",
    "style": "blackwork",
    "price": 1500,
    "image_url": "https://example.com/images/mandala.jpg",
    "master": 1
  }
]
```

> **Зміна:** у ескіза з'явилося поле `master` (id майстра). Воно потрібне, щоб пов'язати ескізи з майстрами та реалізувати обмеження на видалення майстра.

#### Окремий ескіз

**Опис:** Отримання ескіза за його id.

* Request Method: `GET`
* Endpoint: `/api/v1/designs/{id}`
* Response Status: `200 OK`
* Response Body:

```json
{
  "id": 1,
  "title": "Орнаментальна мандала",
  "style": "blackwork",
  "price": 1500,
  "image_url": "https://example.com/images/mandala.jpg",
  "master": 1
}
```

#### Створення ескіза

**Опис:** Додавання нового ескіза до каталогу.

* Request Method: `POST`
* Endpoint: `/api/v1/designs`
* Request Body:

```json
{
  "title": "Орнаментальна мандала",
  "style": "blackwork",
  "price": 1500,
  "image_url": "https://example.com/images/mandala.jpg",
  "master": 1
}
```

* Response Status: `201 Created`
* Response Body: створений ескіз (як у прикладі вище, з полем `id`).

Поля: `title` --- рядок; `style` --- рядок; `price` --- ціле число більше 0; `image_url` --- коректний URL; `master` --- id існуючого майстра.

#### Редагування ескіза

**Опис:** Повне оновлення даних ескіза.

* Request Method: `PUT`
* Endpoint: `/api/v1/designs/{id}`
* Request Body: ті самі поля, що й при створенні.
* Response Status: `200 OK`
* Response Body: оновлений ескіз.

#### Видалення ескіза

**Опис:** Видалення ескіза з каталогу.

* Request Method: `DELETE`
* Endpoint: `/api/v1/designs/{id}`
* Response Status: `200 OK`
* Response Body: видалений ескіз.

### 2. Майстри (Masters)

#### Список майстрів

* Request Method: `GET`
* Endpoint: `/api/v1/masters`
* Response Status: `200 OK`
* Response Body:

```json
[
  {
    "id": 1,
    "name": "Олена Корж",
    "specialization": "blackwork"
  }
]
```

#### Окремий майстер

* Request Method: `GET`
* Endpoint: `/api/v1/masters/{id}`
* Response Status: `200 OK`
* Response Body: об'єкт майстра (як у прикладі вище).

#### Створення майстра

* Request Method: `POST`
* Endpoint: `/api/v1/masters`
* Request Body:

```json
{
  "name": "Олена Корж",
  "specialization": "blackwork"
}
```

* Response Status: `201 Created`
* Response Body: створений майстер (з полем `id`).

Поля: `name` --- обов'язковий рядок; `specialization` --- необов'язковий рядок.

#### Редагування майстра

* Request Method: `PUT`
* Endpoint: `/api/v1/masters/{id}`
* Request Body: ті самі поля, що й при створенні.
* Response Status: `200 OK`
* Response Body: оновлений майстер.

#### Видалення майстра

* Request Method: `DELETE`
* Endpoint: `/api/v1/masters/{id}`
* Response Status: `200 OK`
* Response Body: видалений майстер.
* Обмеження: майстра не можна видалити, якщо за ним закріплені ескізи (див. розділ нижче).

## Обмеження предметної області та помилки

| Ситуація | Статус | Обґрунтування |
|---|---|---|
| Невалідні дані (порожнє поле, ціна ≤ 0, некоректний URL, неіснуючий `master`) | `400 Bad Request` | Запит коректний за формою, але дані не проходять валідацію |
| Ескіз або майстер із таким id не існує | `404 Not Found` | Запитаного ресурсу не знайдено |
| Видалення майстра, за яким закріплені ескізи | `409 Conflict` | Запит коректний, але суперечить поточному стану даних |

Формат помилки однаковий для всіх ендпоінтів:

```json
{
  "error": {
    "code": "conflict",
    "message": "Неможливо видалити майстра «Олена Корж», оскільки за ним закріплено ескізів: 3. Спершу видаліть ці ескізи або змініть їхнього майстра."
  }
}
```

Для помилок валідації (`400`) додатково повертається `details` з помилками по полях:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Невалідні дані. Деталі в полі details.",
    "details": {
      "price": ["Ціна має бути більшою за 0."]
    }
  }
}
```

## CORS

Для роботи фронтенду, запущеного на іншому порту, на бекенді налаштовано CORS через `django-cors-headers`. Дозволені лише конкретні адреси (`http://127.0.0.1:5500` та `http://localhost:5500`), вони вказані в `CORS_ALLOWED_ORIGINS` у файлі `config/settings.py`.
