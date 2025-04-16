from datetime import datetime
import pytz  # pip install pytz

# Example UTC time
utc_time_str = "2025-04-17T22:15:00Z"
# Convert string to datetime object
utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%SZ")

# Set as UTC timezone
utc_time = utc_time.replace(tzinfo=pytz.UTC)

# Convert to local time (e.g., America/New_York)
local_timezone = pytz.timezone("America/Santo_Domingo")
local_time = utc_time.astimezone(local_timezone)

print("Local arrival time:", local_time.strftime("%Y-%m-%d %H:%M:%S %Z"))
