# def poker(hands):
#     scores = [(i, score(hand.split())) for i, hand in enumerate(hands)]
#     print(scores)
#     winner = sorted(scores , key=lambda x:x[1])[-1][0]
#     return hands[winner]
#
# def score(hand):
#     ranks = '23456789TJQKA'
#     rcounts = {ranks.find(r): ''.join(hand).count(r) for r, _ in hand}.items()
#     score, ranks = zip(*sorted((cnt, rank) for rank, cnt in rcounts)[::-1])
#     if len(score) == 5:
#         if ranks[0:2] == (12, 3): #adjust if 5 high straight
#             ranks = (3, 2, 1, 0, -1)
#         straight = ranks[0] - ranks[4] == 4
#         flush = len({suit for _, suit in hand}) == 1
#         '''no pair, straight, flush, or straight flush'''
#         score = ([1, (3,1,1,1)], [(3,1,1,2), (5,)])[flush][straight]
#     return score, ranks
#
# poker(['8C TS KC 9H 4S', '7D 2S 5D 3S AC', '8C AD 8D AC 9C', '7C 5H 8D TD KS'])
#  # '8C AD 8D AC 9C'
#
#

mk=[[2, 3.8, 18.2], [1, 3.5, 52], [0, 3.45, 2.59]]
winner = sorted(mk , key=lambda x:x[0])
print(winner)