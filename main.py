import copy
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from mpl_toolkits.basemap import Basemap
from PIL import ImageTk


# create the main window
root = tk.Tk()
var=IntVar()
root.title('COVID-19 data analysis program')
root.geometry('600x600')

# create a text box to show query result
text0 = Text(root, height=8)
text0.place(x=50, y=215, width=500, height=200)

# create a canvas to show the image
canvas = tk.Canvas(root)
image_file = ImageTk.PhotoImage(file='image.png')
image = canvas.create_image(0, 0, anchor='nw', image=image_file)
canvas.place(x=50, y=445, height=125, width=500)

# define sql to get file from mysql database
engine = create_engine('mysql+pymysql://:@localhost:3306/test')
sqlConfirmed = ''' select * from time_series_covid_19_confirmed; '''
sqlDeaths = ''' select * from time_series_covid_19_deaths; '''
sqlRecovered = ''' select * from time_series_covid_19_recovered; '''
dataConfirmed = pd.read_sql_query(sqlConfirmed, engine)

# get date information from file and write to a combobox
data0 = dataConfirmed.iloc[0, 4:]
date = data0.index
dateCombo = ttk.Combobox(root)
listDate = []
for i in date:
    listDate.append(i)
listDate.reverse()
dateCombo['value'] = listDate
dateCombo['state'] = 'readonly'


# give the confirm message when click the exit button
def Quit():
    Q = tkinter.messagebox.askyesno(title='提示', message='quit program?')
    if Q:
        root.quit()
        root.destroy()

# if login as admin, function of activate query, deactivate query and update file to database would be shown
def new_Login():
    def login():
        username = entryUserName.get()
        password = entryPassword.get()
        if username == "admin" and password == "admin":
            tk.messagebox.showinfo(title='Login success', message="Hello, administrator!")
            window1.destroy()

            bLogin.place_forget()
            adminin = tk.Label(root,text="Admin")
            adminin.place(x=0, y=25, width=100, height=20)

            queryUser.place_forget()
            queryAdmin = tk.Label(root, text='all queries : ')
            queryAdmin.place(x=130, y=100)

            queryCombo['value'] = list0
            queryCombo.current(0)

            def logout():
                blogout.place_forget()
                bUpdate.place_forget()
                adminin.place_forget()
                bLogin.place(x=35, y=25)

                queryAdmin.place_forget()
                queryUser.place(x=120, y=100)

                bactivate.place_forget()
                bdeactivate.place_forget()

                queryCombo['value'] = list1
                queryCombo.current(0)

                bResultQuery5.place_forget()
                bResultQuery8.place_forget()
                bResultQuery1.place_forget()
                bResultQuery11.place_forget()
                dateCombo.place_forget()
                countryCombo.place_forget()
                ProvinceCombo.place_forget()
                bOK11.place_forget()

                queryCombo.current(0)
                queryOk()

                bResultQuery1.place_forget()
                bResultQuery2.place_forget()
                bResultQuery3.place_forget()
                bResultQuery4.place_forget()
                bResultQuery5.place_forget()
                bResultQuery6.place_forget()
                bResultQuery7.place_forget()
                bResultQuery8.place_forget()
                bResultQuery9.place_forget()
                bResultQuery10.place_forget()
                bResultQuery11.place_forget()
                dateCombo.place_forget()
                countryCombo.place_forget()
                ProvinceCombo.place_forget()
                bOK11.place_forget()



            blogout=Button(root, text="logout", command=logout)
            blogout.place(x=80, y=20)

            bUpdate=Button(root, text="update", command=update)
            bUpdate.place(x=130, y=60)

            def activate():
                temp = queryCombo.get()
                if list1.count(temp) == 0:
                    list1.append(temp)
                    list1.sort()
                text0.delete('1.0', 'end')
                text0.insert('end', 'Query ' + temp + ' is now activated')

            bactivate=Button(root, text="activate", command=activate)
            bactivate.place(x=235, y=40)

            def deactivate():
                temp = queryCombo.get()
                if list1.count(temp) == 1:
                    list1.remove(temp)
                    list1.sort()
                text0.delete('1.0', 'end')
                text0.insert('end', 'Query ' + temp + ' is now deactivated')

            bdeactivate=Button(root, text="deactivate", command=deactivate)
            bdeactivate.place(x=330, y=40)

        else:
            tk.messagebox.showinfo(title="Error",message="Error, the user name or password is wrong!")
            window1.lift()

    window1 = tk.Toplevel(root)
    window1.title("Admin login")
    window1.geometry("280x120")
    varName = tk.StringVar()
    varName.set("")
    varPsword = tk.StringVar()
    varPsword.set("")
    Name=tk.StringVar()
    Name.set("")
    labelName = tk.Label(window1,text="user name:",justify=tk.RIGHT)
    labelPsword = tk.Label(window1,text="password:",justify=tk.RIGHT)
    entryUserName = tk.Entry(window1,textvariable=varName)
    entryPassword = tk.Entry(window1,show="*",textvariable=varPsword)
    button_Login = tk.Button(window1,text="login",command=login)
    button_Cancel = tk.Button(window1, text="cancel", command=window1.destroy)
    labelName.place(x=20, y=15)
    labelPsword.place(x=20, y=40)
    entryUserName.place(x=100, y=20)
    entryPassword.place(x=100, y=45)
    button_Login.place(x=90, y=80)
    button_Cancel.place(x=170, y=80)

