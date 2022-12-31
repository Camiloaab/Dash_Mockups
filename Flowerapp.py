import dash
from dash import dcc
from dash import html,dash_table
import pandas as pd
import numpy as np
import plotly.express as px
from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
import dash_bootstrap_components as dbc
from datetime import date
from sample_data import sensitivity_list,choices,last_week_date, last_year_date, last_month_date,results_list,genotype_list,type_list,next_month_date,next_year_date,next_week_date
from be.controllers.filtering_tools import filter_dataframe,make_plotable,next_monday
from be.controllers.scatter_plot import scatter_graph
from be.controllers.adequacy_bar_graph import make_adequacy_graph
from be.controllers.sensitivity_graph import sensitivity_scatter_graph


######################### SOME DATA
bloques_list=['Bloque 23', 'Bloque 30', 'Bloque 33', 'Bloque 39', 'Bloque 55', 'Bloque 64','Todos los bloques']
variedades_list=['Potomac crimson',
 'Potomac early orange',
 'Potomac early rosse',
 'Potomac early white',
 'Potomac early pink',
 'Potomac early yellow',
 'Alma',
 'Soleado',
 'Aneto',
 'Veronica',
 'Candy crush mint',
 'Candy crush red',
 'Lucy',
 'Skylie']
########################
###########################
df_info = pd.DataFrame(columns=["Variedad","Tallos sembrados","Disponibles a fin del periodo"])
for variedad in variedades_list[:5]:
    row=pd.DataFrame({"Variedad":variedad,"Tallos sembrados":np.random.choice(range(1000,2000)),"Disponibles a fin del periodo":np.random.choice(range(1000,1800))},index=[0])
    df_info=pd.concat([df_info,row])#,ignore_index=True)
# info=dbc.Table(dftest.to_dict('records'), [{"name": i, "id": i} for i in dftest.columns])
# df_info=pd.read_csv("info_df.csv")

info = dbc.Table.from_dataframe(df_info, striped=True, bordered=True, hover=True,style={"width":"100%","margin-bottom":"20px","margin-top":"60px","margin-left":"20px"},id="info_table")




Records_df=pd.read_csv("Records.csv")
Records_df["day"]=pd.to_datetime(Records_df["day"])

############# GRAPH BY TYPE


# filtered_df=filter_dataframe(frequency_df,pd.to_datetime(last_month_date),pd.to_datetime(last_week_date))
# type_graph= scatter_graph(filtered_df,"Liquid based",["All"]+type_list)

table_header = [
    html.Thead(html.Tr([html.Th("Tests"), html.Th("Daily Avg"),html.Th("Positivity rate")]))
]

row1 = html.Tr([html.Td("345",id="tests"), html.Td("45.6",id="average"),html.Td("Positivity rate",id="positivity_rate")])


table_body = [html.Tbody([row1])]

table = dbc.Table(table_header + table_body, bordered=True,style={"width":"100%","margin-bottom":"20px","margin-top":"60px","margin-left":"20px"})
###############
def make_drop(lista:list,id:str,multi=False):
    menu=dcc.Dropdown(id=id,
    options=[ {"label": i, "value": i} for i in lista],
    value=lista[-1],
    clearable=False,
    multi=multi


        )
    return {"drop":menu}


###################  GENERATE THE DROPDOWN ELEMENTS  #######################


dropletter=make_drop(['Próxima semana', 'Próximo mes'],"dropletter")
type_drop=make_drop(type_list+["All test types"],"type")
results_drop=make_drop(results_list+["All results"],"results")###### it starts at 1 to rule out the "All results" option
genotype_drop=make_drop(genotype_list+["All genotypes"],"genotype")
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
                                src=app.get_asset_url("trigal.png"),
                                style={"width":"100%","height":"20%"}
                            ),
                            href="https://umiamihealth.org/en/",
                        ),
                        html.H1("Pronóstico de producción",style={"text-align":"center"}),
                        html.P('Seleccione un periodo de tiempo para hacer el pronóstico'),
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        dropletter["drop"]
                                    ],
                                ),
                            ],
                        ),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.DatePickerSingle(
                                    id = 'date_start',
                                    style={"width":"100%"}
                                        )
                            ],
                        ),
                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.DatePickerSingle(
                                    id = 'date_end',
                                    style={"width":"100%"}
                                        )
                            ],
                        ),
                        html.P('Seleccione una variedad'),
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        variedades_drop["drop"]
                                    ],
                                ),
                            ],
                        ),
                        html.P('Seleccione un bloque'),
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        bloques_drop["drop"]
                                    ],
                                ),
                            ],
                        ),
                        #table,
                        #drawFigure("200px","sensitivity-graph"),
                        #drawFigure("200px","adequacy-graph"),
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        # html.Div(table,style={"height":"30%"}),
                        html.Div(id="container-button-basic"),#style={"height":"50%"}),
                        html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        type_drop["drop"]
                                    ],
                                    style={"height":"50px"}
                                ),
                        html.Div(drawFigure("400px","types-graph"),style={"height":"20%"}),
                        # html.Div(id='container-button-basic')
                        #dcc.Graph(id="map-graph"),
                        # html.Div(
                        #             className="div-for-dropdown",
                        #             children=[
                        #                 # Dropdown to select times
                        #                 results_drop["drop"]
                        #             ],
                        #         ),
                        #dcc.Graph(id="histogram"),
                        # drawFigure("230px","result-graph"),
                        # html.Div(
                        #             className="div-for-dropdown",
                        #             children=[
                        #                 genotype_drop["drop"]
                        #             ],
                        #         ),
                        # drawFigure("230px","genotype-graph")
                    ],
                ),
            ],
            style={"margin-top":"0px","padding":"0px"}
        )
    ]
)


