from typing import Iterator

from opablt.models import Ballot, Election


def content_lines(s: str) -> Iterator[str]:
    lines = s.split("\n")
    for line in lines:
        # Ignore comments
        # FIXME: This is potentially wrong if candidate names or election titles
        # have a # in them; we should probably handle quoted strings
        line, *_ = line.split("#", 1)
        line = line.strip()
        if line:
            yield line


def strip_quotes(s: str) -> str:
    return s.removesuffix('"').removeprefix('"')


def parse_blt_string(s: str) -> Election:
    line_iter = content_lines(s)
    first_line = next(line_iter)
    n_candidates, n_seats = [int(n) for n in first_line.split()]

    withdrawn_candidate_indices: list[int] = []
    line = next(line_iter)
    if line.startswith("-"):
        # Some candidates have withdrawn. This line looks like
        # -4 -1
        withdrawn_candidate_indices = [int(n) - 1 for n in line.split("-") if n]
        line = next(line_iter)

    # Loop until end of ballots marker
    ballots: list[Ballot] = []
    while line != "0":
        ballot_iter = iter(line.split())
        weight = int(next(ballot_iter))
        ranks: list[tuple[int, ...] | None] = []
        for ballot_rank in ballot_iter:
            if ballot_rank == "0":
                break
            if ballot_rank == "-":
                ranks.append(None)
                continue
            candidates = ballot_rank.split("=")
            ranks.append(tuple(int(n) - 1 for n in candidates))
        ballots.append(Ballot(weight=weight, votes=tuple(ranks)))
        line = next(line_iter)

    candidate_names = []
    for _ in range(n_candidates):
        candidate_names.append(strip_quotes(next(line_iter)))

    election_name = strip_quotes(next(line_iter))

    return Election(
        title=election_name,
        n_seats=n_seats,
        withdrawn_candidates=tuple(withdrawn_candidate_indices),
        candidates=tuple(candidate_names),
        ballots=tuple(ballots),
    )