# after selecting query from combobox, first clean text box and execute the query
def queryOk():
    text0.delete('1.0', 'end')
    order = queryCombo.get()
# for different query, different comboboxes and buttons will be shown
# query1
    if order == "All Confirmed Cases" :
        bResultQuery1.place(x=445, y=150)
        bResultQuery2.place_forget()
        bResultQuery3.place_forget()
        bResultQuery4.place_forget()
        bResultQuery5.place_forget()
        bResultQuery6.place_forget()
        bResultQuery7.place_forget()
        bResultQuery8.place_forget()
        bResultQuery9.place_forget()
        bResultQuery10.place_forget()
        bResultQuery11.place_forget()

        dateCombo.place(x=100, y=150, width=100, height=30)
        dateCombo.current(0)
        countryCombo.place_forget()
        ProvinceCombo.place_forget()
        bOK11.place_forget()
# query2
    if order == "All Deaths" :
        bResultQuery1.place_forget()
        bResultQuery2.place(x=445, y=150)
        bResultQuery3.place_forget()
        bResultQuery4.place_forget()
        bResultQuery5.place_forget()
        bResultQuery6.place_forget()
        bResultQuery7.place_forget()
        bResultQuery8.place_forget()
        bResultQuery9.place_forget()
        bResultQuery10.place_forget()
        bResultQuery11.place_forget()

        dateCombo.place(x=100, y=150, width=100, height=30)
        dateCombo.current(0)
        countryCombo.place_forget()
        ProvinceCombo.place_forget()
        bOK11.place_forget()
# query3
    if order == "All Recovered Cases" :
        bResultQuery1.place_forget()
        bResultQuery2.place_forget()
        bResultQuery3.place(x=445, y=150)
        bResultQuery4.place_forget()
        bResultQuery5.place_forget()
        bResultQuery6.place_forget()
        bResultQuery7.place_forget()
        bResultQuery8.place_forget()
        bResultQuery9.place_forget()
        bResultQuery10.place_forget()
        bResultQuery11.place_forget()

        dateCombo.place(x=100, y=150, width=100, height=30)
        dateCombo.current(0)
        countryCombo.place_forget()
        ProvinceCombo.place_forget()
        bOK11.place_forget()
