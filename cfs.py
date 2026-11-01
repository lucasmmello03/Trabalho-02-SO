TOLERANCIA = 1e-9


def desempate_geral(candidatos):
    return min(candidatos, key=lambda p: (p["chegada"], p["id"]))


def escolher_proximo(prontos):
    menor = min(p["vruntime"] for p in prontos)
    candidatos = [p for p in prontos if p["vruntime"] - menor <= TOLERANCIA]

    if len(candidatos) == 1:
        return candidatos[0]

    nunca_executaram = [p for p in candidatos if p["ultima_execucao"] is None]
    if nunca_executaram:
        return desempate_geral(nunca_executaram)

    return min(candidatos, key=lambda p: p["ultima_execucao"])


def simular_cfs(processos):
    pendentes = []
    for p in processos:
        pendentes.append({
            "id": p["id"],
            "chegada": p["chegada"],
            "peso": p["peso"],
            "restante": p["cpu"],
            "vruntime": 0.0,
            "ultima_execucao": None,
        })
    pendentes.sort(key=lambda p: (p["chegada"], p["id"]))

    prontos = []
    referencia = 0.0
    tempo = 0
    linha_do_tempo = []

    while pendentes or prontos:
        chegando = [p for p in pendentes if p["chegada"] == tempo]
        if chegando:
            if prontos:
                vruntime_inicial = min(p["vruntime"] for p in prontos)
            else:
                vruntime_inicial = referencia
            for p in chegando:
                p["vruntime"] = vruntime_inicial
                pendentes.remove(p)
                prontos.append(p)

        if not prontos:
            proxima_chegada = pendentes[0]["chegada"]
            linha_do_tempo.append(("OCIOSO", tempo, proxima_chegada))
            tempo = proxima_chegada
            continue

        atual = escolher_proximo(prontos)

        linha_do_tempo.append((atual["id"], tempo, tempo + 1))
        atual["vruntime"] += 1024 / atual["peso"]
        atual["restante"] -= 1
        tempo += 1
        atual["ultima_execucao"] = tempo

        if atual["restante"] == 0:
            prontos.remove(atual)

        if prontos:
            referencia = min(p["vruntime"] for p in prontos)
        else:
            referencia = atual["vruntime"]

    return linha_do_tempo
