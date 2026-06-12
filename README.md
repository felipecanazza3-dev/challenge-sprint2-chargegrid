
# ChargeGrid Intelligence - Prova de Conceito (Sprint 2)

## Descrição da Solução
Este repositório apresenta a Prova de Conceito (PoC) desenvolvida em Python para a expansão comercial do ecossistema GoodWe. O objetivo principal do sistema é gerenciar uma rede de eletropostos inteligentes voltados para frotas e comércios, mitigando os riscos de sobrecarga na rede elétrica local e aplicando regras de cobrança automatizadas.

A solução foi construída utilizando os pilares da Orientação a Objetos (POO), garantindo modularidade, facilidade de manutenção e escalabilidade.

---

## Pilares do Desafio Implementados

### 1. Gerenciamento Inteligente de Demanda (Controle de Carga)
O sistema monitora em tempo real a potência total solicitada pelos veículos conectados. Caso a demanda ultrapasse a capacidade física suportada pela infraestrutura do estabelecimento, o algoritmo de controle entra em ação, redistribuindo e limitando a potência de cada estação de forma equitativa para evitar quedas de energia (blackouts) ou multas por ultrapassagem de demanda contratada.

### 2. Tarifação Dinâmica e Pagamento
Integração com a lógica de variação de preço baseada no horário do consumo. O sistema identifica automaticamente a faixa horária de recarga para aplicar as tarifas correspondentes:
* Horário de Pico: Tarifa diferenciada (crítica) para desestimular o uso excessivo quando a rede comercial está sobrecarregada.
* Horário Comercial e Fora de Pico: Tarifas reduzidas para incentivar o carregamento em momentos de ociosidade da rede.

### 3. Simulação e Fluxo Lógico (PoC Digital)
Uma simulação completa que demonstra os carros ocupando as estações, a ativação dos algoritmos de proteção e o cálculo de faturamento das sessões de recarga, exibindo os resultados diretamente no console de execução.

---

## Arquitetura e Fluxo do Sistema

O sistema funciona através de um ciclo contínuo de verificação e execução, estruturado da seguinte forma:

1. Entrada de Dados: O veículo elétrico é conectado a uma estação de recarga disponível, informando seu modelo, capacidade total da bateria e o nível de carga atual.
2. Análise de Cenário comercial: O módulo de inteligência artificial do sistema consulta o horário atual para determinar qual faixa de tarifação deve ser aplicada sobre o consumo de energia.
3. Balanceamento e Proteção de Rede: O algoritmo soma a demanda máxima de todas as estações ativas. Caso o total ultrapasse o limite físico suportado pelo comércio, a potência de cada totem é reduzida proporcionalmente em tempo real.
4. Processamento da Carga e Cobrança: O sistema injeta a energia corrigida nos veículos, calcula o valor financeiro correspondente à sessão e atualiza o faturamento acumulado do eletroposto.

Estrutura das Entidades (Classes):
* VeiculoEletrico: Gerencia os dados de capacidade (em kWh), porcentagem de carga e o cálculo de energia necessária para completar a bateria.
* EstacaoRecarga: Representa os totens físicos de carregamento, controlando o status da vaga (Disponível/Ocupada) e a potência alocada.
* ChargeGridIA: Camada lógica responsável por analisar as tarifas por horário e executar o algoritmo de balanceamento de carga para evitar sobrecarga.
* SistemaChargeGrid: Coordenador geral do sistema que unifica as estações, executa os ciclos de simulação e consolida os dados financeiros.

---

## Materiais Técnicos Relevantes

Tecnologias e Dependências:
* Linguagem de Programação: Python 3.10 ou superior.
* Biblioteca Datetime: Módulo nativo do Python utilizado para capturar o horário do sistema operacional em tempo real e determinar a flutuação de tarifas de forma automatizada.
* Biblioteca Time: Módulo nativo utilizado para simular o intervalo de tempo necessário para a injeção de carga nos veículos durante os testes práticos.

Paradigma de Desenvolvimento:
* Programação Orientada a Objetos (POO): Utilização de classes, encapsulamento de atributos e métodos específicos para representar fielmente o comportamento físico de uma estação de recarga no ambiente digital.

---

## Como Executar o Projeto

### Pré-requisitos
* Python 3.10 ou superior instalado na máquina.

### Passo a Passo
1. Clone este repositório ou baixe o arquivo de código.
2. Certifique-se de que o arquivo principal está nomeado como main.py.
3. Abra o terminal na pasta do arquivo e execute o comando:
   ```bash
   python main.py
