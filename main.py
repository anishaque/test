import pandas as pd
import plotly.express as px
import dash
from dash import html,dcc
from dash.dependencies import Input, Output,State
from datetime import datetime
import dash_bootstrap_components as dbc
import dash_daq as daq
import plotly.graph_objects as go

data=pd.read_csv(r"C:\Users\Anishaque\Downloads\Analysis.csv")
data

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.PULSE], suppress_callback_exceptions=True)
# Calculate the total number of unique companies, users, and countries
total_companies = len(data['company_names'].unique())
total_users = len(pd.concat([data['receiver_id'], data['sender_id']]).unique())
total_countries = len(data['country'].unique())


# Create a violet-themed map
geo_distribution = px.scatter_geo(data, locations='country', locationmode='country names', color='company_names',
                         hover_name='company_names', title='<span style="color: #8A2BE2;">Geographical Distribution</span>')
geo_distribution.update_geos(
    bgcolor='#FDFEFE',
    showcoastlines=True, coastlinecolor="white",
    showland=True, landcolor="#A7FC83",
    showocean=True, oceancolor="#FDFEFE",
    showframe=False  # Remove map border
)
geo_distribution.update_layout(
    plot_bgcolor='white'  # Set white background
)


# Create a violet-themed pie chart with light pastel colors
top_companies = data.groupby('company_names')['points'].sum().nlargest(5)
pie_chart = px.pie(
    data,
    names=top_companies.index,
    values=top_companies.values,
    title='<span style="color: #8A2BE2;">Top companies by points</span>',
    color_discrete_sequence=px.colors.qualitative.Light24  # Set light pastel colors
)
pie_chart.update_traces(
    marker=dict(line=dict(color='white', width=2)),  # Add a border to pie chart slices
    textfont=dict(family="Helvetica")
)
pie_chart.update_layout(
    plot_bgcolor='white'  # Set white background
)

# Custom CSS style for rounded cards
rounded_card_style = {
    'borderRadius': '18px',
    'boxShadow': '0 4px 6px 0 rgba(255, 215, 0, 0.3)',
    'marginBottom': '20px',
    'padding': '22px'
}

violet_color = '#810380'

app.layout = html.Div([
    dbc.Container([  # Outer container with left margin
        html.H1("R&R Dashboard", style={'textAlign': 'center', 'color': '#810380', 'font-weight': '900', 'font-family': 'Brush Script','backgroundColor':'white'}),

        html.Div([
            dcc.RadioItems(
                id='summary-options',
                options=[
                    {'label': 'Overall Summary', 'value': 'overall'},
                    {'label': 'Insights', 'value': 'insights'}
                ],
                value='overall',
                labelStyle={'display': 'block'},
                inputStyle={"margin-right": "5px"},style=rounded_card_style
            ),
            html.Br(),
            html.H3(children="Select Date Range:",style={'color':'#63186B','width':'50%','font-size':'15px','font-weight':'normal','font-family'
                                                         :'Helvetica'}),
            dcc.DatePickerSingle(
                id='date-picker',
                display_format='DD/MM/YYYY',
                style={'color':'#810380','font-weight':'100','width': '50%','display': 'inline-block', 'margin-left': '20px'}
            ),
        ], style={'color':'#810380','font-weight':'400','textAlign': 'left', 'margin-top': '20px'}),
        html.Br(),
        html.Div(id='summary-content', style={'color': '#DE3163','font-weight':'bold', 'font-family': 'Helvetica'})
    ], style={'marginLeft': '8%'}),  # Apply left margin here
])


@app.callback(
    Output('summary-options', 'options'),
    [Input('date-picker', 'date')]
)
def update_summary_options(selected_date):
    # Filter data based on the selected date
    filtered_data = data[data['date'] == selected_date]

    # Create options for summary-options based on the filtered data
    options = [
        {'label': 'Data Summary', 'value': 'overall'},
        {'label': 'Insights', 'value': 'insights'}
    ]

    return options


