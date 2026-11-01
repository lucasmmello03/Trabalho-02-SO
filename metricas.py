"""Montagem da linha do tempo de saída e cálculo das métricas (seção 6)."""


def unir_intervalos(linha_do_tempo):
    """Une intervalos seguidos do mesmo processo.

    Exemplo: P01 [0,1) + P01 [1,2)  ->  P01 [0,2)
    Isso só muda a apresentação; a simulação já terminou.
    """
    resultado = []
    for processo, inicio, fim in linha_do_tempo:
        anterior = resultado[-1] if resultado else None
        if anterior and anterior["processo"] == processo and anterior["fim"] == inicio:
            anterior["fim"] = fim
        else:
            resultado.append({"processo": processo, "inicio": inicio, "fim": fim})
    return resultado


def calcular_metricas(processos, linha_do_tempo):
    """Calcula as métricas de cada processo (ordenadas por ID) e as médias.

    turnaround = conclusão - chegada
    espera     = turnaround - tempo de CPU
    resposta   = primeira execução - chegada
    """
    metricas = []

    for p in sorted(processos, key=lambda p: p["id"]):
        # Intervalos em que este processo executou.
        trechos = [t for t in linha_do_tempo if t["processo"] == p["id"]]

        primeira_execucao = trechos[0]["inicio"]   # início do primeiro intervalo
        conclusao = trechos[-1]["fim"]             # fim do último intervalo
        turnaround = conclusao - p["chegada"]

        metricas.append({
            "id": p["id"],
            "primeira_execucao": primeira_execucao,
            "conclusao": conclusao,
            "turnaround": turnaround,
            "espera": turnaround - p["cpu"],
            "resposta": primeira_execucao - p["chegada"],
        })

    quantidade = len(metricas)
    medias = {
        "turnaround": sum(m["turnaround"] for m in metricas) / quantidade,
        "espera": sum(m["espera"] for m in metricas) / quantidade,
        "resposta": sum(m["resposta"] for m in metricas) / quantidade,
    }

    return metricas, medias
