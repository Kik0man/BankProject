import os
import sys
from typing import Any, Dict, List

from src.file_reader import read_csv_file, read_excel_file
from src.masks import get_mask_account, get_mask_card_number
from src.processing import count_transactions_by_category, filter_by_description, filter_by_state, sort_by_date
from src.utils import load_transactions
from src.widget import get_date

# Добавляем путь к src для импорта модулей
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


def display_transaction(transaction: Dict[str, Any]) -> None:
    """Отображает одну транзакцию в читаемом формате."""
    # Дата
    date_str = get_date(transaction["date"])
    print(f"{date_str} {transaction['description']}")

    # Откуда
    if "from" in transaction and transaction["from"]:
        from_str = transaction["from"]
        if "счет" in from_str.lower() or "счёт" in from_str.lower():
            # Это счет
            digits = "".join(filter(str.isdigit, from_str))
            masked_from = f"Счет {get_mask_account(digits)}"
        else:
            # Это карта
            digits = "".join(filter(str.isdigit, from_str))
            card_name = from_str.replace(digits, "").strip()
            masked_from = f"{card_name} {get_mask_card_number(digits)}"
        print(f"{masked_from} -> ", end="")
    else:
        print("Открытие вклада -> ", end="")

    # Куда
    to_str = transaction["to"]
    if "счет" in to_str.lower() or "счёт" in to_str.lower():
        # Это счет
        digits = "".join(filter(str.isdigit, to_str))
        masked_to = f"Счет {get_mask_account(digits)}"
    else:
        # Это карта
        digits = "".join(filter(str.isdigit, to_str))
        card_name = to_str.replace(digits, "").strip()
        masked_to = f"{card_name} {get_mask_card_number(digits)}"
    print(f"{masked_to}")

    # Сумма и валюта
    if "operationAmount" in transaction:
        amount = transaction["operationAmount"]["amount"]
        currency = transaction["operationAmount"]["currency"]["name"]
        print(f"Сумма: {amount} {currency}")
    elif "amount" in transaction:
        amount = transaction["amount"]
        currency = transaction.get("currency_name", "руб.")
        print(f"Сумма: {amount} {currency}")

    print()


def get_user_yes_no(prompt: str) -> bool:
    """Получает ответ Да/Нет от пользователя."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ["да", "д", "yes", "y"]:
            return True
        elif answer in ["нет", "н", "no", "n"]:
            return False
        else:
            print("Пожалуйста, введите 'Да' или 'Нет'")


def get_user_choice(options: List[str], prompt: str) -> str:
    """Получает выбор пользователя из списка options."""
    while True:
        print(prompt)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        try:
            choice = int(input("Ваш выбор: ").strip())
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print(f"Пожалуйста, введите число от 1 до {len(options)}")
        except ValueError:
            print("Пожалуйста, введите число")


def main() -> None:
    """Основная функция программы."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")

    # Выбор типа файла
    file_type = get_user_choice(
        [
            "Получить информацию о транзакциях из JSON-файла",
            "Получить информацию о транзакциях из CSV-файла",
            "Получить информацию о транзакциях из XLSX-файла",
        ],
        "",
    )

    transactions = []
    file_path = ""

    try:
        if "JSON" in file_type:
            print("Для обработки выбран JSON-файл.")
            file_path = "data/operations.json"
            transactions = load_transactions(file_path)
        elif "CSV" in file_type:
            print("Для обработки выбран CSV-файл.")
            file_path = "data/transactions.csv"
            transactions = read_csv_file(file_path)
        elif "XLSX" in file_type:
            print("Для обработки выбран XLSX-файл.")
            file_path = "data/transactions_excel.xlsx"
            transactions = read_excel_file(file_path)
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return

    if not transactions:
        print("Не удалось загрузить транзакции или файл пуст.")
        return

    print(f"Загружено {len(transactions)} транзакций")

    # Фильтрация по статусу
    available_states = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print(f"Доступные для фильтрации статусы: {', '.join(available_states)}")

        state_input = input("Статус: ").strip().upper()

        if state_input in available_states:
            filtered_transactions = filter_by_state(transactions, state_input)
            print(f"Операции отфильтрованы по статусу '{state_input}'")
            break
        else:
            print(f"Статус операции '{state_input}' недоступен.")

    # Сортировка по дате
    if get_user_yes_no("\nОтсортировать операции по дате? Да/Нет: "):
        sort_order = get_user_choice(
            ["по возрастанию", "по убыванию"], "\nОтсортировать по возрастанию или по убыванию?"
        )
        reverse = sort_order == "по убыванию"
        filtered_transactions = sort_by_date(filtered_transactions, reverse)
        print(f"Операции отсортированы {sort_order}")

    # Фильтрация по валюте (только для RUB)
    if get_user_yes_no("\nВыводить только рублевые транзакции? Да/Нет: "):
        rub_transactions = []
        for transaction in filtered_transactions:
            if "operationAmount" in transaction:
                currency = transaction["operationAmount"]["currency"]["code"]
                if currency == "RUB":
                    rub_transactions.append(transaction)
            elif "currency_code" in transaction:
                if transaction["currency_code"] == "RUB":
                    rub_transactions.append(transaction)
        filtered_transactions = rub_transactions
        print("Оставлены только рублевые транзакции")

    # Фильтрация по описанию
    if get_user_yes_no("\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет: "):
        search_word = input("Введите слово для поиска в описании: ").strip()
        if search_word:
            filtered_transactions = filter_by_description(filtered_transactions, search_word)
            print(f"Операции отфильтрованы по слову '{search_word}'")

    # Вывод результатов
    print("\n" + "=" * 50)
    print("Распечатываю итоговый список транзакций...")
    print("=" * 50)

    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Всего банковских операций в выборке: {len(filtered_transactions)}\n")

    for transaction in filtered_transactions:
        display_transaction(transaction)

    # Дополнительная статистика по категориям
    if get_user_yes_no("\nПоказать статистику по категориям операций? Да/Нет: "):
        all_descriptions = set()
        for transaction in filtered_transactions:
            if "description" in transaction:
                all_descriptions.add(transaction["description"])

        if all_descriptions:
            categories_stats = count_transactions_by_category(filtered_transactions, list(all_descriptions))
            print("\nСтатистика по категориям:")
            for category, count in categories_stats.items():
                if count > 0:
                    print(f"  {category}: {count} операций")


if __name__ == "__main__":
    main()