# query4
    if order == "Case Scatter Map" :
            bResultQuery1.place_forget()
            bResultQuery2.place_forget()
            bResultQuery3.place_forget()
            bResultQuery4.place(x=445, y=150)
            bResultQuery5.place_forget()
            bResultQuery6.place_forget()
            bResultQuery7.place_forget()
            bResultQuery8.place_forget()
            bResultQuery9.place_forget()
            bResultQuery10.place_forget()
            bResultQuery11.place_forget()

            dateCombo.place_forget()
            countryCombo.place_forget()
            ProvinceCombo.place_forget()
            bOK11.place_forget()
# query5
    if order == "Key Area Confirmed Cases" :
        bResultQuery1.place_forget()
        bResultQuery2.place_forget()
        bResultQuery3.place_forget()
        bResultQuery4.place_forget()
        bResultQuery5.place(x=445, y=150)
        bResultQuery6.place_forget()
        bResultQuery7.place_forget()
        bResultQuery8.place_forget()
        bResultQuery9.place_forget()
        bResultQuery10.place_forget()
        bResultQuery11.place_forget()

        dateCombo.place(x=100, y=150, width=100, height=30)
        dateCombo.current(0)
        countryCombo.place_forget()
        ProvinceCombo.place_forget()
        bOK11.place_forget()
# query6
    if order == "Key Area Deaths" :
        bResultQuery1.place_forget()
        bResultQuery2.place_forget()
        bResultQuery3.place_forget()
        bResultQuery4.place_forget()
        bResultQuery5.place_forget()
        bResultQuery6.place(x=445, y=150)
        bResultQuery7.place_forget()
        bResultQuery8.place_forget()
        bResultQuery9.place_forget()
        bResultQuery10.place_forget()
        bResultQuery11.place_forget()

        dateCombo.place(x=100, y=150, width=100, height=30)
        dateCombo.current(0)
        countryCombo.place_forget()
        ProvinceCombo.place_forget()
        bOK11.place_forget()
# query7
    if order == "Key Area Recovered Cases" :
        bResultQuery1.place_forget()
        bResultQuery2.place_forget()
        bResultQuery3.place_forget()
        bResultQuery4.place_forget()
        bResultQuery5.place_forget()
        bResultQuery6.place_forget()
        bResultQuery7.place(x=445, y=150)
        bResultQuery8.place_forget()
        bResultQuery9.place_forget()
        bResultQuery10.place_forget()
        bResultQuery11.place_forget()

        dateCombo.place(x=100, y=150, width=100, height=30)
        dateCombo.current(0)
        countryCombo.place_forget()
        ProvinceCombo.place_forget()
        bOK11.place_forget()
# query8
    if order == "Most Confirmed Cases" :
        bResultQuery1.place_forget()
        bResultQuery2.place_forget()
        bResultQuery3.place_forget()
        bResultQuery4.place_forget()
        bResultQuery5.place_forget()
        bResultQuery6.place_forget()
        bResultQuery7.place_forget()
        bResultQuery8.place(x=445, y=150)
        bResultQuery9.place_forget()
        bResultQuery10.place_forget()
        bResultQuery11.place_forget()

        dateCombo.place(x=100, y=150, width=100, height=30)
        dateCombo.current(0)
        countryCombo.place_forget()
        ProvinceCombo.place_forget()
        bOK11.place_forget()
# query9
    if order == "Most Deaths" :
        bResultQuery1.place_forget()
        bResultQuery2.place_forget()
        bResultQuery3.place_forget()
        bResultQuery4.place_forget()
        bResultQuery5.place_forget()
        bResultQuery6.place_forget()
        bResultQuery7.place_forget()
        bResultQuery8.place_forget()
        bResultQuery9.place(x=445, y=150)
        bResultQuery10.place_forget()
        bResultQuery11.place_forget()

        dateCombo.place(x=100, y=150, width=100, height=30)
        dateCombo.current(0)
        countryCombo.place_forget()
        ProvinceCombo.place_forget()
        bOK11.place_forget()
