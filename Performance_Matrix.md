# Confusion matrix

from sklearn.metrics import confusion_matrix
matrix=confusion_matrix(y_test, prediction,labels=[1,0])
cm=pd.DataFrame(matrix,index=['positive','negative'],columns=['positive','negative'])
print(cm)

## Output
-------------------------------------------------
             positive   negative
positive       346        84
negative         0      1830
---------------------------------------------------

# Calculate Accuracy
from sklearn.metrics import accuracy_score
acc = accuracy_score(y_test,prediction)
print('Accuracy: ',acc)

# Calculate Recall
from sklearn.metrics import recall_score
recall= recall_score(y_test, prediction)
print('Recall: ',recall)

# Calculate Precision
from sklearn.metrics import precision_score
precision= precision_score(y_test, prediction)
print('Precision: ',precision)

## Output:
Accuracy:  0.9628318584070796
Recall:  0.8046511627906977
Precision:  1.0

# F1 Score
from sklearn.metrics import f1_score
f1score= f1_score(y_test,prediction)
print("F1 Score: ",f1score)

## Output:
F1 Score:  0.8917525773195877

# Calculate AUC 
from sklearn.metrics import roc_curve, auc
fpr, tpr, treshold = roc_curve(y_test, prediction)
roc_auc = auc(fpr, tpr)
print("AUC: ",roc_auc)

## Output:
AUC:  0.9023255813953488

# Plotting AUC
import matplotlib.pyplot as plt
plt.subplots(1, figsize=(5,5))
plt.plot(fpr, tpr)
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()
