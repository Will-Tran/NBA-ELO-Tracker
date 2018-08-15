import requests
import csv
import numpy as np
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool

try:
    
    r = requests.get("https://projects.fivethirtyeight.com/nba-model/nba_elo.csv")
    with open("nba_elo.csv", "wb") as f:
        f.write(r.content)
    
    team = input('Type ALL below to see all teams available.\nOtherwise, please enter the team here: ')
    
    if team == "ALL":
        print("ATL\t Atlanta Hawks")
        print("BOS\t Boston Celtics")
        print("BRK\t Brooklyn Nets")
        print("CHO\t Charlotte Hornets")
        print("CHI\t Chicago Bulls")
        print("CLE\t Cleveland Cavaliers")
        print("DAL\t Dallas Mavericks")
        print("DEN\t Denver Nuggets")
        print("DET\t Detroit Pistons")
        print("GSW\t Golden State Warriors")
        print("HOU\t Houston Rockets")
        print("IND\t Indiana Pacers")
        print("LAC\t Los Angeles Clippers")
        print("LAL\t Los Angeles Lakers")
        print("MEM\t Memphis Grizzlies")
        print("MIA\t Miami Heat")
        print("MIL\t Milwaukee Bucks")
        print("MIN\t Minnesota Timberwolves")
        print("NOP\t New Orleans Pelicans")
        print("NYK\t New York Knicks")
        print("OKC\t Oklahoma City Thunders")
        print("ORL\t Orlando Magic")
        print("PHI\t Philadelphia 76ers")
        print("PHO\t Phoenix Suns")
        print("POR\t Portland Trail Blazers")
        print("SAC\t Sacramento Kings")
        print("SAS\t San Antonio Spurs")
        print("TOR\t Toronto Raptors")
        print("UTA\t Utah Jazz")
        print("WAS\t Washington Wizards")
    
    else:
        map = {"ATL" : "Atlanta Hawks", "BOS" : "Boston Celtics", "BRK" : "Brooklyn Nets", 
               "CHO" : "Charlotte Hornets", "CHI" : "Chicago Bulls", "CLE" : "Cleveland Cavaliers", 
               "DAL" : "Dallas Mavericks", "DEN" : "Denver Nuggets", "DET" : "Detroit Pistons", 
               "GSW" : "Golden State Warriors", "HOU" : "Houston Rockets", "IND" : "Indiana Pacers",
               "LAC" : "Los Angeles Clippers", "LAL" : "Los Angeles Lakers", "MEM" : "Memphis Grizzlies",
               "MIA" : "Miami Heat", "MIL" : "Milwaukee Bucks", "MIN" : "Minnesota Timberwolves", 
               "NOP" : "New Orleans Pelicans", "NYK" : "New York Knicks", "OKC" : "Oklahoma City Thunders",
               "ORL" : "Orlando Magic", "PHI" : "Philadelphia 76ers", "PHO" : "Phoenix Suns",
               "POR" : "Portland Trail Blazers", "SAC" : "Sacramento Kings", "SAS" : "San Antonio Spurs",
               "TOR" : "Toronto Raptors", "UTA" : "Utah Jazz", "WAS" : "Washington Wizards"}
        teamname = map[team]
            
        Date = []
        ELO = []       
        
        with open('nba_elo.csv') as myFile:
            reader = csv.reader(myFile, delimiter = ',')
            for row in reader:
                if team in row[4] and row[10] != "":
                    Date.append(row[0])
                    ELO.append(row[10])
                elif team in row[5] and row[11] != "":
                    Date.append(row[0])
                    ELO.append(row[10])
        
        data = {'DateTime' : pd.Series(Date,dtype='datetime64[ns]'),'Float' : pd.Series(ELO)}
        d = pd.DataFrame(data)
        d['Date'] = [x.strftime("%m-%d-%Y") for x in d['DateTime']]
        d['ELO'] = d['Float'].astype(float).astype(int)
        
        output_file("nba.html", title="NBA ELO History")
        
        MaxELO = np.amax(d['ELO'])
        MinELO = np.amin(d['ELO'])
        MaxPos = np.argmax(d['ELO'])
        MinPos = np.argmin(d['ELO'])
        MaxDate = d['Date'][MaxPos]
        MinDate = d['Date'][MinPos]
        
        maximum = {'MaxDate' : pd.Series(MaxDate,dtype='datetime64[ns]'), 'MaxELO' : pd.Series(MaxELO)}
        m = pd.DataFrame(maximum)
        m['MxDate'] = [x.strftime("%m-%d-%Y") for x in m['MaxDate']]
        m['MxELO'] = m['MaxELO'].astype(float).astype(int)
        minimum = {'MinDate' : pd.Series(MinDate,dtype='datetime64[ns]'), 'MinELO' : pd.Series(MinELO)}
        mm = pd.DataFrame(minimum)
        mm['MnDate'] = [x.strftime("%m-%d-%Y") for x in mm['MinDate']]
        mm['MnELO'] = mm['MinELO'].astype(float).astype(int)
        
        p = figure(width=1500, height=1000, x_axis_type="datetime",tools='pan,wheel_zoom,box_zoom,reset,previewsave,hover,hover,hover',logo=None)
        
        main = p.line(x='DateTime', y='Float', source=ColumnDataSource(d), color = 'navy', legend=team + ' ELO Rating')
        maxpoint = p.circle(x='MaxDate',y='MaxELO', source=ColumnDataSource(m), color = 'red',legend='Max ELO',size=15)
        minpoint = p.circle(x='MinDate',y='MinELO', source=ColumnDataSource(mm), color = 'blue',legend='Min ELO',size=15)
        
        p.title.text = teamname + " ELO History"
        p.legend.location = "top_left"
        p.grid.grid_line_alpha=1
        p.xaxis.axis_label = 'Date'
        p.yaxis.axis_label = 'ELO'
        p.ygrid.band_fill_color="olive"
        p.ygrid.band_fill_alpha = 0
        
        hover = p.select(dict(type=HoverTool))
        hover[0].renderers = [main]
        hover[0].tooltips = [("Date", "@Date"), ("ELO", "@ELO")]
        hover[1].renderers = [maxpoint]
        hover[1].tooltips = [("Max Date", "@MxDate"), ("Max ELO", "@MxELO")]
        hover[2].renderers = [minpoint]
        hover[2].tooltips = [("Min Date", "@MnDate"), ("Min ELO", "@MnELO")]
        hover.mode = 'mouse'
        
        show(p)
except:
    print("Invalid team. Please try again.")