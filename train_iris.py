from sklearn.datasets import load_iris  # [web:33]
from sklearn.model_selection import train_test_split  # [web:36]
from sklearn.ensemble import RandomForestClassifier  # [web:36]
import joblib

iris = load_iris()
X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

joblib.dump(clf, "model.joblib")