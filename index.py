# 1. Faça uma análise estatística inicial dos dados, plotando as quantidades médias, desvios padrões
# de todas as variáveis dos dados; (1,0 ponto)
import pandas

dataset = pandas.read_csv("./SA_heart.csv")

print(dataset.describe())