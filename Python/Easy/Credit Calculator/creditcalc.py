from math import ceil, log
import argparse
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--type')
    ap.add_argument('--payment', type=int)
    ap.add_argument('--principal', type=int)
    ap.add_argument('--periods', type=int)
    ap.add_argument('--interest',type=float)
    args = ap.parse_args()
    if not args.type or not args.interest or args.interest <= 0:
        incorrect()
    interest = args.interest / 1200
    if args.type == 'diff':
        if good(args.principal) and good(args.periods) and not args.payment:
            calculate_diff(args.principal, args.periods, interest)
        else:
            incorrect()
    elif args.type == 'annuity':
        if not args.periods and good(args.payment) and good(args.principal):
            calculate_num_of_payments(args.payment, args.principal, interest)
        elif not args.payment and good(args.principal) and good(args.periods):
            calculate_annuity_payment(args.principal, args.periods, interest)
        elif not args.principal and good(args.periods) and good(args.payment):
            calculate_principal(args.periods, args.payment, interest)
        else:
            incorrect()
    else:
        incorrect()


def good(x):
    return type(x) == type(int()) and x > 0


def calculate_diff(p, n, i):
    total = 0
    for m in range(1, n + 1):
        curr = ceil(p / n + i * (p - ((p * (m - 1)) / n)))
        print(f'Month {m}: paid out {curr}')
        total += curr
    print(f'\nOverpayment = {total - p}')


def incorrect():
    print('Incorrect parameters')
    sys.exit()


def calculate_annuity_payment(p, n, i):
    a = ceil(p * (i * (1 + i) ** n) / ((1 + i) ** n - 1))
    print(f'Your annuity payment = {a}!', f'Overpayment = {a * n - p}', sep='\n')


def calculate_principal(n, a, i):
    p = ceil(a / ((i * (1 + i) ** n) / ((1 + i) ** n - 1)))
    print(f'Your credit principal = {p}!', f'Overpayment = {a * n - p}', sep='\n')


def calculate_num_of_payments(a, p, i):
    n = ceil(log(a / (a - i * p), 1 + i))
    years, months = n // 12, n % 12
    s, null = 's', ''
    print(f"You need {(f'{years} year{s if years > 1 else null} ' if years else '')}{'and ' if years and months else ''}{f'{months} month{s if months > 1 else null} ' if months else ''}to repay this credit!")
    print(f'Overpayment = {a * n - p}')


if __name__ == '__main__':
    main()
