import random

import pandas as pandas

path = "C:/JCTDrive/Admin/Power BI Lev/מחקר הצלחה בתואר/studentsFullFlat.xlsx"
df = pandas.read_excel(path)
encoded_set = {0}
randId = 0
for i in df.itertuples():
    while randId in encoded_set:
        randId = random.randint(1,1000000)
    encoded_set.add(randId)
    print(f'{i[1]}\t{randId}')
