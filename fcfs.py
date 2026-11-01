"""Algoritmo FCFS (First Come, First Served).

Regras do enunciado (4.1):
- Manter uma fila pela ordem de chegada.
- O processo escolhido executa até concluir.
- Novas chegadas não interrompem o processo atual.
"""


def simular_fcfs(processos):
    """Simula o FCFS e devolve a linha do tempo: lista de (processo, inicio, fim)."""

    # A fila é a lista ordenada por chegada; em empate, pelo ID (desempate geral).
    fila = sorted(processos, key=lambda p: (p["chegada"], p["id"]))

    tempo = 0
    linha_do_tempo = []

    for processo in fila:
        # Se o processo ainda não chegou, a CPU fica ociosa até a chegada dele.
        if tempo < processo["chegada"]:
            linha_do_tempo.append(("OCIOSO", tempo, processo["chegada"]))
            tempo = processo["chegada"]

        # O processo executa do início ao fim, sem interrupção.
        inicio = tempo
        fim = tempo + processo["cpu"]
        linha_do_tempo.append((processo["id"], inicio, fim))
        tempo = fim

    return linha_do_tempo
