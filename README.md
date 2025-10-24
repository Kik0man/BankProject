# Проект банковское дело

# Описание

Проект банковское дело - домашние задания по теме разработка на Python, 
которые по мере продвижения добавляются в этот проект

## Тестирование

Проект был протестирован по всем модулям, при тестировании была создана папка tests, 
внутри которой и были созданы модули для тестирования. Были созданы фикстуры.
Все модули прошли тест, функциональный код покрыт тестами более чем на 80%, а именно 94%.

## Установка:

1. Клонируйте репозиторий:
```
https://github.com/Kik0man/BankProject.git
```
2. Установите зависимости:
```
pip install -r requirements.txt
```

# Использование:

Практического использования пока что нет, основная задача, это научиться правильно создавать код 
и работать с GitHUB, но если есть желание, то:
1. Перейдите на страницу в вашем веб-браузере.
2. Создайте новую учетную запись или войдите существующей.
3. Создайте новую запись в блоге или оставьте комментарий к существующей.

## Документация:

Дополнительную информацию о структуре проекта и API можно найти в [документации](C:\Users\Astolfo\PycharmProjects\Bank_Project/README.md).


## Лицензия:

По лицензии пока нет информации, так как еще не дошли до этого.

# Новый модуль обработки банковских транзакций

Новый модуль предоставляет функции для работы с банковскими операциями.

## Функции
Всего было добавлено 3 функции: filter_by_currency, 
transaction_descriptions(transactions),
transaction_descriptions(transactions)

### filter_by_currency(transactions, currency_code)
Фильтрует транзакции по валюте.
```
usd_transactions = filter_by_currency(transactions, "USD")
for transaction in usd_transactions:
    print(transaction['id'])
```
### transaction_descriptions(transactions)
Извлекает описания операций.
```
descriptions = transaction_descriptions(transactions)
for description in descriptions:
    print(description)
```
### card_number_generator(start, end)
Генерирует номера карт в заданном диапазоне.
```
for card in card_number_generator(1, 5):
    print(card)
```

# Новый модуль работы с json и API

## Модуль utils принимает на вход файл operations.json и получает данные

## Модуль external_api сравнивает актуальный курс валют и производит конвертацию валюты

## Тесты новых модулей

### Для тестирования модулей были написаны тесты test_utils & test_external_api


# Новый модуль file-reader.py
Он отвечает за чтение файлов форматов csv и excel
функция read_csv_file отвечает за чтение csv файлов, а read_excel_file за excel файлы