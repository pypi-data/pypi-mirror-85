from pad_sequences import pad_sequences_multi


def test1():
    # expected
    expected = []
    expected.append([[0, 0, 0], [1, 1, 1], [1, 1, 1]])
    expected.append([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    # padded sequence
    seq = []
    seq.append([[1, 1, 1], [1, 1, 1]])
    seq.append([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    padded = pad_sequences_multi(seq, padding='pre')
    # compare
    assert padded == expected


def test2():
    # expected
    expected = []
    expected.append([[1, 1, 1], [1, 1, 1], [0, 0, 0]])
    expected.append([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    # padded sequence
    seq = []
    seq.append([[1, 1, 1], [1, 1, 1]])
    seq.append([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    padded = pad_sequences_multi(seq, padding='post')
    # compare
    assert padded == expected


def test3():
    # expected
    expected = []
    expected.append([[7, 8, 9], [1, 1, 1], [1, 1, 1]])
    expected.append([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    # padded sequence
    seq = []
    seq.append([[1, 1, 1], [1, 1, 1]])
    seq.append([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    padded = pad_sequences_multi(seq, padding='pre', value=[7, 8, 9])
    # compare
    assert padded == expected


def test4():
    # expected
    expected = []
    expected.append([[5, 5, 5], [1, 1, 1], [1, 1, 1]])
    expected.append([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    # padded sequence
    seq = []
    seq.append([[1, 1, 1], [1, 1, 1]])
    seq.append([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    padded = pad_sequences_multi(seq, padding='pre', value=5)
    # compare
    assert padded == expected


def test5():
    # expected
    expected = []
    expected.append([[0, 0, 0], [1, 1, 1], [2, 2, 2]])
    expected.append([[2, 2, 2], [3, 3, 3], [4, 4, 4]])
    # padded sequence
    seq = []
    seq.append([[1, 1, 1], [2, 2, 2]])
    seq.append([[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4]])
    padded = pad_sequences_multi(seq, padding='pre',
                                 truncating='pre', maxlen=3)
    # compare
    assert padded == expected


def test6():
    # expected
    expected = []
    expected.append([[0, 0, 0], [1, 1, 1], [2, 2, 2]])
    expected.append([[1, 1, 1], [2, 2, 2], [3, 3, 3]])
    # padded sequence
    seq = []
    seq.append([[1, 1, 1], [2, 2, 2]])
    seq.append([[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4]])
    padded = pad_sequences_multi(seq, padding='pre',
                                 truncating='post', maxlen=3)
    # compare
    assert padded == expected


def test7():
    # expected
    expected = []
    expected.append([[1, 1, 1], [2, 2, 2], [0, 0, 0]])
    expected.append([[1, 1, 1], [2, 2, 2], [3, 3, 3]])
    # padded sequence
    seq = []
    seq.append([[1, 1, 1], [2, 2, 2]])
    seq.append([[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4]])
    padded = pad_sequences_multi(seq, padding='post',
                                 truncating='post', maxlen=3)
    # compare
    assert padded == expected
