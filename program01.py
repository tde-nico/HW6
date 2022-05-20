''' 
Il sindaco si una città deve pianificare un nuovo quartiere.  Voi fate
parte dello studio di architetti che deve progettare il quartiere.  Vi
viene fornito un file che contiene divisi in righe, le informazioni
che descrivono in pianta le fasce East-West (E-W) di palazzi, ciascuno
descritto da larghezza, altezza, colore da usare in pianta.

I palazzi devono essere disposti in pianta rettangolare
in modo che:
  - tutto intorno al quartiere ci sia una strada di larghezza minima
    indicata.
  - in direzione E-W (orizzontale) ci siano le strade principali,
    dritte e della stessa larghezza minima, a separare una fascia di
    palazzi E-W dalla successiva.  Ciascuna fascia E-W di palazzi può
    contenere un numero variabile di palazzi.  Se una fascia contiene
    un solo palazzo verrà disposto al centro della fascia.
  - in direzione North-South (N-S), tra ciascuna coppia di palazzi
    consecutivi, ci dev'essere almeno lo spazio per una strada
    secondaria, della stessa larghezza minima delle altre.

Vi viene chiesto di calcolare la dimensione minima dell'appezzamento
che conterrà i palazzi.  Ed inoltre di costruire la mappa che li
mostra in pianta.

Il vostro studio di architetti ha deciso di disporre i palazzi in modo
che siano **equispaziati** in direzione E-W, e di fare in modo che
ciascuna fascia E-W di palazzi sia distante dalla seguente dello
spazio minimo necessario alle strade principali.

Per rendere il quartiere più vario, il vostro studio ha deciso che i
palazzi, invece di essere allineati con il bordo delle strade
principali, devono avere se possibile un giardino davanti (a S) ed uno
dietro (a N) di uguale profondità.  Allo stesso modo, dove possibile,
lo spazio tra le strade secondarie ed i palazzi deve essere
distribuito uniformemente in modo che tutti possano avere un giardino
ad E ed uno a W di uguali dimensioni.  Solo i palazzi che si
affacciano sulle strade sul lato sinistro e destro della mappa non
hanno giardino su quel lato.

Vi viene fornito un file txt che contiene i dati che indicano quali
palazzi mettere in mappa.  Il file contiene su ciascuna riga, seguiti
da 1 virgola e/o 0 o più spazi o tab, gruppi di 5 valori interi che
rappresentano per ciascun palazzo:
  - larghezza
  - altezza
  - canale R del colore
  - canale G del colore
  - canale B del colore

Ciascuna riga contiene almeno un gruppo di 5 interi positivi relativi
ad un palazzo da disegnare. Per ciascun palazzo dovete disegnare un
rettangolo del colore indicato e di dimensioni indicate

Realizzate la funzione ex(file_dati, file_png, spaziatura) che:
  - legge i dati dal file file_dati
  - costruisce una immagine in formato PNG della mappa e la salva nel
    file file_png
  - ritorna le dimensioni larghezza,altezza dell'immagine della mappa

La mappa deve avere sfondo nero e visualizzare tutti i palazzi come segue:
  - l'argomento spaziatura indica il numero di pixel da usare per lo
    spazio necessario alle strade esterne, principali e secondarie,
    ovvero la spaziatura minima in orizzontale tra i rettangoli ed in
    verticale tra le righe di palazzi
  - ciascun palazzo è rappresentato da un rettangolo descritto da una
    quintupla del file
  - i palazzi descritti su ciascuna riga del file devono essere
    disegnati, centrati verticalmente, su una fascia in direzione
    E-W della mappa
  - i palazzi della stessa fascia devono essere equidistanti
    orizzontalmente l'uno dall'altro con una **distanza minima di
    'spaziatura' pixel tra un palazzo ed il seguente** in modo che tutti
    i primi palazzi si trovino sul bordo della strada verticale di
    sinistra e tutti gli ultimi palazzi di trovino sul bordo della
    strada di destra
    NOTA se la fascia contiene un solo palazzo dovrà essere disegnato
    centrato in orizzontale
  - ciascuna fascia di palazzi si trova ad una distanza minima in
    verticale dalla seguente per far spazio alla strada principale
    NOTE la distanza in verticale va calcolata tra i due palazzi più
    alti delle due fasce consecutive. 
    Il palazzo più grosso della prima riga si trova appoggiato al
    bordo della strada principale E-W superiore. 
    Il palazzo più grosso dell'ultima riga si trova appoggiato al
    bordo della strada principale E-W inferiore 
  - l'immagine ha le dimensioni minime possibili, quindi:
     - esiste almeno un palazzo della prima/ultima fascia a
       'spaziatura' pixel dal bordo superiore/inferiore
     - esiste almeno una fascia che ha il primo ed ultimo palazzo a
       'spaziatura' pixel dal bordo sinistro/destro
     - esiste almeno una fascia che non ha giardini ad E ed O

    NOTA: nel disegnare i palazzi potete assumere che le coordinate
        saranno sempre intere (se non lo sono avete fatto un errore).
    NOTA: Larghezza e altezza dei rettangoli sono tutti multipli di due.
'''
import images


