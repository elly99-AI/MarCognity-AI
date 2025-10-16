# © 2025 Elena Marziali — Code released under Apache 2.0 license.
# See LICENSE in the repository for details.
# Removal of this copyright is prohibited.

# The system can analyze text and generate interactive visualizations
# (e.g., bar charts, line plots, scatter plots) using Plotly.

# === Function to generate the interactive chart ===
def extract_numeric_values(text):
    """ Extracts numeric ranges from the problem text. """
    pattern = r"(\d+)\s*-\s*(\d+)|(\d+\.\d+|\d+)\s*(K|Pa|m/s)?"
    matches = re.findall(pattern, text)

    values = []
    for match in matches:
        if match[0] and match[1]:  # Range (300 - 600)
            values.append((int(match[0]), int(match[1])))
        elif match[2]:  # Single number with optional unit
            values.append(float(match[2]))

    return values if values else [1, 10]  # Default if no numbers found

# Determines the most suitable chart type based on content
def determine_chart_type(text):
    text_lower = text.lower()
    if re.search(r"(growth|decay|population)", text_lower):
        return "exponential_growth"
    elif re.search(r"(oscillation|frequency|wave)", text_lower):
        return "sinusoidal"
    elif re.search(r"(temperature|pressure)", text_lower):
        return "temperature_pressure"
    elif re.search(r"(speed|time|acceleration)", text_lower):
        return "motion"
    elif "linear" in text_lower:
        return "linear"
    elif "logarithmic" in text_lower:
        return "logarithmic"
    elif "gaussian" in text_lower or "normal distribution" in text_lower:
        return "gaussian"
    else:
        return "generic"

# Extracts numeric values from text for visualization
def extract_numeric_values(text):
    numbers = [float(n) for n in re.findall(r"\d+(?:\.\d+)?", text)]
    if len(numbers) >= 2:
        return numbers[:2]
    elif len(numbers) == 1:
        return [numbers[0], numbers[0] + 10]
    else:
        return [1, 10]

# Generates and saves the interactive chart
# The chart is displayed in the notebook and also saved as a PNG image.
def generate_interactive_chart(problem):
    chart_type = determine_chart_type(problem)
    start, end = extract_numeric_values(problem)
    x = np.linspace(start, end, 100)
    fig = go.Figure()

    if chart_type == "exponential_growth":
        y = np.exp(x / max(x))
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="Exponential Growth"))
    elif chart_type == "sinusoidal":
        y = np.sin(x)
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="Sinusoidal Wave"))
    elif chart_type == "motion":
        y = x ** 2
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="Speed vs Time"))
    elif chart_type == "linear":
        y = x
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="Linear Trend"))
    elif chart_type == "logarithmic":
        x_log = np.where(x <= 0, 1e-3, x)
        y = np.log(x_log)
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="Logarithmic"))
    elif chart_type == "gaussian":
        mu, sigma = np.mean(x), np.std(x)
        y = np.exp(-((x - mu)**2) / (2 * sigma**2))
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="Gaussian"))
    else:
        y = np.sin(x)
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="Generic"))

    caption = f"Visualization of the '{chart_type}' model from {start} to {end} for the problem: \"{problem}\""
    fig.update_layout(
        title=caption,
        xaxis_title="X Axis",
        yaxis_title="Y Axis",
        template="plotly_white"
    )
    fig.show()

    fig.write_image("grafico_output.png", format="png", width=800, height=500)
    print("Image saved as 'grafico_output.png'")
    return fig, caption

# === Run example chart ===
example_problem = "growth"
fig, caption = generate_interactive_chart(example_problem)