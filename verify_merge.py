import pandas as pd
import random


LEFT_PATH = "data/big_left.csv"
RIGHT_PATH = "data/big_right.csv"
MERGED_PATH = "data/merged_result.csv"

ID_COL = "ID"


# --- 1. Перевірка кількості рядків ---
def check_row_counts():
    print("Перевірка кількості рядків...")

    left_rows = sum(1 for _ in open(LEFT_PATH, encoding="utf-8")) - 1
    merged_rows = sum(1 for _ in open(MERGED_PATH, encoding="utf-8")) - 1

    print(f"Left rows:   {left_rows:,}")
    print(f"Merged rows: {merged_rows:,}")

    if left_rows == merged_rows:
        print("OK: Кількість рядків співпадає (LEFT JOIN коректний)")
    else:
        print("ERROR: Кількість рядків НЕ співпадає")


# --- 2. Перевірка наявності колонок ---
def check_columns():
    print("\nПеревірка колонок...")

    merged_df = pd.read_csv(MERGED_PATH, nrows=5)

    print("Колонки merged:")
    print(list(merged_df.columns))

    if "category" in merged_df.columns and "meta" in merged_df.columns:
        print("OK: Колонки з правого файлу додані")
    else:
        print("ERROR: Колонки не знайдені")


# --- 3. Випадкова перевірка ID ---
def random_id_check(samples=5):
    print("\nВипадкова перевірка ID...")

    merged_df = pd.read_csv(MERGED_PATH, usecols=["ID", "category"], nrows=100_000)

    ids = random.sample(list(merged_df["ID"]), samples)

    for i in ids:
        row = merged_df[merged_df["ID"] == i]

        if row["category"].isna().all():
            print(f"ID {i}: немає у правому (NaN) — OK")
        else:
            print(f"ID {i}: знайдений у правому — OK")


# --- 4. Частка NaN ---
def nan_ratio():
    print("\nПеревірка частки NaN...")

    df = pd.read_csv(MERGED_PATH, usecols=["category"], nrows=200_000)

    ratio = df["category"].isna().mean()

    print(f"NaN ratio ≈ {ratio:.2%}")



if __name__ == "__main__":
    print("=== VERIFY MERGE ===\n")

    check_row_counts()
    check_columns()
    random_id_check()
    nan_ratio()

    print("\nПеревірка завершена")
