import streamlit as st
from core import parser
from core import solver
import pulp
from pulp import LpStatus
from pulp import LpVariable
import plotly.express as px


import json
def on_click():
    st.write(parser.use_ai(user_input))


st.title("Natural Language Linear Optimisation Solver")
user_input = st.text_area("Enter optimisation problem: ", key="user_input")

if st.button("Enter"):
    names , values = [], []
    result = parser.use_ai(user_input)
    model = solver.solve(json.loads(result))
    status = LpStatus[model.status]
    st.success(status)

    if status == "Optimal":
        for var in model.variables():
            st.write(var.name, "=", var.varValue)
            names.append(var.name)
            values.append(var.varValue)
        
        fig = px.bar(
            x=names,
            y=values,
            labels={"x": "Variable", "y": "Optimal Value"},
            title="Optimal Solution",
            color=values,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)
    else:
        st.error("Does not work")
    if st.button("View log"):
        with open("run.log", "r") as file:
            content = file.read()
        st.text(content)