@app.callback(
    Output('summary-content', 'children'),
    [Input('summary-options', 'value'), Input('date-picker', 'date')]
)
def update_summary(selected_option, selected_date):
    if selected_option == 'overall':
        return html.Div([
            dbc.Card(html.H2("Summary", style={'color': '#810380','font-weight':'bold','text-align': 'center'}),style=rounded_card_style),
            html.Br(),
            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.H3("Total Companies", className="card-title", style={'color': '#63186B', 'text-align': 'center'}),
                            html.P(total_companies, className="card-text", style={'color': '#63186B', 'text-align': 'center'})
                        ]),
                        style=rounded_card_style  # Apply rounded card style
                    ),
                    width={'size': 4}
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.H3("Total Users", className="card-title", style={'color': '#63186B', 'text-align': 'center'}),
                            html.P(total_users, className="card-text", style={'color': '#63186B', 'text-align': 'center'})
                        ]),
                        style=rounded_card_style  # Apply rounded card style
                    ),
                    width={'size': 3}
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.H3("Total Countries", className="card-title", style={'color': '#63186B', 'text-align': 'center'}),
                            html.P(total_countries, className="card-text", style={'color': '#63186B', 'text-align': 'center'})
                        ]),
                        style=rounded_card_style  # Apply rounded card style
                    ),
                    width={'size': 4}
                )
            ], style =rounded_card_style),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(figure=geo_distribution, config={'displayModeBar': False}),
                    style=rounded_card_style  # Apply rounded card style
                ),
                dbc.Col(
                    dcc.Graph(figure=pie_chart, config={'displayModeBar': False}),
                    style=rounded_card_style  # Apply rounded card style
                )
            ]),
            html.H5("Company", style={'color': '#810380','font-weight':'block', 'margin-top': '20px'}),
            dbc.Card(
                dcc.Dropdown(
                id='company-dropdown',
                options=[{'label': company, 'value': company} for company in data['company_names'].unique()],
                value=data['company_names'].unique()[0],
                style={'color':'#1592FA ','width': '50%'}
            ),
            style=rounded_card_style
        ),
            html.Div(id='company-summary', style={'color': '#810380', 'font-family': 'Helvetica'})
        ])
    elif selected_option == 'insights':
        return html.Div([
            dbc.Card(html.H2("Insights", style={'color': '#33F80C', 'text-align': 'center'}),style=rounded_card_style),
            dbc.Card(html.Nav([
                html.A('Country with Most Users', href='#', className='nav-link', id='country-link', n_clicks=0,style={'color': '#FC2A09'}),
                html.A('Company with Most Users', href='#', className='nav-link', id='company-link', n_clicks=0,style={'color': '#FC2A09'}),
                html.A('Most awarding sender', href='#', className='nav-link', id='sender-link', n_clicks=0,style={'color': '#FC2A09'}),
                html.A('Most awarded receiver', href='#', className='nav-link', id='receiver-link', n_clicks=0,style={'color': '#FC2A09'})


            ], className='nav', style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),style=rounded_card_style),

            html.Div(id='output-container', style={'color': 'black'})
        ])



@app.callback(
    Output('company-summary', 'children'),
    [Input('company-dropdown', 'value')]
)
def update_company_summary(selected_company):
    company_data = data[data['company_names'] == selected_company]

    receiver_amount_sum = company_data.groupby('receiver_id')['points'].sum()

    # Sort the receiver_amount_sum Series in descending order and take the top 5 receivers
    top_receivers = receiver_amount_sum.sort_values(ascending=False).head(5)

    bar_chart = px.bar(
        x=top_receivers.index,
        y=top_receivers.values,
        title=f'<span style="color: #8A2BE2;">Top receivers of {selected_company} by points</span>',
        color_discrete_sequence=['#FA1004'] * len(top_receivers)  # Set bar color to violet
    )
    bar_chart.update_layout(
        paper_bgcolor='white',  # Set white background
        plot_bgcolor='white',  # Set white background
        xaxis_title="Receiver ID",
        yaxis_title="Points"
    )
    # Set the tick format for the x-axis labels
    bar_chart.update_xaxes(tickvals=top_receivers.index, ticktext=top_receivers.index)

    time_series_data = company_data.groupby('date')['points'].sum().reset_index()
    time_series_fig = px.line(
        time_series_data,
        x='date',
        y='points',
        title=f'<span style="color: #8A2BE2;">Time series trend of points for {selected_company}</span>'
    )
    time_series_fig.update_traces(
        line=dict(color='#04FCF5')  # Set trend line color to violet
    )
    time_series_fig.update_layout(
        paper_bgcolor='white',  # Set white background
        plot_bgcolor='white',  # Set white background
        xaxis_title="Date",
        yaxis_title="Total Points"
    )

    return html.Div([
        dbc.Row([
            dbc.Col(
                dcc.Graph(figure=bar_chart, config={'displayModeBar': False}),
                style=rounded_card_style  # Apply rounded card style
            ),
            dbc.Col(
                dcc.Graph(figure=time_series_fig, config={'displayModeBar': False}),
                style=rounded_card_style  # Apply rounded card style
            )
        ])
    ])
