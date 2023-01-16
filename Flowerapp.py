import dash
from dash import dcc
from dash import html,dash_table
import pandas as pd
import numpy as np
import plotly.express as px
from dash.dependencies import Input, Output,State
from plotly import graph_objs as go
from plotly.graph_objs import *
import dash_bootstrap_components as dbc
from datetime import date,timedelta,datetime
from sample_data import sensitivity_list,choices,last_week_date, last_year_date, last_month_date,results_list,genotype_list,type_list,next_month_date,next_year_date,next_week_date
from production_prediction import get_available_stalks
from be.controllers.filtering_tools import filter_dataframe,make_plotable,next_monday,filter_planted_after,daterange
from be.controllers.scatter_plot import scatter_graph

##########################


        ##############UPDATE REPORT

        # tallos_sembrados=filtered_df[filtered_df["variety"]==variedad]["stems"].sum()
        # tallos_sembrados=f"{tallos_sembrados:,}"
        # disponibles=get_available_stalks(filtered_df[filtered_df["variety"]==variedad],end_date_prediction,1)
        # disponibles=f"{disponibles:,}"
        # row=pd.DataFrame({"Variedad":variedad.capitalize(),"Tallos sembrados":tallos_sembrados,"Disponibles en "+str(end_date_prediction.date()):disponibles},index=[0])
        # df_report=pd.concat([df_report,row])#,ignore_index=True)



#starting_date_planted = date.today() - timedelta(days = 300)
df=pd.read_csv("production.csv")
df["planted_on"]=pd.to_datetime(df["planted_on"])
df["planted_on"]=df['planted_on'].dt.date

for i in range(1,24):
    df["fecha_dia_"+str(i)]=pd.to_datetime(df["fecha_dia_"+str(i)])
    # df["fecha_dia_"+str(i)]=df['fecha_dia_'+str(i)].dt.date

#df=filter_planted_after(df,starting_date_planted)
######################################
A=date(2021,7,1)
B=A+timedelta(days=15)
dias=daterange(A,B)
var=dict()
for variedad in ["chelsea","potomac early white"]:
        draw_df=pd.DataFrame()
        draw_df["x"]=dias
        draw_df["y"]=list(map(lambda z: get_available_stalks(df[df["variety"]==variedad],z,1),dias))
        var[variedad]=draw_df
flowers_graph=scatter_graph("aneto",var)


######

# for variedad in ["chelsea","potomac early white"]:
#         draw_df=pd.DataFrame()
#         draw_df["x"]=dias
#         draw_df["y"]=list(map(lambda z: get_available_stalks(df[df["variety"]==variedad],z,1),dias))
#         var[variedad]=draw_df

######################### SOME DATA
bloques_list=["Todos los bloques"]+list(df["block"].unique())
variedades_list=list(df["variety"].unique())
########################
###########################
# df_info = pd.DataFrame(columns=["Variedad","Tallos sembrados","Disponibles a fin del periodo"])
# for variedad in variedades_list[:5]:
#     row=pd.DataFrame({"Variedad":variedad.capitalize(),"Tallos sembrados":np.random.choice(range(1000,2000)),"Disponibles a fin del periodo":np.random.choice(range(1000,1800))},index=[0])
#     df_info=pd.concat([df_info,row])#,ignore_index=True)
# info=dbc.Table(dftest.to_dict('records'), [{"name": i, "id": i} for i in dftest.columns])
# df_info=pd.read_csv("info_df.csv")

# info = dbc.Table.from_dataframe(df_info, striped=True, bordered=True, hover=True,style={"width":"100%","margin-bottom":"20px","margin-top":"60px","margin-left":"20px"},id="info_table")




# Records_df=pd.read_csv("Records.csv")
# Records_df["day"]=pd.to_datetime(Records_df["day"])



# table_header = [
#     html.Thead(html.Tr([html.Th("Tests"), html.Th("Daily Avg"),html.Th("Positivity rate")]))
# ]

# row1 = html.Tr([html.Td("345",id="tests"), html.Td("45.6",id="average"),html.Td("Positivity rate",id="positivity_rate")])


# table_body = [html.Tbody([row1])]

# table = dbc.Table(table_header + table_body, bordered=True,style={"width":"100%","margin-bottom":"20px","margin-top":"60px","margin-left":"20px"})
###############
def make_drop(lista:list,id:str,multi=False):
    menu=dcc.Dropdown(id=id,
    options=[ {"label": i, "value": i} for i in lista],
    value=lista[0],
    clearable=False,
    multi=multi


        )
    return {"drop":menu}


