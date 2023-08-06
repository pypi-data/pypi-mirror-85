"""
This module implements the command line application that will fetch the current
event date and print out how long it is from now.
"""

from datetime import datetime, timedelta

from ywit_event_countdown.countdown import get_time_difference


def main():
    """Main function to be called from entry_point script"""

    time_left = get_time_difference(datetime.now(tz=datetime.now().astimezone().tzinfo))
    days = time_left // timedelta(days=1)
    hours = time_left // timedelta(hours=1) % 24
    minutes = time_left // timedelta(minutes=1) % 60
    if minutes < 0:
        print(
            "The event has already happened. Watch https://netapp.ywit.io for"
            " next year's announcement."
        )
    else:
        print(
            f"There are {days} days, {hours} hours, and {minutes} minutes left"
            " until the next NetApp YWIT event!"
        )


if __name__ == "__main__":
    main()
