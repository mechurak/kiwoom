class KellyBetting:
    # basic batting
    # b : 1 + ratio ex) 1.05
    # p : winning probability
    # q : losing probability
    # x : % of total money to bet per a game
    def on_betting(self, totalamount, b, p, q):
        x = (b*p-q)/b

        return x*totalamount
