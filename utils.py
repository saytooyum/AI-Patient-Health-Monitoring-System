def calculate_risk(heart_rate, spo2, temperature):

    # Critical Conditions
    if (
        heart_rate > 120
        or temperature > 38.5
        or spo2 < 90
    ):
        return "Critical"

    # Warning Conditions
    elif (
        heart_rate > 100
        or temperature > 37.5
        or spo2 < 95
    ):
        return "Warning"

    return "Normal"