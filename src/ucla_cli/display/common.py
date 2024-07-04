def status_color(status):
    if "Open" in status:
        return "green"
    elif "Waitlist" in status:
        return "yellow"
    elif "Closed" in status:
        return "red"
    elif "Cancelled" in status:
        return "grey"