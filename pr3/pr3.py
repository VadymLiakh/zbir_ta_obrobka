import pandas as pd
import numpy as np


def memory_usage_mb(df):
    """Повертає використання пам'яті DataFrame у МБ."""
    return df.memory_usage(deep=True).sum() / 1024**2


def generate_energy_dataset(rows=1_000_000):
    """
    Генерує великий штучний енергетичний набір даних.
    """
    np.random.seed(42)

    df = pd.DataFrame({
        "meter_id": np.random.randint(1000, 5000, size=rows),  # ID лічильника
        "region": np.random.choice(["North", "South", "East", "West", "Center"], size=rows),
        "energy_type": np.random.choice(["Solar", "Wind", "Hydro", "Thermal", "Nuclear"], size=rows),
        "consumption_kwh": np.random.uniform(50, 5000, size=rows),  # споживання
        "voltage": np.random.uniform(210, 240, size=rows),          # напруга
        "current": np.random.uniform(1, 100, size=rows),            # струм
        "temperature": np.random.uniform(-20, 45, size=rows),       # температура
        "is_peak_hour": np.random.choice([True, False], size=rows), # пікова година
        "status": np.random.choice(["OK", "Warning", "Critical"], size=rows)
    })

    return df


def optimize_dataframe(df):
    """
    Оптимізація типів даних:
    - int -> менші int типи
    - float -> float32
    - object -> category, якщо мало унікальних значень
    - bool -> bool
    """
    df_optimized = df.copy()

    for col in df_optimized.columns:
        col_type = df_optimized[col].dtype

        if pd.api.types.is_integer_dtype(col_type):
            df_optimized[col] = pd.to_numeric(df_optimized[col], downcast="integer")

        elif pd.api.types.is_float_dtype(col_type):
            df_optimized[col] = pd.to_numeric(df_optimized[col], downcast="float")

        elif pd.api.types.is_bool_dtype(col_type):
            df_optimized[col] = df_optimized[col].astype("bool")

        elif pd.api.types.is_object_dtype(col_type):
            unique_ratio = df_optimized[col].nunique() / len(df_optimized[col])
            if unique_ratio < 0.5:
                df_optimized[col] = df_optimized[col].astype("category")

    return df_optimized


def print_dtype_changes(df_before, df_after):
    print("\nЗміни типів даних:")
    print("-" * 50)
    for col in df_before.columns:
        if df_before[col].dtype != df_after[col].dtype:
            print(f"{col}: {df_before[col].dtype} -> {df_after[col].dtype}")


def main():
    print("Генерація великого енергетичного набору даних...")
    df = generate_energy_dataset(rows=1_000_000)

    print("\nПерші 5 рядків датасету:")
    print(df.head())

    print("\nТипи даних ДО оптимізації:")
    print(df.dtypes)

    memory_before = memory_usage_mb(df)
    print(f"\nВикористання пам'яті ДО оптимізації: {memory_before:.2f} МБ")

    df_optimized = optimize_dataframe(df)

    print("\nТипи даних ПІСЛЯ оптимізації:")
    print(df_optimized.dtypes)

    # Зберегти початковий датасет
    df.to_csv("energy_before.csv", index=False)

    # Зберегти оптимізований датасет
    df_optimized.to_csv("energy_after.csv", index=False)

    memory_after = memory_usage_mb(df_optimized)
    print(f"\nВикористання пам'яті ПІСЛЯ оптимізації: {memory_after:.2f} МБ")

    saved_memory = memory_before - memory_after
    saved_percent = (saved_memory / memory_before) * 100

    print(f"\nЗекономлено пам'яті: {saved_memory:.2f} МБ")
    print(f"Відсоток економії: {saved_percent:.2f}%")

    print_dtype_changes(df, df_optimized)


if __name__ == "__main__":
    main()
