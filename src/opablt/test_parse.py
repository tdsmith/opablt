from opablt import Ballot, parse

OPAVOTE_EXAMPLE = """\
4 2          # Four candidates are competing for two seats
-2           # Bob has withdrawn
1 4 1 3 2 0  # First ballot
1 3 4 1 2 0  # Chuck first, Amy second, Diane third, Bob fourth
1 2 4 1 0    # Bob first, Amy second, Diane third
1 4 3 0      # Amy first, Chuck second
6 4 3 0      # Amy first, Chuck second with a weight of 6
1 0          # An empty ballot
1 2 - 3 0    # Bob first, no one second, Chuck third
1 2=3 1 0    # Bob and Chuck first, Diane second
1 2 3 4 1 0  # Last ballot
0            # End of ballots marker
"Diane"      # Candidate 1
"Bob"        # Candidate 2
"Chuck"      # Candidate 3
"Amy"        # Candidate 4
"Gardening Club Election"  # Title
"""


def test_parse():
    election = parse.parse_blt_string(OPAVOTE_EXAMPLE)
    assert election.n_seats == 2
    assert len(election.candidates) == 4
    assert election.withdrawn_candidates == (1,)

    assert election.ballots == (
        Ballot(1, ((3,), (0,), (2,), (1,))),
        Ballot(1, ((2,), (3,), (0,), (1,))),
        Ballot(1, ((1,), (3,), (0,))),
        Ballot(1, ((3,), (2,))),
        Ballot(6, ((3,), (2,))),
        Ballot(1, ()),
        Ballot(1, ((1,), None, (2,))),
        Ballot(1, ((1, 2), (0,))),
        Ballot(1, ((1,), (2,), (3,), (0,))),
    )

    assert election.candidates == ("Diane", "Bob", "Chuck", "Amy")
    assert election.title == "Gardening Club Election"
