from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib
import numpy as np

def format_y_tick(y, _):
    if y >= 1000:
        return f'{int(y/1000)}k'
    elif y <= -1000:
        return f'{int(y/1000)}k'
    else:
        return y
    
def plot_by_date(Income_by_date,Monthly,type):
    if type == 'Income':
        color = ['#0E1B14','#5CA182','#589D7D','#A4CCB9','#F2F8F5']
    elif type == 'Spending':
        color = ['#1B0E0E','#A15C5C','#9D5858','#CCA4A4','#F5F2F2']
    elif type == 'Balance':
        color = ['#0E1B14','#5CA182','#589D7D','#A4CCB9','#F2F8F5']
    matplotlib.rcParams['font.family'] = 'Calibri'
    if type == 'Balance':
        plt.figure(figsize=(6, 5))
    else:
        plt.figure(figsize=(6, 4))
    cumulative_Income = Monthly
    all_x = []
    all_y = []
    total_Income = Monthly
    counter = 1
    for date,data in enumerate(Income_by_date):
        total_Income += data
    for date,data in enumerate(Income_by_date):
        x = int(date)
        cumulative_Income += float(data)
        y = cumulative_Income
        all_x.append(x)
        all_y.append(y)
        
        text = f"${cumulative_Income:.1f}"
        length = len(text)
        if counter%2 != 0:
            plt.annotate(text, (x, y), textcoords="offset points", xytext=(0,-10-length*4), ha='center', fontsize=8, weight='bold',color=color[0],
                        bbox=dict(boxstyle="round,pad=0.5,rounding_size=0.99", facecolor=color[4], edgecolor=color[2], lw=0.5),rotation=90)
        else:
            plt.annotate(text, (x, y), textcoords="offset points", xytext=(0,13), ha='center', fontsize=8,weight='bold',color=color[0],
                        bbox=dict(boxstyle="round,pad=0.5,rounding_size=0.99",  facecolor=color[4], edgecolor=color[2], lw=0.5),rotation=90)
        counter += 1
    plt.plot(all_x, all_y, color=color[3], zorder=1, linestyle='--')  
    plt.scatter(all_x, all_y, edgecolor=color[2], facecolor='white', zorder=2) 
    plt.xticks(rotation=45)
    plt.grid(False)
    plt.tight_layout()
    min_x = min(all_x)
    max_x = max(all_x)
    min_y = min(all_y)
    max_y = max(all_y)
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(format_y_tick))
    plt.gcf().set_facecolor(color[4])
    plt.gca().set_facecolor(color[4])
    # Set the color of all text elements
    plt.gca().set_title(f'{type}', color=color[0])  # Title
    plt.gca().set_xlabel('Date', color=color[0])  # X-axis label
    plt.gca().set_ylabel(f'Cumulative {type} ($)', color=color[0])  # Y-axis label
    plt.gca().tick_params(axis='x', color=color[0])  # X-axis tick labels
    plt.gca().tick_params(axis='y', color=color[0])  # Y-axis tick labels
    if type == 'Income':
        plt.yticks(np.linspace(0, max_y, 10))
    elif type == 'Spending':
        plt.yticks(np.linspace(min_y, 0, 10))
    elif type == 'Balance':
        plt.yticks(np.linspace(min_y, max_y, 10))

    for annotation in plt.gca().texts:
        annotation.set_color(color=color[0])
    plt.xlim(min_x-1, max_x+1)
    if type == 'Income':
        plt.ylim(min_y-(max_y-min_y)*0.5, max_y+(max_y-min_y)*0.5)
    elif type == 'Spending':
        plt.ylim(min_y-(max_y-min_y)*0.6, max_y+(max_y-min_y)*0.5)
    elif type == 'Balance':
        plt.ylim(min_y-(max_y-min_y)*0.3, max_y+(max_y-min_y)*0.3)
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=500)
    buffer.seek(0)

    return buffer