@app.callback(
    Output(component_id= 'date_start', component_property='date'),
    Output(component_id= 'date_end', component_property='date'),
    Input(component_id='dropletter', component_property='value')
)
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
    return start_date, end_date

####################### CALL BACK UPDATE GRAPHS
@app.callback(

    Output(component_id='types-graph', component_property='figure'),
    Output('container-button-basic', 'children'),
    # Output(component_id='result-graph', component_property='figure'),
    # Output(component_id='genotype-graph', component_property='figure'),
    # Output(component_id='adequacy-graph', component_property='figure'),
    # Output(component_id='sensitivity-graph', component_property='figure'),
    # Output(component_id='tests', component_property='children'),
    # Output(component_id='average', component_property='children'),
    # Output(component_id='positivity_rate', component_property='children'),

    Input(component_id= 'date_start', component_property='date'),
    Input(component_id= 'date_end', component_property='date'),
    Input(component_id='type', component_property='value'),
    Input(component_id='variedades_drop', component_property='value')

    # Input(component_id='results', component_property='value'),
    # Input(component_id='genotype', component_property='value'),

)
def update_graphs(start_date,end_date,type_label,variedades_selected):#result_label,genotype_label):
    if type_label==None:
        type_label="Liquid based"
    # if result_label==None:
    #     type_label="Negative"
    # if genotype_label==None:
    #     genotype_label="HPV 16"

    type_label=str(type_label)
    # result_label=str(result_label)
    # genotype_label=str(genotype_label)

    #################### FILTER BY DATE

    filtered_Rec_df=filter_dataframe(Records_df,pd.to_datetime(start_date),pd.to_datetime(end_date))

########### UPDATE NUMBER OF TEST
    number_of_tests=filtered_Rec_df.shape[0]

 ########## UPDATE AVERAGE
    number_of_days=filtered_Rec_df["day"].nunique()

    average="No tests"
    if number_of_days !=0:
        average=round(number_of_tests/number_of_days,1)

########## UPDATE POSITIVE RATE
    number_of_negatives=filtered_Rec_df[filtered_Rec_df["result"]=="Negative"].shape[0]
    number_of_positives=number_of_tests-number_of_negatives
    positive_rate = "No tests"
    if number_of_tests !=0:
        positive_rate=round(number_of_positives/number_of_tests,3)


################### GROUP BY WEEK WHEN NEEDED

    if pd.Timedelta(pd.to_datetime(end_date)-pd.to_datetime(start_date)).days>100:
        filtered_Rec_df["day"]=filtered_Rec_df["day"].apply(lambda z:next_monday(z))




############# GRAPH BY TYPE
    if type_label[:3]=="All":
        type_label="All"
    # if genotype_label[:3]=="All":
    #     genotype_label="All"
    # if result_label[:3]=="All":
    #     result_label="All"

    types_dict=dict()
    for possibility in ["All"]+type_list:
        types_dict[possibility]=make_plotable(filtered_Rec_df,{"type":possibility})

    type_graph=scatter_graph(type_label,types_dict)

#################################### GRAPH BY RESULT ############


    df_info = pd.DataFrame(columns=["Variedad","Tallos sembrados","Disponibles a fin del periodo"])
    for variedad in variedades_selected:
        row=pd.DataFrame({"Variedad":variedad,"Tallos sembrados":np.random.choice(range(1000,2000)),"Disponibles a fin del periodo":np.random.choice(range(1000,1800))},index=[0])
        df_info=pd.concat([df_info,row])#,ignore_index=True)


    info = dbc.Table.from_dataframe(df_info, striped=True, bordered=True, hover=True,style={"width":"100%","margin-bottom":"20px","margin-top":"60px","margin-left":"20px"},id="info_table")
    return  type_graph,info#,number_of_tests,average,positive_rate


#######################################################


if __name__ == "__main__":
    app.run_server(debug=True)
