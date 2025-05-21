import matplotlib.pyplot as plt
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

# Initialize FastAPI app
app = FastAPI()

# Project imports
from employee_events.employee import Employee
from employee_events.team import Team

from report.utils import load_model
from report.base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable,
)
from report.combined_components import FormGroup, CombinedComponent
from report.base_components.htmx_tags import H1, Div

# Components
class ReportDropdown(Dropdown):
    def build_component(self, name, model, id=None):
        self.label = model.name
        return super().build_component(name, model)  # Removed `id`

    def component_data(self, name, model, id=None):
        return model.names()

class Header(BaseComponent):
    def build_component(self, name, model, id=None):
        return H1(model.name)

class LineChart(MatplotlibViz):
    def visualization(self, name, model, asset_id):
        import pandas as pd
        df = pd.DataFrame({
            "event_date": pd.date_range(start="2024-01-01", periods=10),
            "Positive": range(10),
            "Negative": range(10, 0, -1)
        })
        df = df.set_index("event_date")
        fig, ax = plt.subplots()
        df.plot(ax=ax)
        ax.set_title("Cumulative Event Counts")
        ax.set_xlabel("Day")
        ax.set_ylabel("Events")
        self.set_axis_styling(ax, border_color="black", font_color="black")
        return fig

class BarChart(MatplotlibViz):
    def visualization(self, name, model, asset_id):
        pred = 0.42
        fig, ax = plt.subplots()
        ax.barh([''], [pred])
        ax.set_xlim(0, 1)
        ax.set_title('Predicted Recruitment Risk', fontsize=20)
        self.set_axis_styling(ax, border_color="black", font_color="black")
        return fig

class Visualizations(CombinedComponent):
    children = [LineChart(), BarChart()]

    def outer_div(self, *args, **kwargs):
        rendered_children = [child(*args, **kwargs) for child in self.children]
        div = Div(cls='grid')
        div.children = rendered_children
        return div




class NotesTable(DataTable):
    def component_data(self, entity_id, model):
        return model.notes(entity_id)


class DashboardFilters(FormGroup):
    id = "top-filters"
    action = "/update_data"
    method = "POST"
    children = [
        Radio(values=["Employee", "Team"], name='profile_type', hx_get='/update_dropdown', hx_target='#selector'),
        ReportDropdown(id="selector", name="user-selection"),
    ]

class Report(CombinedComponent):
    children = [
        Header(),
        DashboardFilters(),
        Visualizations(),
        NotesTable(),
    ]

report = Report()

@app.get("/")
def index():
    return report(1, Employee())

@app.get("/employee/{id}")
def employee(id: str):
    return report(id, Employee())

@app.get("/team/{id}")
def team(id: str):
    return report(id, Team())

@app.get('/update_dropdown')
def update_dropdown(profile_type: str):
    dropdown = DashboardFilters.children[1]
    if profile_type == 'Team':
        return dropdown(None, Team())
    elif profile_type == 'Employee':
        return dropdown(None, Employee())

@app.post('/update_data')
async def update_data(r):
    data = await r.form()
    profile_type = data.get('profile_type')
    entity_id = data.get('user-selection')
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{entity_id}", status_code=303)
    elif profile_type == 'Team':
        return RedirectResponse(f"/team/{entity_id}", status_code=303)
