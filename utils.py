import pickle, hashlib


def serialize(data):
    return pickle.dumps(data, protocol=4)

#SHA-256 of a data
def sha256(data):
    return hashlib.sha256( serialize(data) ).hexdigest()


if __name__ == "__main__":
    test = ['abc', 'cdf', 'ebc']
    assert sha256(test) == '22910a031de59d4f4b48b868c64cac76d1353ec5474c31be3430182f9df52aa5'
