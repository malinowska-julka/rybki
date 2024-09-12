from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import csv
import math
from functions import *
from constants import *

if __name__ == "__main__":
    rybki = csv.DictReader(open("data/rybki_igor.csv"))  # processed_rybki_final.csv"))
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
            try:
                img = Image.open("images/rybki_img/" + rybka["image_path"])
                result.paste(img, (RYBKA_WID_LEFT, RYBKA_HEIGHT_UP))
            except:
                print("Brak zdjęcia rybki")

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
            # akcja print
            match rybka["kolor_akcji"]:
                case "GDY ZAGRYWASZ":
                    draw.rectangle(
                        (
                            (0, ACTION_REC_HEIGHT_START),
                            (CARD_WIDTH, ACTION_REC_HEIGHT_END),
                        ),
                        fill="PowderBlue",
                    )
                case "GDY AKTYWUJESZ":
                    draw.rectangle(
                        (
                            (0, ACTION_REC_HEIGHT_START),
                            (CARD_WIDTH, ACTION_REC_HEIGHT_END),
                        ),
                        fill="#A67B5B",
                    )
                case "RAZ MIĘDZY TURAMI":
                    draw.rectangle(
                        (
                            (0, ACTION_REC_HEIGHT_START),
                            (CARD_WIDTH, ACTION_REC_HEIGHT_END),
                        ),
                        fill="Pink",
                    )
                case "KONIEC RUNDY":
                    draw.rectangle(
                        (
                            (0, ACTION_REC_HEIGHT_START),
                            (CARD_WIDTH, ACTION_REC_HEIGHT_END),
                        ),
                        fill="DodgerBlue",
                    )
                case "RAZ W GRZE":
                    draw.rectangle(
                        (
                            (0, ACTION_REC_HEIGHT_START),
                            (CARD_WIDTH, ACTION_REC_HEIGHT_END),
                        ),
                        fill="Gray",
                    )
                case _:
                    draw.rectangle(
                        (
                            (0, ACTION_REC_HEIGHT_START),
                            (CARD_WIDTH, ACTION_REC_HEIGHT_END),
                        ),
                        fill="PowderBlue",
                    )

            tekst_akcji = rybka["kolor_akcji"] + ", " + rybka["akcja"]
            tekst_akcji, coor_and_foods = insert_next_lines(tekst_akcji, font_name)
            for change_food in coor_and_foods:
                im = Image.open("images/" + change_food[1] + ".png")
                result.paste(im, change_food[0], im)
            draw.text(
                (5, ACTION_HEIGHT_START),
                tekst_akcji,
                fill="Black",
                font=font_name,
                align="left",  # TODO CHANGE FONT FOR ACTIONS
            )

            # TODO REPLACE FOOD/EGGS NAMES TO IMAGES
            # TODO tekst ustalona wysokosc w zależnosci od wielkosci ryby
            # (stosunek rozmiaru tekstu do rozmiaru ryby???)

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
            images, coors, sep, coors_sep = food_draw(rybka["food"], food_rodzaje)
            for i in range(len(images)):
                im = Image.open(images[i])
                result.paste(im, coors[i], im)
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
            ikra = Image.open("images/jajo.png")
            result.paste(ikra, (KRYJOWKA_WIDTH - 10, KRYJOWKA_HEIGHT + 100), ikra)

            result.save("cards/draw_" + rybka["name"] + ".png")

    # TODO ikra liczba i rozmieszczenie i czy cos z tym ze zyworodna?
    # TODO punkty
    # TODO ogon zmniejszyc i length i zmienic kolory
    # TODO background transparent albo moze jak kolizja to zmniejszaj obraz o pixel?
