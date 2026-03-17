import csv
import random
import string
import os
from pathlib import Path


# --- Генерація випадкового тексту ---
def rand_str(n: int) -> str:
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=n))


# --- Функція створення 2 великих CSV ---
def generate_two_big_csv(
    left_path: str,
    right_path: str,
    rows: int,
    text_len_left: int = 250,
    text_len_right: int = 250
):
    Path(left_path).parent.mkdir(parents=True, exist_ok=True)

    with open(left_path, "w", newline="", encoding="utf-8") as f1, \
         open(right_path, "w", newline="", encoding="utf-8") as f2:

        w1 = csv.writer(f1)
        w2 = csv.writer(f2)

        # Заголовки
        w1.writerow(["ID", "amount", "payload"])
        w2.writerow(["ID", "category", "meta"])

        for i in range(rows):

            # Лівий файл
            w1.writerow([
                i,
                random.randint(0, 10_000_000),
                rand_str(text_len_left)
            ])

            # Правий файл
            w2.writerow([
                i,
                random.choice(["A", "B", "C", "D"]),
                rand_str(text_len_right)
            ])

            if i % 100_000 == 0 and i != 0:
                print(f"Згенеровано {i:,} рядків...")



# --- Перевірка розміру ---
def show_size(path):
    size_gb = os.path.getsize(path) / (1024**3)
    print(f"{path} = {size_gb:.2f} GB")


if __name__ == "__main__":

    rows = 5_000_000  # ← під це часто виходить >1GB

    left_file = "data/big_left.csv"
    right_file = "data/big_right.csv"

    generate_two_big_csv(left_file, right_file, rows)

    show_size(left_file)
    show_size(right_file)