# query10
    if order == "Most Recovered Cases" :
        bResultQuery1.place_forget()
        bResultQuery2.place_forget()
        bResultQuery3.place_forget()
        bResultQuery4.place_forget()
        bResultQuery5.place_forget()
        bResultQuery6.place_forget()
        bResultQuery7.place_forget()
        bResultQuery8.place_forget()
        bResultQuery9.place_forget()
        bResultQuery10.place(x=445, y=150)
        bResultQuery11.place_forget()

        dateCombo.place(x=100, y=150, width=100, height=30)
        dateCombo.current(0)
        countryCombo.place_forget()
        ProvinceCombo.place_forget()
        bOK11.place_forget()
# query11
    if order == "Trend Chart" :
        bResultQuery1.place_forget()
        bResultQuery2.place_forget()
        bResultQuery3.place_forget()
        bResultQuery4.place_forget()
        bResultQuery5.place_forget()
        bResultQuery6.place_forget()
        bResultQuery7.place_forget()
        bResultQuery8.place_forget()
        bResultQuery9.place_forget()
        bResultQuery10.place_forget()
        bResultQuery11.place(x=445, y=150)

        dateCombo.place_forget()
        countryCombo.place(x=100, y=150, width=100, height=30)
        countryCombo.current(8)
        ProvinceCombo.place(x=270, y=150, width=150, height=30)
        okquery11()
        bOK11.place(x=215, y=150)

# define different commands for different query
def query1():
    text0.delete('1.0', 'end')
    data = pd.read_sql_query(sqlConfirmed, engine)
    currentdate = dateCombo.get()
    sum1 = data.loc[:,[currentdate]].apply(sum)
    left = str(sum1).split(' ')[0]
    right = str(sum1).split(' ')[4].split('\n')[0]
    temp = 'The number of all confirmed cases up to ' + left + ' is ' + right
    text0.insert('end', temp)

def query2():
    text0.delete('1.0', 'end')
    data = pd.read_sql_query(sqlDeaths, engine)
    currentdate = dateCombo.get()
    sum1 = data.loc[:,[currentdate]].apply(sum)
    left = str(sum1).split(' ')[0]
    right = str(sum1).split(' ')[4].split('\n')[0]
    temp = 'The number of all deaths up to ' + left + ' is ' + right
    text0.insert('end', temp)

def query3():
    text0.delete('1.0', 'end')
    data = pd.read_sql_query(sqlRecovered, engine)
    currentdate = dateCombo.get()
    sum1 = data.loc[:,[currentdate]].apply(sum)
    left = str(sum1).split(' ')[0]
    right = str(sum1).split(' ')[4].split('\n')[0]
    temp = 'The number of all recovered cases up to ' + left + ' is ' + right
    text0.insert('end', temp)

def query4():
    data1 = pd.read_csv('COVID19_open_line_list.csv')
    m = Basemap()
    m.drawcoastlines()
    m.drawmapboundary(fill_color='none')
    m.fillcontinents(color='none')
    parallels = np.arange(-90., 90., 10.)
    m.drawparallels(parallels,labels=[False, True, True, False])
    meridians = np.arange(-180., 180., 20.)
    m.drawmeridians(meridians,labels=[True, False, False, True])
    m.scatter(data1['longitude'], data1['latitude'], s=100)
    plt.show()

def query5():
    text0.delete('1.0', 'end')
    data = pd.read_sql_query(sqlConfirmed, engine)
    currentdate = dateCombo.get()
    data = data.loc[:,[currentdate,'Province/State','Country/Region']]
    data = data.sort_values(by=currentdate, ascending = False)
    temp = data.head(10)
    text0.insert('end', 'Ten key areas with most confirmed cases:\n\n')
    text0.insert('end', temp)

def query6():
    text0.delete('1.0', 'end')
    data = pd.read_sql_query(sqlDeaths, engine)
    currentdate = dateCombo.get()
    data = data.loc[:,[currentdate,'Province/State','Country/Region']]
    data = data.sort_values(by=currentdate, ascending = False)
    temp = data.head(10)
    text0.insert('end', 'Ten key areas with most deaths:\n\n')
    text0.insert('end', temp)

