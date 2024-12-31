def gpa_standard_points(percentage: float | int) -> float:
    if percentage >= 93:
        return 4.00
    elif 93 > percentage >= 90:
        return 3.67
    elif 90 > percentage >= 87:
        return 3.33
    elif 87 > percentage >= 83:
        return 3.00
    elif 83 > percentage >= 80:
        return 2.67
    elif 80 > percentage >= 77:
        return 2.33
    elif 77 > percentage >= 73:
        return 2.00
    elif 73 > percentage >= 70:
        return 1.67
    elif 70 > percentage >= 67:
        return 1.00
    elif 67 > percentage >= 65:
        return 1.00
    elif 65 > percentage:
        return 0.00
    else:
        return 0.00


def gpa_honors_points(percentage: float | int) -> float:
    if percentage >= 93:
        return 4.50
    elif 93 > percentage >= 90:
        return 4.17
    elif 90 > percentage >= 87:
        return 3.83
    elif 87 > percentage >= 83:
        return 3.50
    elif 83 > percentage >= 80:
        return 3.17
    elif 80 > percentage >= 77:
        return 2.83
    elif 77 > percentage >= 73:
        return 2.50
    elif 73 > percentage >= 70:
        return 2.17
    elif 70 > percentage >= 67:
        return 1.00
    elif 67 > percentage >= 65:
        return 1.00
    elif 65 > percentage:
        return 0.00
    else:
        return 0.00


def gpa_ap_points(percentage: float | int) -> float:
    if percentage >= 93:
        return 5.00
    elif 93 > percentage >= 90:
        return 4.67
    elif 90 > percentage >= 87:
        return 4.33
    elif 87 > percentage >= 83:
        return 4.00
    elif 83 > percentage >= 80:
        return 3.67
    elif 80 > percentage >= 77:
        return 3.33
    elif 77 > percentage >= 73:
        return 3.00
    elif 73 > percentage >= 70:
        return 2.67
    elif 70 > percentage >= 67:
        return 1.00
    elif 67 > percentage >= 65:
        return 1.00
    elif 65 > percentage:
        return 0.00
    else:
        return 0.00
