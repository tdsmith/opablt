import attr


@attr.frozen
class Ballot:
    weight: int
    votes: tuple[tuple[int, ...] | None, ...]


@attr.frozen
class Election:
    title: str
    n_seats: int
    withdrawn_candidates: tuple[int, ...]
    candidates: tuple[str, ...]
    ballots: tuple[Ballot, ...]
