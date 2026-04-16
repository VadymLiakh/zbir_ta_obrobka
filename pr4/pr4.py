import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error


def generate_energy_time_series(n=200):
    """Генерує часовий ряд енергоспоживання."""
    np.random.seed(42)

    time_index = pd.date_range(start="2025-01-01", periods=n, freq="h")

    trend = np.linspace(100, 150, n)
    seasonality = 20 * np.sin(np.linspace(0, 8 * np.pi, n))
    noise = np.random.normal(0, 3, n)

    consumption = trend + seasonality + noise

    df = pd.DataFrame({
        "timestamp": time_index,
        "consumption": consumption
    })

    return df


def create_missing_values(df, missing_ratio=0.1):
    """Створює пропущені значення у часовому ряді."""
    df_missing = df.copy()

    np.random.seed(10)
    missing_indices = np.random.choice(df.index, size=int(len(df) * missing_ratio), replace=False)

    original_values = df.loc[missing_indices, "consumption"].copy()
    df_missing.loc[missing_indices, "consumption"] = np.nan

    return df_missing, missing_indices, original_values


def calculate_errors(true_values, predicted_values):
    """Обчислює похибки."""
    mae = mean_absolute_error(true_values, predicted_values)
    rmse = np.sqrt(mean_squared_error(true_values, predicted_values))
    return mae, rmse


def main():
    # 1. Генерація часового ряду
    df = generate_energy_time_series(n=200)

    # 2. Створення пропусків
    df_missing, missing_indices, original_values = create_missing_values(df, missing_ratio=0.1)

    # 3. Лінійна інтерполяція
    df_linear = df_missing.copy()
    df_linear["consumption"] = df_linear["consumption"].interpolate(method="linear")

    # 4. Поліноміальна інтерполяція
    df_polynomial = df_missing.copy()
    df_polynomial["consumption"] = df_polynomial["consumption"].interpolate(method="polynomial", order=2)

    # 5. Сплайн-інтерполяція
    df_spline = df_missing.copy()
    df_spline["consumption"] = df_spline["consumption"].interpolate(method="spline", order=3)

    # 6. Оцінка похибки тільки на тих місцях, де були пропуски
    true_vals = original_values.values
    linear_vals = df_linear.loc[missing_indices, "consumption"].values
    polynomial_vals = df_polynomial.loc[missing_indices, "consumption"].values
    spline_vals = df_spline.loc[missing_indices, "consumption"].values

    linear_mae, linear_rmse = calculate_errors(true_vals, linear_vals)
    poly_mae, poly_rmse = calculate_errors(true_vals, polynomial_vals)
    spline_mae, spline_rmse = calculate_errors(true_vals, spline_vals)

    # 7. Вивід результатів
    print("ПОРІВНЯННЯ МЕТОДІВ ІНТЕРПОЛЯЦІЇ")
    print("-" * 50)
    print(f"Лінійна інтерполяція:     MAE = {linear_mae:.4f}, RMSE = {linear_rmse:.4f}")
    print(f"Поліноміальна інтерполяція: MAE = {poly_mae:.4f}, RMSE = {poly_rmse:.4f}")
    print(f"Сплайн-інтерполяція:      MAE = {spline_mae:.4f}, RMSE = {spline_rmse:.4f}")

    # 8. Визначення найкращого методу
    results = {
        "Лінійна": linear_rmse,
        "Поліноміальна": poly_rmse,
        "Сплайн": spline_rmse
    }

    best_method = min(results, key=results.get)
    print("-" * 50)
    print(f"Найменшу похибку має метод: {best_method}")


if __name__ == "__main__":
    main()
