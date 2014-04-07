#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
    import_csv.py
    ~~~~~~~~~~~~~~~~~~~~
    
    Import csv file into database.
    
    The CSV file should be in this format:

    Datetime;price;quantity;mileage
    2013/10/03 07:00:00;34.01;25.90;149340

    :copyright: (c) 2014 by Patrick Rabu.
    :license: GPL-3, see LICENSE for more details.    
"""

import sys
import time
import datetime
import locale
import csv
import sqlite3

csvfile = sys.argv[1]
db = sqlite3.connect(sys.argv[2])
car_id = sys.argv[3]

cursor = db.cursor()

with open(csvfile, 'rb') as f:
    locale.setlocale(locale.LC_ALL, 'fra_fra')
    
    reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
    reader.next() # Skip the first row
    for row in reader:
        dt = datetime.datetime.strptime(row[0], "%Y/%m/%d %H:%M:%S")
        price = locale.atof(row[1])
        quantity = locale.atof(row[2])
        mileage = locale.atoi(row[3])

        cursor.execute('''insert into refills(datetime, quantity, price, mileage, car_id) 
            values (?, ?, ?, ?, ?)''', (dt, quantity, price, mileage, car_id))
                        
        db.commit()

db.close()
