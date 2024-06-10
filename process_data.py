import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import random
import os

def kryjowki_update(info):
    specific_kryjowki = []
    tokens = info.split()
    # kryjowki
    for word in tokens:
        for i in range(len(kryjowka_rodzaje)):
            if kryjowka_rodzaje[i] in word:
                if kryjowka_dict.get(kryjowka_rodzaje[i]) not in specific_kryjowki:
                    specific_kryjowki.append(kryjowka_dict.get(kryjowka_rodzaje[i]))

    if len(specific_kryjowki) == 1 :
        return specific_kryjowki[0]
    elif len(specific_kryjowki) == 0:
        return 'kokos'
    else:
        return kryjowki[random.randint(0, len(kryjowki)- 1)]

def breeding_update(info):
    tokens_bre = info.split()
    # breeding type
    for word in tokens_bre:
        if 'żyworodne' in word:
            return 'żyworodne'
            break
        if 'jajorodne' in word:
            return 'jajorodne'
            break

def temp_update(top_temp):
    dec= random.randint(0,5)

    if top_temp < 27:
        if dec in (0,1,2):
            return 'images/zimne.png'
        elif dec == 4:
            return 'images/zimno-srednia.png'
        elif dec == 3:
            return 'images/zimno-ciepla.png'
        else:
            return 'images/trzy_razem.png'

    elif top_temp == 28:
        if dec in (0, 1):
            return 'images/srednie.png'
        elif dec == 2:
            return 'images/zimne.png'
        elif dec == 4:
            return 'images/zimno-srednia.png'
        elif dec == 3:
            return 'images/srednio-ciepla.png'
        else:
            return 'images/trzy_razem.png'
    else:
        if dec in (0, 1, 2):
            return 'images/hot.png'
        elif dec == 4:
            return 'images/srednio-ciepla.png'
        elif dec == 3:
            return 'images/zimno-ciepla.png'
        else:
            return 'images/trzy_razem.png'

def food_update(food):
    if any(f_type in food for f_type in food_rodzaje):
        jedzonko = food.split(',')

        if 'roślinny' in jedzonko:
            jedzonko.remove('roślinny')
        ile = len(jedzonko)
        if ile >= 3:
            how_many = random.randint(1, 3)
            which=[]
            for i in range(how_many):
                which.append(jedzonko[random.randint(0, ile - 1)])
            return which
        else:
            return jedzonko

    else:
        hopsa = random.randint(0,1)
        if hopsa == 0:
            rand_list = ['random']
        else:
            rand_list = ['ślimaki']

        dec = random.randint(0,2)
        for i in range(dec):
           rand_list.append(food_rodzaje[random.randint(0,5)])

        return rand_list

def assign_image(name):
    name = name.replace(' ', '')
    path = "/home/julia/Desktop/rybki/rybki_scrapy/images/rybki_img"
    files_list = os.listdir(path)
    file_names = [i.replace('.png','') for i in files_list]

    for i in range(len(file_names)):
        if file_names[i].casefold() in name.casefold():
            return files_list[i]



def food_sep(food):
    if len(food) == 1:
        return ''
    else:
        dec = random.randint(0,2)
        if dec in (0,1): return '+'
        else: return '/'

df = pd.read_csv('rybki_all_info.csv')

food_rodzaje = ['glony', 'mrożony', 'suchy', 'żywy', 'ślimaki','random']
kryjowka_rodzaje = ['roślin', 'kamie', 'korzen', 'kryj', 'drewn', 'kokos', 'zarośn']
kryjowki = ['roślinka', 'kamienie', 'korzenie', 'kokos', 'domek', 'kamienie', 'korzenie', 'kokos', 'domek']
kryjowka_dict = {'roślin': 'roślinka',
                 'kamie' : 'kamienie',
                 'korzen': 'korzenie',
                 'drewn' : 'korzenie',
                 'kokos' : 'kokos',
                 'kryj' : 'domek',
                 'zarośn' : 'roślinka'
                 }

df["Lowest_temperature"] = df.temperature.apply(lambda x: int(x.split()[0]))
df["Top_temperature"] = df.temperature.apply(lambda x:  int(x.split()[2][0:2]))
df["length"] = df.length.apply(lambda x: x.split()[0])
df["kryjowka_info"] = df.kryjowka_info.apply(kryjowki_update)
df["breeding_info"] = df.breeding_info.apply(breeding_update)
df["temperature"] = df.Top_temperature.apply(temp_update)
df["food"] = df.food.apply(food_update)
df["food_separator"] = df.food.apply(food_sep)
df["image_path"] = df.name.apply(assign_image)
#sns.displot(df, x="kryjowka_info")
#plt.savefig('kryjowki.png')

#print(df['kryjowka_info'].unique())

#pd.set_option('display.max_columns', None)
#print(df.sort_values('Lowest_temperature', ascending=True))
df.to_csv("processed_rybki_final.csv")

#print(df[df['breeding_info'] == 'żyworodne'])





