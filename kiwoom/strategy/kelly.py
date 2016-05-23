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
