import arcade
import math
import random



BREDDE = 800
HOEJDE = 600
SPORLAENGDE = 10000
COLOR = arcade.csscolor.GREEN
COLOR_KASSE = arcade.csscolor.TURQUOISE


def kasse():
    global kasse_center_x, kasse_center_y
    kasse_center_x = (BREDDE/2 + (random.randint(-300, 300)))
    kasse_center_y = (HOEJDE/2 + (random.randint(-200, 200)))
    print(f"Kassens koordinater er ({kasse_center_x};{kasse_center_y})")


def linje(tid, stationaert_punkt, retningsvektor):
    x_0, y_0 = stationaert_punkt
    r_x, r_y = retningsvektor
    x = x_0 + r_x * tid
    y = y_0 + r_y * tid - 9.82*(tid**2)
    return x, y



def tegn(delta_tid):
    arcade.start_render()
    # Beregner punkt på linjen
    x, y = linje(tegn.tid/60, (0,0), (HASTIGHED, HASTIGHED))
    # Tegner punktet på linjen
    arcade.draw_circle_filled(x, y, 5, COLOR_KASSE)
    # Fjerner det første punkt i sporet, hvis sporet er for langt
    if len(tegn.spor) > SPORLAENGDE:
        tegn.spor.pop(0)
    # Tegner sporet
    for punkt in tegn.spor:
        arcade.draw_circle_filled(*punkt, 2, COLOR_KASSE)
    # Stopper animationen, hvis punktet rammer kassen
    if (x > (kasse_center_x - 25) and x < (kasse_center_x + 25))\
            and (y > (kasse_center_y - 25) and y < (kasse_center_y + 25)):
        # tiden holdes konstant, så animationen stopper
        tegn.tid = tegn.tid
    # Kører animationen, hvis punktet ikke rammer kassen, men er inden for vinduet
    elif (x >= 0 and x < BREDDE) and (y >= 0 and y <= HOEJDE):
        # Tiden opdateres med 1
        tegn.tid += delta_tid * 60
        # Tilføjer det sidste nye punkt til sporet
        tegn.spor.append((x, y))

    # Stopper animationen, hvis punktet på ikke rammer kassen, og er uden for vinduet
    else:
        # Tiden holdes konstant, så animationen stopper
        tegn.tid = tegn.tid

    arcade.draw_rectangle_filled(kasse_center_x, kasse_center_y, 50, 50, COLOR_KASSE)


def main():
    print(f"\nVinduets størrelse er {BREDDE}x{HOEJDE}")
    kasse()
    global VINKEL, HASTIGHED
    VINKEL = 0
    HASTIGHED = 0
    valg_af_vinkel_faerdig = False
    while not valg_af_vinkel_faerdig:
        valg_vinkel = int(input("\nDu skal kaste en bold mod kassen, hvilken vinkel vil du kaste med? "))
        if valg_vinkel < 0 or valg_vinkel > 90:
            print("\nDu skal vælge en vinkel mellem 0 og 90 grader")
        elif valg_vinkel >= 0 and valg_vinkel <= 90:
            VINKEL += valg_vinkel
            valg_af_vinkel_faerdig = True
        else:
            print("\nDu har valgt noget, som programmet ikke kunne forstå, prøv igen")

    valg_af_hastighed_faerdig = False
    while not valg_af_hastighed_faerdig:
        valg_hastighed = int(input("\nHvor hurtigt vil du kaste bolden? (m/s) "))
        if valg_hastighed < 0:
            print("\nDu skal vælge en positiv hastighed")
        elif valg_hastighed == 0:
            print("\nDin hastighed skal være større end 0")
        elif valg_hastighed >= 0:
            HASTIGHED += valg_hastighed
            valg_af_hastighed_faerdig = True
        else:
            print("\nDu har valgt noget, som programmet ikke kunne forstå, prøv igen")


    arcade.open_window(BREDDE, HOEJDE, "Spilvindue", True, False)
    arcade.set_background_color(COLOR)
    tegn.tid = 0
    tegn.spor = list()
    arcade.schedule(tegn, 1 / 60)  # Funktionen tegn kaldes 60 gange i sekundet
    arcade.run()

if __name__ == "__main__":
    main()



