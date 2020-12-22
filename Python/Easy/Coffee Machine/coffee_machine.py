# Write your code here
BUY = 'buy'
FILL = 'fill'
TAKE = 'take'
REMAINING = 'remaining'
BACK = 'back'
EXIT = 'exit'

# states
CMD = 0
COFFEE = 1
FILL_WATER = 2
FILL_MILK = 3
FILL_BEANS = 4
FILL_CUPS = 5

WATER = 'water'
MILK = 'milk'
BEANS = 'coffee beans'
CUPS = 'cups'
MONEY = 'money'

STARTING_WATER = 400
STARTING_MILK = 540
STARTING_BEANS = 120
STARTING_CUPS = 9
STARTING_MONEY = 550

ESPRESSO = 1
LATTE = 2
CAPPUCCINO = 3

COSTS_TYPES = (WATER, MILK, BEANS)
COFFEE_COSTS = {ESPRESSO: {WATER: 250, MILK: 0, BEANS: 16, MONEY: 4},
                LATTE: {WATER: 350, MILK: 75, BEANS: 20, MONEY: 7},
                CAPPUCCINO: {WATER: 200, MILK: 100, BEANS: 12, MONEY: 6}}


def main():
    cm = CoffeeMachine({WATER: STARTING_WATER, MILK: STARTING_MILK, BEANS: STARTING_BEANS, CUPS: STARTING_CUPS,
                        MONEY: STARTING_MONEY})

    action = input('Write action (buy, fill, take, remaining, exit):\n')
    while action != EXIT:
        cm.handle_input(action)
        action = input()


class CoffeeMachine:

    def __init__(self, start_content: dict):
        self.content = start_content
        self.state = CMD

    def handle_input(self, cmd):
        if self.state == CMD:
            if cmd == BUY:
                self.state = COFFEE
                print('\nWhat do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:')
            elif cmd == FILL:
                self.state = FILL_WATER
                print('\nWrite how many ml of water do you want to add:')
            elif cmd == TAKE:
                self.take()
            elif cmd == REMAINING:
                self.remaining()
        elif self.state == COFFEE:
            self.buy(cmd)
        else:
            self.fill(cmd)

    def buy(self, cmd):
        self.state = CMD
        if cmd == BACK:
            return
        option = int(cmd)
        for cost in COSTS_TYPES:
            if COFFEE_COSTS[option][cost] > self.content[cost]:
                print(f'Sorry, not enough {cost}!')
                return
        print('I have enough resources, making you a coffee!')
        for cost in COSTS_TYPES:
            self.content[cost] -= COFFEE_COSTS[option][cost]
        self.content[CUPS] -= 1
        self.content[MONEY] += COFFEE_COSTS[option][MONEY]
        print('\nWrite action (buy, fill, take, remaining, exit):')

    def fill(self, cmd):
        amount = int(cmd)
        if self.state == FILL_WATER:
            self.content[WATER] += amount
            self.state = FILL_MILK
            print('Write how many ml of milk do you want to add:')
        elif self.state == FILL_MILK:
            self.content[MILK] += amount
            self.state = FILL_BEANS
            print('Write how many grams of coffee do you want to add:')
        elif self.state == FILL_BEANS:
            self.content[BEANS] += amount
            self.state = FILL_CUPS
            print('Write how many disposable cups of coffee do you want to add:')
        elif self.state == FILL_CUPS:
            self.content[CUPS] += amount
            self.state = CMD

    def take(self):
        print(f'I gave you ${self.content[MONEY]}')
        self.content[MONEY] = 0

    def remaining(self):
        self.print_info()
        print('\nWrite action (buy, fill, take, remaining, exit):')

    def print_info(self):
        print(f"""\nThe coffee machine has:
{self.content[WATER]} of water
{self.content[MILK]} of milk
{self.content[BEANS]} of coffee beans
{self.content[CUPS]} of disposable cups
{self.content[MONEY]} of money""")


if __name__ == '__main__':
    main()
