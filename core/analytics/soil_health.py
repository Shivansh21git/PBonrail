IDEAL_RANGES = {
    "nitrogen": (50, 150),      # in ppm 
    "phosphorus": (30, 80),    # in ppm
    "potassium": (40, 200),   # in ppm
    "temperature": (18, 35),   # in °C
    "humidity": (30, 60),      # in %
}


def get_status(value, min_val, max_val):
    
    if value is None:
        return "No Data"

    if value < min_val:
        return "Low"
    elif value > max_val:
        return "High"
    else:
        return "Optimal"


def calculate_soil_health(data):
    print(type(data))
    health_report = {}
    total_parameters = len(IDEAL_RANGES)
    optimal_count = 0

    for parameter, (min_val, max_val) in IDEAL_RANGES.items():
        value = data.get(parameter)
        # print(parameter)
        # print(value)
        status = get_status(value, min_val, max_val)
        health_report[parameter]  = status
        
        if status == "Optimal":
            optimal_count += 1
    score = int((optimal_count / total_parameters) * 100)

    if score >= 80:
        label = "Healthy"
    elif score >= 60:
        label = "Moderate"
    else:
        label = "Poor"

    return {    
        "score": score,
        "label": label,
        "health_report": health_report
        }