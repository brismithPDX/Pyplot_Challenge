import pandas
import csv
from datetime import datetime
import matplotlib.pyplot as plt


# Cleans the provided .xlsx file into something human readable and not shitty
def clean_data(input_file, output_file):
    gc_data = pandas.read_excel(input_file, header=0, usecols='c:f')
    gc_data.to_csv(output_file, encoding='utf-8', index=False, header=0)


# Converts file supplied date stamp string into ISO formatted date stamp string
def convert_date_stamp(date):
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]

    iso_date = year + '-' + month + '-' + day

    return iso_date


# Modifies a CSV file with non-standard date stamp string with ISO standard date stamp string
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


# Creates the required 4 year precipitation graphs for a given data field
def plot_precipitation(input_file, field, output_file):
    headers = ['Date', 'Rainfall', 'Snowpack', 'Snowfall']
    df = pandas.read_csv(input_file, names=headers)

    # Convert current date strings into python datetime data type for consumption by mathlibplot
    df['Date'] = df['Date'].map(lambda x: datetime.strptime(str(x), '%Y-%m-%d'))

    # Squeeze available date time ranges into desired date time range
    df_2013 = df[df.Date < datetime.strptime('2014-01-01', '%Y-%m-%d')]

    df_2014 = df[df.Date < datetime.strptime('2015-01-01', '%Y-%m-%d')]
    df_2014 = df_2014[df_2014.Date > datetime.strptime('2014-01-01', '%Y-%m-%d')]

    df_2015 = df[df.Date < datetime.strptime('2016-01-01', '%Y-%m-%d')]
    df_2015 = df_2015[df_2015.Date > datetime.strptime('2015-01-01', '%Y-%m-%d')]

    df_2016 = df[df.Date < datetime.strptime('2017-01-01', '%Y-%m-%d')]
    df_2016 = df_2016[df_2016.Date > datetime.strptime('2016-01-01', '%Y-%m-%d')]

    # configure 2013 plots
    x_2013 = df_2013['Date']
    y_2013 = df_2013[field]

    plt.subplot(4, 1, 1)
    plt.plot(x_2013, y_2013)
    plt.ylabel("2013")

    # configure 2014 plots
    x_2014 = df_2014['Date']
    y_2014 = df_2014[field]

    plt.subplot(4, 1, 2)
    plt.plot(x_2014, y_2014)
    plt.ylabel("2014")

    # configure 2015 plots
    x_2015 = df_2015['Date']
    y_2015 = df_2015[field]

    plt.subplot(4, 1, 3)
    plt.plot(x_2015, y_2015)
    plt.ylabel("2015")

    # configure 2016 plots
    x_2016 = df_2016['Date']
    y_2016 = df_2016[field]

    plt.subplot(4, 1, 4)
    plt.plot(x_2016, y_2016)
    plt.ylabel("2016")
    plt.xticks(rotation=45)  # added to resolve readability issues of the x-axis labels from incomplete 2016 data set

    # Create and Display all Plots for each year
    plt.suptitle(field + " in inches per year", bbox={'facecolor': 'white', 'edgecolor': 'none', 'pad': 10})
    plt.show()


# Do the required work in the required order to get required results
clean_data('govt_camp_2013_01_to_2016_03.xlsx', 'Output.csv')

fix_time_format("Output.csv")

plot_precipitation("Output.csv", 'Rainfall', 'rainfall.png')
plot_precipitation("Output.csv", 'Snowpack', 'snowpack.png')
plot_precipitation("Output.csv", "Snowfall", 'snowfall.png')
