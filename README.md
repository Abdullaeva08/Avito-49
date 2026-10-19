<div align="center">

# 🛒 Avito-49

**Сервис объявлений в стиле Avito на Python**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.x-092E20?logo=django&logoColor=white)
![Status](https://img.shields.io/badge/status-in%20development-orange)

</div>

---

## 📖 О проекте

**Avito-49** — учебный проект: платформа для размещения и поиска объявлений по аналогии с Avito. Пользователи публикуют объявления о товарах и услугах, а покупатели просматривают, ищут и фильтруют их.

Проект создан в рамках курса Python (поток 49).

## ✨ Возможности

> Оставьте в списке только то, что реально реализовано в коде.

- 👤 Регистрация и авторизация пользователей
- 📝 Создание, редактирование и удаление объявлений
- 🗂 Категории товаров
- 🖼 Загрузка фотографий
- 🔍 Поиск и фильтрация (категория, цена, город)
- ⭐ Избранное
- 🛠 Админ-панель для управления контентом

## 🧰 Технологии

| Назначение | Инструмент |
|---|---|
| Язык | Python 3 |
| Фреймворк | Django |
| База данных | SQLite (по умолчанию) |
| Изображения | Pillow |

## 🚀 Быстрый старт

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/Abdullaeva08/Avito-49.git
cd Avito-49
```

### 2. Создайте виртуальное окружение

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Установите зависимости

```bash
pip install -r requirements.txt
# если файла нет:
pip install django pillow
```

### 4. Примените миграции

```bash
python manage.py migrate
```

### 5. Создайте суперпользователя

```bash
python manage.py createsuperuser
```

### 6. Запустите сервер

```bash
python manage.py runserver
```

Приложение: **http://127.0.0.1:8000/**
Админ-панель: **http://127.0.0.1:8000/admin/**

> Если `manage.py` лежит во вложенной папке, сначала перейдите в неё командой `cd`.

## 🗺 Планы развития

- [ ] REST API (Django REST Framework)
- [ ] Чат между покупателем и продавцом
- [ ] Рейтинги и отзывы
- [ ] Деплой (Docker + PostgreSQL)
- [ ] Тесты

## 🤝 Участие в разработке

1. Сделайте fork репозитория
2. Создайте ветку: `git checkout -b feature/my-feature`
3. Закоммитьте изменения: `git commit -m "Add my feature"`
4. Отправьте ветку: `git push origin feature/my-feature`
5. Откройте Pull Request

## 👩‍💻 Автор

[@Abdullaeva08](https://github.com/Abdullaeva08)

---

<div align="center">
⭐ Если проект был полезен, поставьте звезду!
</div>
