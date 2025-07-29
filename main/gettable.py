import pandas as pd

def gettable(url):
    df = pd.read_html(url)
    print(df)

if __name__=='__main__':
    # url = json.loads(d["choices"][0]["message"]["tool_calls"][0]["function"]["arguments"])["url"]
    gettable('https://en.wikipedia.org/wiki/List_of_highest-grossing_films')