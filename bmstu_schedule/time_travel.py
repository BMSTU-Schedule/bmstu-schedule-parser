import os

future_date_str = "DD MMM YYYY hh:mm:ss"
os.system('hwclock --set %s' % future_date_str)
