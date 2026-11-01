"""Leitura e validação da entrada JSON (seções 5.1 e 5.3).

Qualquer problema lança ErroEntrada com uma mensagem.
O simulador transforma essa exceção em {"erro": "..."} e encerra com código 1.
"""

import json

ALGORITMOS_IMPLEMENTADOS = ["FCFS", "CFS"]
PESO_PADRAO = 1024


class ErroEntrada(Exception):
    pass


def eh_inteiro(valor):
    # Em Python, True e False também são int; eles não podem ser aceitos.
    return isinstance(valor, int) and not isinstance(valor, bool)


def ler_entrada(texto):
    """Converte o texto JSON em um dicionário validado."""
    try:
        dados = json.loads(texto)
    except json.JSONDecodeError:
        raise ErroEntrada("A entrada não é um JSON válido.")

    if not isinstance(dados, dict):
        raise ErroEntrada("A entrada deve ser um objeto JSON.")

    algoritmo = validar_algoritmo(dados)
    validar_configuracao(dados)
    processos = validar_processos(dados, algoritmo)

    return {"algoritmo": algoritmo, "processos": processos}


def validar_algoritmo(dados):
    algoritmo = dados.get("algoritmo")
    if algoritmo is None:
        raise ErroEntrada("O campo 'algoritmo' é obrigatório.")
    if algoritmo not in ALGORITMOS_IMPLEMENTADOS:
        raise ErroEntrada(f"Algoritmo não implementado: {algoritmo}. Use FCFS ou CFS.")
    return algoritmo


def validar_configuracao(dados):
    # FCFS e CFS não têm parâmetros: basta ser um objeto (ex.: {}).
    # Parâmetros de outros algoritmos, como "quantum", são ignorados.
    if not isinstance(dados.get("configuracao"), dict):
        raise ErroEntrada("O campo 'configuracao' é obrigatório e deve ser um objeto.")


def validar_processos(dados, algoritmo):
    lista = dados.get("processos")
    if not isinstance(lista, list) or len(lista) == 0:
        raise ErroEntrada("O campo 'processos' deve ser uma lista não vazia.")

    processos = []
    ids_usados = []

    for p in lista:
        if not isinstance(p, dict):
            raise ErroEntrada("Cada processo deve ser um objeto.")

        # id: string não vazia, única e diferente de OCIOSO.
        pid = p.get("id")
        if not isinstance(pid, str) or pid == "":
            raise ErroEntrada("O id do processo deve ser uma string não vazia.")
        if pid == "OCIOSO":
            raise ErroEntrada("O id OCIOSO é reservado.")
        if pid in ids_usados:
            raise ErroEntrada(f"O id {pid} está repetido.")
        ids_usados.append(pid)

        # chegada: inteiro maior ou igual a zero.
        chegada = p.get("chegada")
        if not eh_inteiro(chegada) or chegada < 0:
            raise ErroEntrada(f"A chegada de {pid} deve ser um inteiro maior ou igual a zero.")

        # cpu: inteiro estritamente positivo.
        cpu = p.get("cpu")
        if not eh_inteiro(cpu) or cpu <= 0:
            raise ErroEntrada(f"O tempo de CPU de {pid} deve ser um inteiro positivo.")

        # peso: só é usado (e validado) no CFS; se omitido, vale 1024.
        peso = PESO_PADRAO
        if algoritmo == "CFS" and "peso" in p:
            peso = p["peso"]
            if not eh_inteiro(peso) or peso <= 0:
                raise ErroEntrada(f"O peso de {pid} deve ser um inteiro positivo.")

        processos.append({"id": pid, "chegada": chegada, "cpu": cpu, "peso": peso})

    return processos
