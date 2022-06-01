import re
import os
import numpy as np


def clean_text(text):
    # acronym
    text = re.sub(r"can\'t", "can not", text)
    text = re.sub(r"cannot", "can not ", text)
    text = re.sub(r"what\'s", "what is", text)
    text = re.sub(r"What\'s", "what is", text)
    text = re.sub(r"\'ve ", " have ", text)
    text = re.sub(r"n\'t", " not ", text)
    text = re.sub(r"i\'m", "i am ", text)
    text = re.sub(r"I\'m", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r"c\+\+", "cplusplus", text)
    text = re.sub(r"c \+\+", "cplusplus", text)
    text = re.sub(r"c \+ \+", "cplusplus", text)
    text = re.sub(r"c#", "csharp", text)
    text = re.sub(r"f#", "fsharp", text)
    text = re.sub(r"g#", "gsharp", text)
    text = re.sub(r" e mail ", " email ", text)
    text = re.sub(r" e \- mail ", " email ", text)
    text = re.sub(r" e\-mail ", " email ", text)
    text = re.sub(r",000", '000', text)
    text = re.sub(r"\'s", " ", text)

    # spelling correction
    text = re.sub(r"ph\.d", "phd", text)
    text = re.sub(r"PhD", "phd", text)
    text = re.sub(r"pokemons", "pokemon", text)
    text = re.sub(r"pokémon", "pokemon", text)
    text = re.sub(r"pokemon go ", "pokemon-go ", text)
    text = re.sub(r" e g ", " eg ", text)
    text = re.sub(r" b g ", " bg ", text)
    text = re.sub(r" 9 11 ", " 911 ", text)
    text = re.sub(r" j k ", " jk ", text)
    text = re.sub(r" fb ", " facebook ", text)
    text = re.sub(r"facebooks", " facebook ", text)
    text = re.sub(r"facebooking", " facebook ", text)
    text = re.sub(r"insidefacebook", "inside facebook", text)
    text = re.sub(r"donald trump", "trump", text)
    text = re.sub(r"the big bang", "big-bang", text)
    text = re.sub(r"the european union", "eu", text)
    text = re.sub(r" usa ", " america ", text)
    text = re.sub(r" us ", " america ", text)
    text = re.sub(r" u s ", " america ", text)
    text = re.sub(r" U\.S\. ", " america ", text)
    text = re.sub(r" US ", " america ", text)
    text = re.sub(r" American ", " america ", text)
    text = re.sub(r" America ", " america ", text)
    text = re.sub(r" quaro ", " quora ", text)
    text = re.sub(r" mbp ", " macbook-pro ", text)
    text = re.sub(r" mac ", " macbook ", text)
    text = re.sub(r"macbook pro", "macbook-pro", text)
    text = re.sub(r"macbook-pros", "macbook-pro", text)

    # special replacement
    text = re.sub(r"&", " and ", text)
    text = re.sub(r"\|", " or ", text)
    text = re.sub(r"=", " equal ", text)
    text = re.sub(r"\+", " plus ", text)
    text = re.sub(r"₹", " rs ", text)  # 测试！
    text = re.sub(r"\$", " dollar ", text)
    text = re.sub(r"\t+", " ", text)
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"^\s+|\s+$^", "", text)
    text = re.sub('[☎]+', "", text)
    text = re.sub('[★]+', "", text)
    text = re.sub('[❤☮☺☯⚇♔✉✔😉→™₪☓♠♥♦♣†🎄♦☻–¡¶♫😜✽△←✎¤¢]+', "", text)
    text = re.sub('[♥]+', "", text)
    text = re.sub('സംവാദം മോസ്കോ മെട്രോ', "", text)
    text = re.sub('[κρανιώνας]+', "", text)
    text = re.sub('[дреновени]+', "", text)
    text = re.sub("[​><·;:\`\~\-?\s+\.\!\/_,$%^\*)+(+\"\'\[\]{+}+\\]+|[+——！•，：。？、~@#￥%……&*‘’“”（）「」]+", " ", text)
    text = re.sub(r'f+u+c+k+', 'fuck', text)
    text = re.sub('[働労勞連絡見学迷惑]+', '', text)

    text = re.sub(r"\$(\d+)", lambda m: m.group(1) + ' dollar ', text)
    text = re.sub(r"(\d+)\$", lambda m: m.group(1) + ' dollar ', text)


    text = re.sub(r'\d+', '', text)
    text = re.sub(r"googling", " google ", text)
    text = re.sub(r"googled", " google ", text)
    text = re.sub(r"googleable", " google ", text)
    text = re.sub(r"googles", " google ", text)
    text = re.sub(r" rs(\d+)", lambda m: ' rs ' + m.group(1), text)
    text = re.sub(r"(\d+)rs", lambda m: ' rs ' + m.group(1), text)
    text = re.sub(r"the european union", " eu ", text)
    text = re.sub(r"dollars", " dollar ", text)

    # remove extra space
    text = ' '.join(text.split(' '))
    return text


def read_data(file_dir):
    data = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                text = ''
                for line in open(file_path, 'r', encoding='ascii').readlines():
                    text +=  clean_text(line)
                data.append(text)
            except Exception as e:
                continue
    return data

if __name__ == '__main__':
    file_dir = r'./data/news/'
    data = read_data(file_dir)
    print(np.shape(data))
    print(data[0])
