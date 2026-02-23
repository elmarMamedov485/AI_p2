# test_nqueens.py
import unittest
from solver import nQueens


def is_valid_assignment(assign):
    """Helper: assert assignment has no row or diagonal conflicts."""
    for i, a in assign.items():
        for j, b in assign.items():
            if i == j:
                continue
            # if any constraint fails, constraints_check returns False
            assert nQueens.constraints_check(i, j, a, b), f"Conflict between {i}:{a} and {j}:{b}"


def test_constraints_check_basic():
    # same row -> conflict
    assert not nQueens.constraints_check(1, 2, 3, 3)
    # same diagonal -> conflict
    assert not nQueens.constraints_check(1, 3, 1, 3)  # |1-3| == |1-3|
    # different row and not diagonal -> ok
    assert nQueens.constraints_check(1, 2, 1, 2) is False  # same row (should be False)
    assert nQueens.constraints_check(1, 2, 1, 3)  # ok


def test_ac3_presearch_domains_nonempty():
    q4 = nQueens(4)
    ok, domains = q4.AC_3_preseach()
    assert ok is True
    # domains should be subsets of original domain and non-empty
    for v, d in domains.items():
        assert len(d) > 0
        assert set(d).issubset(set(range(1, q4.n + 1)))


def test_backtracking_finds_solution_n4():
    q4 = nQueens(4)
    result = q4.backtracking_search()
    # backtracking_search should return a dict assignment on success
    assert isinstance(result, dict)
    assert len(result) == 4
    is_valid_assignment(result)


def test_min_conflicts_finds_solution_n8():
    q8 = nQueens(8)
    ok, assignment = q8.min_conflict(max_steps=5000)
    assert ok is True, "min_conflict failed to find solution within 5000 steps"
    # assignment length should be n and valid
    assert isinstance(assignment, dict)
    assert len(assignment) == 8
    is_valid_assignment(assignment)


def test_select_var_mrv_respects_domain_sizes():
    q = nQueens(4)
    # tweak domains to create a clear MRV choice
    q.domains[1] = [1, 2]
    q.domains[2] = [1]         # smallest domain -> should be chosen
    q.domains[3] = [1, 2, 3]
    q.domains[4] = [2, 3]
    q.assignment = {}
    assert q.select_var() == 2


def test_forward_checking_detects_failure_and_prunes():
    # Setup a situation where forward checking will empty a neighbor domain
    q = nQueens(3)
    # Assign variable 1 = 1 (simulate we just assigned it)
    q.assignment = {1: 1}
    q.domains = {1: [1], 2: [1], 3: [1, 2, 3]}
    inferences, new_domains = q.forward_checking(1)
    # Domain for variable 2 should become empty because only value 1 conflicts with assigned 1
    assert inferences is False
    assert isinstance(new_domains, dict)
    assert new_domains[2] == []


def test_lcv_returns_permutation_of_domain():
    q = nQueens(5)
    var = 3
    # default domains are 1..n
    lcv_list = q.lcv(var)
    # LCV should return same elements as current domain (permutation)
    assert set(lcv_list) == set(q.domains[var])
    assert len(lcv_list) == len(q.domains[var])


if __name__ == "__main__":
    unittest.main(["-q"])