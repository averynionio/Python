from state_machine import (State, Event, acts_as_state_machine, after, before, InvalidStateTransition)
import random

@acts_as_state_machine
class Process:
    checkout = State(initial=True)
    payment = State()
    pending = State()
    confirmed = State()
    canceled = State()

    paymentInfo = Event(from_states=checkout, to_state=payment)
    submitOrder = Event(from_states=payment, to_state=pending)
    passPending = Event(from_states=pending, to_state=confirmed)
    disapprove = Event(from_states=pending,to_state=checkout)
    cancel = Event(from_states=confirmed,to_state=checkout)
    back = Event(from_states=(canceled,confirmed),to_state=checkout)

    def __init__(self,name):
        self.name = name

    @after('paymentInfo')
    def doneCheckOut(self):
        print(f'{self.name} said please enter your credit card information!')

    @after('submitOrder')
    def donePayment(self):
        print(f'{self.name} received the order request and we are verifying your order.')

    @after('passPending')
    def donePending(self):
        print(f'{self.name} Congratulations, your order is now complete.')

    @after('disapprove')
    def disapproveHappend(self):
        print(f'{self.name} said sorry your order was not approved, please remove some items in your shopping cart.')

    @after('cancel')
    def doneCancel(self):
        print(f'{self.name} said sorry to hear you cancel your order, but I am glad to help.')

    @before('back')
    def doneComfird(self):
        print(f'{self.name} Alex said good to see you coming back..')

class OrderApp:
    def __init__(self, n):
        self.count = n;
        self.process = Process("Avery")

    def beginAPP(self):
        try:
            self.process.paymentInfo()
        except InvalidStateTransition as err:
            print(f'Error: {self.process.name} cannot got application in {self.process.current_state} state')

    def submitAPP(self):
        try:
            self.process.submitOrder()
            approved = random.randint(0, 9) >= 2
            if approved == True:
                try:
                    self.process.passPending()
                except InvalidStateTransition as err:
                    print(f'Error: {self.process.name} cannot got application in {self.process.current_state} state')
            else:
                self.process.disapprove()
        except InvalidStateTransition as err:
            print(f'Error: {self.process.name} cannot got application in {self.process.current_state} state')

    def cancelAPP(self):
        try:
            self.process.cancel()
        except:
            print(f'Error: {self.process.name} cannot got application in {self.process.current_state} state')

    def returnAPP(self):
        try:
            self.process.back()
        except:
            print(f'Error: {self.process.name} cannot got application in {self.process.current_state} state')

    def getCount(self):
        return self.count;

    def setCount(self, n):
        self.count = n

def state_info(process):
    print(f'state of {process.name}: {process.current_state}')

def showMenu():
    print("COMMAND MENU")
    print("begin - Begin Checkout")
    print("submit - Submit your order")
    print("cancel - Cancel my order")
    print("return - Back to Checkout")
    print("exit - Exit program")
    print()

def main():
    avery = Process("Avery")
    app = OrderApp(avery)
    showMenu()
    state_info(avery)

    while True:
        command = input("Command: ")
        if command == "begin":
            app.beginAPP()
        elif command == "submit":
            app.submitAPP()
        elif command == "cancel":
            app.cancelAPP()
        elif command == "return":
            app.returnAPP()
        elif command == "exit":
            print("Bye!")
            break
        else:
            print("Not a valid command. Please try again.\n")


if __name__ == "__main__":
    main()