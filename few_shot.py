import json
import pandas as pd

class FewShotPosts:
    def __init__(self, filepath="data/processed_posts.json"):
        self.df = None
        self.unique_tags = None
        self.load_posts(filepath)

    def load_posts(self, filepath):
        with open(filepath, encoding='utf-8') as file:
            posts = json.load(file)
            self.df = pd.json_normalize(posts)
            self.df['length'] = self.df['line_count'].apply(self.categorize_length)
            all_tags = self.df['tags'].apply(lambda x: x).sum()
            self.unique_tags = set(all_tags)
            pass

    def categorize_length(self, line_count):
        if line_count < 5:
            return "Short"

        elif 5 <= line_count <= 10:
            return "Medium"

        else:
            return "Long"

    def get_tags(self):
        return self.unique_tags

    def get_filtered_posts(self, language, length, tag):
        df_filtered = self.df[
            (self.df['language'] == language) &
            (self.df['length'] == length) &
            (self.df['tags'].apply(lambda tags : tag in tags))
        ]
        return df_filtered.to_dict(orient='records')
    pass


if __name__ == "__main__":
    fs = FewShotPosts()
    print(fs.get_tags())
    posts = fs.get_filtered_posts("English", "Medium", "Job Search")
    print(posts)
    pass