###################  GENERATE THE DROPDOWN ELEMENTS  #######################


dropletter=make_drop(['Hoy', 'En 9',''],"dropletter")
# type_drop=make_drop(type_list+["All test types"],"type")
# results_drop=make_drop(results_list+["All results"],"results")###### it starts at 1 to rule out the "All results" option
# genotype_drop=make_drop(genotype_list+["All genotypes"],"genotype")
bloques_drop=make_drop(bloques_list,"bloques_drop",multi=True)
variedades_drop=make_drop(variedades_list,"variedades_drop",multi=True)




def drawFigure(altura,id):
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure={},
                    id=id,
                    config={
                        'displayModeBar': False
                    },
                )
            ])
        ),
    ])

app = dash.Dash()





# Layout of Dash App
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.A(
                            html.Img(
                                className="logo",
                                src=app.get_asset_url("capiro.jpeg"),
                                style={"width":"100%","height":"10%","align":"centered"}
                            ),
                            href="https://floreseltrigal.com/",
                        ),
                        html.H1("Nutrición de plantas",style={"text-align":"center"}),
                        # html.P('Seleccione la fecha de inicio del pronóstico'),
                        # # html.Div(
                        # #     className="row",
                        # #     children=[
                        # #         html.Div(
                        # #             className="div-for-dropdown",
                        # #             children=[
                        # #                 dropletter["drop"]
                        # #             ],
                        # #         ),
                        # #     ],
                        # # ),
                        # html.Div(
                        #     className="div-for-dropdown",
                        #     children=[
                        #         dcc.DatePickerSingle(
                        #             id = 'date_start',
                        #             style={"width":"100%"},
                        #             date=date.today()
                        #                 )
                        #     ],
                        # ),
                        dbc.Label("Precio de Potasio por Kg", html_for="slider"),
                        dcc.Slider(300000, 600000, 1000,
                        value=100,
                        id='my-slider',
                        tooltip={"placement": "bottom", "always_visible": True},
                        marks= {
                        300000: {'label': '300k'},
                        400000: {'label': '400k'},
                        500000: {'label': '500k'},
                        600000:{'label':'600k'},
                        },
                        ),
                        html.H1(""),
                        dbc.Label("Precio de Fósforo por Kg", html_for="slider"),
                        dcc.Slider(500000, 2000000, 1000,
                        value=100,
                        id='my-slider',
                        tooltip={"placement": "bottom", "always_visible": True},
                        marks={
                        500000: {'label': '500k', },
                        1000000: {'label': '1M'},
                        1500000: {'label': '1.5M'},
                        2000000: {'label': '2M'}
                        },
                        ),
                        html.H1(""),
                        dbc.Label("Precio de Nitrógeno por Kg", html_for="slider"),
                        dcc.Slider(100000, 300000, 1000,
                        value=100,
                        id='my-slider',
                        tooltip={"placement": "bottom", "always_visible": True},
                        marks={
                        100000: {'label': '100k'},
                        150000: {'label': '150k'},
                        200000: {'label': '200k'},
                        250000: {'label': '250k'},
                        300000: {'label': '300k'},
                        },
                        ),
                        html.H1(""),
                        #html.Div(id='slider-output-container'),
                        # Change to side-by-side for mobile layout
                        # html.Div(
                        #     className="div-for-dropdown",
                        #     children=[
                        #         dcc.DatePickerSingle(
                        #             id = 'date_end',
                        #             style={"width":"100%"}
                        #                 )
                        #     ],
                        # ),
                        # html.P('Seleccione una variedad'),
                        # html.Div(
                        #     className="row",
                        #     children=[
                        #         html.Div(
                        #             className="div-for-dropdown",
                        #             children=[
                        #                 variedades_drop["drop"]
                        #             ],
                        #         ),
                        #     ],
                        # ),
                        # html.P('Seleccione un bloque'),
                        # html.Div(
                        #     className="row",
                        #     children=[
                        #         html.Div(
                        #             className="div-for-dropdown",
                        #             children=[
                        #                 bloques_drop["drop"]
                        #             ],
                        #         ),
                        #     ],
                        # ),
                        html.Div(html.Button('Calcular', id='play_button',className="me-1", n_clicks=0,style={"textalign":"center"})),
                        html.P([
                        html.Span("Advertencia: ", style={"color": "orange"}),
                        html.Span("las predicciones de este modelo son estadísticas y están sujetas a errores.")],style={"margin-top":"40px"}),
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        # html.Div(table,style={"height":"30%"}),
                        html.Div(id="container-button-basic"),#style={"height":"50%"}),
                        html.Div(flowers_graph,style={"height":"20%"}),
                    ],
                ),
            ],
            style={"margin-top":"0px","padding":"0px"}
        )
    ]
)