class Building:
    def __init__(self, data):
        self._width, self._height = data[:2]
        self._color = data[2:]

    def render(self):
        self._image = [[self._color]*self._width for i in range(self._height)]

    def paste(self, other, x, y):
        for Y in range(y, y+other._height):
            for X in range(x, x+other._width):
                self._image[Y][X] = other._color


def read_file(file) -> list:
    with open(file, 'r', encoding='utf-8') as f:
        data = f.readlines()
    return data


def str_to_nums(string) -> list:
    nums = []
    num = ''
    for char in string:
        if char.isdigit():
            num += char
        else:
            if num:
                nums.append(num)
            num = ''
    return list(map(int, nums))
        


def get_data(file_dati) -> tuple:
    new_data, widths, heights = [], [], []
    for row in read_file(file_dati):
        new_line, row_widths, row_heights = [], [], []
        nums = str_to_nums(row)
        lenght = len(nums)
        index = 0
        while index < lenght:
            width, height, red, green, blue = nums[index:index+5]
            new_line += [Building((width, height, red, green, blue))]
            row_widths += [width]
            row_heights += [height]
            index += 5
        new_data.append(new_line)
        widths.append(row_widths)
        heights.append(row_heights)
    return new_data, widths, heights


def measure(widths, heights, spacing) -> tuple:
    max_heights = list(map(lambda x: max(x), heights))
    measures = (max(map(lambda x: sum(x)+(len(x)+1)*spacing, widths)), sum(max_heights)+(len(max_heights)+1)*spacing)
    return measures, max_heights


def multi_col_pasting(biru, y, image, horizontal_gardens, height, spacing):
    x = spacing
    for building in biru:
        image.paste(building, x, y+(height-building._height)//2)
        x += spacing + building._width + horizontal_gardens


def render(measures, widths, max_heights, buildings, spacing, file_png) -> list:
    image = Building((measures[0], measures[1], 0, 0, 0))
    image.render()
    y = spacing
    for row, biru in enumerate(buildings):
        biru_lenght = len(biru)
        if biru_lenght == 1:
            image.paste(biru[0], (measures[0]-biru[0]._width)//2, y)
        else:
            horizontal_gardens = (measures[0]-sum(widths[row])-(biru_lenght+1)*spacing)//(biru_lenght-1)
            multi_col_pasting(biru, y, image, horizontal_gardens, max_heights[row], spacing)
        y += spacing + max_heights[row]
    images.save(image._image, file_png)


def ex(file_dati, file_png, spaziatura):
    buildings, widths, heights = get_data(file_dati)
    measures, max_heights = measure(widths, heights, spaziatura)
    render(measures, widths, max_heights, buildings, spaziatura, file_png)
    return measures



if __name__ == '__main__':
    #test = ex('matrices/mat-3-1.txt', 'example.png', 1) # 'example', 42, (288, 348), 0.5
    test = ex('matrices/example.txt', 'example.png', 42)
    print(test)














