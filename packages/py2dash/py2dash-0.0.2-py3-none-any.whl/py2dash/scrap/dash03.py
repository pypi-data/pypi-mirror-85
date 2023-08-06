"""Displays a dropdown with sklearn estimator classes choices and the inputs for any chosen one"""

# -*- coding: utf-8 -*-
import os
import dash
import dash_core_components as dcc
import dash_html_components as hc
from dash.dependencies import Input, Output, State

from otolite.skdash.util import extract_name_and_default, SignatureExtractor
from py2dash.component_makers import div_list_from_func
from py2dash.component_makers import dropdown_from_list

from otolite.skdash.controller import Controller, estimators
from otolite.skdash.controller import run_model

from py2dash.util import Ids

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

extract_signature = SignatureExtractor(attrs=('name', 'default', 'annotation'))

undefined = extract_name_and_default(dcc.Input)[0]['default']

func = run_model

div_list = div_list_from_func(func)
if func == run_model:
    div_list.extend([
        hc.Button(id='submit-button', n_clicks=0, children='Submit'),
        hc.Div(id='output-state')])


ids = Ids()

app.layout = hc.Div([
    hc.Div([
        hc.Label('Learner Kind'),
        dropdown_from_list(Controller.list_learner_kinds(), id=ids.learner_kind)]),
    hc.Div(id=ids.learner_maker_page,
           children=[
               dcc.Location(id='url', refresh=False),
               hc.Div(id=ids.end_of_page),
               hc.Div(id=ids.a_place_for_prints)])
])


@app.callback(
    Output(ids.end_of_page, 'children'),
    [Input(ids.learner_kind, 'value')]
)
def update_output_div(input_val):
    div_list = div_list_from_func(dict(estimators)[input_val])
    func_params = hc.Div(div_list, ids.func_params)
    submit_button = hc.Div([hc.P(), hc.Button(id=ids.submit_button, n_clicks=0, children='Submit')])
    func_params_div = hc.Div([func_params, submit_button], id=ids.func_params_div)
    return func_params_div


def ensure_bool(x):
    if isinstance(x, bool):
        return x
    else:
        if isinstance(x, str):
            if x.lower().startswith('t'):
                return True
            elif x.lower().startswith('f'):
                return False
        elif isinstance(x, int):
            return bool(x)
    raise ValueError(f"Couldn't convert to a boolean: {x}")


if __name__ == '__main__':
    app.run_server(debug=True)
