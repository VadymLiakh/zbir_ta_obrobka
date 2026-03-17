import pandas as pd
import numpy as np


def generate_orders_csv(filename="orders.csv", n_rows=15000, seed=42):
    rng = np.random.default_rng(seed)

    products = [
        "Laptop", "Phone", "Tablet", "Headphones", "Monitor",
        "Keyboard", "Mouse", "Printer", "Camera", "Smartwatch"
    ]

    cities = [
        "Kyiv", "Lviv", "Odesa", "Dnipro", "Kharkiv",
        "Warsaw", "Krakow", "Gdansk", "Wroclaw", "Poznan"
    ]

    # Базові параметри по товарах
    product_base_price = {
        "Laptop": 42000,
        "Phone": 26000,
        "Tablet": 18000,
        "Headphones": 3200,
        "Monitor": 11000,
        "Keyboard": 1800,
        "Mouse": 950,
        "Printer": 7800,
        "Camera": 23000,
        "Smartwatch": 9000,
    }

    start_date = np.datetime64("2024-01-01")
    end_date = np.datetime64("2025-12-31")
    days_range = (end_date - start_date).astype(int)

    product = rng.choice(
        products,
        size=n_rows,
        p=[0.15, 0.19, 0.08, 0.12, 0.09, 0.11, 0.11, 0.04, 0.04, 0.07]
    )

    city = rng.choice(
        cities,
        size=n_rows,
        p=[0.14, 0.09, 0.08, 0.08, 0.07, 0.18, 0.11, 0.08, 0.10, 0.07]
    )

    order_date = start_date + rng.integers(0, days_range + 1, size=n_rows).astype("timedelta64[D]")
    quantity = rng.integers(1, 6, size=n_rows)
    discount = np.round(rng.uniform(0, 0.25, size=n_rows), 2)
    rating = np.round(rng.normal(4.2, 0.55, size=n_rows), 1)

    # Генерація ціни з шумом по кожному товару
    price = []
    for p in product:
        base = product_base_price[p]
        noisy_price = base * rng.uniform(0.75, 1.30)
        price.append(round(noisy_price, 2))
    price = np.array(price)

    total = np.round(price * quantity * (1 - discount), 2)

    df = pd.DataFrame({
        "order_id": np.arange(1, n_rows + 1),
        "order_date": order_date.astype(str),
        "city": city,
        "product": product,
        "price": price,
        "quantity": quantity,
        "discount": discount,
        "rating": rating,
        "total": total
    })

    # 1. Додаємо "бруд" у city/product: пробіли, різний регістр
    dirty_idx_city = rng.choice(df.index, size=int(n_rows * 0.06), replace=False)
    dirty_idx_product = rng.choice(df.index, size=int(n_rows * 0.06), replace=False)

    df.loc[dirty_idx_city[:len(dirty_idx_city)//2], "city"] = (
        " " + df.loc[dirty_idx_city[:len(dirty_idx_city)//2], "city"].astype(str) + " "
    )
    df.loc[dirty_idx_city[len(dirty_idx_city)//2:], "city"] = (
        df.loc[dirty_idx_city[len(dirty_idx_city)//2:], "city"].astype(str).str.upper()
    )

    df.loc[dirty_idx_product[:len(dirty_idx_product)//2], "product"] = (
        " " + df.loc[dirty_idx_product[:len(dirty_idx_product)//2], "product"].astype(str).str.lower() + " "
    )
    df.loc[dirty_idx_product[len(dirty_idx_product)//2:], "product"] = (
        df.loc[dirty_idx_product[len(dirty_idx_product)//2:], "product"].astype(str).str.upper()
    )

    # 2. Пропуски в quantity та discount
    qty_nan_idx = rng.choice(df.index, size=int(n_rows * 0.03), replace=False)
    disc_nan_idx = rng.choice(df.index, size=int(n_rows * 0.03), replace=False)
    df.loc[qty_nan_idx, "quantity"] = np.nan
    df.loc[disc_nan_idx, "discount"] = np.nan

    # 3. Некоректний rating
    bad_rating_idx = rng.choice(df.index, size=int(n_rows * 0.015), replace=False)
    half = len(bad_rating_idx) // 2
    df.loc[bad_rating_idx[:half], "rating"] = rng.uniform(-2, 0.9, size=half)
    df.loc[bad_rating_idx[half:], "rating"] = rng.uniform(5.1, 8.0, size=len(bad_rating_idx) - half)

    # 4. Викиди в price
    outlier_idx = rng.choice(df.index, size=int(n_rows * 0.01), replace=False)
    df.loc[outlier_idx, "price"] = np.round(df.loc[outlier_idx, "price"] * rng.uniform(4, 9, size=len(outlier_idx)), 2)

    # 5. Частина total буде некоректною
    wrong_total_idx = rng.choice(df.index, size=int(n_rows * 0.025), replace=False)
    df.loc[wrong_total_idx, "total"] = np.round(
        df.loc[wrong_total_idx, "total"] * rng.uniform(0.7, 1.3, size=len(wrong_total_idx)),
        2
    )

    # 6. Дублікат order_id
    dup_part = df.sample(frac=0.02, random_state=seed).copy()
    dup_part["order_id"] = dup_part["order_id"].values
    df = pd.concat([df, dup_part], ignore_index=True)

    # Перемішування
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)

    df.to_csv(filename, index=False, encoding="utf-8-sig")

    print(f"Файл '{filename}' успішно створено.")
    print(f"Кількість рядків: {len(df)}")
    print("Колонки:", list(df.columns))
    print("\nПерші 5 рядків:")
    print(df.head())


if __name__ == "__main__":
    generate_orders_csv()