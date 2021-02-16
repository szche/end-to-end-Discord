import pickle


def serialize(data):
    return pickle.dumps(data, protocol=4)
