import unittest
from collections import Counter
import pandas as pd
from gacha import load_data, award_mapping

class TestGacha(unittest.TestCase):
    def setUp(self):
        # テスト用のデータをロード
        self.data = load_data("present_members.csv")
        self.award_names = list(award_mapping.keys())

    def test_draws(self):
        # 各賞について100回抽選を行う
        for award_name in self.award_names:
            results = []
            for _ in range(10000):
                # draw_person関数を呼び出し、結果を記録
                person = self.draw_person(award_name)
                if person is not None:
                    results.append(person['氏名'])

            # 結果をカウントして表示
            result_count = Counter(results)
            print(f"Award: {award_name}")
            for name, count in result_count.items():
                percentage = (count / 10000) * 100  # パーセンテージを計算
                print(f"{name}: {count} times ({percentage:.2f}%)")

    def draw_person(self, award_name):
        # display_random_person関数のロジックを模倣して、ランダムに人を選ぶ
        csv_award_name = award_mapping.get(award_name, None)
        if csv_award_name is None:
            return None

        filtered_data = self.data[self.data['【プレゼント選択】プレゼント抽選への参加をご希望される場合は、以下から1つお選びください。'] == csv_award_name]
        if not filtered_data.empty:
            return filtered_data.sample().iloc[0]
        return None

if __name__ == '__main__':
    unittest.main()