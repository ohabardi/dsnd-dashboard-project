from report.base_components.base_component import BaseComponent
import io
import base64
from matplotlib import pyplot as plt

class MatplotlibViz(BaseComponent):
    def __call__(self, entity_id, model):
        fig = self.visualization("Visualization", model, entity_id)
        return self.render_plot(fig)

    def visualization(self, name, model, asset_id):
        raise NotImplementedError("Subclasses must implement visualization()")

    def render_plot(self, fig):
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return f"<img src='data:image/png;base64,{img_base64}'/>"

    def set_axis_styling(self, ax, border_color="black", font_color="black"):
        for spine in ax.spines.values():
            spine.set_color(border_color)
        ax.xaxis.label.set_color(font_color)
        ax.yaxis.label.set_color(font_color)
        ax.title.set_color(font_color)
        ax.tick_params(axis='x', colors=font_color)
        ax.tick_params(axis='y', colors=font_color)
