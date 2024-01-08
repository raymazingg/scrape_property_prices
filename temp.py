import plotly.express as px

# Sample data
data = {
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    'Sales': [100, 120, 150, 130, 160, 140],
    'Region': ['A', 'B', 'A', 'B', 'A', 'B']
}

# Create a line chart with custom colors and category order
fig = px.line(data_frame=data, x='Month', y='Sales', color='Region',
              category_orders={'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']})

# Customize the color scale
fig.update_traces(marker=dict(size=12),
                  line=dict(width=2))

# Customize the layout
fig.update_layout(title='Monthly Sales by Region',
                  xaxis_title='Month',
                  yaxis_title='Sales')

# Show the plot
fig.show()