# @app.callback(
#     Output(component_id= 'date_start', component_property='date'),
#     # Output(component_id= 'date_end', component_property='date'),
#     Input(component_id='dropletter', component_property='value')
# )
def update_time_range(input_range):
    """Control time range selection."""
    start_date=last_year_date
    end_date=date.today()
    if input_range == 'Próxima semana':
        end_date = next_week_date
    elif input_range == 'Próximo mes':
        end_date =next_month_date
    else:
        end_date = next_month_date
    start_date = date.today()
    return start_date#, end_date

####################### CALL BACK UPDATE GRAPHS
# @app.callback(

#     Output(component_id='stems_graph', component_property='figure'),
#     Output('container-button-basic', component_property='children'),
#     # Output(component_id='play_button',component_property='enabled'),
#     # Output(component_id='play_button',component_property="n_clicks"),

#     State(component_id= 'date_start', component_property='date'),
#     # Input(component_id= 'date_end', component_property='date'),
#     State(component_id='variedades_drop', component_property='value'),
#     State(component_id='bloques_drop', component_property='value'),
#     Input(component_id='play_button',component_property="n_clicks")

# )
def update_graphs(start_date,variedades_selected,bloques_selected,n_clicks):

    ################### FILTER BY DATE
    #end_date_prediction =pd.to_datetime(end_date).to_pydatetime()
    start_date_prediction =(pd.to_datetime(start_date).to_pydatetime())
    end_date_prediction=(start_date_prediction+timedelta(days=15))
    starting_date_planted = (start_date_prediction- timedelta(days = 120)).date()
    filtered_df=filter_planted_after(df,starting_date_planted)


    ########### This is to make sure that the value of dropdown is a list.
    ############ In case only one option is chosen, the value becomes a string, which is annoying.
    if type(variedades_selected)!=list:
        variedades_selected=[variedades_selected]
    if type(bloques_selected)!=list:
        bloques_selected=[bloques_selected]


    ################### FILTER BY BLOCK
    if type(bloques_selected)!=list:
        bloques_selected=[bloques_selected]

    # if "Todos los bloques" not in bloques_selected:
    #     df=df#[df["block"].isin(70,68)]
    # print(bloques_selected)

    if "Todos los bloques" not in bloques_selected:
        filtered_df=df[df["block"].isin(bloques_selected)]


    df_report = pd.DataFrame()





    ################################### MAKE GRAPH
    A=date(2021,7,1)
    B=A+timedelta(days=15)
    dias=daterange(start_date_prediction,end_date_prediction)
    #print(dias)
    var=dict()
    for variedad in variedades_selected:
        draw_df=pd.DataFrame()
        draw_df["x"]=dias
        draw_df["y"]=list(map(lambda z: get_available_stalks(filtered_df[filtered_df["variety"]==variedad],z,1),dias))
        var[variedad]=draw_df

        ##############UPDATE REPORT

        tallos_sembrados=filtered_df[filtered_df["variety"]==variedad]["stems"].sum()
        tallos_sembrados=f"{tallos_sembrados:,}"
        disponibles=get_available_stalks(filtered_df[filtered_df["variety"]==variedad],end_date_prediction,1)
        disponibles=f"{disponibles:,}"
        row=pd.DataFrame({"Variedad":variedad.capitalize(),"Tallos sembrados":tallos_sembrados,"Disponibles en "+str(end_date_prediction.date()):disponibles},index=[0])
        df_report=pd.concat([df_report,row])#,ignore_index=True)
    flowers_graph=scatter_graph("aneto",var)

    report = dbc.Table.from_dataframe(df_report, striped=True, bordered=True, hover=True,style={"width":"100%","margin-bottom":"20px","margin-top":"60px","margin-left":"20px"},id="info_table")

    return  flowers_graph,report#,True#,0#,number_of_tests,average,positive_rate


#######################################################
# @app.callback(


#     Output(component_id='play_button',component_property="disabled"),
#     Input(component_id='stems_graph', component_property='figure')

# )
# def unpush(thing):
#     return False
if __name__ == "__main__":
    app.run_server(debug=True)
