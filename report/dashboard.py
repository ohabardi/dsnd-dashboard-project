from fasthtml.common import *
import matplotlib.pyplot as plt

from employee_events.employee import Employee
from employee_events.team import Team
from report.utils import load_model

from base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable
)

from combined_components import FormGroup, CombinedComponent

class ReportDropdown(Dropdown):
    def build_component(self, model):
        self.label = model.name
        return super().build_component(model)

    def component_data(self, model):
        return model.names()

class Header(BaseComponent):
    def build_component(self, model):
        return H1(model.name)

class LineChart(MatplotlibViz):
    def visualization(self, model, asset_id):
        df = model.event_counts(asset_id)
        df = df.fillna(0)
        df = df.set_index("date")
        df = df.sort_index()
        df = df.cumsum()
        df.columns = ["Positive", "Negative"]

        fig, ax = plt.subplots()
        df.plot(ax=ax)

        self.set_axis_styling(ax, border_color="black", font_color="black")
        ax.set_title("Cumulative Event Counts")
        ax.set_xlabel("Date")
        ax.set_ylabel("Event Count")

        return fig

class BarChart(MatplotlibViz):
    predictor = load_model()

    def visualization(self, model, asset_id):
        df = model.model_data(asset_id)
        proba = self.predictor.predict_proba(df)[:, 1]

        if model.name == "team":
            pred = proba.mean()
        else:
            pred = proba[0]

        fig, ax = plt.subplots()
        ax.barh([""], [pred])
        ax.set_xlim(0, 1)
        ax.set_title("Predicted Recruitment Risk", fontsize=20)

        self.set_axis_styling(ax, border_color="black", font_color="black")

        return fig

class Visualizations(CombinedComponent):
    children = [LineChart(), BarChart()]
    outer_div_type = Div(cls='grid')

class NotesTable(DataTable):
    def component_data(self, model, entity_id):
        return model.notes(entity_id)

class DashboardFilters(FormGroup):
    id = "top-filters"
    action = "/update_data"
    method = "POST"

    children = [
        Radio(
            values=["Employee", "Team"],
            name='profile_type',
            hx_get='/update_dropdown',
            hx_target='#selector'
        ),
        ReportDropdown(
            id="selector",
            name="user-selection")
    ]

class Report(CombinedComponent):
    children = [
        Header(),
        DashboardFilters(),
        Visualizations(),
        NotesTable()
    ]

app = App()
report = Report()

@app.get('/')
def index():
    return report(1, Employee())

@app.get('/employee/{id}')
def employee_report(id: str):
    return report(id, Employee())

@app.get('/team/{id}')
def team_report(id: str):
    return report(id, Team())

@app.get('/update_dropdown{r}')
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    print('PARAM', r.query_params['profile_type'])
    if r.query_params['profile_type'] == 'Team':
        return dropdown(None, Team())
    elif r.query_params['profile_type'] == 'Employee':
        return dropdown(None, Employee())

@app.post('/update_data')
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data._dict['profile_type']
    id = data._dict['user-selection']
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == 'Team':
        return RedirectResponse(f"/team/{id}", status_code=303)

serve()
