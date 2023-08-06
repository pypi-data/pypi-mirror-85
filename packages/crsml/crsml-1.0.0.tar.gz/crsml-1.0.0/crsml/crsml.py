from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,confusion_matrix
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score

def run_random_forest(X_data,Y_data,test_size=0.0,model_path="rmf.pkl",n_estimators=100,random_state=0):
    clf = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)
    if test_size==0:
        clf.fit(X_data, Y_data)
        pickle.dump(clf, open(model_path, 'wb'))
        print(accuracy_score(Y_data,clf.predict(X_data)))
    else:
        X_train,X_test,y_train,y_test=train_test_split(X_data,Y_data,test_size=test_size)
        clf.fit(X_train, y_train)
        pickle.dump(clf, open(model_path, 'wb'))

        y_pred=clf.predict(X_test)
        print(y_pred)
        print(accuracy_score(y_test,y_pred))
        print(confusion_matrix(y_test,y_pred))

def search_best_random_forest(X_data,Y_data,cv=5,model_path="",params={}):
    clf = RandomForestClassifier(random_state=0)

    if len(params)==0:
        parameters = {'n_estimators': range(10, 200, 20), 'max_depth': range(5, 30, 5)}
    else:
        n_estimators=params.get("n_estimators")
        max_depth=params.get("max_depth")
        if n_estimators and max_depth and isinstance(n_estimators, list) and isinstance(max_depth, list):
            parameters = {'n_estimators': n_estimators, 'max_depth': max_depth}
        else:
            print("------params参数错误------")
            parameters = {'n_estimators': range(10, 200, 20), 'max_depth': range(5, 30, 5)}
    gsearch = GridSearchCV(estimator=clf, param_grid=parameters, scoring='accuracy', cv=cv)
    gsearch.fit(X_data, Y_data)
    print("gsearch.best_params_", gsearch.best_params_)
    print("gsearch.best_score_", gsearch.best_score_)
    print("gsearch.best_estimator_", gsearch.best_estimator_)

    gsearch.best_estimator_.fit(X_data, Y_data)
    if model_path:
        pickle.dump(clf, open(model_path, 'wb'))
    else:
        pickle.dump(clf, open(f"best_rmf_n_estimators_{gsearch.best_params_.get('n_estimators')}_max_depth_{gsearch.best_params_.get('max_depth')}.pkl", 'wb'))

def evaluate_random_forest(X_data,Y_data,cv=5,n_estimators=100,max_depth=20):
    clf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=0)
    scores = cross_val_score(clf, X_data, Y_data, cv=cv, scoring='accuracy')
    print(scores)
    print(sum(scores)/cv)