"""File to generate sample data for testing."""
from datetime import date, timedelta, datetime
import random
import math
import pandas as pd
import numpy as np


#Initialization of variables to be used
days = 90
amplitude = 20
displacement = 50
noise = 0.4
day = date.today().day
month = date.today().month
year = date.today().year

if month == 1:
    year = year - 1
    month = 12

last_month_date = date(year, month -1, day)
last_week_date = date.today() - timedelta(days = 7)
last_year_date = date.today() - timedelta(days = 365)

next_year_date=date.today() +timedelta(days = 365)
next_month_date = date.today()+timedelta(days=30)
next_week_date = date.today() + timedelta(days = 7)



adequacy_list=["Sat","Insat_P","Insat_NP"]##### This referes to Satisfactory/Instatisfactory and Processed Not processed
choices = ['True positive', 'False positive', 'False negative', 'True negative']
value_sign=["Positive","Negative"]
sensitivity_list=["Sensitivity Conventional", "Sensitivity Liquid based","Sensitivity all types"]

###################

genotype_list=["HPV 16","HPV 31","HPV 18","HPV 35"]
type_list=["Liquid based","Conventional"]
results_list = ['Negative', 'ASC-US', 'ASC-H', 'LSIL', 'SCC']
tree_values = [100, 40, 60, 30, 30]
tree_labels = ["Satisfactory","Yes", "No", "Processed", "Not Processed"]
tree_parents = ["", "Satisfactory", "Satisfactory", "No", "No"]

##############  DAYS OF THE WEEK
def week_day(n):
    days_of_the_week=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    return days_of_the_week[n%7]

