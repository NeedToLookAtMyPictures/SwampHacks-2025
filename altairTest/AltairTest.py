import altair as alt
from vega_datasets import data

cars = data.cars()

# make the chart
chart = alt.Chart(cars).mark_point().encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',
).interactive()
chart.save('chart.html')