def query7():
    text0.delete('1.0', 'end')
    data = pd.read_sql_query(sqlRecovered, engine)
    currentdate = dateCombo.get()
    data = data.loc[:,[currentdate,'Province/State','Country/Region']]
    data = data.sort_values(by=currentdate, ascending = False)
    temp = data.head(10)
    text0.insert('end', 'Ten key areas with most recovered cases:\n\n')
    text0.insert('end', temp)

def query8():
    text0.delete('1.0', 'end')
    data = pd.read_sql_query(sqlConfirmed, engine)
    currentdate = dateCombo.get()
    temp ='The country/rigion with most confirmed cases on ' + currentdate +' is ' + str(data.iloc[data[currentdate].argmax(),1])
    text0.insert('end', temp)

def query9():
    text0.delete('1.0', 'end')
    data = pd.read_sql_query(sqlDeaths, engine)
    currentdate = dateCombo.get()
    temp ='The country/rigion with most deaths on ' + currentdate +' is ' + str(data.iloc[data[currentdate].argmax(),1])
    text0.insert('end', temp)

def query10():
    text0.delete('1.0', 'end')
    data = pd.read_sql_query(sqlRecovered, engine)
    currentdate = dateCombo.get()
    temp ='The country/rigion with most recovered cases on ' + currentdate +' is ' + str(data.iloc[data[currentdate].argmax(),1])
    text0.insert('end', temp)

def okquery11():
    dataConfirmed3 = copy.deepcopy(dataConfirmed)
    dataConfirmed3 = dataConfirmed3.loc[:,['Province/State','Country/Region']]
    dataConfirmed3 = dataConfirmed3['Province/State'][dataConfirmed3['Country/Region'].isin([countryCombo.get()])]
    listProvince = []
    for i in dataConfirmed3:
        listProvince.append(i)
    ProvinceCombo['value'] = listProvince
    ProvinceCombo.current(0)

def query11():
    crindex = dataConfirmed.index[dataConfirmed['Country/Region'] == countryCombo.get()]
    psindex = dataConfirmed.index[dataConfirmed['Province/State'] == ProvinceCombo.get()]

    if ProvinceCombo.get() == 'None':
        dataConfirmed4 = dataConfirmed.iloc[crindex[0], 4:]
        dataConfirmed4 = dataConfirmed4.to_frame()
        date = dataConfirmed4.index
        dataConfirmed4['date'] = date
        dataConfirmed4=dataConfirmed4.rename(columns={crindex[0]:countryCombo.get()})
        y0 = countryCombo.get()
        dataConfirmed4.plot(kind='line', linestyle='-', x='date', y= y0, marker='o', markerfacecolor='red', title='Trend of covid 19 confirmed')
        plt.show()
    else:
        dataConfirmed4 = dataConfirmed.iloc[psindex[0], 4:]
        dataConfirmed4 = dataConfirmed4.to_frame()
        date = dataConfirmed4.index
        dataConfirmed4['date'] = date
        dataConfirmed4=dataConfirmed4.rename(columns={psindex[0]:ProvinceCombo.get()})
        y0 = ProvinceCombo.get()
        dataConfirmed4.plot(kind='line', linestyle='-', x='date', y= y0, marker='o', markerfacecolor='red', title='Trend of covid 19 confirmed')
        plt.show()

# read local csv file and update to mysql database
def update():
    text0.delete('1.0', 'end')
    dfConfirmed = pd.read_csv("time_series_covid_19_confirmed.csv", sep=',')
    pd.io.sql.to_sql(dfConfirmed, 'time_series_covid_19_confirmed', con=engine, index=False, if_exists='replace')
    dfDeaths = pd.read_csv("time_series_covid_19_deaths.csv", sep=',')
    pd.io.sql.to_sql(dfDeaths, 'time_series_covid_19_deaths', con=engine, index=False, if_exists='replace')
    dfRecovered = pd.read_csv("time_series_covid_19_recovered.csv", sep=',')
    pd.io.sql.to_sql(dfRecovered, 'time_series_covid_19_recovered', con=engine, index=False, if_exists='replace')
    text0.insert('end', 'read local csv file and update to mysql database successfully')

