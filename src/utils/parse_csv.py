from dotenv import load_dotenv
import os
import pandas as pd

from typing import Dict, List

load_dotenv()
bird_csv_path = os.environ['BIRD_CSV']
bird_df = pd.read_csv(bird_csv_path)


def get_unique_power_categories(df: pd.DataFrame) -> List[str]:
    uniques = df['power_category'].unique()
    return uniques.tolist()


if __name__ == '__main__':
    print(get_unique_power_categories(bird_df))
    print('test')