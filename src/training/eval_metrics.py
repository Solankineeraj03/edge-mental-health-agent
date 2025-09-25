from sklearn.metrics import accuracy_score, precision_recall_fscore_support

def classification_report(y_true, y_pred, average="binary"):
    acc = accuracy_score(y_true, y_pred)
    p, r, f1, _ = precision_recall_fscore_support(y_true, y_pred, average=average)
    return {"accuracy": acc, "precision": p, "recall": r, "f1": f1}