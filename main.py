NUMERO_INVALIDO = "Numero de tweet invalido."
NO_ENCONTRADOS = "No se encontraron tweets."
INPUT_INVALIDO = "Input invalido."
FIN = "Finalizando..."
RESULTADOS_BUSQUEDA = "Resultados de la busqueda:"
TWEETS_ELIMINADOS = "Tweets eliminados:"

def mostrar_menu():
    print("1. Crear Tweet")
    print("2. Buscar Tweet")
    print("3. Eliminar Tweet")
    print("4. Salir")

def normalizar(texto):
    texto = texto.lower()
    palabra = ""
    palabras = []

    for letra in texto:
        if letra.isalnum():
            palabra += letra
        elif palabra:
            palabras.append(palabra)
            palabra = ""

    if palabra:
        palabras.append(palabra)
    return palabras

def tokenizar_segmentos(palabra):
    n = 3
    segmentos = set()
    for i in range(len(palabra)):
        for j in range(i + n, len(palabra) + 1):
            segmentos.add(palabra[i:j])
    return segmentos

def busqueda_binaria(lista, clave):
    izquierda = 0
    derecha = len(lista) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        actual = lista[medio][0]

        if actual == clave:
            return medio
        elif actual < clave:
            izquierda = medio + 1
        else:
            derecha = medio - 1

    return -1

def insertar_en_orden(indice, clave, tweet_id):
    izquierda = 0
    derecha = len(indice)
    while izquierda < derecha:
        medio = (izquierda + derecha) // 2
        if indice[medio][0] < clave:
            izquierda = medio + 1
        else:
            derecha = medio

    if izquierda < len(indice) and indice[izquierda][0] == clave:
        indice[izquierda][1].add(tweet_id)
    else:
        indice.insert(izquierda, (clave, {tweet_id}))

def crear_tweet(tweets, indice_palabras, indice_segmentos, siguiente_id):
    while True:
        print("Ingrese su tweet: ")
        tweet = input(" ").strip()
        palabras_normalizadas = normalizar(tweet)

        if not palabras_normalizadas:
            print(INPUT_INVALIDO)
            continue

        tweets[siguiente_id] = tweet
        for palabra in palabras_normalizadas:
            insertar_en_orden(indice_palabras, palabra, siguiente_id)
            for segmento in tokenizar_segmentos(palabra):
                insertar_en_orden(indice_segmentos, segmento, siguiente_id)

        print(f"Listo! {siguiente_id}")
        return siguiente_id + 1

def buscar_tweet(tweets, indice_palabras, indice_segmentos):
    print("Ingrese las palabras claves a buscar: ")
    entrada = input(" ").strip()
    tokens_busqueda = normalizar(entrada)

    if not tokens_busqueda:
        print(NO_ENCONTRADOS)
        return

    resultados = None
    for token in tokens_busqueda:
        ids_encontrados = set()

        pos = busqueda_binaria(indice_palabras, token)
        if pos != -1:
            ids_encontrados.update(indice_palabras[pos][1])

        pos_seg = busqueda_binaria(indice_segmentos, token)
        if pos_seg != -1:
            ids_encontrados.update(indice_segmentos[pos_seg][1])

        if not ids_encontrados:
            resultados = set()
            break

        if resultados is None:
            resultados = ids_encontrados
        else:
            resultados &= ids_encontrados

    if not resultados:
        print(NO_ENCONTRADOS)
        return

    print(RESULTADOS_BUSQUEDA)
    for tweet_id in sorted(resultados):
        print(f"{tweet_id}. {tweets[tweet_id]}")

def eliminar_tweet(tweets, indice_palabras, indice_segmentos):
    while True:
        print("Ingrese la palabra clave para filtrar:")
        palabra_clave = input(" ").strip()
        tokens = normalizar(palabra_clave)

        if not tokens:
            print(NO_ENCONTRADOS)
            continue

        token = tokens[0]
        ids = set()
        pos = busqueda_binaria(indice_palabras, token)
        if pos != -1:
            ids.update(indice_palabras[pos][1])

        pos_seg = busqueda_binaria(indice_segmentos, token)
        if pos_seg != -1:
            ids.update(indice_segmentos[pos_seg][1])

        if not ids:
            print(NO_ENCONTRADOS)
            continue

        print(RESULTADOS_BUSQUEDA)
        for tweet_id in sorted(ids):
            print(f"{tweet_id}. {tweets[tweet_id]}")
        print("Ingrese los numeros de tweets a eliminar (ej: 0,2-4):")
        entrada = input(" ").replace(" ", "")
        if not entrada:
            print(INPUT_INVALIDO)
            continue

        try:
            seleccionados = set()
            partes = entrada.split(",")
            for parte in partes:
                if "-" in parte:
                    ini, fin = map(int, parte.split("-"))
                    if ini > fin:
                        raise ValueError
                    seleccionados.update(range(ini, fin + 1))
                else:
                    seleccionados.add(int(parte))

            if not seleccionados.issubset(ids):
                print(NUMERO_INVALIDO)
                continue

            print(TWEETS_ELIMINADOS)
            for id_eliminar in sorted(seleccionados):
                print(f"{id_eliminar}. {tweets[id_eliminar]}")
                palabras = normalizar(tweets[id_eliminar])
                for palabra in palabras:
                    pos = busqueda_binaria(indice_palabras, palabra)
                    if pos != -1:
                        indice_palabras[pos][1].discard(id_eliminar)
                        if not indice_palabras[pos][1]:
                            indice_palabras.pop(pos)
                    for segmento in tokenizar_segmentos(palabra):
                        pos_seg = busqueda_binaria(indice_segmentos, segmento)
                        if pos_seg != -1:
                            indice_segmentos[pos_seg][1].discard(id_eliminar)
                            if not indice_segmentos[pos_seg][1]:
                                indice_segmentos.pop(pos_seg)

                tweets.pop(id_eliminar)
            return
        except:
            print(INPUT_INVALIDO)


def main():
    opcion = 0
    tweets = {}
    indice_palabras = []
    indice_segmentos = []
    siguiente_id = 0

    while opcion != 4:
        mostrar_menu()
        try:
            opcion = int(input("ingrese una opcion: "))
        except ValueError:
            print(INPUT_INVALIDO)
            continue

        if opcion == 1:
            siguiente_id = crear_tweet(tweets, indice_palabras, indice_segmentos, siguiente_id)
        elif opcion == 2:
            buscar_tweet(tweets, indice_palabras, indice_segmentos)
        elif opcion == 3:
            eliminar_tweet(tweets, indice_palabras, indice_segmentos)
        elif opcion == 4:
            print(FIN)
        else:
            print(INPUT_INVALIDO)


if __name__ == "__main__":
    main()
