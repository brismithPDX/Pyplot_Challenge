import pandas
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def clean_data(input_file, output_file):
    gcdata = pandas.read_excel(input_file, header=0, usecols='c:f')
    gcdata.to_csv(output_file, encoding='utf-8', index=False, header=0)


def convert_date_stamp(date):
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]

    iso_date = year + '-' + month + '-' + day

    return iso_date


def fix_time_format(input_file):

    data = []

    file = open(input_file)
    reader = csv.DictReader(file, fieldnames=['Date', 'rainfall', 'snowpack', 'snowfall'])
    for line in reader:
        date = convert_date_stamp(line['Date'])

        string = "" + date + "," + line['rainfall'] + "," + line['snowpack'] + "," + line['snowfall'] + ""
        data.append(string)

    file.close()

    file = open(input_file, "w")
    file.write("\n".join(data))
    file.close()


def plot_precipitation(input_file):
    headers = ['Date', 'Rainfall', 'Snowpack', 'Snowfall']
    df = pandas.read_csv(input_file, names=headers)

    df['Date'] = df['Date'].map(lambda x: datetime.strptime(str(x), '%Y-%m-%d'))
    x = df['Date']
    y = df['Rainfall']

    plt.plot(x, y)
    plt.gcf().autofmt_xdate()

    plt.show()


clean_data('govt_camp_2013_01_to_2016_03.xlsx', 'Output.csv')

fix_time_format("Output.csv")

plot_precipitation("Output.csv")
