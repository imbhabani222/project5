import pandas as pd
# !pip install Dash
import dash
from dash.dependencies import Input, Output 
import dash_html_components as html
import dash_core_components as dcc
import webbrowser  
import plotly.graph_objects as go  
import plotly.express as Px
from dash.exceptions import PreventUpdate

app=dash.Dash()

def load_data():
     dataset_name="global_terror.csv"
     
     global df
     df=pd.read_csv(dataset_name)
     
     
     month={
         "January":1,
         "February":2,
         "March":3,
         "April":4,
         "May":5,
         "June":6,
         "July":7,
         "August":8,
         "Septmber":9,
         "October":10,
         "November":11,
         "December":12
         }
     
     
     global month_list
     month_list=[{"label":key,"value":values}for key,values in month.items()]
     
     global date_list
     date_list=[x for x in range(1,32)]
     
          
     global region_list
     region_list=[{"label":str(i),"value":str(i)} for i in sorted(df["region_txt"].unique().tolist())]
     
     
     global country_list
     country_list=df.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()
     print(country_list)
     
     
     global state_list
     state_list=df.groupby("country_txt")["provstate"].unique().apply(list).to_dict()
     
     global city_list
     city_list=df.groupby("provstate")["city"].unique().apply(list).to_dict()
     
     
     global attack_type_list
     attack_type_list=[{"label":str(i),"value":str(i)}for i in df["attacktype1_txt"].unique().tolist()]
     
     global year_list
     year_list=sorted(df["iyear"].unique().tolist())
     
     global year_dict
     year_dict={str(year):str(year) for year in year_list}
     
     
     global chart_dropdown_values
     chart_dropdown_values = {"Terrorist Organisation":'gname', 
                             "Target Nationality":'natlty1_txt', 
                             "Target Type":'targtype1_txt', 
                             "Type of Attack":'attacktype1_txt', 
                             "Weapon Type":'weaptype1_txt', 
                             "Region":'region_txt', 
                             "Country Attacked":'country_txt'
                          }
                              
     chart_dropdown_values = [{"label":keys, "value":value} for keys, value in chart_dropdown_values.items()]
     

def create_app_ui():
    main_layout= html.Div(
            [
                html.H1(children="Terrorism Analysis with insights",id="main_title"),
                
                dcc.Tabs(id="Tabs", value="Tab",children=[
                     dcc.Tab(label="Map tool", id="Map tool", value="Map", children =[
                         dcc.Tabs(id = "subtabs", value = "WorldMap",children = [
                             dcc.Tab(label="World Map tool", id="World", value="WorldMap"),
                             dcc.Tab(label="India Map tool", id="India", value="IndiaMap")
                             ]),   
                dcc.Dropdown(id="Month",
                    options=month_list,
                    multi = True,
                    placeholder="select Month", 
                    ),
                dcc.Dropdown(id="Date",
                    options=[{"label":"All","value":"All"}],
                    multi = True,
                    placeholder="select Date",
                    ),
                dcc.Dropdown(id="Region",
                    options=region_list,
                    multi = True,
                    placeholder="select Region"
                    ),
                dcc.Dropdown(id="country",
                    options=[{"label":"All","value":"All"}],
                    multi = True,
                    placeholder="select country",
                    
                    ),
                dcc.Dropdown(id="state",
                    options=[{"label":"All","value":"All"}],
                    multi =  True,
                    placeholder="select state",
                    
                    ),
                 dcc.Dropdown(id="city",
                    options=[{"label":"All","value":"All"}],
                    multi = True,
                    placeholder="select city",
                  
                    ),
                dcc.Dropdown(id="attack",
                    options=attack_type_list,
                    multi = True,
                    placeholder="select attack type",
                    
                    ),
                html.H5("Select the Year",id="Year_title"),
                dcc.RangeSlider(
                    id="year_slider",
                    min=min(year_list),
                    max=max(year_list),
                    value=[min(year_list),max(year_list)],
                    marks=year_dict,
                    step=None
                    ),
                html.Br(),
                ]),
                dcc.Tab(label = "Chart Tool", id="chart tool", value="Chart", children=[
                     dcc.Tabs(id = "subtabs2", value = "WorldChart",children = [
                         dcc.Tab(label="World Chart tool", id="WorldC", value="WorldChart"),
                         dcc.Tab(label="India Chart tool", id="IndiaC", value="IndiaChart")
                        ]),
                dcc.Dropdown(id="Ch_Dropdown", options = chart_dropdown_values, placeholder="Select option", value = "region_txt"), 
                  html.Br(),
                  html.Br(),
                  html.Hr(),
                  dcc.Input(id="search", placeholder="Search Filter"),
                  html.Hr(),
                  html.Br(),
                  dcc.RangeSlider(
                    id='chyear_slider',
                    min=min(year_list),
                    max=max(year_list),
                    value=[min(year_list),max(year_list)],
                    marks=year_dict,
                    step=None
                    ),
                  html.Br()
                 ])
            ]),
        html.Div(id = "graph-object", children ="Here is the graph")
        ])
    return main_layout


