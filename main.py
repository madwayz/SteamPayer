import pyqiwi
from config import TOKEN


class SteamPayer(object):
    def __init__(self, token):
        self.steam_form_id = 25549
        self.token = token
        self.wallet = None
        self.logins_list = self._get_logins_list()
        self.amount = 0

    def auth(self):
        self.wallet = pyqiwi.Wallet(token=self.token)
        self._get_wallet()

    def broadcast_pay(self):
        for account in self.logins_list:
            if not self._is_amount_valid():
                print(f'ОШИБКА. Для оплаты допустимо не менее {self.get_min_amount()} рублей на аккаунт'
                      f' и {self.get_min_balance()} рублей на счету')
                return

            self.wallet.send(pid=self.steam_form_id,
                                        amount=amount,
                                        comment='Отправлено с помощью SteamPayer',
                                        recipient=account)

            print(f'[{account}] Провожу оплату на сумму {amount} рублей.')

    def set_amount(self, amount):
        self.amount = abs(amount)

    def _get_wallet(self):
        print('='*12 + 'SteamPayer' + '='*12)
        for account in self.wallet.accounts:
            alias = account.alias.split('_')[-1].upper()
            balance = account.balance.get("amount")

            print(f'{alias} | Остаток на счёте: {balance}')

        print('='*34 + '\n')

    @staticmethod
    def _get_logins_list():
        with open('accounts.txt', 'r') as f:
            return [line.strip('\n') for line in f.readlines()]

    def get_min_balance(self):
        return self.count_logins() * 10

    def get_min_amount(self):
        return int(self.get_min_balance() / self.count_logins())

    def count_logins(self):
        return len(self.logins_list)

    def count_accounts(self):
        return len(self.wallet.accounts)

    def _is_have_money(self):
        for account in self.wallet.accounts:
            balance = account.balance.get("amount")
            accept_status = balance >= self.amount
            return accept_status

    def _is_amount_valid(self):
        return self.amount >= self.get_min_amount() and self._is_have_money()


if __name__ == '__main__':
    payer = SteamPayer(TOKEN)
    payer.auth()

    msg = f'Введите сумму (от {payer.get_min_amount()} рублей) для оплаты на аккаунты: '
    amount = float(input(msg))

    payer.set_amount(amount)
    payer.broadcast_pay()