@app.callback(
    Output('output-container', 'children'),
    [Input('country-link', 'n_clicks'),
     Input('company-link', 'n_clicks'),
     Input('sender-link', 'n_clicks'),
     Input('receiver-link', 'n_clicks')]
)
def update_output(country_clicks, company_clicks, sender_clicks, receiver_clicks):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    print(dash.callback_context.triggered[0])
    print(f"Changed ID: {changed_id}")
    print(f"Country Clicks: {country_clicks}")
    print(f"Company Clicks: {company_clicks}")
    print(f"Sender Clicks: {sender_clicks}")
    print(f"Receiver Clicks: {receiver_clicks}")

    if 'country-link' in changed_id:
        # Group the data by country, count unique senders and receivers
        country_user_counts = data.groupby("country")[["sender_id", "receiver_id"]].nunique().reset_index()

        country_user_counts.rename(columns={"sender_id": "senders", "receiver_id": "receivers"}, inplace=True)

        # Calculate the total users in each country
        country_user_counts["total_users"] = country_user_counts["senders"] + country_user_counts["receivers"]

        # Sort the countries by total users in descending order
        sorted_countries = country_user_counts.sort_values("total_users", ascending=False)

        # Get the top three countries with most users
        top_countries = sorted_countries.head(3)

        # Create a list of HTML elements for displaying the results
        result_elements = [
            html.H3("Top Countries with Most Users"),
            html.Ul([html.Li(f"{row['country']}: {row['total_users']} users") for idx, row in top_countries.iterrows()])
        ]
        return result_elements

    elif 'company-link' in changed_id:
        print("company")
        # Group the data by company_names, count unique senders and receivers
        company_user_counts = data.groupby("company_names")[["sender_id", "receiver_id"]].nunique().reset_index()
        company_user_counts.rename(columns={"sender_id": "senders", "receiver_id": "receivers"}, inplace=True)

        # Calculate the total users in each company
        company_user_counts["total_users"] = company_user_counts["senders"] + company_user_counts["receivers"]

        # Sort the companies by total users in descending order
        sorted_companies = company_user_counts.sort_values("total_users", ascending=False)

        # Get the top three companies with most users
        top_companies = sorted_companies.head(3)

        # Create a list of HTML elements for displaying the results
        result_elements = [
            html.H3("Top Companies with Most Users"),
            html.Ul([html.Li(f"{row['company_names']}: {row['total_users']} users") for idx, row in top_companies.iterrows()])
        ]
        return result_elements

    elif 'sender-link' in changed_id:
        df=data[data['Feed_type']=="Award"]
        sender_counts = df['sender_id'].value_counts()
        top_sender_ids = sender_counts.head(3)
        top_sender_elements = [html.Li(f"Sender ID: {sender}, Awards given: {count}") for sender, count in
                               top_sender_ids.items()]
        result_element = [
            html.H3("Top Senders with Most Awards Given"),
            html.Ul(top_sender_elements)]
        return result_element

    elif 'receiver-link' in changed_id:
        df=data[data['Feed_type']=="Award"]
        receiver_counts = df['receiver_id'].value_counts()
        top_receiver_ids = receiver_counts.head(3)
        top_receiver_elements = [html.Li(f"Receiver ID: {receiver}, Awards received: {count}") for receiver, count in
                               top_receiver_ids.items()]
        result_element = [
            html.H3("Top Receivers with Most Awards Received"),
            html.Ul(top_receiver_elements)]
        return result_element

if __name__ == '__main__':
    app.run_server(port=5000, debug=True)