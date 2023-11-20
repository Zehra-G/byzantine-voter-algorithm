'''
This is an initial implementation of the Byzantine voter resistant ranking profile algorithm of:

Melnyk, Darya, Yuyi Wang, and Roger Wattenhofer. "Byzantine preferential voting."
International Conference on Web and Internet Economics. Cham: Springer International
Publishing, 2018.

Zehra Gundogdu & Colin Huh
CS381 FA23 Final Project
Check In 1

'''

from collections import defaultdict
import random

class Node:
    def __init__(self, node_id, total_nodes):
        
        #ID for individual node
        self.node_id = node_id
        #Number of total nodes 
        self.total_nodes = total_nodes
        #Rankings for the individual node
        self.rankings = None
        self.fixed_pairs = set()


    def rankings(self,canidatesnum ):
        #This function determines the rankings for all the nodes

        #Empty list of the prefrences of the node 
        prefrences = []
        
        #Create a list of all the canidates
        for i in range(canidatesnum):
            prefrences.append(i)
        #Create a random ordering of the canidates for each node
        for i in range(canidatesnum):
            self.rankings.append(random.choice(prefrences))
        return self.rankings

        

        

    def broadcast_ranking(self):
        return self.rankings

    def propose_pairs(self, rankings):
        proposals = set()
        for i in range(len(rankings)):
            for j in range(i + 1, len(rankings)):
                ci, cj = rankings[i], rankings[j]
                if self.count_rankings_above(ci, cj) >= self.total_nodes - self.threshold:
                    proposals.add((ci, cj))
        return proposals

    def count_rankings_above(self, ci, cj):
        count = 0
        for ranking in self.rankings:
            if ranking.index(ci) < ranking.index(cj):
                count += 1
        return count

    def receive_proposal(self, proposals):
        received_proposals = defaultdict(int)
        for proposal in proposals:
            received_proposals[proposal] += 1

        for proposal, count in received_proposals.items():
            if count >= self.threshold + 1:
                self.fix_pair(proposal)

    def fix_pair(self, pair):
        self.fixed_pairs.add(pair)
        # Adjust own ranking to satisfy fixed pairs (not implemented in this example)

    def broadcast_fixed_pairs(self):
        return self.fixed_pairs

    def dictator_phase(self, dictator_ranking):
        # Dictator suggests its own ranking during Dictator Phase
        if self.is_correct_node():
            self.rankings = dictator_ranking

    def is_correct_node(self):
        # Simulating a check for correctness (replace with actual implementation)
        return random.choice([True, False])

    def decision_phase(self, dictator_ranking):
        if all(pair in self.fixed_pairs for pair in dictator_ranking):
            self.rankings = dictator_ranking

class Algorithm:

    def __init__(self,numcanidates):

        self.numcanidates = numcanidates



    def determine_rankings(self,nodes):
        #Nodes is a list of all nodes that we are running the algorithm on
        
        for i in range(len(nodes)):
            node = nodes[i]
            node.rankings(self.numcanidates)


    def consensus_algorithm(nodes, rounds):
        for round_number in range(rounds):
            # Select t + 1 different nodes as dictators for the round
            round_dictators = random.sample(nodes, len(nodes[0].fixed_pairs) + 1)

            for node in nodes:
            # Communication Phase
                node.broadcast_ranking()
                proposals = node.propose_pairs(node.rankings)
                node.receive_proposal(proposals)

            # Dictator Phase
                dictator_ranking = round_dictators[round_number].broadcast_ranking()
                node.dictator_phase(dictator_ranking)

            # Decision Phase
                node.decision_phase(dictator_ranking)

        return [node.rankings for node in nodes]
