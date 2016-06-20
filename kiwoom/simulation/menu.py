__author__ = 'sangchae'

class Menu:
    def menu_decide(self, test):
        print("Welcome My Master again.")
        print("Please choose what you want to do today.")
        print("1. Simulation") # yahoo api
        print("2. Start EL") # Kiwoom api
        mode = input()

        if mode == '1':
            print("Which strategy do you want to simulate?")
            print("1. Golen Gross")
            print("2. Bollinger Band")
            print("3. Envelope")

            simul = input()
            return simul
        else:
            pass
