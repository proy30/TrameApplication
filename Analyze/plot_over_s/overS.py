import plotly.graph_objects as go

def line_plot(selected_headers, filtered_data):
    x_axis = selected_headers[1] if len(selected_headers) > 1 else None
    y_axis = selected_headers[2] if len(selected_headers) > 2 else None

    x = [row[x_axis] for row in filtered_data] if x_axis else []
    y = [row[y_axis] for row in filtered_data] if y_axis else []

    return go.Figure(
        data=go.Scatter(
            x=x,
            y=y,
            mode='lines+markers',
            line=dict(color='blue', width=2),
            marker=dict(size=8)
        ),
        layout=go.Layout(
            title="Interactive 1D plot over s",
            xaxis=dict(title="s"),
            yaxis=dict(title="Y axis"),
            margin=dict(l=20, r=20, t=25, b=30)
        )
    )
