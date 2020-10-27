import plotly.graph_objects as go
import plotly.express as px

def showfig(dat, a, b, c):
    fig = px.scatter_3d(dat, x = a, y = b, z = c)
    fig.show()