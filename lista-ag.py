#Import das bibliotecas necessárias
import random
import numpy
import math
import matplotlib.pyplot as plt

#Criação do objeto agente
class Agente:
	#Definição do método construtor
	#Cada agente terá um vetor de tamanho informado globalmente com valores entre -range e +range
	#O fitness inicial é iniciado com qualquer valor
	def __init__(self):
		self.cromossomo = numpy.random.uniform(-dominio, dominio, tamanho_cromossomo)
		self.fitness = 0

	#Imprime o cromossomo e o seu fitness
	def __cromossomo__(self):
		return 'Cromossomo: ' + str(self.cromossomo) + ' Fitness: ' + str(self.fitness)

#Definições de variáveis globais para o algoritmo genético
tamanho_cromossomo = 2
populacao = 50
geracoes = 10
#Domínios das funções: Schwefel = 500, Rastrigin = 5, função_exponencial = 2
dominio = 500
#Funções: 1 = Schwefel, 2 = Rastrigin, 3 = função_exponencial
funcao = 1 
#Estratégias de seleção: 1 = Torneio, 2 = Roleto
selecao = 1 
#Métodos de crossover: 1 = Uniforme, 2 = Aritmético
metodo = 1 

#Rotina do algoritmo genético
def ag():
	#Inicia uma população de tamanho informado globalmente com agente em posições aleatórias dentro do espaço do problema
	agentes = init_agentes(populacao)
	agentes = fitness(agentes, funcao)
	melhores = []
	piores = []
	media = []
	avaliacao(agentes, melhores, piores, media)
	#Itera até acabar o número de gerações estipulado
	#Dentro de cada geração são executados todos os processos do algoritmo genético
	for geracao in xrange(geracoes):
		print 'Geração: ' + str(geracao + 1) + ' Melhor agente: ' + melhores[geracao].__cromossomo__() + ' Pior agente: ' + piores[geracao].__cromossomo__() + ' Media da gera?o: ' + str(media[geracao])
		agentes = selecao(agentes, selecao)
		agentes = crossover(agentes, metodo)
		agentes = mutacao(agentes)
		agentes = fitness(agentes, funcao)
		avaliacao(agentes, melhores, piores, media)
		#Definição de outras condições de parada
		#if any(agente.fitness > threshold for agente in agentes):
		#	print 'Threshold alcançado!'
		#	exit(0)

#Método para inicialização aleatória da população de agentes
def init_agentes(populacao):
	return [Agente() for _ in xrange(populacao)]

def fitness(agentes, funcao):
	if funcao == 1:
		for agente in agentes:
			agente.fitness = schwefel(agente.cromossomo)
	elif funcao == 2:
		for agente in agentes:
			agente.fitness = rastrigin(agente.cromossomo)
	else:
		for agente in agentes:
			agente.fitness = funcao_exponencial(agente.cromossomo)
	return sorted(agentes, key=lambda agente: agente.fitness)

#Definições das diferentes fórmulas de fitness pedidas na lista
#Necessário conferir corretude das funções através de plot do gráfico
#Fitness segundo a função de Schwefel
def schwefel(cromossomo):
	alpha = 418.982887
	fit = 0
	for i in range(len(cromossomo)):
		fit -= cromossomo[i]*math.sin(math.sqrt(math.fabs(cromossomo[i])))
	return float(fit) + alpha*len(cromossomo)

#Fitness segundo a função de Rastrigin
def rastrigin(cromossomo):
	fit = 10*len(cromossomo)
	for i in range(len(cromossomo)):
		fit += cromossomo[i]**2 - (10*math.cos(2*math.pi*cromossomo[i]))
	return fit

#Fitness segundo a função dado pelo professor
def funcao_exponencial(cromossomo):
	exp = 0
	for i in range(len(cromossomo)):
	    exp += cromossomo[i]**2
	return cromossomo[1] * math.exp(-exp)

def selecao(agentes, selecao):
        if selecao == 1:
                agentes = torneio(agentes)
        else:
                agentes = roleta(agentes)
        return agentes

