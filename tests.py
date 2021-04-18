from puzzle import Puzzle

p = Puzzle([
    (1, 0),
    (2, 1),
    (3, 3),
    (4, 2)
])

def assert_conntent_equal(L1, L2):
    assert len(L1) == len(L2) and sorted(L1) == sorted(L2)

def assert_encode_decode(i, v):
    id, value = p.decode_cell(p.encode_cell(i, v))
    assert id == i
    assert value == v

def test_neighbor():
    assert_conntent_equal(p.get_neighbors_ids(1), [2, 3])
    assert_conntent_equal(p.get_neighbors_ids(2), [1, 4])
    assert_conntent_equal(p.get_neighbors_ids(3), [1, 4])
    assert_conntent_equal(p.get_neighbors_ids(4), [2, 3])


def test_cell_is_empty():
    assert_conntent_equal(p.cell_is_not_empty(1), [1, 2, 3, 4])
    assert_conntent_equal(p.cell_is_not_empty(2), [5, 6, 7, 8])
    assert_conntent_equal(p.cell_is_not_empty(3), [9, 10, 11, 12])
    assert_conntent_equal(p.cell_is_not_empty(4), [13, 14, 15, 16])

def test_equal_to():
    assert_conntent_equal(p.cell_is_equal_to(1, 1), [1])
    assert_conntent_equal(p.cell_is_equal_to(1, 2), [2])
    assert_conntent_equal(p.cell_is_equal_to(1, 3), [3])
    assert_conntent_equal(p.cell_is_equal_to(1, 4), [4])

    assert_conntent_equal(p.cell_is_equal_to(2, 1), [5])
    assert_conntent_equal(p.cell_is_equal_to(2, 2), [6])
    assert_conntent_equal(p.cell_is_equal_to(2, 3), [7])
    assert_conntent_equal(p.cell_is_equal_to(2, 4), [8])
    
    assert_conntent_equal(p.cell_is_equal_to(3, 1), [9])
    assert_conntent_equal(p.cell_is_equal_to(3, 2), [10])
    assert_conntent_equal(p.cell_is_equal_to(3, 3), [11])
    assert_conntent_equal(p.cell_is_equal_to(3, 4), [12])

    assert_conntent_equal(p.cell_is_equal_to(4, 1), [13])
    assert_conntent_equal(p.cell_is_equal_to(4, 2), [14])
    assert_conntent_equal(p.cell_is_equal_to(4, 3), [15])
    assert_conntent_equal(p.cell_is_equal_to(4, 4), [16])

def test_get_value():
    assert p.get_cell_value(1) == 0
    assert p.get_cell_value(2) == 1
    assert p.get_cell_value(3) == 3
    assert p.get_cell_value(4) == 2

def test_encode_decode():
    assert_encode_decode(1, 1)
    assert_encode_decode(1, 2)
    assert_encode_decode(1, 3)
    assert_encode_decode(1, 4)

    assert_encode_decode(2, 1)
    assert_encode_decode(2, 2)
    assert_encode_decode(2, 3)
    assert_encode_decode(2, 4)

    assert_encode_decode(3, 1)
    assert_encode_decode(3, 2)
    assert_encode_decode(3, 3)
    assert_encode_decode(3, 4)

    assert_encode_decode(4, 1)
    assert_encode_decode(4, 2)
    assert_encode_decode(4, 3)
    assert_encode_decode(4, 4)