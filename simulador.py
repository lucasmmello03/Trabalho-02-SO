
import json
import sys

from cfs import simular_cfs
from fcfs import simular_fcfs
from metricas import calcular_metricas, unir_intervalos
from validacao import ErroEntrada, ler_entrada


def main():
    try:
        entrada = ler_entrada(sys.stdin.read())
    except ErroEntrada as erro:
        print(json.dumps({"erro": str(erro)}, ensure_ascii=False))
        sys.exit(1)

    algoritmo = entrada["algoritmo"]
    processos = entrada["processos"]

    if algoritmo == "FCFS":
        linha_do_tempo = simular_fcfs(processos)
    else:
        linha_do_tempo = simular_cfs(processos)

    linha_do_tempo = unir_intervalos(linha_do_tempo)
    metricas, medias = calcular_metricas(processos, linha_do_tempo)

    resultado = {
        "algoritmo": algoritmo,
        "linha_do_tempo": linha_do_tempo,
        "processos": metricas,
        "medias": medias,
    }
    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
