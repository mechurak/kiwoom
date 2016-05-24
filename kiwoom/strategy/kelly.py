<<<<<<< HEAD
"""
-- how to maximize the profit by betting money
If we know the probability of p and q, we can decide x eventually.
What would be parameters affecting winning probability?
- # of news, # of magazines, KOSPI/KOSDAQ, other countries' indicators such as NASDAQ,
- oil price, currency, interest, theme, ...
"""
class KellyBetting:
    def __init__(self):
        print("kelly betting class")
    # basic batting
    # b : 1 + ratio ex) 1.05
    # p : winning probability
    # q : losing probability
    # x : % of total money to bet per a game
    def betting(self, totalamount, b, p, q):
        x = (b*p-q)/b

        return x*totalamount


=======
class KellyBetting:
    # basic batting
    # b : 1 + ratio ex) 1.05
    # p : winning probability
    # q : losing probability
    # x : % of total money to bet per a game
    def on_betting(self, totalamount, b, p, q):
        x = (b*p-q)/b

        return x*totalamount
>>>>>>> origin/master
