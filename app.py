from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px

app = Flask(__name__)

# Sample data path
data_path = 'your_data.csv'

def get_column_names():
    df = pd.read_csv(data_path)
    return df.columns.tolist()

def get_plot_styles():
    return ['scatter', 'line', 'lines+markers']

def get_figure(df, x_column, y_columns, plot_style):
    # Plot individual Y-axis columns
    if plot_style == 'scatter':
        fig = px.scatter(df, x=x_column, y=y_columns, title='Your Data Visualization',
                        labels={'value': 'Y-axis Values'}, color_discrete_sequence=px.colors.qualitative.Set1)
    elif plot_style == 'line':
        fig = px.line(df, x=x_column, y=y_columns, title='Your Data Visualization',
                        labels={'value': 'Y-axis Values'}, color_discrete_sequence=px.colors.qualitative.Set1)
    elif plot_style == 'lines+markers':
        fig = px.line(df, x=x_column, y=y_columns, title='Your Data Visualization',
                        labels={'value': 'Y-axis Values'}, color_discrete_sequence=px.colors.qualitative.Set1, markers=True)
    else:
        # Default
        fig = px.line(df, x=x_column, y=y_columns, title='Your Data Visualization',
                        labels={'value': 'Y-axis Values'}, color_discrete_sequence=px.colors.qualitative.Set1)

    return fig


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        x_column = request.form['x_column']
        y_columns = request.form.getlist('y_column')
        plot_style = request.form['plot_style']
        sum_y_columns = 'sum_y_columns' in request.form
        hidden_y_columns = request.form.getlist('hidden_y_columns')

        # Remove the selected x_column from y_columns if it was selected
        y_columns = [column for column in y_columns if column != x_column]

        # Reload data with selected columns
        df = pd.read_csv(data_path)

        # Calculate statistics for the selected Y-axis columns
        mean_value = df[y_columns].mean().to_dict()
        std_value = df[y_columns].std().to_dict()
        min_value = df[y_columns].min().to_dict()
        max_value = df[y_columns].max().to_dict()

        if sum_y_columns:
            # Sum the selected Y-axis columns
            df['sum_y_columns'] = df[y_columns].sum(axis=1)
            y_column_sum = ['sum_y_columns']

            mean_value = df[y_column_sum].mean().to_dict()
            std_value = df[y_column_sum].std().to_dict()
            min_value = df[y_column_sum].min().to_dict()
            max_value = df[y_column_sum].max().to_dict()

            fig_sum = get_figure(df=df, x_column=x_column, y_columns=y_column_sum, plot_style=plot_style)

            # Convert the Plotly figure to HTML
            plot_sum_html = fig_sum.to_html(full_html=False)

            return render_template(
                'index.html',
                plot_sum=plot_sum_html,
                x_column=x_column,
                y_columns=y_columns,
                column_names=get_column_names(),
                plot_styles=get_plot_styles(),
                selected_plot_style=plot_style,
                sum_y_columns=sum_y_columns,
                hidden_y_columns=hidden_y_columns,
                mean_value=mean_value,
                std_value=std_value,
                min_value=min_value,
                max_value=max_value
            )

        else:
            fig = get_figure(df=df, x_column=x_column, y_columns=y_columns, plot_style=plot_style)

            # Convert the Plotly figure to HTML
            plot_html = fig.to_html(full_html=False)

            return render_template(
                'index.html',
                plot=plot_html,
                x_column=x_column,
                y_columns=y_columns,
                column_names=get_column_names(),
                plot_styles=get_plot_styles(),
                selected_plot_style=plot_style,
                sum_y_columns=sum_y_columns,
                hidden_y_columns=hidden_y_columns,
                mean_value=mean_value,
                std_value=std_value,
                min_value=min_value,
                max_value=max_value
            )

    # Initial render without form submission (use first and second columns as default)
    df = pd.read_csv(data_path)
    default_x_column = get_column_names()[0]
    default_y_column = get_column_names()[1]

    # Calculate statistics for the default Y-axis column
    default_mean_value = df[default_y_column].mean()
    default_std_value = df[default_y_column].std()
    default_min_value = df[default_y_column].min()
    default_max_value = df[default_y_column].max()

    # Initialize empty dictionaries for statistics
    mean_value = {default_y_column: default_mean_value}
    std_value = {default_y_column: default_std_value}
    min_value = {default_y_column: default_min_value}
    max_value = {default_y_column: default_max_value}

    default_fig = px.line(df, x=default_x_column, y=[default_y_column],
                          title='Your Data Visualization', labels={'value': 'Y-axis Values'},
                          color_discrete_sequence=px.colors.qualitative.Set1)

    default_plot_html = default_fig.to_html(full_html=False)

    return render_template('index.html', plot=default_plot_html, x_column=default_x_column,
                           y_columns=[default_y_column], column_names=get_column_names(), plot_styles=get_plot_styles(),
                           selected_plot_style='lines', sum_y_columns=False,
                           mean_value=mean_value, std_value=std_value, min_value=min_value, max_value=max_value)


if __name__ == '__main__':
    app.run(debug=True)
