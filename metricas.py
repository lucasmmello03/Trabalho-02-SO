
def unir_intervalos(linha_do_tempo):
    
    resultado = []
    for processo, inicio, fim in linha_do_tempo:
        anterior = resultado[-1] if resultado else None
        if anterior and anterior["processo"] == processo and anterior["fim"] == inicio:
            anterior["fim"] = fim
        else:
            resultado.append({"processo": processo, "inicio": inicio, "fim": fim})
    return resultado


def calcular_metricas(processos, linha_do_tempo):

    metricas = []

    for p in sorted(processos, key=lambda p: p["id"]):

        trechos = [t for t in linha_do_tempo if t["processo"] == p["id"]]

        primeira_execucao = trechos[0]["inicio"]  
        conclusao = trechos[-1]["fim"]             
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