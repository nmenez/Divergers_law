# Divergers_law
In political science, Duverger's law holds that plurality-rule elections (such as first past the post) structured within single-member districts tend to favor a two-party system and that "the double ballot majority system and proportional representation tend to favor multipartism."  This is my attempt at modeling this law
 
 this is a basic simulation where congress is composed of districts that send one representative.  The representative is the party member that has a pluarity of votes.
 If a party gets less than give_up_seats seats over two election cycles the party ceases to exist and its voters then vote for the next party that represent their views.
 
 Poltical positions are modeled as an N-space where each dimension represents a voter's agreement with a party.  0 denotes complete
 disagreement while 1 represents complete agreement.  How close a party's position to a voter's views is represented by the euclidean distance. 
 
 Voters have a change_mind parameter that allows the voter to change their mind on an issue from election to election. 
