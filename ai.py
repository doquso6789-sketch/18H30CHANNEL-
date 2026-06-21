import json
import random
from collections import Counter
from sklearn.linear_model import LogisticRegression

# ======================
def load_data():
    with open("data.json","r") as f:
        return json.load(f)

# ======================
def features(data, num):

    freq = data.count(num)

    last = len(data)
    for i in reversed(range(len(data))):
        if data[i] == num:
            last = len(data) - i
            break

    return [freq, last]

# ======================
def train():

    data = load_data()
    nums = list(set(data))

    X, y = [], []

    for i in range(len(data)):
        for n in nums:
            X.append(features(data[:i+1], n))
            y.append(1 if n == data[i] else 0)

    model = LogisticRegression(max_iter=200)
    model.fit(X, y)

    return model, data

# ======================
def predict(model, data):

    nums = list(set(data))
    scores = {}

    for n in nums:
        prob = model.predict_proba([features(data, n)])[0][1]
        scores[n] = prob

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    hot = [x[0] for x in sorted_scores[:10]]

    cold = [x[0] for x in sorted_scores[-10:]]

    bach_thu = hot[0]

    xien2 = random.sample(hot[:6], 2)
    xien3 = random.sample(hot[:10], 3)

    lo3 = [f"{random.randint(0,999):03d}" for _ in range(5)]

    special = hot[0]

    confidence = round(sorted_scores[0][1], 3)

    return {
        "hot": hot,
        "cold": cold,
        "bach_thu": bach_thu,
        "xien2": xien2,
        "xien3": xien3,
        "lo3": lo3,
        "special": special,
        "confidence": confidence
    }
