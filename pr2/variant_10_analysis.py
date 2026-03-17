import pandas as pd


def run_variant_10(input_file="orders.csv", output_file="variant_10_result.csv"):
    # 1. Завантаження даних
    df = pd.read_csv(input_file, encoding="utf-8-sig")

    print("Початкові дані:")
    print(df.head())
    print("\nРозмір таблиці:", df.shape)

    # 2. Очищення product
    df["product"] = df["product"].astype(str).str.strip().str.title()

    # 3. Приведення total до числа
    df["total"] = pd.to_numeric(df["total"], errors="coerce")

    # 4. Видалення рядків без потрібних даних
    df = df.dropna(subset=["product", "total"]).copy()

    # 5. Групування по product з агрегаціями
    grouped = (
        df.groupby("product")["total"]
        .agg(count="count", sum="sum", mean="mean", median="median", std="std")
        .reset_index()
    )

    # 6. Сортування за сумою виручки
    grouped = grouped.sort_values(by="sum", ascending=False).reset_index(drop=True)

    # 7. Загальна виручка
    total_revenue = grouped["sum"].sum()

    # 8. Формування топ-5 + інші
    top_5 = grouped.head(5).copy()
    others = grouped.iloc[5:].copy()

    if not others.empty:
        others_row = pd.DataFrame([{
            "product": "Інші",
            "count": others["count"].sum(),
            "sum": others["sum"].sum(),
            "mean": others["sum"].sum() / others["count"].sum() if others["count"].sum() != 0 else 0,
            "median": others["median"].median(),
            "std": others["std"].mean(skipna=True)
        }])
        final_result = pd.concat([top_5, others_row], ignore_index=True)
    else:
        final_result = top_5.copy()

    # 9. Частка у загальній виручці
    final_result["share_%"] = (final_result["sum"] / total_revenue) * 100

    # 10. Округлення
    grouped = grouped.round({
        "sum": 2,
        "mean": 2,
        "median": 2,
        "std": 2
    })

    final_result = final_result.round({
        "sum": 2,
        "mean": 2,
        "median": 2,
        "std": 2,
        "share_%": 2
    })

    # 11. Виведення
    print("\nПовна агрегована таблиця:")
    print(grouped)

    print("\nТоп-5 товарів + Інші:")
    print(final_result)

    # 12. Збереження результату
    final_result.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"\nРезультат збережено у файл: {output_file}")


if __name__ == "__main__":
    run_variant_10()