import random
import time
from datetime import datetime


class VeiculoEletrico:
    """Representa um veículo que chega para carregar no posto comercial."""

    def __init__(self, modelo: str, capacidade_bateria: float, carga_atual: float):
        self.modelo = modelo
        self.capacidade_bateria =  capacidade_bateria # em kWh
        self.carga_atual = carga_atual  # em %
        self.Kwh_necessarios = (100 - carga_atual) * capacidade_bateria / 100

    def atualizar_carga(self, kwh_injetados: float):
        porcentagem_ganha = (kwh_injetados / self.capacidade_bateria) * 100
        self.carga_atual = min(100.0, self.carga_atual + porcentagem_ganha)


class EstacaoRecarga:
    """Representa uma vaga/totem de carregamento do ChargeGrid."""

    def __init__(self, id_estacao: int, potencia_maxima: float = 50.0):
        self.id_estacao = id_estacao
        self.potencia_maxima = potencia_maxima  # em kW
        self.potencia_atual_alocada = 0.0  # Dinâmico via IA/Controle de Demanda
        self.veiculo_atual = None
        self.status = "Disponível"

    def ocupar_estacao(self, veiculo: VeiculoEletrico):
        self.veiculo_atual = veiculo
        self.status = "Ocupada"

    def liberar_estacao(self):
        self.veiculo_atual = None
        self.status = "Disponível"
        self.potencia_atual_alocada = 0.0


class ChargeGridIA:
    """Inteligência Artificial e Controle Inteligente de Demanda."""

    def __init__(self, limite_rede_kw: float):
        self.limite_rede_kw = limite_rede_kw  # Limite máximo que o comércio aguenta

    def analisar_tarifa_por_horario(self) -> dict:
        """Simula a variação de preço (Tarifação Inteligente)."""
        hora_atual = datetime.now().hour
        # Horário de pico em comércio geralmente é das 17h às 20h
        if 17 <= hora_atual <= 20:
            return {"tipo": "Pico", "preco_kwh": 2.10, "fator_demanda": "Crítico"}
        elif 8 <= hora_atual <= 16:
            return {"tipo": "Comercial", "preco_kwh": 1.40, "fator_demanda": "Moderado"}
        else:
            return {"tipo": "Fora de Pico", "preco_kwh": 0.90, "fator_demanda": "Baixo"}

    def otimizar_potencia_estacoes(self, estacoes: list):
        """Algoritmo de Controle de Demanda (IA) para balanceamento de carga."""
        estacoes_ativas = [e for e in estacoes if e.status == "Ocupada"]
        if not estacoes_ativas:
            return

        # CORRIGIDO: Alterado de estacoes_active para estacoes_ativas
        demanda_solicitada = sum(e.potencia_maxima for e in estacoes_ativas)

        print(f"\n--- [IA] Monitoramento de Demanda Comercial ---")
        print(f"Capacidade Máxima da Rede: {self.limite_rede_kw} kW")
        print(f"Demanda Teórica Solicitada: {demanda_solicitada} kW")

        # Se a demanda passar do limite do prédio, a IA corta/ajusta a potência de cada um
        if demanda_solicitada > self.limite_rede_kw:
            print("Alerta de Sobrecarga! IA recalculando distribuição de energia...")
            potencia_por_estacao = self.limite_rede_kw / len(estacoes_ativas)
            for estacao in estacoes_ativas:
                estacao.potencia_atual_alocada = potencia_por_estacao
                print(f" -> Estação #{estacao.id_estacao} limitada a {potencia_por_estacao:.2f} kW")
        else:
            print(" Rede estável. Fornecendo potência máxima permitida.")
            for estacao in estacoes_ativas:
                estacao.potencia_atual_alocada = estacao.potencia_maxima


class SistemaChargeGrid:
    """Gerenciador Geral do Sistema."""

    def __init__(self, limite_rede: float):
        self.estacoes = [EstacaoRecarga(1), EstacaoRecarga(2), EstacaoRecarga(3)]
        self.ia = ChargeGridIA(limite_rede)
        self.historico_faturamento = 0.0

    def exibir_status(self):
        print("\n================ STATUS REQUISITOS CHARGEGRID ================")
        for e in self.estacoes:
            carro = e.veiculo_atual.modelo if e.veiculo_atual else "Nenhum"
            carga = f"{e.veiculo_atual.carga_atual:.1f}%" if e.veiculo_atual else "-"
            print(
                f"Estação {e.id_estacao} | Status: {e.status} | Carro: {carro} | Carga: {carga} | Potência Alocada: {e.potencia_atual_alocada} kW")
        print("==============================================================")

    def simular_ciclo_carregamento(self):
        tarifa = self.ia.analisar_tarifa_por_horario()
        print(f"\n[Tarifação] Horário Atual | Tipo: {tarifa['tipo']} | Valor/kWh: R${tarifa['preco_kwh']:.2f}")

        # IA roda o balanceamento de carga
        self.ia.otimizar_potencia_estacoes(self.estacoes)

        print("\nIniciando ciclo de carregamento rápido simulado...")
        time.sleep(1)

        for e in self.estacoes:
            if e.status == "Ocupada" and e.veiculo_atual:
                carro = e.veiculo_atual
                # Simula a energia entregue em um intervalo de tempo proporcional à potência alocada
                energia_entregue = e.potencia_atual_alocada * 0.2  # simulação de fração de tempo

                if energia_entregue > carro.Kwh_necessarios:
                    energia_entregue = carro.Kwh_necessarios

                carro.atualizar_carga(energia_entregue)
                custo_sessao = energia_entregue * tarifa['preco_kwh']
                self.historico_faturamento += custo_sessao

                print(f"⚡ Estação #{e.id_estacao} recarregou {energia_entregue:.2f} kWh no {carro.modelo}.")
                print(f"💵 Custo parcial da sessão: R${custo_sessao:.2f} | Carga Atual: {carro.carga_atual:.1f}%")

                if carro.carga_atual >= 100.0:
                    print(f"🔋 {carro.modelo} totalmente carregado! Liberando vaga.")
                    e.liberar_estacao()


# --- EXECUÇÃO DO PROTÓTIPO DIGITAL ---
if __name__ == "__main__":
    # Criamos o sistema simulando um comércio que aguenta no MÁXIMO 90kW de recarga simultânea
    # Como temos 3 estações de 50kW (Total 150kW), a IA vai ter que agir!
    sistema = SistemaChargeGrid(limite_rede=90.0)

    # Chegada de veículos elétricos comerciais
    carro1 = VeiculoEletrico("BYD Dolphin Plus", capacidade_bateria=60.5, carga_atual=20.0)
    carro2 = VeiculoEletrico("GWM Ora 3", capacidade_bateria=48.0, carga_atual=45.0)
    carro3 = VeiculoEletrico("Volvo XC40 Electric", capacidade_bateria=78.0, carga_atual=10.0)

    # Ocupando as vagas do posto
    sistema.estacoes[0].ocupar_estacao(carro1)
    sistema.estacoes[1].ocupar_estacao(carro2)
    sistema.estacoes[2].ocupar_estacao(carro3)

    # Mostra o painel inicial
    sistema.exibir_status()

    # Executa a simulação do algoritmo de IA e Tarifação
    sistema.simular_ciclo_carregamento()

    # Mostra o painel após o processamento da IA
    sistema.exibir_status()
    print(f"\n Faturamento Total Acumulado no Terminal Comercial: R${sistema.historico_faturamento:.2f}\n")