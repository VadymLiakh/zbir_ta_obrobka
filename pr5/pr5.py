import pandas as pd
import numpy as np


def generate_energy_data(rows=30):
    """Генерує невеликий набір енергетичних даних з пропусками."""
    np.random.seed(42)

    data = {
        "timestamp": pd.date_range(start="2025-01-01", periods=rows, freq="h"),
        "consumption_kwh": np.random.uniform(100, 500, size=rows),
        "voltage": np.random.uniform(210, 240, size=rows),
        "temperature": np.random.uniform(-10, 35, size=rows)
    }

    df = pd.DataFrame(data)

    # Створення пропущених значень
    missing_indices = np.random.choice(rows, size=6, replace=False)
    df.loc[missing_indices[:2], "consumption_kwh"] = np.nan
    df.loc[missing_indices[2:4], "voltage"] = np.nan
    df.loc[missing_indices[4:], "temperature"] = np.nan

    return df


def fill_with_mean(df, column):
    """Заповнення пропусків середнім значенням."""
    df_copy = df.copy()
    df_copy[column] = df_copy[column].fillna(df_copy[column].mean())
    return df_copy


def fill_with_median(df, column):
    """Заповнення пропусків медіаною."""
    df_copy = df.copy()
    df_copy[column] = df_copy[column].fillna(df_copy[column].median())
    return df_copy


def fill_with_previous(df, column):
    """Заповнення пропусків попереднім значенням."""
    df_copy = df.copy()
    df_copy[column] = df_copy[column].ffill()
    return df_copy


def fill_with_next(df, column):
    """Заповнення пропусків наступним значенням."""
    df_copy = df.copy()
    df_copy[column] = df_copy[column].bfill()
    return df_copy


def main():
    df = generate_energy_data()

    print("ПОЧАТКОВІ ДАНІ З ПРОПУСКАМИ:")
    print(df)
    print("\nКількість пропущених значень:")
    print(df.isnull().sum())

    # Для прикладу обробляю тільки consumption_kwh
    column = "consumption_kwh"

    df_mean = fill_with_mean(df, column)
    df_median = fill_with_median(df, column)
    df_previous = fill_with_previous(df, column)
    df_next = fill_with_next(df, column)

    print("\n" + "=" * 60)
    print(f"ЗАПОВНЕННЯ ПРОПУСКІВ У СТОВПЦІ: {column}")
    print("=" * 60)

    print("\n1. Імпутація середнім:")
    print(df_mean[[ "timestamp", column ]])

    print("\n2. Імпутація медіаною:")
    print(df_median[[ "timestamp", column ]])

    print("\n3. Заповнення попереднім значенням (ffill):")
    print(df_previous[[ "timestamp", column ]])

    print("\n4. Заповнення наступним значенням (bfill):")
    print(df_next[[ "timestamp", column ]])

    print("\nКількість пропусків після обробки:")
    print("Середнє:", df_mean[column].isnull().sum())
    print("Медіана:", df_median[column].isnull().sum())
    print("Попереднє значення:", df_previous[column].isnull().sum())
    print("Наступне значення:", df_next[column].isnull().sum())


if __name__ == "__main__":
    main()
