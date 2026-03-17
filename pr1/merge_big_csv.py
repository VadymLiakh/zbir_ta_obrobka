import pandas as pd
from pathlib import Path


def merge_large_csv(
    left_csv: str,
    right_csv: str,
    output_csv: str,
    id_col: str = "ID",
    chunksize: int = 200_000
):
    Path(output_csv).parent.mkdir(parents=True, exist_ok=True)

    print("Читаємо правий CSV у пам'ять...")
    right_df = pd.read_csv(right_csv)

    if id_col not in right_df.columns:
        raise ValueError(f"У {right_csv} немає колонки {id_col}")

    # Індекс для швидкого join
    right_df = right_df.set_index(id_col)

    first_chunk = True

    print("Починаємо об'єднання...")

    for chunk_num, chunk in enumerate(
        pd.read_csv(left_csv, chunksize=chunksize)
    ):

        print(f"Chunk {chunk_num}...")

        if id_col not in chunk.columns:
            raise ValueError(f"У {left_csv} немає колонки {id_col}")

        chunk = chunk.set_index(id_col)

        merged = chunk.join(right_df, how="left")

        merged.reset_index().to_csv(
            output_csv,
            mode="a",
            index=False,
            header=first_chunk
        )

        first_chunk = False

    print("Об'єднання завершено")


if __name__ == "__main__":

    merge_large_csv(
        left_csv="data/big_left.csv",
        right_csv="data/big_right.csv",
        output_csv="data/merged_result.csv",
        chunksize=200_000
    )
