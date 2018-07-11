import random


def pick_winner(raffle_slots, total_slots):
    """Picks a winner from a list of raffle slots and with the total number of
    slots.

    :param raffle_slots: The raffle slots to pick a winner from
    :type raffle_slots: list[object]
    :param total_slots: The total number of slots in the pool of raffle slots
    :type total_slots: int.
    :returns: object|None -- The winning raffle slot record. None if there are
    no winners.
    """
    if total_slots == 0:
        return None

    threshold = random.randint(1, total_slots)
    cum_sum = 0
    for raffle_slot in raffle_slots:
        cum_sum += raffle_slot.slots

        if threshold <= cum_sum:
            return raffle_slot
