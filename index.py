# 1. Faça uma análise estatística inicial dos dados, plotando as quantidades médias, desvios padrões
# de todas as variáveis dos dados; (1,0 ponto)
import pandas
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve, ConfusionMatrixDisplay

dataset = pandas.read_csv("./SA_heart.csv")

# Removendo a coluna de identificação e transformando a coluna famhist para numérica
clear_dataset = pandas.get_dummies(dataset, drop_first=True)
clear_dataset = clear_dataset.drop(columns=['id'])

#print(clear_dataset.head(10))
print(clear_dataset.describe())

#plt.close("all")

figure, (graph11, graph12) = plt.subplots(1, 2)
graph11 = clear_dataset.describe().loc['mean'].plot.bar(title='Média', ax=graph11)
graph12 = clear_dataset.describe().loc['std'].plot.bar(title='Desvio padrão', ax=graph12)

figure.set_figheight(5)
figure.set_figwidth(20)
plt.show()

# Separando as variaveis e os resultados
X = clear_dataset.drop('chd', axis=1).values
Y = clear_dataset['chd'].values

# Modelo CART 
decisionTree = DecisionTreeClassifier()

KFolds = StratifiedKFold(n_splits=10)

legends = []
scores = []
confusion_matrixes = []
i = 0

for train, test in KFolds.split(X, Y):
    X_train, X_test, Y_train, Y_test = X[train], X[test], Y[train], Y[test]
    decisionTree.fit(X_train, Y_train)
    y_pred_prob = decisionTree.predict_proba(X_test)[:, 1]
    y_pred = decisionTree.predict(X_test)
    confusion_matrixes.append(confusion_matrix(Y_test, y_pred))
    auc_score = roc_auc_score(Y_test, y_pred_prob)
    scores.append(auc_score)
    legends.append(f'Fold {i} - AUC score: {auc_score}')
    fpr, tpr, threshold = roc_curve(Y_test, y_pred_prob)
    plt.plot(fpr, tpr)
    i += 1

plt.title('Roc Curve de Cada Iteração')
plt.legend(legends)