# save data from mysql database as csv file
def download():
    text0.delete('1.0', 'end')
    dlConfirmed = pd.read_sql_query(sqlConfirmed, engine)
    dlConfirmed.to_csv('Confirmed.csv')
    dlDeaths = pd.read_sql_query(sqlDeaths, engine)
    dlDeaths.to_csv('Deaths.csv')
    dlRecovered = pd.read_sql_query(sqlRecovered, engine)
    dlRecovered.to_csv('Recovered.csv')
    text0.insert('end', 'save data from mysql database as csv file successfully')

# define all queries and fault queries, write them to comboboxes
queryUser = tk.Label(root, text='select query : ')
queryUser.place(x=120, y=100)
queryCombo = ttk.Combobox(root)
list0 = ['All Confirmed Cases', 'All Deaths', 'All Recovered Cases', 'Case Scatter Map',
         'Key Area Confirmed Cases', 'Key Area Deaths', 'Key Area Recovered Cases',
         'Most Confirmed Cases', 'Most Deaths', 'Most Recovered Cases', 'Trend Chart', ]
list1 = ['All Confirmed Cases', 'Case Scatter Map', 'Key Area Confirmed Cases', 'Most Confirmed Cases', 'Trend Chart']
queryCombo['value'] = list1
queryCombo.current(0)
queryCombo['state'] = 'readonly'
queryCombo.place(x=220, y=100, width=200, height=30)

# set buttons and commands
bQueryOk=Button(root, text="OK", command=queryOk)
bQueryOk.place(x=450, y=100)
bLogin=Button(root, text="login", command=new_Login)
bLogin.place(x=35, y=25)
bExit=Button(root, text="exit", relief=tk.RAISED, command=Quit)
bExit.place(x=535, y=25)
bDownload=Button(root, text="download", command=download)
bDownload.place(x=35, y=60)

bResultQuery1=Button(root, text="show", command=query1)
bResultQuery2=Button(root, text="show", command=query2)
bResultQuery3=Button(root, text="show", command=query3)
bResultQuery4=Button(root, text="show", command=query4)
bResultQuery5=Button(root, text="show", command=query5)
bResultQuery6=Button(root, text="show", command=query6)
bResultQuery7=Button(root, text="show", command=query7)
bResultQuery8=Button(root, text="show", command=query8)
bResultQuery9=Button(root, text="show", command=query9)
bResultQuery10=Button(root, text="show", command=query10)
bOK11=Button(root, text="OK", command=okquery11)
bResultQuery11=Button(root, text="show", command=query11)

# get country from file and write to the combobox
countryCombo = ttk.Combobox(root)
dataConfirmed2 = copy.deepcopy(dataConfirmed)
dataConfirmed2 = dataConfirmed2['Country/Region']
dataConfirmed2.drop_duplicates(keep='first', inplace=True)
listCountry = []
for i in dataConfirmed2:
    listCountry.append(i)
countryCombo['value'] = listCountry
countryCombo.current(8)
countryCombo['state'] = 'readonly'

# get province from file and write to the combobox
ProvinceCombo = ttk.Combobox(root)
dataConfirmed3 = copy.deepcopy(dataConfirmed)
dataConfirmed3 = dataConfirmed3.loc[:, ['Province/State', 'Country/Region']]
dataConfirmed3 = dataConfirmed3['Province/State'][dataConfirmed3['Country/Region'].isin([countryCombo.get()])]
listProvince = []
for i in dataConfirmed3:
    listProvince.append(i)
ProvinceCombo['value'] = listProvince
ProvinceCombo.current(0)
ProvinceCombo['state'] = 'readonly'

import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)


if __name__ == "__main__":
    mainloop()
