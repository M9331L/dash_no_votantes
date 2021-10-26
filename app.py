# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 18:15:30 2021

@author: Usuario
"""
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import os
import plotly.express as px
import pandas as pd
import pymysql



app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server


conn = pymysql.connect(host='dev.cgow0w1dxxju.us-east-1.rds.amazonaws.com',port=int(3306),user='pancho',passwd='pancho_2021',db='censo2010')

query = '''
select a.seccion_id,a.votante,sum(a.count) as cantidad, a.valor as tipo, a.concepto
from padrones2021d.nacional_stats_no_votantesPASO_PBA_viz_secciones a
where a.concepto in ('VotoDuro-Edad', 'VotoBlando-Edad', 'VotoPosible-Edad', 'VotoImposible-Edad') 
group by a.seccion_id, a.votante,a.valor,a.concepto;'''
df = pd.read_sql_query(query,conn)
df['concepto'] = df['concepto'].str[:-5]
df["cantidad_str"] = df["cantidad"].apply(lambda x : "{:,.0f}".format(x))
df.head()

query = '''
select a.seccion_id,'Total' as votante, (sum(a.count) + cantidad_n) as cantidad, a.valor as tipo, a.concepto 
from padrones2021d.nacional_stats_no_votantesPASO_PBA_viz_secciones a
 inner join
 (select b.seccion_id,b.votante, sum(b.count) as cantidad_n,b.valor, b.concepto from padrones2021d.nacional_stats_no_votantesPASO_PBA_viz_secciones b
 where b.concepto in ('VotoDuro-Edad', 'VotoBlando-Edad', 'VotoPosible-Edad', 'VotoImposible-Edad') and b.votante='No Votantes'
  group by b.seccion_id, b.votante,b.valor,b.concepto) b
on a.seccion_id = b.seccion_id and a.valor = b.valor and a.concepto=b.concepto
where a.concepto in ('VotoDuro-Edad', 'VotoBlando-Edad', 'VotoPosible-Edad', 'VotoImposible-Edad') and a.votante='Votantes'
group by a.seccion_id, a.votante,a.valor,a.concepto;'''
df_1 = pd.read_sql_query(query,conn)
df_1['concepto'] = df_1['concepto'].str[:-5]
df_1["cantidad_str"] = df_1["cantidad"].apply(lambda x : "{:,.0f}".format(x))
df_1.head()

df_final = pd.concat([df,df_1])


path_data = "data"
data_name = os.path.join(path_data,'municipios_completo.csv')
name = pd.read_csv(data_name)
rango = pd.DataFrame({'tipo':['1','2','3','4','5','6'],'rango':['16_17','18_29','30_44','45_69','70_85','85omas']})


df_final = df_final.merge(name,on='seccion_id')
df_final = df_final.merge(rango,on='tipo')


data_anios = os.path.join(path_data,'voto_y_no_voto_anios.csv')
df_anios = pd.read_csv(data_anios)


# Create the dash layout
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                html.Div(
                className="three columns div-user-controls",
                children=[
                    html.Div(
                        className='row',
                        children=[
                            html.Img(
                            className="logo", src=app.get_asset_url("dash-logo-new.png")
                        ),

                        html.Div(
                            children=[
                                html.H2("VOTANTES Y NO VOTANTES PROVINCIA DE BUENOS AIRES"),
                        html.P(
                            """Analisis de datos de los votantes y no votantes de PBA en el añio 2021, 2017 y 2015"""
                        ),                    
                            ]
                        ),
                        html.Hr(),
                        html.H6('Seleccione concepto'),

                    
                    html.Div(
                        className='div-for-dropdown',
                        children=[
                            dcc.RadioItems(
                                id='concept',
                        options=[
                                 {'label': 'Votantes', 'value': 'Votantes'},
                                 {'label': 'No votantes', 'value': 'No Votantes'},
                                 {'label': 'Total', 'value': 'Total'},
                        ],
                        value='No Votantes',
                    )

                        ]
                    ),  

                    html.H6('Seleccione Municipio'),

                      html.Div(
                        className='div-for-dropdown',
                        children=[
                            dcc.Dropdown(
                                id="my_dropdown",
                                options=[
                                {'label': 	"	Adolfo Alsina	"	, 'value': 	1	},
                                {'label': 	"	Alberti	"	, 'value': 	2	},
                                {'label': 	"	Almirante Brown	"	, 'value': 	3	},
                                {'label': 	"	Avellaneda	"	, 'value': 	4	},
                                {'label': 	"	Ayacucho	"	, 'value': 	5	},
                                {'label': 	"	Azul	"	, 'value': 	6	},
                                {'label': 	"	Bahia Blanca	"	, 'value': 	7	},
                                {'label': 	"	Balcarce	"	, 'value': 	8	},
                                {'label': 	"	Baradero	"	, 'value': 	9	},
                                {'label': 	"	Arrecifes	"	, 'value': 	10	},
                                {'label': 	"	Berazategui	"	, 'value': 	11	},
                                {'label': 	"	Berisso	"	, 'value': 	12	},
                                {'label': 	"	Bolivar	"	, 'value': 	13	},
                                {'label': 	"	Bragado	"	, 'value': 	14	},
                                {'label': 	"	Brandsen	"	, 'value': 	15	},
                                {'label': 	"	Campana	"	, 'value': 	16	},
                                {'label': 	"	Cañuelas	"	, 'value': 	17	},
                                {'label': 	"	Capitan Sarmiento	"	, 'value': 	18	},
                                {'label': 	"	Carlos Casares	"	, 'value': 	19	},
                                {'label': 	"	Carlos Tejedor	"	, 'value': 	20	},
                                {'label': 	"	Carmen De Areco	"	, 'value': 	21	},
                                {'label': 	"	Patagones	"	, 'value': 	22	},
                                {'label': 	"	Castelli	"	, 'value': 	23	},
                                {'label': 	"	Colon	"	, 'value': 	24	},
                                {'label': 	"	Coronel Dorrego	"	, 'value': 	25	},
                                {'label': 	"	Coronel Pringles	"	, 'value': 	26	},
                                {'label': 	"	Coronel Rosales	"	, 'value': 	27	},
                                {'label': 	"	Coronel Suarez	"	, 'value': 	28	},
                                {'label': 	"	Chacabuco	"	, 'value': 	29	},
                                {'label': 	"	Chascomus	"	, 'value': 	30	},
                                {'label': 	"	Chivilcoy	"	, 'value': 	31	},
                                {'label': 	"	Daireaux	"	, 'value': 	32	},
                                {'label': 	"	Dolores	"	, 'value': 	33	},
                                {'label': 	"	Ensenada	"	, 'value': 	34	},
                                {'label': 	"	Escobar	"	, 'value': 	35	},
                                {'label': 	"	Esteban Echeverria	"	, 'value': 	36	},
                                {'label': 	"	Exaltacion De La Cruz	"	, 'value': 	37	},
                                {'label': 	"	Florencio Varela	"	, 'value': 	38	},
                                {'label': 	"	General Alvarado	"	, 'value': 	39	},
                                {'label': 	"	General Alvear	"	, 'value': 	40	},
                                {'label': 	"	General Arenales	"	, 'value': 	41	},
                                {'label': 	"	General Belgrano	"	, 'value': 	42	},
                                {'label': 	"	General Guido	"	, 'value': 	43	},
                                {'label': 	"	General La Madrid	"	, 'value': 	44	},
                                {'label': 	"	General Las Heras	"	, 'value': 	45	},
                                {'label': 	"	General Lavalle	"	, 'value': 	46	},
                                {'label': 	"	General Madariaga	"	, 'value': 	47	},
                                {'label': 	"	General Paz	"	, 'value': 	48	},
                                {'label': 	"	General Pinto	"	, 'value': 	49	},
                                {'label': 	"	General Pueyrredon	"	, 'value': 	50	},
                                {'label': 	"	General Rodriguez	"	, 'value': 	51	},
                                {'label': 	"	General San Martin	"	, 'value': 	52	},
                                {'label': 	"	San Miguel	"	, 'value': 	53	},
                                {'label': 	"	General Viamonte	"	, 'value': 	54	},
                                {'label': 	"	General Villegas	"	, 'value': 	55	},
                                {'label': 	"	Adolfo Gonzales Chaves	"	, 'value': 	56	},
                                {'label': 	"	Guamini	"	, 'value': 	57	},
                                {'label': 	"	Hipolito Yrigoyen	"	, 'value': 	58	},
                                {'label': 	"	Benito Juarez	"	, 'value': 	59	},
                                {'label': 	"	Junin	"	, 'value': 	60	},
                                {'label': 	"	La Matanza	"	, 'value': 	61	},
                                {'label': 	"	Lanus	"	, 'value': 	62	},
                                {'label': 	"	La Plata	"	, 'value': 	63	},
                                {'label': 	"	Laprida	"	, 'value': 	64	},
                                {'label': 	"	Las Flores	"	, 'value': 	65	},
                                {'label': 	"	Leandro N. Alem	"	, 'value': 	66	},
                                {'label': 	"	Lincoln	"	, 'value': 	67	},
                                {'label': 	"	Loberia	"	, 'value': 	68	},
                                {'label': 	"	Lobos	"	, 'value': 	69	},
                                {'label': 	"	Lomas De Zamora	"	, 'value': 	70	},
                                {'label': 	"	Lujan	"	, 'value': 	71	},
                                {'label': 	"	Magdalena	"	, 'value': 	72	},
                                {'label': 	"	Maipu	"	, 'value': 	73	},
                                {'label': 	"	Mar Chiquita	"	, 'value': 	74	},
                                {'label': 	"	Marcos Paz	"	, 'value': 	75	},
                                {'label': 	"	Mercedes	"	, 'value': 	76	},
                                {'label': 	"	Merlo	"	, 'value': 	77	},
                                {'label': 	"	Monte	"	, 'value': 	78	},
                                {'label': 	"	Moreno	"	, 'value': 	79	},
                                {'label': 	"	Moron	"	, 'value': 	80	},
                                {'label': 	"	Navarro	"	, 'value': 	81	},
                                {'label': 	"	Necochea	"	, 'value': 	82	},
                                {'label': 	"	Nueve De Julio	"	, 'value': 	83	},
                                {'label': 	"	Olavarria	"	, 'value': 	84	},
                                {'label': 	"	Pehuajo	"	, 'value': 	85	},
                                {'label': 	"	Pellegrini	"	, 'value': 	86	},
                                {'label': 	"	Pergamino	"	, 'value': 	87	},
                                {'label': 	"	Pila	"	, 'value': 	88	},
                                {'label': 	"	Pilar	"	, 'value': 	89	},
                                {'label': 	"	Pinamar	"	, 'value': 	90	},
                                {'label': 	"	Puan	"	, 'value': 	91	},
                                {'label': 	"	Quilmes	"	, 'value': 	92	},
                                {'label': 	"	Ramallo	"	, 'value': 	93	},
                                {'label': 	"	Rauch	"	, 'value': 	94	},
                                {'label': 	"	Rivadavia	"	, 'value': 	95	},
                                {'label': 	"	Rojas	"	, 'value': 	96	},
                                {'label': 	"	Roque Perez	"	, 'value': 	97	},
                                {'label': 	"	Saavedra	"	, 'value': 	98	},
                                {'label': 	"	Saladillo	"	, 'value': 	99	},
                                {'label': 	"	Salliquelo	"	, 'value': 	100	},
                                {'label': 	"	Salto	"	, 'value': 	101	},
                                {'label': 	"	San Andres De Giles	"	, 'value': 	102	},
                                {'label': 	"	San Antonio De Areco	"	, 'value': 	103	},
                                {'label': 	"	San Cayetano	"	, 'value': 	104	},
                                {'label': 	"	San Fernando	"	, 'value': 	105	},
                                {'label': 	"	San Isidro	"	, 'value': 	106	},
                                {'label': 	"	San Nicolas	"	, 'value': 	107	},
                                {'label': 	"	San Pedro	"	, 'value': 	108	},
                                {'label': 	"	San Vicente	"	, 'value': 	109	},
                                {'label': 	"	Suipacha	"	, 'value': 	110	},
                                {'label': 	"	Tandil	"	, 'value': 	111	},
                                {'label': 	"	Tapalque	"	, 'value': 	112	},
                                {'label': 	"	Tigre	"	, 'value': 	113	},
                                {'label': 	"	Tornquist	"	, 'value': 	114	},
                                {'label': 	"	Trenque Lauquen	"	, 'value': 	115	},
                                {'label': 	"	Tordillo	"	, 'value': 	116	},
                                {'label': 	"	Tres Arroyos	"	, 'value': 	117	},
                                {'label': 	"	Tres De Febrero	"	, 'value': 	118	},
                                {'label': 	"	La Costa	"	, 'value': 	119	},
                                {'label': 	"	Monte Hermoso	"	, 'value': 	120	},
                                {'label': 	"	Veinticinco De Mayo	"	, 'value': 	121	},
                                {'label': 	"	Vicente Lopez	"	, 'value': 	122	},
                                {'label': 	"	Villa Gesell	"	, 'value': 	123	},
                                {'label': 	"	Villarino	"	, 'value': 	124	},
                                {'label': 	"	Zarate	"	, 'value': 	125	},
                                {'label': 	"	Tres Lomas	"	, 'value': 	126	},
                                {'label': 	"	Florentino Ameghino	"	, 'value': 	127	},
                                {'label': 	"	Presidente Peron	"	, 'value': 	128	},
                                {'label': 	"	Jose C. Paz	"	, 'value': 	129	},
                                {'label': 	"	Malvinas Argentinas	"	, 'value': 	130	},
                                {'label': 	"	Punta Indio	"	, 'value': 	131	},
                                {'label': 	"	Ezeiza	"	, 'value': 	132	},
                                {'label': 	"	Ituzaingo	"	, 'value': 	133	},
                                {'label': 	"	Hurlingham	"	, 'value': 	134	},
                                {'label': 	"	Lezama	"	, 'value': 	135	}
                                ],
                                optionHeight=35,                   
                                value=1,                    
                                disabled=False,                    
                                multi=False,                    
                                searchable=True,                
                                search_value='',                 
                                placeholder='Please select...', 
                                clearable=False,
                            )                              
                        ]
                    ),
                
                        ],
                    )                  
            ]
        ),

        # Plots
        html.Div(   
            className="nine columns div-for-charts bg-dark",             
                children=[html.Div(
                    className="row",
                    children=[
                        html.Div(
                            className='six columns',
                            children=[dcc.Graph(
                                id='the_graph',
                                config={
                                    'displayModeBar': False
                                    })]
                        ),
                        
                        html.Div(
                            className='six columns',
                            children=[dcc.Graph(
                                id='the_graph_2',
                                config={
                                    'displayModeBar': False
                                    })]
                        ),
                    ]                    
                ),
                    html.Div(
                        className='div-for-charts2',
                            children=[dcc.Graph(
                                id='the_graph_3',
                                config={
                                    'displayModeBar': False
                                    })]
                        ),                  
            ]
        ),
            ],
        ),

    ]
)

#---------------------------------------------------------------
# Connecting the Dropdown values to the graph
@app.callback(
    [Output(component_id='the_graph', component_property='figure'),
    Output(component_id='the_graph_2', component_property='figure'),
    Output(component_id='the_graph_3', component_property='figure')],
    [Input(component_id='my_dropdown', component_property='value'),
     Input(component_id='concept', component_property='value')]
)

def build_graph(num_chosen,vot):
    
    dff = df_final
    dff = dff[dff['votante'] == vot]
    dff = dff.sort_values(['votante','seccion_id','tipo'], ascending=False )
    
    fig1 = px.sunburst(dff[dff['seccion_id'] == num_chosen], path=['nombre','rango','concepto', 'cantidad_str'], values='cantidad'
                  ,color = 'rango',color_discrete_map={'16_17':'#1F77B4', '18_29':'#2CA02C', '30_44':'#FF7F0E', '45_69':'#D62728','70_85':'#9467BD','85omas':'#17BECF'})

    fig1.update_layout(bargroupgap=0, bargap=0.1, plot_bgcolor="#323130", paper_bgcolor="#323130", font=dict(size=14,color="white"),
                          title="Distribucion - Edad en Tipos de Voto", showlegend=False)
    
    fig2 = px.bar(dff[dff['seccion_id'] == num_chosen], x="concepto", y="cantidad", text="cantidad_str", color="rango",
              barmode='stack', color_discrete_map={'16_17':'#1F77B4', '18_29':'#2CA02C', '30_44':'#FF7F0E', '45_69':'#D62728','70_85':'#9467BD','85omas':'#17BECF'}
             ,category_orders={"concepto": ["VotoDuro","VotoBlando","VotoImposible","VotoPosible"]
                                                                  ,"rango": ["16_17","18_29","30_44","45_69","70_85","85omas"]})

    fig2.update_layout(xaxis_title='Tipo de Voto',yaxis_title='No Votantes',bargroupgap=0, bargap=0.1, plot_bgcolor="#323130", paper_bgcolor="#323130", font=dict(size=14,color="white"),
                       showlegend=True, legend_title = 'Rango')
    
    df_a = df_anios[df_anios['seccion_id']==str(num_chosen)]
    
    V21 = df_a['V21']
    NV21 = df_a['NV21'] 

    V21yV17 = df_a['V17yV21']
    V21yNV17 = df_a['NV17yV21']
    NV21yV17 = df_a['V17yNV21']
    NV21yNV17 = df_a['NV17yNV21']
    
    V21yV17yV15 = df_a['V15yV17yV21']
    V21yV17yNV15 = df_a['NV15yV17yV21']
    V21yNV17yV15 = df_a['V15yNV17yV21']
    V21yNV17yNV15 = df_a['NV15yNV17yV21']
    
    NV21yV17yV15 = df_a['V15yV17yNV21']
    NV21yV17yNV15 = df_a['NV15yV17yNV21']
    NV21yNV17yV15 = df_a['V15yNV17yNV21']
    NV21yNV17yNV15 = df_a['NV15yNV17yNV21']
    # data
    label = ["VOT PASO 21: "+ str(V21.values[0]), "NV PASO 21: "+ str(NV21.values[0]),
             "V21 y V17: " + str(V21yV17.values[0]), "V21 y NV17: "+ str(V21yNV17.values[0])
             ,"NV21 y V17: "+ str(NV21yV17.values[0]), "NV21 y NV17: "+ str(NV21yNV17.values[0]),
             "V21 y V17 y V15: "+ str(V21yV17yV15.values[0]),"V21 y V17 y NV15: "+ str(V21yV17yNV15.values[0])
             ,"V21 y NV17 y V15: "+ str(V21yNV17yV15.values[0]),"V21 y NV17 y NV15: "+ str(V21yNV17yNV15.values[0]),
             "NV21 y V17 y V15: "+ str(NV21yV17yV15.values[0]),"NV21 y V17 y NV15: "+ str(NV21yV17yNV15.values[0])
             ,"NV21 y NV17 y V15: "+ str(NV21yNV17yV15.values[0]),"NV21 y NV17 y NV15: "+ str(NV21yNV17yNV15.values[0])]
    
    source = [0, 0, 1, 1,
              2, 2, 3, 3,
             4, 4, 5, 5]
    target = [2, 3, 4, 5,
              6, 7, 8, 9,
             10, 11, 12, 13]
    value = [V21yV17, V21yNV17, NV21yV17, NV21yNV17, 
            V21yV17yV15, V21yV17yNV15, V21yNV17yV15, V21yNV17yNV15,
            NV21yV17yV15,NV21yV17yNV15,NV21yNV17yV15,NV21yNV17yNV15]
    
    # 4= NV PASO 15; 0= NV PASO 17; 5=VOT PASO 15; 1= VOT PASO 17; 2= NV PASO 21; 3=VOT PASO 21
    
    color_node = [
     '#2CA02C','#E74C3C', '#2CA02C', '#FFEB3B',
        '#F39C12', '#E74C3C','#2CA02C', '#FFEB3B' ,
        '#F39C12','#F39C12','#FFEB3B','#F39C12','#F39C12','#E74C3C',
    ]
    color_link = [
     '#C8E6C9','#FFF9C4', '#FFE0B2', '#FADBD8',
       '#C8E6C9', '#FFF9C4', '#FFE0B2', '#FFE0B2',
        '#FFF9C4','#FFE0B2','#FFE0B2','#FADBD8'
    ]
    # data to dict, dict to sankey
    link = dict(source = source, target = target, value = value, label=value, color=color_link)
    node = dict(label = label, pad=50, thickness=5, color=color_node)
    data = go.Sankey(link = link, node=node)
    # plot
    fig3 = go.Figure(data)      
    fig3.update_layout(bargroupgap=0, bargap=0.1, plot_bgcolor="#323130", paper_bgcolor="#323130", font=dict(size=14,color="white"),
                          title="Diagrama por añios", showlegend=False)
    return [fig1,fig2,fig3]

if __name__ == '__main__':
    app.run_server(debug=False)
#app.run_server(debug=False,host='0.0.0.0',port='8080')