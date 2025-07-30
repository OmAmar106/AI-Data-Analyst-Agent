import pandas as pd
import pandas as pd
from bs4 import BeautifulSoup,Tag
import requests
from collections import Counter
from response import response
import json

def gettable(url,choosetable):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    tables = soup.find_all("table")

    dfs = pd.read_html(res.text)
    result = []
    for i, table in enumerate(tables):
        df = dfs[i]
        if df.empty or df.shape[0] * df.shape[1] == 0:
            continue
        
        prev_text = ""
        prev = table.find_previous(lambda tag: (
            isinstance(tag, Tag) and 
            tag.name in ["p", "h1", "h2", "h3", "h4","caption"] and 
            tag.get_text(strip=True)
        ))

        prev_text = prev.get_text(strip=True) if prev else f"Table {i}"

        caption_tag = table.caption
        caption = caption_tag.string.strip() if caption_tag and caption_tag.string else prev_text or f"Table {i}"
        
        inside_tag = table.find(True)
        inside = inside_tag.get_text(strip=True) if inside_tag else ""

        result.append((caption, inside,df))

    TABLE = {
        "type": "function",
        "function": {
            "name": "extract_table_index",
            "description": "Tell the Index of the most relevant table according to the given statement related to Data Analysis",
            "parameters": {
                "type": "object",
                "properties": {
                    "index": {
                        "type": "integer",
                        "description": "The index (1-based) of the item in the array that best matches the user's query"
                    }
                },
                "required": ["index"],
                "additionalProperties": False
            },
            "strict": True
        }
    }

    d = Counter(i[0] for i in result)

    result = [i for i in result if d[i[0]]==1]
    Lfilter = [(" text above table: "+i[0][:30]+" --- "+"text inside table: "+i[1][:30]+" ---  columns: "+' '.join(list(map(str,list(i[2].columns)[:10])))) for i in result[:10]]
    
    for i in range(len(Lfilter)):
        Lfilter[i] = str(i+1)+': '+Lfilter[i]

    # print(Lfilter)
    # print(choosetable+'\n\n\nWhich of these match the given message by user the best?\n'+'\n'.join(Lfilter))
    # return

    Lindex = None
    choosetable[0]["content"] += '\n\n\nWhich of these match the given message by user the best?\n'+'\n'.join(Lfilter)
    for i in range(10):
        Lindex = response(TABLE,choosetable)
        data = json.loads(Lindex["choices"][0]["message"]["tool_calls"][0]["function"]["arguments"])
        Lindex = data['index']
    #     code,type1 = d["code"],d["data_type"]
        Lindex -= 1
        if Lindex<len(Lfilter):
            return result[Lindex][2]
    return None

if __name__=='__main__':
    # url = json.loads(d["choices"][0]["message"]["tool_calls"][0]["function"]["arguments"])["url"]
    messages = [
        {
            "role":"user",
            "content":"""
                Scrape the list of highest grossing films from Wikipedia. It is at the URL:
                https://en.wikipedia.org/wiki/List_of_highest-grossing_films

                Answer the following questions and respond with a JSON array of strings containing the answer.

                1. How many $2 bn movies were released before 2020?
                2. Which is the earliest film that grossed over $1.5 bn?
                3. What's the correlation between the Rank and Peak?
                4. Draw a scatterplot of Rank and Peak along with a dotted red regression line through it.
                Return as a base-64 encoded data URI, `"data:image/png;base64,iVBORw0KG..."` under 100,000 bytes.            
            """
        }
    ]
    print(gettable('https://en.wikipedia.org/wiki/List_of_highest-grossing_films',messages))