@app.callback(
        dash.dependencies.Output("graph-object","children"),
        [
         dash.dependencies.Input("Tabs", "value"),
         dash.dependencies.Input("Month","value"),
         dash.dependencies.Input("Date","value"),
         dash.dependencies.Input("Region","value"),
         dash.dependencies.Input("country","value"),
         dash.dependencies.Input("state","value"),
         dash.dependencies.Input("city","value"),
         dash.dependencies.Input("attack","value"),
         dash.dependencies.Input("year_slider","value"),
         dash.dependencies.Input("chyear_slider", "value"),
         dash.dependencies.Input("Ch_Dropdown", "value"),
         dash.dependencies.Input("search", "value"),
         dash.dependencies.Input("subtabs2", "value")
         ]
        )
def Update_graph_ui(Tabs_val,month_val,date_val,reg_val,con_val,sta_val,city_val,att_val,year_value,ch_yr_selector, ch_dp_val, search,
                    subtabs2):
    figure=None
    
    if Tabs_val=="Map":
        print("datatype :",str(type(month_val)))
        print("value :",str(month_val))
        
        print("datatype :",str(type(date_val)))
        print("value :",str(date_val))
        
        print("datatype :",str(type(reg_val)))
        print("value :",str(reg_val))
        
        print("datatype :",str(type(con_val)))
        print("value :",str(con_val))
        
        print("datatype :",str(type(sta_val)))
        print("value :",str(sta_val))
        
        print("datatype :",str(type(city_val)))
        print("value :",str(city_val))
        
        print("datatype :",str(type(att_val)))
        print("value :",str(att_val))
        
        print("datatype :",str(type(year_value)))
        print("value :",str(year_value))
        
        year_range=range(year_value[0],year_value[1]+1)
        new_df=df[df["iyear"].isin(year_range)] 
    
        if month_val is None or month_val==[]:
            pass
        else:
            if date_val is None or date_val==[]:
                new_df=new_df[new_df["imonth"].isin(month_val)]
            else:
                new_df=new_df[(new_df["imonth"].isin(month_val)) & 
                              (new_df["iday"].isin(date_val))]
        
                                                               
        if reg_val is None or reg_val==[] :
            pass
        else:
            if con_val is None or con_val==[]:
                new_df=new_df[new_df["region_txt"].isin(reg_val)]
            else:
                if sta_val is None or sta_val==[]:
                    new_df=new_df[(new_df["region_txt"].isin(reg_val)) & 
                                  (new_df["country_txt"].isin(con_val))]
                else:
                    if city_val is None or city_val==[]:
                        new_df=new_df[(new_df["region_txt"].isin(reg_val)) & 
                                      (new_df["country_txt"].isin(con_val)) &
                                      (new_df["provstate"].isin(sta_val))]
                    else:
                        new_df=new_df[(new_df["region_txt"].isin(reg_val)) & 
                                      (new_df["country_txt"].isin(con_val)) & 
                                      (new_df["provstate"].isin(sta_val)) & 
                                      (new_df["city"].isin(city_val))]
        
        
        if att_val is None or att_val==[]:
            pass
        else:
            new_df=new_df[(new_df["attacktype1_txt"].isin(att_val))]
        mapFigure = go.Figure()
        
        if new_df.shape[0]:
            pass
        else: 
            new_df = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
               'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])
            
            new_df.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]
            
        
        mapFigure=Px.scatter_mapbox(
                                 new_df,
                                 lat="latitude",
                                 lon="longitude",
                                 color="attacktype1_txt",
                                 hover_data=["region_txt","country_txt","provstate","city","attacktype1_txt","nkill","iyear"],
                                 zoom=1
                                 )
        mapFigure.update_layout(mapbox_style="open-street-map",
                             autosize=True,
                             margin=dict(l=0,r=0,t=25,b=20),
                             )
        figu=mapFigure
    
    elif Tabs_val=="Chart":
        figu = None
        year_range_c = range(ch_yr_selector[0], ch_yr_selector[1]+1)
        chart_df = df[df["iyear"].isin(year_range_c)]
        
        
        if subtabs2 == "WorldChart":
            pass
        elif subtabs2 == "IndiaChart":
            chart_df = chart_df[(chart_df["region_txt"]=="South Asia") &(chart_df["country_txt"]=="India")]
        if ch_dp_val is not None and chart_df.shape[0]:
            if search is not None:
                chart_df = chart_df.groupby("iyear")[ch_dp_val].value_counts().reset_index(name = "count")
                chart_df  = chart_df[chart_df[ch_dp_val].str.contains(search, case=False)]
            else:
                chart_df = chart_df.groupby("iyear")[ch_dp_val].value_counts().reset_index(name="count")
        
        
        if chart_df.shape[0]:
            pass
        else: 
            chart_df = pd.DataFrame(columns = ['iyear', 'count', ch_dp_val])
        
            chart_df.loc[0] = [0, 0,"No data"]
        figu = Px.area(chart_df, x="iyear", y ="count", color = ch_dp_val)


    return dcc.Graph(figure=figu)

