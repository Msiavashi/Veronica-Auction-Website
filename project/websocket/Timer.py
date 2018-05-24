from datetime import datetime
import time

class CountDownTimer:

    # temporary functions just for test, a utility class should handle these functions
    def dateDiffInSeconds(self, date1, date2):
        timedelta = date2 - date1
        return timedelta.days * 24 * 3600 + timedelta.seconds

    # temporary function which is described in this class previously
    def daysHoursMinutesSecondsFromSeconds(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        return (days, hours, minutes, seconds)

    def getCurrentTimerTime(self,auction_time):
        self.leaving_date = datetime.strptime(auction_time , '%Y-%m-%d %H:%M:%S')
        self.now = datetime.now()
        self.response = self.daysHoursMinutesSecondsFromSeconds(self.dateDiffInSeconds(self.now, self.leaving_date))
        return '%d days, %d hours, %d minutes, %d seconds' % self.response

    def isFinished(self):
        ctime = sum(self.response)
        if ctime == 0:
            return True

    def has_seconds(a_string):
        return "." in a_string.split(":")[2]

timer = CountDownTimer()
