from datetime import timedelta


def get_time_hh_mm_ss(sec):
    # create timedelta and convert it into string
    periods = [["year", 31536000],
               ["day", 86400],
               ["hour", 3600],
               ["minute", 60],
               ["second", 1]]

    str_ = []
    for per in periods:
        t, sec = divmod(sec, per[1])
        str_ += [f"{t} {per[0]}{'s' if t > 1 else ''},"] if t else []
    if len(str_) > 1:
        str_.insert(-1, "and")
        str_[-3] = str_[-3].rstrip(", ")
    print(str_[-3].rstrip(","))
    print(" ".join(str_).rstrip(", "))


get_time_hh_mm_ss(3233243)