@app.callback(
  Output("date", "options"),
  [Input("month", "value")])
def update_date_c(month):
    option = []
    if month:
        option= [{"label":m, "value":m} for m in date_list]
    return option

@app.callback([Output("Region", "value"),
               Output("Region", "disabled"),
               Output("country", "value"),
               Output("country", "disabled")],
              [Input("subtabs", "value")])
def update_r(tab):
    region = None
    disabled_r = False
    country = None
    disabled_c = False
    if tab == "WorldMap":
        pass
    elif tab=="IndiaMap":
        region = ["South Asia"]
        disabled_r = True
        country = ["India"]
        disabled_c = True
    return region, disabled_r, country, disabled_c





@app.callback(
     dash.dependencies.Output("Date","options"),
     [
       dash.dependencies.Input("Month","value"),
     ]
     )
def update_date(month_val):
    date_list=[x for x in range(1,32)]
    option=[]
    if month_val:
        option = [{"label":m, "value":m} for m in date_list]
    return option
    


@app.callback(
     Output("country","options"),
     [
     Input("Region","value"),
     ]
     )
def update_country(reg_val):
    option=[]
    if reg_val is None:
        raise PreventUpdate
    else:
        for var in reg_val:
            if var in country_list.keys():
                option.extend(country_list[var])
    return [{'label':m, 'value':m} for m in option]
    


@app.callback(
     Output("state","options"),
     [
      Input("country","value"),
     ]
     )
def update_state(con_val):
    option=[]
    if con_val is None:
        raise PreventUpdate
    else:
        for var in con_val:
            if var in state_list.keys():
                option.extend(state_list[var])
    return [{'label':m, 'value':m} for m in option]

@app.callback(
     Output("city","options"),
     [
     Input("state","value"),
     ]
     )
def update_city(sta_val):
    option=[]
    if sta_val is None:
        raise PreventUpdate
    else:
        for var in sta_val:
            if var in city_list.keys():
                option.extend(city_list[var])
    return [{'label':m, 'value':m} for m in option]
    global figure
    figure=go.Figure() 
   

def open_browser():
    webbrowser.open_new(" http://127.0.0.1:8050/")
    
    
    
def main():
    print("Starting the main function.....")
    load_data()
    open_browser()
    create_app_ui()
    global app
    app.layout=create_app_ui()
    app.title="Terrorism Analysis with Insights"
    app.run_server()
    print("Ending the main function.......")
    df= None
    app=None
    
    
if __name__=='__main__':
    print("My project is Starting.......")
    main()
    print("My project is Ending.......")    
    
    
    