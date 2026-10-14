import random
import math

class DecisionTree:
    def __init__(self, max_depth=5):
        self.max_depth = max_depth
        self.tree = None

    def fit(self, X, y):
        self.tree = self._build_tree(X, y, 0)

    def _build_tree(self, X, y, depth):
        if not X or not y:
            return None
        
        # If all targets are the same, return a leaf
        if len(set(y)) == 1:
            return y[0]
            
        # If max depth reached, return most common target
        if depth >= self.max_depth:
            return max(set(y), key=y.count)

        best_split = self._get_best_split(X, y)
        if not best_split:
            return max(set(y), key=y.count)

        left_X, left_y, right_X, right_y, feature_idx, threshold = best_split
        
        left_branch = self._build_tree(left_X, left_y, depth + 1)
        right_branch = self._build_tree(right_X, right_y, depth + 1)
        
        return {
            'feature_idx': feature_idx,
            'threshold': threshold,
            'left': left_branch,
            'right': right_branch
        }

    def _get_best_split(self, X, y):
        best_gini = 1.0
        best_split = None
        num_features = len(X[0])
        
        for feature_idx in range(num_features):
            # Try splitting on all unique values
            thresholds = set(row[feature_idx] for row in X)
            for threshold in thresholds:
                left_X, left_y, right_X, right_y = [], [], [], []
                for i in range(len(X)):
                    if X[i][feature_idx] <= threshold:
                        left_X.append(X[i])
                        left_y.append(y[i])
                    else:
                        right_X.append(X[i])
                        right_y.append(y[i])
                        
                if not left_y or not right_y:
                    continue
                    
                gini = self._calculate_gini(left_y, right_y)
                if gini < best_gini:
                    best_gini = gini
                    best_split = (left_X, left_y, right_X, right_y, feature_idx, threshold)
                    
        return best_split

    def _calculate_gini(self, left_y, right_y):
        total = len(left_y) + len(right_y)
        
        def gini_impurity(group):
            size = len(group)
            if size == 0:
                return 0
            score = 0.0
            classes = set(group)
            for c in classes:
                p = group.count(c) / size
                score += p * p
            return 1.0 - score
            
        return (len(left_y)/total) * gini_impurity(left_y) + (len(right_y)/total) * gini_impurity(right_y)

    def predict_one(self, x, tree):
        if not isinstance(tree, dict):
            return tree
        
        if x[tree['feature_idx']] <= tree['threshold']:
            return self.predict_one(x, tree['left'])
        else:
            return self.predict_one(x, tree['right'])

    def predict(self, X):
        return [self.predict_one(x, self.tree) for x in X]


class PureRandomForestClassifier:
    def __init__(self, n_estimators=10, max_depth=5, max_features=None):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.max_features = max_features
        self.trees = []

    def fit(self, X, y):
        self.trees = []
        n_samples = len(X)
        for _ in range(self.n_estimators):
            # Bootstrap sampling
            indices = [random.randint(0, n_samples - 1) for _ in range(n_samples)]
            X_sample = [X[i] for i in indices]
            y_sample = [y[i] for i in indices]
            
            tree = DecisionTree(max_depth=self.max_depth)
            tree.fit(X_sample, y_sample)
            self.trees.append(tree)

    def predict(self, X):
        predictions = []
        for x in X:
            tree_preds = [tree.predict_one(x, tree.tree) for tree in self.trees]
            # Majority vote
            majority = max(set(tree_preds), key=tree_preds.count)
            predictions.append(majority)
        return predictions

    def predict_proba(self, X):
        probs = []
        for x in X:
            tree_preds = [tree.predict_one(x, tree.tree) for tree in self.trees]
            # Calculate probability for class 1
            prob_1 = tree_preds.count(1) / len(tree_preds)
            probs.append([1 - prob_1, prob_1])
        return probs
