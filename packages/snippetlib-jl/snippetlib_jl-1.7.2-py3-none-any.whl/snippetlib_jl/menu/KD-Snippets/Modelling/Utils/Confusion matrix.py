# calculate the confusion matrix between true and predicted label

predictions = clf.predict(X_test)

confusion_matrix = pd.crosstab(y_test, predictions)
confusion_matrix.columns.name = ''
confusion_matrix.index = ['predicted '+str(val) for val in confusion_matrix.columns]
confusion_matrix