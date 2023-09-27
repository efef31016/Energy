from bokeh.models import Button, CustomJS, Select, ColumnDataSource, TextInput, Legend, LegendItem
from bokeh.layouts import column
from bokeh.plotting import show, figure
from bokeh.events import ButtonClick
from bokeh.layouts import gridplot


import numpy as np


x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)
options = ["sin", "cos", "tan", "cos+sin-tan"]


source1 = ColumnDataSource(data={"x": x, "y1": y})
source2 = ColumnDataSource(data={"x": x, "y2": y})
source3 = ColumnDataSource(data={"x": x, "y3": y})


select1 = Select(title="Select function 1:", options=options, value=options[0])
amp1 = TextInput(title="Input integer:", value="1")
freq1 = TextInput(title="Input integer:", value="1")
loc1 = TextInput(title="Input integer:", value="0")
select2 = Select(title="Select function 2:", options=options, value=options[0])
amp2 = TextInput(title="Input integer:", value="1")
freq2 = TextInput(title="Input integer:", value="1")
loc2 = TextInput(title="Input integer:", value="0")
select3 = Select(title="Select function 3:", options=options, value=options[0])
amp3 = TextInput(title="Input integer:", value="1")
freq3 = TextInput(title="Input integer:", value="1")
loc3 = TextInput(title="Input integer:", value="0")
button = Button(label="Click")

template = [
    [select1,select2,select3],
    [amp1,amp2,amp3],
    [freq1,freq2,freq3],
    [loc1,loc2,loc3]
]

legend = Legend(items=[LegendItem(label="Function 1", renderers=[]),
                       LegendItem(label="Function 2", renderers=[]),
                       LegendItem(label="Function 3", renderers=[])], location=(0, 0))


# color: https://docs.bokeh.org/en/latest/docs/reference/palettes.html
plot = figure(title="Function Plot", width=600, height=800)
line1 = plot.line("x", "y1", legend_label="Function 1", line_color="#de2d26", source=source1, line_width=2)
line2 = plot.line("x", "y2", legend_label="Function 2", line_color="#2ca25f", source=source2, line_width=2)
line3 = plot.line("x", "y3", legend_label="Function 3", line_color="#756bb1", source=source3, line_width=2)
plot.legend.location = "top_right"
plot.legend.title = "Functions"
plot.legend.label_text_font = "times"
plot.legend.label_text_font_style = "italic"
plot.legend.label_text_color = "navy"
plot.legend.border_line_width = 3
plot.legend.border_line_color = "navy"
plot.legend.border_line_alpha = 0.8
plot.legend.background_fill_color = "navy"
plot.legend.background_fill_alpha = 0.2


legend.items[0].renderers = [line1]
legend.items[1].renderers = [line2]
legend.items[2].renderers = [line3]


arg_dict = {"source1": source1, "source2": source2, "source3": source3,
            "template": template,"legend": legend}

callback = CustomJS(args=arg_dict, code="""
    var selected_function1 = template[0][0].value;
    var selected_function2 = template[0][1].value;
    var selected_function3 = template[0][2].value;
    var amp1 = parseInt(template[1][0].value);
    var amp2 = parseInt(template[1][1].value);
    var amp3 = parseInt(template[1][2].value);
    var freq1 = parseInt(template[2][0].value);
    var freq2 = parseInt(template[2][1].value);
    var freq3 = parseInt(template[2][2].value);
    var loc1 = parseInt(template[3][0].value);
    var loc2 = parseInt(template[3][1].value);
    var loc3 = parseInt(template[3][2].value);
    
    var x = source1.data['x'];
    var y1 = source1.data['y1'];
    var y2 = source2.data['y2'];
    var y3 = source3.data['y3'];
    
    if (selected_function1 == "sin") {
        for (var i = 0; i < x.length; i++) {
            y1[i] = amp1 * Math.sin(freq1 * (x[i]-loc1));
            legend.items[0].label = selected_function1;
        }
    } else if (selected_function1 == "cos") {
        for (var i = 0; i < x.length; i++) {
            y1[i] = amp1 * Math.cos(freq1 * (x[i]-loc1));
            legend.items[0] = selected_function1;
        }
    } else if (selected_function1 == "tan") {
        for (var i = 0; i < x.length; i++) {
            y1[i] = amp1 * Math.tan(freq1 * (x[i]-loc11));
            legend.items[0] = selected_function1;
        }
    } else if (selected_function1 == "sin+cos") {
        for (var i = 0; i < x.length; i++) {
            y1[i] = amp1 * Math.sin(freq1 * (x[i]-loc1)) + amp1 * Math.cos(freq1 * (x[i]-loc1)) - amp1 * Math.tan(freq1 * (x[i]-loc1));
            legend.items[0] = selected_function1;
        }
    }
    
    if (selected_function2 == "sin") {
        for (var i = 0; i < x.length; i++) {
            y2[i] = amp2 * Math.sin(freq2 * (x[i]-loc2));
            legend.items[1] = selected_function2;
        }
    } else if (selected_function2 == "cos") {
        for (var i = 0; i < x.length; i++) {
            y2[i] = amp2 * Math.cos(freq2 * (x[i]-loc2));
            legend.items[1] = selected_function2;
        }
    } else if (selected_function2 == "tan") {
        for (var i = 0; i < x.length; i++) {
            y2[i] = amp2 * Math.tan(freq2 * (x[i]-loc2));
            legend.items[1] = selected_function2;
        }
    } else if (selected_function2 == "sin+cos") {
        for (var i = 0; i < x.length; i++) {
            y2[i] = amp2 * Math.sin(freq2 * (x[i]-loc2)) + amp2 * Math.cos(freq2 * (x[i]-loc2)) - amp2 * Math.tan(freq2 * (x[i]-loc2));
            legend.items[1] = selected_function2;
        }
    }
    
    if (selected_function3 == "sin") {
        for (var i = 0; i < x.length; i++) {
            y3[i] = amp3 * Math.sin(freq3 * (x[i]-loc3));
            legend.items[2] = selected_function3;
        }
    } else if (selected_function3 == "cos") {
        for (var i = 0; i < x.length; i++) {
            y3[i] = amp3 * Math.cos(freq3 * (x[i]-loc3));
            legend.items[2] = selected_function3;
        }
    } else if (selected_function3 == "tan") {
        for (var i = 0; i < x.length; i++) {
           y3[i] = amp3 * Math.tan(freq3 * (x[i]-loc3));
           legend.items[2] = selected_function3;
        }
    } else if (selected_function3 == "sin+cos") {
        for (var i = 0; i < x.length; i++) {
            y3[i] = amp3 * Math.sin(freq3 * (x[i]-loc3)) + amp3 * Math.cos(freq3 * (x[i]-loc3)) - amp3 * Math.tan(freq3 * (x[i]-loc3));
            legend.items[2] = selected_function3;
        }
    }
    
    source1.change.emit();
    source2.change.emit();
    source3.change.emit();
    legend.change.emit();
""")


button.js_on_event(ButtonClick, callback)


layout = gridplot(template, toolbar_location=None)
grid = gridplot([[layout], [button], [plot]], toolbar_location=None)
show(grid)