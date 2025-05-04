def obtener_ids_por_token(token, indice_palabras, indice_segmentos):
    ids = set()
    pos = busqueda_binaria(indice_palabras, token)
    if pos != -1:
        ids.update(indice_palabras[pos][1])
    pos_seg = busqueda_binaria(indice_segmentos, token)
    if pos_seg != -1:
        ids.update(indice_segmentos[pos_seg][1])
    return ids

def mostrar_tweets_filtrados(ids, tweets):
    print("Resultados de la busqueda:")
    for tweet_id in sorted(ids):
        print(f"{tweet_id}. {tweets[tweet_id]}")

def parsear_seleccion(entrada):
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
    return seleccionados

def eliminar_indices(tweet, tweet_id, indice_palabras, indice_segmentos):
    palabras = normalizar(tweet)
    for palabra in palabras:
        pos = busqueda_binaria(indice_palabras, palabra)
        if pos != -1:
            indice_palabras[pos][1].discard(tweet_id)
            if not indice_palabras[pos][1]:
                indice_palabras.pop(pos)
        for segmento in tokenizar_segmentos(palabra):
            pos_seg = busqueda_binaria(indice_segmentos, segmento)
            if pos_seg != -1:
                indice_segmentos[pos_seg][1].discard(tweet_id)
                if not indice_segmentos[pos_seg][1]:
                    indice_segmentos.pop(pos_seg)

def eliminar_tweet(tweets, indice_palabras, indice_segmentos):
    while True:
        print("Ingrese el tweet a eliminar:")
        palabra_clave = input(" ").strip()
        tokens = normalizar(palabra_clave)

        if not tokens:
            print("No se encontraron tweets.")
            continue

        token = tokens[0]
        ids = obtener_ids_por_token(token, indice_palabras, indice_segmentos)

        if not ids:
            print("No se encontraron tweets.")
            continue

        mostrar_tweets_filtrados(ids, tweets)

        print("Ingrese los numeros de tweets a eliminar:")
        entrada = input(" ").replace(" ", "")
        if not entrada:
            print("Input invalido.")
            continue

        try:
            seleccionados = parsear_seleccion(entrada)
            if not seleccionados.issubset(ids):
                print("Numero de tweet invalido.")
                continue

            print("Tweets eliminados:")
            for id_eliminar in sorted(seleccionados):
                print(f"{id_eliminar}. {tweets[id_eliminar]}")
                eliminar_indices(tweets[id_eliminar], id_eliminar, indice_palabras, indice_segmentos)
                tweets.pop(id_eliminar)
            return

        except:
            print("Input invalido.")
