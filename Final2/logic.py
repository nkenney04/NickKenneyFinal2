from PyQt6.QtWidgets import *
from gui import *
import csv
import re

class Logic(QMainWindow,Ui_LawnCare):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.prices_button.clicked.connect(lambda : self.prices())
        self.signup_button.clicked.connect(lambda : self.signup())
        self.revenuebutton.clicked.connect(lambda : self.revenue())
        self.clients_button.clicked.connect(lambda : self.display_clients())


    def prices(self):
        self.output_box.clear()
        self.error_msg.clear()
        global name
        global address
        global sqfootage
        global mow_price
        global seed_price
        global fert_price
        global aeration_price
        global total_price

        sqft_str = self.sqft_input.text()
        name = self.name_input.text()
        strip_name = name.replace(' ', '')
        address = self.address_input.text()
        try:
            '''This is all exception handling.'''
            if name == '':
                raise ValueError('Name Required')
            elif not strip_name.isalpha():
                raise ValueError('Name must only contain letters.')
            elif len(name) < 3:
                raise ValueError('Name must have at least 3 letters.')
            elif not bool(re.search(' .', name)):
                raise ValueError('Name must at least contain a last initial.')
            elif address == '':
                raise ValueError('Address required')
            elif len(address) <= 8:
                raise ValueError('Please Enter Valid Address')
            elif not bool(re.search('[A-Za-z]', address) and bool(re.search('[1-9]', address))):
                raise ValueError('Please Enter Valid Address')
            elif sqft_str == '':
                raise ValueError('Square Footage required')
            elif sqft_str.isdigit() and int(sqft_str) <= 0:
                raise ValueError('Square footage must be greater than 0')
            elif not sqft_str.isdigit():
                raise ValueError('Square footage must be numeric')
            else:
                '''This else statement decides the price for each service based on 
                square footage and then sends it to the gui output.
                '''
                sqfootage = int(sqft_str)
                if 0 < sqfootage <= 5000:
                    mow_price = 35.00
                    seed_price = 40.00
                    fert_price = 45.00
                    aeration_price = 75.00
                    total_price = mow_price + seed_price + fert_price + aeration_price
                    self.output_box.setText(f'Mowing: ${mow_price:.2f}\nOverseeding: ${seed_price:.2f}\nFertilling: ${fert_price:.2f}\nAeration: ${aeration_price:.2f}\nTotal: ${total_price:.2f}')
                    self.signup_button.setEnabled(True)
                    self.radio_fert.setEnabled(True)
                    self.radio_mowing.setEnabled(True)
                    self.radio_aeration.setEnabled(True)
                    self.radio_overseeding.setEnabled(True)
                elif 20000 >= sqfootage > 5000:
                    mow_price = (((sqfootage - 5000) // 1000) * 3) + 35
                    seed_price = (((sqfootage - 5000) // 1000) * 5) + 40
                    fert_price = (((sqfootage - 5000) // 1000) * 5) + 45
                    aeration_price = (((sqfootage - 5000) // 1000) * 14) + 75
                    total_price = mow_price + seed_price + fert_price + aeration_price
                    self.output_box.setText(f'Mowing: ${mow_price:.2f}\nOverseeding: ${seed_price:.2f}\nFertilling: ${fert_price:.2f}\nAeration: ${aeration_price:.2f}\nTotal: ${total_price:.2f}')
                    self.signup_button.setEnabled(True)
                    self.radio_fert.setEnabled(True)
                    self.radio_mowing.setEnabled(True)
                    self.radio_aeration.setEnabled(True)
                    self.radio_overseeding.setEnabled(True)


                elif sqfootage > 20000:
                    self.output_box.setText('Thank you for reaching out!\nUnfortunately your yard is too big for us to service!')
                else:
                    raise ValueError('Unknown error.')
        except ValueError as e:
            self.error_msg.setText(f'Invalid:{e}')

    def signup(self):
        '''
        This function checks for what services have been selected and then
        sends thme to the CSV'''
        try:
            customer_file = open('customers.csv', 'r')
            csv_reader = csv.reader(customer_file)
            for row in csv_reader:
                if address == row[1]:
                    raise ValueError('Customer already in system!')
            if self.radio_mowing.isChecked():
                mowing_data = mow_price
            else:
                mowing_data = 'N/A'
            if self.radio_fert.isChecked():
                fertilizer_data = fert_price
            else:
                fertilizer_data = 'N/A'
            if self.radio_overseeding.isChecked():
                seeding_data = seed_price
            else:
                seeding_data = 'N/A'
            if self.radio_aeration.isChecked():
                aeration_data = aeration_price
            else:
                aeration_data = 'N/A'
            self.output_box.setText('Thank you for signing up!')
            customer_file = open('customers.csv', 'a')
            csv_writer = csv.writer(customer_file)
            csv_writer.writerow([name, address, sqfootage, mowing_data, fertilizer_data, seeding_data, aeration_data])
            self.clients_button.setEnabled(True)
            self.revenuebutton.setEnabled(True)
        except ValueError as e:
            self.output_box.setText(f'{e}')

    def display_clients(self):
        '''Reads csv file and sends client names to the GUI'''
        customer_file = open('customers.csv', 'r')
        csv_reader = csv.reader(customer_file)
        new_clients = ''
        reversed_list = list(csv_reader)
        for row in reversed(reversed_list):
            if row[0] != 'Name':
                new_clients = new_clients + f'{row[0]}\n'
        self.output_box.setText(new_clients)

    def revenue(self):
        ''' Reads from csv file and sends service revenues to the GUI'''
        customer_file = open('customers.csv', 'r')
        csv_reader = csv.reader(customer_file)
        total_mowing = 0
        total_fert = 0
        total_aeration = 0
        total_seed = 0
        for row in csv_reader:
            if row[3] != 'N/A' and row [3]!= 'Mowing':
                total_mowing = total_mowing + float(row[3])
            if row[4] != 'N/A' and row[4] != 'Overseeding':
                total_seed = total_seed + float(row[4])
            if row[5] != 'N/A' and row[5] != 'Fertilizer':
                total_fert = total_fert + float(row[5])
            if row[6] != 'N/A' and row [6] != 'Aeration':
                total_aeration = total_aeration + float(row[6])
        self.output_box.setText(f'Mowing Revenue per week: ${total_mowing:.2f}\nOverseeding Revenue per application: ${total_seed:.2f}\nFertilizer Revenue per application: ${total_fert:.2f}\nAeration Revenue per service: ${total_aeration:.2f}')

