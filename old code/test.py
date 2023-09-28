from datetime import datetime

def is_time_in_past_or_future(time_str):
    try:
        # Parse the given time string into a datetime object with the current date
        current_date_time = datetime.now()
        time_obj = datetime.strptime(time_str, '%H:%M').replace(year=current_date_time.year, month=current_date_time.month, day=current_date_time.day)

        # Compare the parsed time with the current time
        if time_obj < current_date_time:
            return "The time is in the past."
        elif time_obj > current_date_time:
            return "The time is in the future."
        else:
            return "The time is now!"
    except ValueError:
        return "Invalid time format. Please use 'HH:MM' format, e.g., '15:21'."

# Example usage
time_str = '15:21'
result = is_time_in_past_or_future(time_str)
print(result)