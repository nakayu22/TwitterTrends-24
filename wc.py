from wordcloud import WordCloud
from collections import defaultdict
from database import get_trends


# トレンドからwordcloudを作成
def makeWc():
    trends_day = get_trends()
    
    d = defaultdict(list)
    for trends_hour in trends_day:
        for trend in trends_hour["topics"]:
            d[trend["topic"]].append(trend["rank"])
    
    # 各トピックの順位の逆数の平均を計算
    d_score = dict()
    for k, v in d.items():
        score = 0
        n = len(v)
        for rank in v:
            score += 1/rank
        d_score[k] = score*n
    
    font_path = ".fonts/ipaexg00401/ipaexg.ttf"
    wc = WordCloud(font_path=font_path, width=480, height=320, background_color="white", max_font_size=100).fit_words(d_score)
    wc.to_file("static/img/wc.png")

    return


if __name__ == "__main__":
    makeWc()