
def simular_fcfs(processos):

    fila = sorted(processos, key=lambda p: (p["chegada"], p["id"]))

    tempo = 0
    linha_do_tempo = []

    for processo in fila:
        if tempo < processo["chegada"]:
            linha_do_tempo.append(("OCIOSO", tempo, processo["chegada"]))
            tempo = processo["chegada"]

        inicio = tempo
        fim = tempo + processo["cpu"]
        linha_do_tempo.append((processo["id"], inicio, fim))
        tempo = fim

    return linha_do_tempo