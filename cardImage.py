from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import random
import csv
import math

random.seed(123)

RYBKA_TEMP = 12
CARD_WIDTH = 800
CARD_HEIGHT = 1100
UPPER_RECT_WID_START = 50
UPPER_RECT_WID_END = 250
UPPER_RECT_HEIGHT = 250
ACTION_REC_HEIGHT_START = 800
ACTION_REC_HEIGHT_END = ACTION_REC_HEIGHT_START + 180
LENGTH_HEIGHT = 710
LENGTH_WIDTH = 610
OGON_HEIGHT = 280
OGON_WIDTH = 35
KRYJOWKA_HEIGHT = OGON_HEIGHT + 150
KRYJOWKA_WIDTH = OGON_WIDTH - 10
RYBKA_WID_LEFT = 50
RYBKA_HEIGHT_UP = 181


def separate_name(text):
    tokens = text.split()
    no_words = len(tokens)
    return [
        " ".join(tokens[0 : no_words // 2]),
        " ".join(tokens[math.ceil(no_words / 2) :]),
    ]


def wysrodkowany_text(text, coordinates_start, coordinates_end, font):
    width = coordinates_end[0] - coordinates_start[0]
    height = coordinates_end[1]
    font_width = font.getlength(text)
    new_width = (width - font_width) / 2 + coordinates_start[0]

    return (new_width, height)


def food_draw(food):
    ims = []
    sep = []
    coors_sep = []
    dec = random.randint(0, 2)
    if dec in (0, 1):
        sep = "images/slash.png"
    else:
        sep = "images/plus.png"

    for i in range(len(food_rodzaje)):
        count = food.count(food_rodzaje[i])
        if count > 1 or food_rodzaje[i] == "random":
            sep = "images/plus.png"
        for x in range(count):
            ims.append("images/" + food_rodzaje[i] + ".png")
    if len(ims) == 1:
        coors = [(127, 177)]
    elif len(ims) == 2:
        coors = [(87, 177), (168, 177)]
        if sep == "images/slash.png":
            coors_sep = [(139, 177)]
        else:
            coors_sep = [(139, 189)]
    else:
        coors = [(62, 177), (127, 177), (192, 177)]
        if sep == "images/slash.png":
            coors_sep = [(113, 177), (174, 177)]
        else:
            coors_sep = [(113, 189), (174, 189)]

    return ims, coors, sep, coors_sep


def temp_draw(temp):

    im = Image.open(temp)
    if temp in ("images/zimne.png", "images/srednie.png", "images/hot.png"):
        coors = (105, 60)
    elif temp == "images/trzy_razem.png":
        coors = (60, 25)
    else:
        coors = (60, 60)
    return im, coors


if __name__ == "__main__":
    rybki = csv.DictReader(open("data/processed_rybki_final.csv"))
    food_rodzaje = ["glony", "mrożony", "suchy", "żywy", "ślimaki", "random"]
    for rybka in rybki:
        if rybka["image_path"] != "":
            result = Image.new("RGBA", (CARD_WIDTH, CARD_HEIGHT))
            font_name = ImageFont.truetype("fonts/Museo_Slab_500_2.otf", 40)
            font_latin = ImageFont.truetype("fonts/freept.otf", 30)

            coor_name = wysrodkowany_text(
                rybka["name"], (UPPER_RECT_WID_END + 1, 70), (CARD_WIDTH, 70), font_name
            )
            long_name = []

            if coor_name[0] < UPPER_RECT_WID_END + 5:
                long_name = separate_name(rybka["name"])

            coor_latin = wysrodkowany_text(
                rybka["latin_name"],
                (UPPER_RECT_WID_END + 1, 120),
                (CARD_WIDTH, 120),
                font_latin,
            )

            draw = ImageDraw.Draw(result)

            # not changing background
            draw.rounded_rectangle(
                ((0, 0), (CARD_WIDTH, CARD_HEIGHT)), 40, fill="PowderBlue"
            )

            # rybka print
            img = Image.open("images/rybki_img/" + rybka["image_path"])
            result.paste(img, (RYBKA_WID_LEFT, RYBKA_HEIGHT_UP))

            draw.line(
                ((UPPER_RECT_WID_END + 1, 50), (CARD_HEIGHT, 50)), fill="DarkSlateGray"
            )
            draw.line(
                ((UPPER_RECT_WID_END + 1, 180), (CARD_HEIGHT, 180)),
                fill="DarkSlateGray",
            )
            draw.rounded_rectangle(
                ((UPPER_RECT_WID_START, -10), (UPPER_RECT_WID_END, UPPER_RECT_HEIGHT)),
                10,
                fill="DodgerBlue",
            )
            draw.rectangle(
                ((0, ACTION_REC_HEIGHT_START), (CARD_WIDTH, ACTION_REC_HEIGHT_END)),
                fill="White",
            )

            # nazwa print

            if len(long_name) == 0:
                draw.text(coor_name, rybka["name"], fill="Black", font=font_name)
                draw.text(coor_latin, rybka["latin_name"], fill="Gray", font=font_latin)

            else:  # nazwa za długa i podzielona na dwie linijki
                draw.text(
                    wysrodkowany_text(
                        long_name[0],
                        (UPPER_RECT_WID_END + 1, 55),
                        (CARD_WIDTH, 55),
                        font_name,
                    ),
                    long_name[0],
                    fill="Black",
                    font=font_name,
                )
                draw.text(
                    wysrodkowany_text(
                        long_name[1],
                        (UPPER_RECT_WID_END + 1, 94),
                        (CARD_WIDTH, 94),
                        font_name,
                    ),
                    long_name[1],
                    fill="Black",
                    font=font_name,
                )
                draw.text(
                    (coor_latin[0], 130),
                    rybka["latin_name"],
                    fill="Gray",
                    font=font_latin,
                )

            # jedzenie print
            images, coors, sep, coors_sep = food_draw(rybka["food"])
            for i in range(len(images)):
                im = Image.open(images[i])
                result.paste(im, coors[i])
            for i in range(len(coors_sep)):
                hopsa = Image.open(sep)
                result.paste(hopsa, coors_sep[i])

            # temp print
            images_temp, coors_temp = temp_draw(rybka["temperature"])
            result.paste(images_temp, coors_temp)

            # dlugosc print
            length = Image.open("images/length.png")
            result.paste(length, (LENGTH_WIDTH, LENGTH_HEIGHT), length)
            font_length = ImageFont.truetype("fonts/Museo_Slab_500_2.otf", 30)
            draw.text(
                (LENGTH_WIDTH + 25, LENGTH_HEIGHT + 20),
                str(math.ceil(float(rybka["length"]))) + " cm",
                fill="Black",
                font=font_length,
            )

            # punkty print
            ogon = Image.open("images/punkty.png")
            result.paste(ogon, (OGON_WIDTH, OGON_HEIGHT), ogon)

            # kryjowka print
            kryjowka = Image.open("images/" + rybka["kryjowka_info"] + ".png")
            result.paste(kryjowka, (KRYJOWKA_WIDTH, KRYJOWKA_HEIGHT), kryjowka)

            # jajeczka
            ikra = Image.open("images/ikra.png")
            result.paste(ikra, (KRYJOWKA_WIDTH - 10, KRYJOWKA_HEIGHT + 100))

            result.save("cards/draw_" + rybka["name"] + ".png")

    # TODO ikra liczba i rozmieszczenie i czy cos z tym ze zyworodna?
    # TODO punkty
    # TODO ogon zmniejszyc i length i zmienic kolory
    # TODO background transparent albo moze jak kolizja to zmniejszaj obraz o pixel?
    # TODO tekst akcji ujednolicic i potem dopiero printowac na karcie
