import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from typing import List, Dict, Any, Tuple, Optional, Union
import base64
from io import BytesIO
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataVisualizer:
    """
    Data visualization component for analytics
    Provides various methods to create visualizations from data
    """
    
    def __init__(self, theme: str = 'plotly'):
        """
        Initialize the DataVisualizer
        
        Args:
            theme: Visualization theme ('plotly', 'seaborn', 'matplotlib')
        """
        self.theme = theme
        
        # Set up themes
        if theme == 'seaborn':
            sns.set_theme(style="whitegrid")
        elif theme == 'matplotlib':
            plt.style.use('ggplot')
    
    def create_line_chart(
        self,
        df: pd.DataFrame,
        x_column: str,
        y_columns: Union[str, List[str]],
        title: str = '',
        x_label: Optional[str] = None,
        y_label: Optional[str] = None,
        color_map: Optional[Dict[str, str]] = None,
        interactive: bool = True,
        output_format: str = 'json'
    ) -> Union[str, bytes]:
        """
        Create a line chart
        
        Args:
            df: Input DataFrame
            x_column: Column for x-axis
            y_columns: Column(s) for y-axis
            title: Chart title
            x_label: X-axis label (defaults to x_column)
            y_label: Y-axis label
            color_map: Mapping of series names to colors
            interactive: Whether to create an interactive chart
            output_format: Output format ('json', 'base64')
            
        Returns:
            JSON string or base64-encoded image
        """
        if isinstance(y_columns, str):
            y_columns = [y_columns]
        
        # Set default labels
        if x_label is None:
            x_label = x_column
        
        if interactive:
            # Create interactive plotly chart
            fig = go.Figure()
            
            for y_column in y_columns:
                color = None
                if color_map and y_column in color_map:
                    color = color_map[y_column]
                
                fig.add_trace(go.Scatter(
                    x=df[x_column],
                    y=df[y_column],
                    mode='lines+markers',
                    name=y_column,
                    line=dict(color=color) if color else None
                ))
            
            fig.update_layout(
                title=title,
                xaxis_title=x_label,
                yaxis_title=y_label,
                legend_title="Series",
                template='plotly_white'
            )
            
            if output_format == 'json':
                return json.dumps(fig.to_dict())
            else:  # base64
                img_bytes = fig.to_image(format="png")
                return base64.b64encode(img_bytes).decode('utf-8')
        
        else:
            # Create static matplotlib/seaborn chart
            plt.figure(figsize=(10, 6))
            
            for y_column in y_columns:
                color = None
                if color_map and y_column in color_map:
                    color = color_map[y_column]
                
                plt.plot(df[x_column], df[y_column], label=y_column, color=color)
            
            plt.title(title)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.legend(title="Series")
            plt.grid(True)
            plt.tight_layout()
            
            # Save to BytesIO and convert to base64 or JSON
            buf = BytesIO()
            plt.savefig(buf, format='png')
            plt.close()
            
            if output_format == 'base64':
                return base64.b64encode(buf.getvalue()).decode('utf-8')
            else:  # json
                # For non-interactive charts, we'll still return base64 data
                # but wrapped in a JSON structure for consistency
                base64_data = base64.b64encode(buf.getvalue()).decode('utf-8')
                return json.dumps({
                    "type": "image",
                    "format": "png",
                    "data": base64_data
                })
    
    def create_bar_chart(
        self,
        df: pd.DataFrame,
        x_column: str,
        y_column: str,
        title: str = '',
        x_label: Optional[str] = None,
        y_label: Optional[str] = None,
        color_column: Optional[str] = None,
        orientation: str = 'vertical',
        interactive: bool = True,
        output_format: str = 'json'
    ) -> Union[str, bytes]:
        """
        Create a bar chart
        
        Args:
            df: Input DataFrame
            x_column: Column for x-axis (categories)
            y_column: Column for y-axis (values)
            title: Chart title
            x_label: X-axis label (defaults to x_column)
            y_label: Y-axis label (defaults to y_column)
            color_column: Column to color bars by
            orientation: Bar orientation ('vertical', 'horizontal')
            interactive: Whether to create an interactive chart
            output_format: Output format ('json', 'base64')
            
        Returns:
            JSON string or base64-encoded image
        """
        # Set default labels
        if x_label is None:
            x_label = x_column
        
        if y_label is None:
            y_label = y_column
        
        if interactive:
            # Create interactive plotly chart
            if orientation == 'vertical':
                if color_column:
                    fig = px.bar(
                        df, x=x_column, y=y_column, color=color_column,
                        title=title, labels={x_column: x_label, y_column: y_label}
                    )
                else:
                    fig = px.bar(
                        df, x=x_column, y=y_column,
                        title=title, labels={x_column: x_label, y_column: y_label}
                    )
            else:  # horizontal
                if color_column:
                    fig = px.bar(
                        df, y=x_column, x=y_column, color=color_column, orientation='h',
                        title=title, labels={x_column: x_label, y_column: y_label}
                    )
                else:
                    fig = px.bar(
                        df, y=x_column, x=y_column, orientation='h',
                        title=title, labels={x_column: x_label, y_column: y_label}
                    )
            
            fig.update_layout(template='plotly_white')
            
            if output_format == 'json':
                return json.dumps(fig.to_dict())
            else:  # base64
                img_bytes = fig.to_image(format="png")
                return base64.b64encode(img_bytes).decode('utf-8')
        
        else:
            # Create static matplotlib/seaborn chart
            plt.figure(figsize=(10, 6))
            
            if orientation == 'vertical':
                if color_column:
                    sns.barplot(x=x_column, y=y_column, hue=color_column, data=df)
                else:
                    sns.barplot(x=x_column, y=y_column, data=df)
            else:  # horizontal
                if color_column:
                    sns.barplot(y=x_column, x=y_column, hue=color_column, data=df)
                else:
                    sns.barplot(y=x_column, x=y_column, data=df)
            
            plt.title(title)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.tight_layout()
            
            # Save to BytesIO and convert to base64 or JSON
            buf = BytesIO()
            plt.savefig(buf, format='png')
            plt.close()
            
            if output_format == 'base64':
                return base64.b64encode(buf.getvalue()).decode('utf-8')
            else:  # json
                base64_data = base64.b64encode(buf.getvalue()).decode('utf-8')
                return json.dumps({
                    "type": "image",
                    "format": "png",
                    "data": base64_data
                })
    
    def create_pie_chart(
        self,
        df: pd.DataFrame,
        names_column: str,
        values_column: str,
        title: str = '',
        interactive: bool = True,
        output_format: str = 'json'
    ) -> Union[str, bytes]:
        """
        Create a pie chart
        
        Args:
            df: Input DataFrame
            names_column: Column for slice names
            values_column: Column for slice values
            title: Chart title
            interactive: Whether to create an interactive chart
            output_format: Output format ('json', 'base64')
            
        Returns:
            JSON string or base64-encoded image
        """
        if interactive:
            # Create interactive plotly chart
            fig = px.pie(
                df, names=names_column, values=values_column,
                title=title
            )
            
            fig.update_layout(template='plotly_white')
            
            if output_format == 'json':
                return json.dumps(fig.to_dict())
            else:  # base64
                img_bytes = fig.to_image(format="png")
                return base64.b64encode(img_bytes).decode('utf-8')
        
        else:
            # Create static matplotlib/seaborn chart
            plt.figure(figsize=(10, 6))
            
            plt.pie(
                df[values_column],
                labels=df[names_column],
                autopct='%1.1f%%',
                startangle=90
            )
            plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
            plt.title(title)
            plt.tight_layout()
            
            # Save to BytesIO and convert to base64 or JSON
            buf = BytesIO()
            plt.savefig(buf, format='png')
            plt.close()
            
            if output_format == 'base64':
                return base64.b64encode(buf.getvalue()).decode('utf-8')
            else:  # json
                base64_data = base64.b64encode(buf.getvalue()).decode('utf-8')
                return json.dumps({
                    "type": "image",
                    "format": "png",
                    "data": base64_data
                })
    
    def create_heatmap(
        self,
        df: pd.DataFrame,
        x_column: str,
        y_column: str,
        value_column: str,
        title: str = '',
        x_label: Optional[str] = None,
        y_label: Optional[str] = None,
        color_scale: Optional[List[str]] = None,
        interactive: bool = True,
        output_format: str = 'json'
    ) -> Union[str, bytes]:
        """
        Create a heatmap
        
        Args:
            df: Input DataFrame
            x_column: Column for x-axis
            y_column: Column for y-axis
            value_column: Column for cell values
            title: Chart title
            x_label: X-axis label (defaults to x_column)
            y_label: Y-axis label (defaults to y_column)
            color_scale: Color scale for values
            interactive: Whether to create an interactive chart
            output_format: Output format ('json', 'base64')
            
        Returns:
            JSON string or base64-encoded image
        """
        # Set default labels
        if x_label is None:
            x_label = x_column
        
        if y_label is None:
            y_label = y_column
        
        # Create pivot table for heatmap
        pivot_df = df.pivot_table(
            values=value_column,
            index=y_column,
            columns=x_column,
            aggfunc='mean'
        )
        
        if interactive:
            # Create interactive plotly chart
            fig = px.imshow(
                pivot_df,
                title=title,
                labels=dict(x=x_label, y=y_label, color=value_column),
                color_continuous_scale=color_scale
            )
            
            fig.update_layout(template='plotly_white')
            
            if output_format == 'json':
                return json.dumps(fig.to_dict())
            else:  # base64
                img_bytes = fig.to_image(format="png")
                return base64.b64encode(img_bytes).decode('utf-8')
        
        else:
            # Create static matplotlib/seaborn chart
            plt.figure(figsize=(12, 8))
            
            sns.heatmap(
                pivot_df,
                annot=True,
                fmt=".1f",
                cmap=color_scale[0] if color_scale else "YlGnBu",
                linewidths=.5
            )
            
            plt.title(title)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.tight_layout()
            
            # Save to BytesIO and convert to base64 or JSON
            buf = BytesIO()
            plt.savefig(buf, format='png')
            plt.close()
            
            if output_format == 'base64':
                return base64.b64encode(buf.getvalue()).decode('utf-8')
            else:  # json
                base64_data = base64.b64encode(buf.getvalue()).decode('utf-8')
                return json.dumps({
                    "type": "image",
                    "format": "png",
                    "data": base64_data
                })
    
    def create_scatter_plot(
        self,
        df: pd.DataFrame,
        x_column: str,
        y_column: str,
        title: str = '',
        x_label: Optional[str] = None,
        y_label: Optional[str] = None,
        color_column: Optional[str] = None,
        size_column: Optional[str] = None,
        trend_line: bool = False,
        interactive: bool = True,
        output_format: str = 'json'
    ) -> Union[str, bytes]:
        """
        Create a scatter plot
        
        Args:
            df: Input DataFrame
            x_column: Column for x-axis
            y_column: Column for y-axis
            title: Chart title
            x_label: X-axis label (defaults to x_column)
            y_label: Y-axis label (defaults to y_column)
            color_column: Column to color points by
            size_column: Column to size points by
            trend_line: Whether to add a trend line
            interactive: Whether to create an interactive chart
            output_format: Output format ('json', 'base64')
            
        Returns:
            JSON string or base64-encoded image
        """
        # Set default labels
        if x_label is None:
            x_label = x_column
        
        if y_label is None:
            y_label = y_column
        
        if interactive:
            # Create interactive plotly chart
            fig = px.scatter(
                df,
                x=x_column,
                y=y_column,
                color=color_column,
                size=size_column,
                title=title,
                labels={x_column: x_label, y_column: y_label},
                trendline='ols' if trend_line else None
            )
            
            fig.update_layout(template='plotly_white')
            
            if output_format == 'json':
                return json.dumps(fig.to_dict())
            else:  # base64
                img_bytes = fig.to_image(format="png")
                return base64.b64encode(img_bytes).decode('utf-8')
        
        else:
            # Create static matplotlib/seaborn chart
            plt.figure(figsize=(10, 6))
            
            if color_column and size_column:
                scatter = plt.scatter(
                    df[x_column],
                    df[y_column],
                    c=df[color_column],
                    s=df[size_column],
                    alpha=0.6
                )
                plt.colorbar(scatter, label=color_column)
            elif color_column:
                scatter = plt.scatter(
                    df[x_column],
                    df[y_column],
                    c=df[color_column],
                    alpha=0.6
                )
                plt.colorbar(scatter, label=color_column)
            elif size_column:
                plt.scatter(
                    df[x_column],
                    df[y_column],
                    s=df[size_column],
                    alpha=0.6
                )
            else:
                plt.scatter(
                    df[x_column],
                    df[y_column],
                    alpha=0.6
                )
            
            if trend_line:
                z = np.polyfit(df[x_column], df[y_column], 1)
                p = np.poly1d(z)
                plt.plot(df[x_column], p(df[x_column]), "r--")
            
            plt.title(title)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.grid(True)
            plt.tight_layout()
            
            # Save to BytesIO and convert to base64 or JSON
            buf = BytesIO()
            plt.savefig(buf, format='png')
            plt.close()
            
            if output_format == 'base64':
                return base64.b64encode(buf.getvalue()).decode('utf-8')
            else:  # json
                base64_data = base64.b64encode(buf.getvalue()).decode('utf-8')
                return json.dumps({
                    "type": "image",
                    "format": "png",
                    "data": base64_data
                })
    
    def create_dashboard(
        self,
        charts: List[Dict[str, Any]],
        title: str = '',
        layout: Optional[List[List[int]]] = None,
        interactive: bool = True,
        output_format: str = 'json'
    ) -> Union[str, bytes]:
        """
        Create a dashboard with multiple charts
        
        Args:
            charts: List of chart configurations
            title: Dashboard title
            layout: Chart layout grid (list of lists of chart indices)
            interactive: Whether to create an interactive dashboard
            output_format: Output format ('json', 'base64')
            
        Returns:
            JSON string or base64-encoded image
        """
        if not interactive:
            # Non-interactive dashboards not supported, fallback to a series of images
            chart_images = []
            
            for chart in charts:
                chart_type = chart.get('type', '')
                chart_data = chart.get('data', pd.DataFrame())
                
                if chart_type == 'line':
                    image = self.create_line_chart(
                        df=chart_data,
                        x_column=chart.get('x_column', ''),
                        y_columns=chart.get('y_columns', []),
                        title=chart.get('title', ''),
                        interactive=False,
                        output_format='base64'
                    )
                elif chart_type == 'bar':
                    image = self.create_bar_chart(
                        df=chart_data,
                        x_column=chart.get('x_column', ''),
                        y_column=chart.get('y_column', ''),
                        title=chart.get('title', ''),
                        interactive=False,
                        output_format='base64'
                    )
                elif chart_type == 'pie':
                    image = self.create_pie_chart(
                        df=chart_data,
                        names_column=chart.get('names_column', ''),
                        values_column=chart.get('values_column', ''),
                        title=chart.get('title', ''),
                        interactive=False,
                        output_format='base64'
                    )
                else:
                    continue
                
                chart_images.append({
                    "title": chart.get('title', ''),
                    "image": image
                })
            
            return json.dumps({
                "dashboard_title": title,
                "charts": chart_images
            })
        
        # Create interactive plotly dashboard
        if layout is None:
            # Default layout: 2 charts per row
            num_charts = len(charts)
            num_rows = (num_charts + 1) // 2
            layout = []
            
            for i in range(num_rows):
                row = []
                for j in range(2):
                    chart_index = i * 2 + j
                    if chart_index < num_charts:
                        row.append(chart_index)
                layout.append(row)
        
        # Calculate subplot dimensions
        max_row = max([max(row) for row in layout]) + 1 if layout else 1
        max_col = len(layout[0]) if layout else 1
        
        # Create subplot figure
        fig = make_subplots(
            rows=max_row,
            cols=max_col,
            subplot_titles=[chart.get('title', '') for chart in charts],
            vertical_spacing=0.1
        )
        
        # Add traces for each chart
        for i, chart in enumerate(charts):
            chart_type = chart.get('type', '')
            chart_data = chart.get('data', pd.DataFrame())
            
            # Find position in layout
            row_idx = 1
            col_idx = 1
            
            for r, row in enumerate(layout):
                if i in row:
                    row_idx = r + 1
                    col_idx = row.index(i) + 1
                    break
            
            if chart_type == 'line':
                y_columns = chart.get('y_columns', [])
                if isinstance(y_columns, str):
                    y_columns = [y_columns]
                
                for y_column in y_columns:
                    fig.add_trace(
                        go.Scatter(
                            x=chart_data[chart.get('x_column', '')],
                            y=chart_data[y_column],
                            mode='lines+markers',
                            name=y_column
                        ),
                        row=row_idx,
                        col=col_idx
                    )
            
            elif chart_type == 'bar':
                fig.add_trace(
                    go.Bar(
                        x=chart_data[chart.get('x_column', '')],
                        y=chart_data[chart.get('y_column', '')],
                        name=chart.get('title', '')
                    ),
                    row=row_idx,
                    col=col_idx
                )
            
            elif chart_type == 'pie':
                fig.add_trace(
                    go.Pie(
                        labels=chart_data[chart.get('names_column', '')],
                        values=chart_data[chart.get('values_column', '')],
                        name=chart.get('title', '')
                    ),
                    row=row_idx,
                    col=col_idx
                )
            
            elif chart_type == 'scatter':
                fig.add_trace(
                    go.Scatter(
                        x=chart_data[chart.get('x_column', '')],
                        y=chart_data[chart.get('y_column', '')],
                        mode='markers',
                        name=chart.get('title', '')
                    ),
                    row=row_idx,
                    col=col_idx
                )
        
        # Update layout
        fig.update_layout(
            title_text=title,
            height=300 * max_row,
            width=500 * max_col,
            template='plotly_white'
        )
        
        if output_format == 'json':
            return json.dumps(fig.to_dict())
        else:  # base64
            img_bytes = fig.to_image(format="png")
            return base64.b64encode(img_bytes).decode('utf-8')
    
    def create_comparative_chart(
        self,
        df: pd.DataFrame,
        category_column: str,
        value_columns: List[str],
        chart_type: str = 'bar',
        title: str = '',
        interactive: bool = True,
        output_format: str = 'json'
    ) -> Union[str, bytes]:
        """
        Create a comparative chart (bar, radar, etc.)
        
        Args:
            df: Input DataFrame
            category_column: Column for categories
            value_columns: Columns for comparison
            chart_type: Type of chart ('bar', 'radar')
            title: Chart title
            interactive: Whether to create an interactive chart
            output_format: Output format ('json', 'base64')
            
        Returns:
            JSON string or base64-encoded image
        """
        if chart_type == 'bar':
            # For bar chart, reshape data to long format
            melted_df = pd.melt(
                df,
                id_vars=[category_column],
                value_vars=value_columns,
                var_name='Metric',
                value_name='Value'
            )
            
            if interactive:
                fig = px.bar(
                    melted_df,
                    x=category_column,
                    y='Value',
                    color='Metric',
                    barmode='group',
                    title=title
                )
                
                fig.update_layout(template='plotly_white')
                
                if output_format == 'json':
                    return json.dumps(fig.to_dict())
                else:  # base64
                    img_bytes = fig.to_image(format="png")
                    return base64.b64encode(img_bytes).decode('utf-8')
            
            else:
                plt.figure(figsize=(12, 8))
                
                sns.barplot(
                    x=category_column,
                    y='Value',
                    hue='Metric',
                    data=melted_df
                )
                
                plt.title(title)
                plt.legend(title='Metric')
                plt.tight_layout()
                
                # Save to BytesIO and convert to base64 or JSON
                buf = BytesIO()
                plt.savefig(buf, format='png')
                plt.close()
                
                if output_format == 'base64':
                    return base64.b64encode(buf.getvalue()).decode('utf-8')
                else:  # json
                    base64_data = base64.b64encode(buf.getvalue()).decode('utf-8')
                    return json.dumps({
                        "type": "image",
                        "format": "png",
                        "data": base64_data
                    })
        
        elif chart_type == 'radar':
            # For radar chart, prepare data in required format
            categories = df[category_column].tolist()
            
            if interactive:
                fig = go.Figure()
                
                for column in value_columns:
                    fig.add_trace(go.Scatterpolar(
                        r=df[column].tolist(),
                        theta=categories,
                        fill='toself',
                        name=column
                    ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, df[value_columns].max().max() * 1.1]
                        )
                    ),
                    title=title,
                    template='plotly_white'
                )
                
                if output_format == 'json':
                    return json.dumps(fig.to_dict())
                else:  # base64
                    img_bytes = fig.to_image(format="png")
                    return base64.b64encode(img_bytes).decode('utf-8')
            
            else:
                # Radar charts in matplotlib require more setup
                num_vars = len(categories)
                angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
                angles += angles[:1]  # Close the polygon
                
                fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
                
                for column in value_columns:
                    values = df[column].tolist()
                    values += values[:1]  # Close the polygon
                    ax.plot(angles, values, linewidth=2, label=column)
                    ax.fill(angles, values, alpha=0.25)
                
                ax.set_theta_offset(np.pi / 2)
                ax.set_theta_direction(-1)
                ax.set_thetagrids(np.degrees(angles[:-1]), categories)
                ax.set_title(title)
                ax.legend(loc='upper right')
                
                plt.tight_layout()
                
                # Save to BytesIO and convert to base64 or JSON
                buf = BytesIO()
                plt.savefig(buf, format='png')
                plt.close()
                
                if output_format == 'base64':
                    return base64.b64encode(buf.getvalue()).decode('utf-8')
                else:  # json
                    base64_data = base64.b64encode(buf.getvalue()).decode('utf-8')
                    return json.dumps({
                        "type": "image",
                        "format": "png",
                        "data": base64_data
                    })
        
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")
    
    def create_correlation_matrix(
        self,
        df: pd.DataFrame,
        columns: Optional[List[str]] = None,
        title: str = 'Correlation Matrix',
        interactive: bool = True,
        output_format: str = 'json'
    ) -> Union[str, bytes]:
        """
        Create a correlation matrix visualization
        
        Args:
            df: Input DataFrame
            columns: Columns to include in correlation matrix (if None, use all numeric columns)
            title: Chart title
            interactive: Whether to create an interactive chart
            output_format: Output format ('json', 'base64')
            
        Returns:
            JSON string or base64-encoded image
        """
        # If no columns specified, use all numeric columns
        if columns is None:
            columns = df.select_dtypes(include=['number']).columns.tolist()
        
        # Calculate correlation matrix
        corr_matrix = df[columns].corr()
        
        if interactive:
            # Create interactive plotly chart
            fig = px.imshow(
                corr_matrix,
                text_auto=True,
                color_continuous_scale='RdBu_r',
                zmin=-1,
                zmax=1,
                title=title
            )
            
            fig.update_layout(template='plotly_white')
            
            if output_format == 'json':
                return json.dumps(fig.to_dict())
            else:  # base64
                img_bytes = fig.to_image(format="png")
                return base64.b64encode(img_bytes).decode('utf-8')
        
        else:
            # Create static matplotlib/seaborn chart
            plt.figure(figsize=(10, 8))
            
            sns.heatmap(
                corr_matrix,
                annot=True,
                fmt=".2f",
                cmap='RdBu_r',
                vmin=-1,
                vmax=1,
                linewidths=.5
            )
            
            plt.title(title)
            plt.tight_layout()
            
            # Save to BytesIO and convert to base64 or JSON
            buf = BytesIO()
            plt.savefig(buf, format='png')
            plt.close()
            
            if output_format == 'base64':
                return base64.b64encode(buf.getvalue()).decode('utf-8')
            else:  # json
                base64_data = base64.b64encode(buf.getvalue()).decode('utf-8')
                return json.dumps({
                    "type": "image",
                    "format": "png",
                    "data": base64_data
                })
    
    def create_forecast_chart(
        self,
        historical_df: pd.DataFrame,
        forecast_df: pd.DataFrame,
        date_column: str,
        value_column: str,
        lower_bound_column: Optional[str] = None,
        upper_bound_column: Optional[str] = None,
        title: str = 'Forecast',
        interactive: bool = True,
        output_format: str = 'json'
    ) -> Union[str, bytes]:
        """
        Create a forecast chart with historical data and forecast
        
        Args:
            historical_df: DataFrame with historical data
            forecast_df: DataFrame with forecast data
            date_column: Column with dates
            value_column: Column with values
            lower_bound_column: Column with lower bound of forecast
            upper_bound_column: Column with upper bound of forecast
            title: Chart title
            interactive: Whether to create an interactive chart
            output_format: Output format ('json', 'base64')
            
        Returns:
            JSON string or base64-encoded image
        """
        if interactive:
            # Create interactive plotly chart
            fig = go.Figure()
            
            # Add historical data
            fig.add_trace(go.Scatter(
                x=historical_df[date_column],
                y=historical_df[value_column],
                mode='lines+markers',
                name='Historical',
                line=dict(color='blue')
            ))
            
            # Add forecast
            fig.add_trace(go.Scatter(
                x=forecast_df[date_column],
                y=forecast_df[value_column],
                mode='lines+markers',
                name='Forecast',
                line=dict(color='red', dash='dash')
            ))
            
            # Add confidence interval if provided
            if lower_bound_column and upper_bound_column:
                fig.add_trace(go.Scatter(
                    x=forecast_df[date_column],
                    y=forecast_df[lower_bound_column],
                    mode='lines',
                    line=dict(width=0),
                    showlegend=False
                ))
                fig.add_trace(go.Scatter(
                    x=forecast_df[date_column],
                    y=forecast_df[upper_bound_column],
                    mode='lines',
                    fill='tonexty',
                    fillcolor='rgba(255, 0, 0, 0.2)',
                    line=dict(width=0),
                    name='Confidence Interval'
                ))
            
            fig.update_layout(
                title=title,
                xaxis_title='Date',
                yaxis_title=value_column,
                template='plotly_white'
            )
            
            if output_format == 'json':
                return json.dumps(fig.to_dict())
            else:  # base64
                img_bytes = fig.to_image(format="png")
                return base64.b64encode(img_bytes).decode('utf-8')
        
        else:
            # Create static matplotlib/seaborn chart
            plt.figure(figsize=(12, 6))
            
            # Plot historical data
            plt.plot(
                historical_df[date_column],
                historical_df[value_column],
                'b-',
                marker='o',
                label='Historical'
            )
            
            # Plot forecast
            plt.plot(
                forecast_df[date_column],
                forecast_df[value_column],
                'r--',
                marker='o',
                label='Forecast'
            )
            
            # Add confidence interval if provided
            if lower_bound_column and upper_bound_column:
                plt.fill_between(
                    forecast_df[date_column],
                    forecast_df[lower_bound_column],
                    forecast_df[upper_bound_column],
                    color='red',
                    alpha=0.2,
                    label='Confidence Interval'
                )
            
            plt.title(title)
            plt.xlabel('Date')
            plt.ylabel(value_column)
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            
            # Save to BytesIO and convert to base64 or JSON
            buf = BytesIO()
            plt.savefig(buf, format='png')
            plt.close()
            
            if output_format == 'base64':
                return base64.b64encode(buf.getvalue()).decode('utf-8')
            else:  # json
                base64_data = base64.b64encode(buf.getvalue()).decode('utf-8')
                return json.dumps({
                    "type": "image",
                    "format": "png",
                    "data": base64_data
                })