from test_data_sergeev import exam_sergeev_data
from test_data_grigoriev import exam_grigoriev_data
import random
import json
import sys
import platform  # Для более надежного определения ОС

# --- НАСТРОЙКИ ТЕСТА ---
SHUFFLE_ANSWER_OPTIONS = False
USE_SINGLE_KEY_INPUT = True  # Новая настройка: использовать ли ввод одной клавишей

# --- Попытка импорта библиотеки для ввода одной клавиши ---
getch_fn = None  # Функция для считывания одного символа

if USE_SINGLE_KEY_INPUT:
    if platform.system() == "Windows":
        try:
            import msvcrt
            # Оборачиваем msvcrt.getch(), чтобы он возвращал строку, а не байты
            # и обрабатывал возможные ошибки декодирования

            def win_getch_wrapper():
                try:
                    char_byte = msvcrt.getch()
                    return char_byte.decode('utf-8', errors='ignore')
                except Exception:  # Ловим общие исключения на всякий случай
                    return ''  # Возвращаем пустую строку в случае ошибки
            getch_fn = win_getch_wrapper
            print("INFO: Используется 'msvcrt' для ввода одной клавишей (Windows).")
        except ImportError:
            print("WARNING: Не удалось импортировать 'msvcrt' на Windows. Будет использоваться стандартный ввод (с нажатием Enter).")
            USE_SINGLE_KEY_INPUT = False

else:
    print("INFO: Ввод одной клавишей отключен в настройках (USE_SINGLE_KEY_INPUT = False). Будет использоваться стандартный ввод.")


# Импортируем данные из других файлов


def load_questions_from_json(filename: str):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Успешно загружены вопросы из файла '{filename}'.")
        return data
    except FileNotFoundError:
        print(
            f"\nОшибка: Файл '{filename}' не найден. Убедитесь, что он находится в той же папке.")
        return None
    except json.JSONDecodeError:
        print(
            f"\nОшибка: Некорректный формат данных в файле '{filename}'. Проверьте синтаксис JSON.")
        return None


def run_test(questions_data: list, shuffle_options: bool):
    if not questions_data:
        print("Не удалось загрузить вопросы для теста.")
        return

    score = 0
    random.shuffle(questions_data)
    total_questions = len(questions_data)

    print("\n--- Начало теста ---")
    if shuffle_options:
        print("Режим перемешивания ответов: ВКЛЮЧЕН.")
    else:
        print("Режим перемешивания ответов: ВЫКЛЮЧЕН.")

    for i, item in enumerate(questions_data):
        print(f"\nВопрос {i + 1}/{total_questions}: {item['question']}")

        options_to_display = list(item['options'])
        if shuffle_options:
            random.shuffle(options_to_display)

        for j, option in enumerate(options_to_display):
            print(f"  {j + 1}. {option}")

        if USE_SINGLE_KEY_INPUT and getch_fn:
            print("Ваш ответ (нажмите цифру): ", end='', flush=True)
            while True:
                user_key = getch_fn()
                if user_key and user_key.isdigit() and 1 <= int(user_key) <= len(options_to_display):
                    user_choice_index = int(user_key) - 1
                    print(user_key)
                    break
                # Выход по 'q' или 'й'
                elif user_key and user_key.lower() in ['q', 'й']:
                    print("\nТест прерван пользователем.")
                    return
                # Игнорируем другие нажатия
        else:  # Стандартный ввод с Enter
            while True:
                try:
                    user_input_str = input(
                        "Ваш ответ (введите номер и нажмите Enter): ")
                    if user_input_str.lower() in ['q', 'й']:
                        print("\nТест прерван пользователем.")
                        return
                    user_choice_index = int(user_input_str) - 1
                    if 0 <= user_choice_index < len(options_to_display):
                        break
                    else:
                        print(
                            f"Ошибка: введите число от 1 до {len(options_to_display)}.")
                except ValueError:
                    print("Ошибка: введите номер варианта ответа.")

        user_answer_text = options_to_display[user_choice_index]
        correct_answer_text = item['answer']

        if user_answer_text == correct_answer_text:
            print("✅ Правильно!")
            score += 1
        else:
            print(f"❌ Неправильно. Верный ответ: {correct_answer_text}")

    print("\n--- Тест завершен ---")

    if total_questions > 0:
        percentage = (score / total_questions) * 100
        print(
            f"Ваш результат: {score} из {total_questions} правильных ответов.")
        print(f"Процент верных ответов: {percentage:.2f}%")
    else:
        print("В тесте не было вопросов.")


if __name__ == "__main__":
    while True:
        print("\n--- Меню выбора теста ---")
        print("1. Экзамен (по варианту Григорьева В.Н.)")
        print("2. Зачет (по варианту Сергеева)")
        print("3. Тест из файла (questions_from_file.json)")
        print("4. Выход")

        choice = input("Выберите тест (1-4) и нажмите Enter: ")

        if choice == '1':
            questions = list(exam_grigoriev_data)
            max_q = len(questions)
            while True:
                try:
                    num_q = int(
                        input(f"Сколько вопросов пройти? (1-{max_q}): "))
                    if 1 <= num_q <= max_q:
                        break
                    else:
                        print(f"Введите число от 1 до {max_q}.")
                except ValueError:
                    print("Ошибка: введите число.")
            selected_questions = random.sample(questions, num_q)
            run_test(selected_questions, shuffle_options=SHUFFLE_ANSWER_OPTIONS)
        elif choice == '2':
            questions = list(exam_sergeev_data)
            max_q = len(questions)
            while True:
                try:
                    num_q = int(
                        input(f"Сколько вопросов пройти? (1-{max_q}): "))
                    if 1 <= num_q <= max_q:
                        break
                    else:
                        print(f"Введите число от 1 до {max_q}.")
                except ValueError:
                    print("Ошибка: введите число.")
            selected_questions = random.sample(questions, num_q)
            run_test(selected_questions, shuffle_options=SHUFFLE_ANSWER_OPTIONS)
        elif choice == '3':
            questions = load_questions_from_json('questions_from_file.json')
            if questions:
                max_q = len(questions)
                while True:
                    try:
                        num_q = int(
                            input(f"Сколько вопросов пройти? (1-{max_q}): "))
                        if 1 <= num_q <= max_q:
                            break
                        else:
                            print(f"Введите число от 1 до {max_q}.")
                    except ValueError:
                        print("Ошибка: введите число.")
                selected_questions = random.sample(questions, num_q)
                run_test(selected_questions,
                         shuffle_options=SHUFFLE_ANSWER_OPTIONS)
        elif choice == '4':
            print("До встречи!")
            break
        else:
            print("Неверный ввод. Пожалуйста, выберите от 1 до 4.")
