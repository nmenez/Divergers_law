import random
from collections import Counter, deque
from string import ascii_uppercase


class PoliticalEntity:
    ''' positions are modeled as uniform variables across a N-dimensional space
        0 means complete disagreement on issue, 1 means complete agreement
        most voters are on a spectrum of agreement with a position
    '''

    def __init__(self, dimensions=10):
        self.positions = [random.random() for _ in range(dimensions)]

    def __repr__(self):
        return ','.join('%0.2f' % p for p in self.positions)


class Party(PoliticalEntity):
    def __init__(self, name):
        super().__init__()
        self.name = name
        # model party positions as simple 0,1 across positions.
        # like yes or no on abortion.  If we didn't do this then
        # we'd find that whichever party is closest
        # to the middle will get all the votes
        self.positions = [round(p) for p in self.positions]

    def __repr__(self):
        return '%s' % self.name

    def dropout(self):
        del self


class Voter(PoliticalEntity):
    def __init__(self, change_mind):
        super().__init__()
        self.change_mind = change_mind
        self.votes = []

    def vote(self, parties):
        '''
            voter will vote for party that most represents his views.
            this is modeled as the euclidean distance on the political
            positions space
        '''
        # voter might change their mind on positions from cycle to cycle
        self.positions = [p + random.choice([self.change_mind, -1 *
                                             self.change_mind, 0])
                          for p in self.positions]
        party_diff = []
        for party in parties:
            diff = sum(abs(p1 - p2)**2 for p1,
                       p2 in zip(self.positions, party.positions))**(1 / 2)
            party_diff.append((party.name, diff))
            
        return min(party_diff, key=lambda p: p[1])[0]


class District:
    # first pass the post district
    def __init__(self, pop, voter_change_mind=0.1):
        self.voters = [Voter(change_mind=voter_change_mind)
                       for _ in range(pop)]
        self.rep = ''

    def election(self, parties):
        results = Counter([voter.vote(parties) for voter in self.voters])
        # rep =
        # self.rep = rep
        return results


def Election_cycle(parties, districts, type='FPTP'):
    ballots = [district.election(parties) for district in districts]

    if type == 'FPTP':
        reps = [max([(party, votes) for party, votes in results.items()],
                    key=lambda x: x[1])[0] for results in ballots]

        congress = Counter(reps)
    return congress


def simulate(party_count, districts_count, rounds,
             give_up_seats=10, voter_change_mind=0.2):
    records = deque([('', ''), ('', '')], maxlen=2)
    parties = [Party(L) for L in ascii_uppercase[:party_count]]
    districts = [District(100, voter_change_mind=voter_change_mind)
                 for _ in range(districts_count)]
    for _ in range(rounds):
        this_congress = Election_cycle(parties, districts)
        worst = [party.name for party in parties
                 if (party.name not in this_congress) or
                 this_congress[party.name] <= give_up_seats]
        records.append(worst)
        if len(parties) > 2:
            for i, party in enumerate(parties):
                if (party.name in records[0]) and (party.name in records[1]):
                    del parties[i]

        print('congress:', this_congress)


party_count = 10
N = 100
rounds = 100
simulate(party_count, N, rounds)
