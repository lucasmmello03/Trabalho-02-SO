# Simulador de escalonamento de processos — FCFS e CFS

Trabalho II de Sistemas Operacionais — IFRS.

**Dupla 1:** Lucas Mello e Rafael Santos

**Algoritmos implementados:** `FCFS` e `CFS` (versão didática do enunciado).

## Requisitos

Python 3.8 ou superior. Não usa bibliotecas externas.

## Execução

```bash
python3 simulador.py < entrada.json > resultado.json
```

O programa lê o JSON da entrada padrão e escreve o resultado na saída padrão. Para comparar os algoritmos, troque `"algoritmo"` entre `"FCFS"` e `"CFS"`; os dois usam `"configuracao": {}`.

Se a entrada for inválida, o programa imprime `{"erro": "..."}` e encerra com código 1.

Os arquivos dos experimentos estão em `experimentos/entradas` e `experimentos/saidas`, e os diagramas de Gantt em `experimentos/gantt`.

## Organização do código

| Arquivo | Responsabilidade |
|---|---|
| `simulador.py` | Lê a entrada, chama a validação, o algoritmo e as métricas, e escreve a saída. |
| `validacao.py` | Leitura e validação da entrada. |
| `fcfs.py` | Algoritmo FCFS. |
| `cfs.py` | Algoritmo CFS. |
| `metricas.py` | União de intervalos seguidos do mesmo processo e cálculo das métricas. |

Cada algoritmo devolve a linha do tempo como uma lista de `(processo, inicio, fim)`, incluindo os trechos `OCIOSO`. As métricas são calculadas a partir dela: a primeira execução é o início do primeiro intervalo do processo e a conclusão é o fim do último.

## Estruturas de dados

**FCFS:** a fila é a lista de processos ordenada por `(chegada, id)`. Ela é percorrida em ordem. Quando o próximo processo ainda não chegou, registra-se um trecho `OCIOSO` até a chegada dele.

**CFS:**
- `pendentes`: lista dos processos que ainda não chegaram, ordenada por `(chegada, id)`.
- `prontos`: **lista simples** dos processos que chegaram e não concluíram. Cada processo guarda `vruntime`, `restante`, `peso` e `ultima_execucao` (o instante em que terminou sua última unidade, ou `None` se nunca executou).
- `referencia`: o último valor de referência, usado para inicializar quem chega quando não há ninguém pronto.

A cada unidade de tempo, a lista `prontos` é percorrida e o próximo processo é escolhido pelas regras do enunciado, nesta ordem:
1. menor `vruntime`, com tolerância `1e-9`;
2. em empate, quem nunca executou; entre esses, menor chegada e depois menor ID;
3. se todos já executaram, quem está há mais tempo sem executar (menor `ultima_execucao`).

**Simplificações em relação ao CFS do Linux:** não há árvore rubro-negra (a lista é percorrida inteira a cada unidade), latência alvo, granularidade mínima nem tabela de pesos por `nice`. A decisão é refeita a cada unidade inteira, e o peso entra apenas em `vruntime += 1024 / peso`.
