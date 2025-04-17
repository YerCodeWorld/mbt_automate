
from datetime import datetime
import pytz

def convert_time(utc_time):
    utc_time = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%SZ")
    # Set as UTC timezone | whatever witchery this does
    utc_time = utc_time.replace(tzinfo=pytz.UTC)
    local_timezone = pytz.timezone("America/Santo_Domingo")
    local_time = utc_time.astimezone(local_timezone)

    # Return converted to 12h time system
    return f"Local arrival time: {local_time.strftime("%I:%M %p")}"


print(convert_time("2025-04-17T16:21:00Z"))