#Salva informações de evolução do algoritmo genético
def avaliacao(agentes, melhores, piores, media):
        melhores.append(agentes[0])
        piores.append(agentes[populacao - 1])
        media.append(sum([agente.fitness for agente in agentes]) / populacao)

#Definições das diferentes abordagens de seleção
#Seleção por Torneio
def torneio(agentes):
	#Vencedores do Torneio
	vencedores = []
	#Itera a seleção pelo tamanho da população
	for _ in xrange(populacao):
		competidor1 = random.choice(agentes)
		competidor2 = random.choice(agentes)
		if competidor1.fitness > competidor2.fitness:
			vencedores.append(competidor1)
		elif competidor2.fitness > competidor1.fitness:
			vencedores.append(competidor2)
		elif random.uniform(0.0, 1.0) <= 0.5:
			vencedores.append(competidor1)
		else :
			vencedores.append(competidor2)
	#Retorna vencedores do Torneio para crossover
	return vencedores

#Seleção por Roleta
def roleta(agentes):
	selecionados = []
	somatorio = sum([agente.fitness for agente in agentes])
	for agente in agentes:
		#Probabilidade maior de encontrar os menores valores de fitness
		agente.fitness = 1 - (agente.fitness / somatorio)
	#Repete o processo de seleção por roleta para metade do tamanho da população
	for _ in xrange(populacao):
		valor = random.uniform(0,1)
		atual = 0
		for agente in agentes:
			atual += agente.fitness
			if atual > valor:
				selecionados.append(agente)
				break
	return selecionados

#Definições das diferentes abrodagens de crossover
#Função abaixo não está completa. Necessário pesquisar crossover em números reais
def crossover(agentes, metodo):
	if metodo == 1:
		return crossover_uniforme(agentes)
	else:
		return crossover_aritmetico(agentes)

#Definição de crossover uniforme. Escolhe um número aleatório uniforme entre os valores dos pais
def crossover_uniforme(agentes):
	descendentes = []
	for _ in xrange(populacao / 2):
		pai1 = random.choice(agentes)
		pai2 = random.choice(agentes)
		filho1 = Agente()
		filho2 = Agente()
		for idx, _ in enumerate(filho1.cromossomo):
			filho1.cromossomo[idx] = numpy.random.uniform(pai1.cromossomo[idx], pai2.cromossomo[idx])
		for idx, _ in enumerate(filho2.cromossomo):
			filho2.cromossomo[idx] = numpy.random.uniform(pai1.cromossomo[idx], pai2.cromossomo[idx])
		descendentes.append(filho1)
		descendentes.append(filho2)
	return descendentes

#Definição de crossover aritmético. Realiza contas aritméticas com os valores dos pais
def crossover_aritmetico(agentes):
	descendentes = []
	alpha = 0.5
	for _ in xrange(populacao / 2):
		pai1 = random.choice(agentes)
		pai2 = random.choice(agentes)
		filho1 = Agente()
		filho2 = Agente()
		for idx, _ in enumerate(filho1.cromossomo):
			filho1.cromossomo[idx] = (alpha * pai1.cromossomo[idx]) + ((1 - alpha) * pai2.cromossomo[idx])
		for idx, _ in enumerate(filho2.cromossomo):
			filho2.cromossomo[idx] = (alpha * pai1.cromossomo[idx]) + ((1 - alpha) * pai2.cromossomo[idx])
		descendentes.append(filho1)
		descendentes.append(filho2)
	return descendentes

#Definição da abordagem de mutação randômica uniforme
def mutacao(agentes):
	for agente in agentes:
		#Itera sobre os valores do cromossomo com 10% de chance de mutação
		for idx, _ in enumerate(agente.cromossomo):
			if random.uniform(0.0, 1.0) <= 0.1:
				#processo de mutação de valores reais no intervalo de domínio
				agente.cromossomo[idx] = numpy.random.uniform(-dominio, dominio)
	return agentes

#Loop principal do programa
if __name__ == '__main__':
	ag()
