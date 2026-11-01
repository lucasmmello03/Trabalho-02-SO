"""Algoritmo CFS (Completely Fair Scheduler) — versão didática do enunciado (4.6).

Estrutura de dados: os processos prontos ficam em uma lista simples.
A cada unidade de tempo, a lista é percorrida para achar o menor vruntime.
Não usamos árvore rubro-negra (o enunciado permite).
"""

TOLERANCIA = 1e-9


def desempate_geral(candidatos):
    """Menor instante de chegada e, depois, menor ID."""
    return min(candidatos, key=lambda p: (p["chegada"], p["id"]))


def escolher_proximo(prontos):
    """Escolhe o processo que vai executar a próxima unidade de tempo."""

    # Regra 1: menor vruntime (comparando com tolerância de 1e-9).
    menor = min(p["vruntime"] for p in prontos)
    candidatos = [p for p in prontos if p["vruntime"] - menor <= TOLERANCIA]

    if len(candidatos) == 1:
        return candidatos[0]

    # Regra 2: empate -> quem nunca executou tem preferência.
    nunca_executaram = [p for p in candidatos if p["ultima_execucao"] is None]
    if nunca_executaram:
        # Regra 3: persistindo o empate, chegada e ID.
        return desempate_geral(nunca_executaram)

    # Regra 2 (continuação): quem está há mais tempo sem executar,
    # ou seja, cuja última execução terminou mais cedo.
    return min(candidatos, key=lambda p: p["ultima_execucao"])


def simular_cfs(processos):
    """Simula o CFS e devolve a linha do tempo: lista de (processo, inicio, fim)."""

    # Cópia dos processos com os campos que a simulação precisa controlar.
    pendentes = []  # processos que ainda não chegaram
    for p in processos:
        pendentes.append({
            "id": p["id"],
            "chegada": p["chegada"],
            "peso": p["peso"],
            "restante": p["cpu"],       # tempo de CPU que ainda falta
            "vruntime": 0.0,
            "ultima_execucao": None,    # instante em que terminou sua última unidade
        })
    pendentes.sort(key=lambda p: (p["chegada"], p["id"]))

    prontos = []         # processos que já chegaram e ainda não concluíram
    referencia = 0.0     # último valor de referência registrado (inicialmente zero)
    tempo = 0
    linha_do_tempo = []

    while pendentes or prontos:

        # 1) Admitir os processos que chegam neste instante.
        #    Todos recebem o mesmo vruntime inicial: o menor entre os presentes
        #    ou, se não houver nenhum, o valor de referência.
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

        # 2) Se ninguém está pronto, a CPU fica ociosa até a próxima chegada.
        if not prontos:
            proxima_chegada = pendentes[0]["chegada"]
            linha_do_tempo.append(("OCIOSO", tempo, proxima_chegada))
            tempo = proxima_chegada
            continue

        # 3) Escolher o processo (a decisão é refeita a cada unidade).
        atual = escolher_proximo(prontos)

        # 4) Executar uma unidade de tempo.
        linha_do_tempo.append((atual["id"], tempo, tempo + 1))
        atual["vruntime"] += 1024 / atual["peso"]
        atual["restante"] -= 1
        tempo += 1
        atual["ultima_execucao"] = tempo

        # 5) Se o processo terminou, ele sai da lista de prontos.
        if atual["restante"] == 0:
            prontos.remove(atual)

        # 6) Atualizar o valor de referência ao fim da unidade.
        if prontos:
            referencia = min(p["vruntime"] for p in prontos)
        else:
            # Ninguém restou: conserva o vruntime do último processo concluído.
            referencia = atual["vruntime"]

    return linha_do_tempo
