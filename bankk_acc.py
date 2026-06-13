import json
import  os



class Account:
    def __init__(self,name,acc_no,pin,balance=0):
        self.name = name
        self.acc_no =  acc_no
        self.pin  = pin
        self.balance = balance
        self.transaction = []
        self.transaction.append(f'Account created with balance ${balance}')
    def deposit(self,amount):
        if amount <= 0:
            print('amount must be greater than 0')
            return False
        self.balance +=  amount
        self.transaction.append(f'Deposited: ${amount}')
        print(f'${amount} Deposited successfully. New balance ${self.balance}')
        return True
    
    def withdraw(self,amount):
        if amount <= 0:
            print('invalid amount')
            return False
        if amount > self.balance:
            print(f'Insufficient funds! Balance: ${self.balance}')
            return False
        self.balance -= amount
        self.transaction.append(f'withdrawn: ${amount}')
        print(f'{amount} withdrawn successfully. New  balance: ${self.balance}')
        return True

    def show_balance(self):
        print(f'{self.name} account balance is {self.balance}')
    
    def show_transaction(self):
         print(f'--- Passbook for  Acc {self.acc_no} - {self.name} ---')
         if len(self.transaction) == 0:
              print('No transaction yet')
              return
         for i,txn in enumerate(self.transaction, 1):
              print(f'{i}. {txn}')
         print(f'Current Balance: ${self.balance}')
         print('----------------------------------------') 
    
    def to_dict(self):
         return{
              'name': self.name,
              'acc_no': self.acc_no,
              'pin': self.pin,
              'balance': self.balance,
              'transaction': self.transaction
         }
    
    @classmethod
    def from_dict(cls,data):
         acc = cls(data['name'], data['acc_no'], data['pin'], data['balance'])
         acc.transaction = data['transaction']
         return acc

class Bank:
    def __init__(self):
        self.file_name = 'bank_data.json'
        self.accounts = {}
        self.next_acc_no = 1001
        
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, 'r') as f:
                    data = json.load(f)
                    self.next_acc_no = data.get('next_acc_no', 1001)
                    self.accounts = {int(k): Account.from_dict(v) for k, v in data.get('accounts', {}).items()}
                    print('Bank data loaded successfully')
            except:
                print('Corrupt file, starting fresh')
        else:
            print('New bank started')
    
    def create_account(self,name,pin):
       acc_no = self.next_acc_no
       self.accounts[acc_no] = Account(name, acc_no, pin)
       self.next_acc_no += 1
       print(f'Account created successfully! Your account No: {acc_no}')
       self.save_data()
       return acc_no
    
    def login(self, acc_no, pin):
     for acc in self.accounts.values():
        if acc.acc_no == acc_no:
            if acc.pin == pin:
                return acc

     print("Invalid Account No or Pin")
     return None
    
    def transfer(self,from_acc_no,pin,to_acc_no,amount):
        sender = self.login(from_acc_no,pin)
        if sender == None:
            print('Transfer failed: Sender login faild')
            return False
        recevier = None
        for acc in self.accounts.values():
            if  acc.acc_no == to_acc_no:
                recevier = acc
                break
        if recevier == None:
                print('Transfer faild: Reciver account')
                return False
        if sender.acc_no == recevier.acc_no:
                print('Transfer failed: Cannot transfer to same account')
                return False
        if sender.withdraw(amount):
                recevier.deposit(amount)
                sender.transaction.append(f'Transferred: ${amount} to Acc {to_acc_no}')
                recevier.transaction.append(f'Received: ${amount} from Acc {from_acc_no}')
                print(f'${amount} transferred successfully from {sender.name} to {recevier.name}')
                self.save_data()
                return True
        else:
                print(f'${amount} Transfer failed: Insufficient balance or invalid amount')
                return False
        
    def save_data(self):
         accounts_dict = {}
         for acc_no, account in self.accounts.items():
              accounts_dict[acc_no] = account.to_dict()

         data = {
              'accounts': accounts_dict,
              'next_acc_no': self.next_acc_no
         }
         with open(self.file_name, 'w') as f:
              json.dump(data, f, indent=4)

    def show_all_accounts(self):
         print('\n---All Bank Accounts---')
         if len(self.accounts) == 0:
              print('No  accounts in bank')
              return
         for acc in self.accounts:
              print(f'{acc.acc_no}: {acc.name} - Balance: ${acc.balance}')
         print(f'Total  Account: {len(self.accounts)}')

    def delete_account(self,acc_no,pin):
         for i, acc in enumerate(self.accounts):
              if acc.acc_no == acc_no:
                   if acc.pin == pin:
                        if acc.balance > 0:
                             print(f'Cannot delete account. Withdraw ${acc.balance} first')
                             return False
                        deleted_acc  = self.accounts[i]
                        self.accounts.pop(i)
                        print(f'Account {deleted_acc.acc_no} - {deleted_acc.name} deleted successfully ')
                        return True
                   else:
                        print('Invalid PIN. Account deletion failed')
                        return False
         print('Acount not found')
         return False
    
sbi = Bank()
nitin_acc_num = sbi.create_account('Nitin', '1111')
himanshi_acc_num = sbi.create_account('Himanshi', '2222')

sbi.login(nitin_acc_num, '1111').deposit(10000)
sbi.transfer(nitin_acc_num, '1111', himanshi_acc_num, 3000)
sbi.login(nitin_acc_num, '1111').withdraw(2000)


print('\n--- Nitin ki Passbook ---')
sbi.login(nitin_acc_num, '1111').show_transaction()

print('\n--- Himanshi ki Passbook ---')
sbi.login(himanshi_acc_num, '2222').show_transaction()