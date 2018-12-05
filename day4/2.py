#!/usr/bin/env python3

# This is by far one of the worst pieces of code I've ever done, please forgive me.

import re
import pandas as pd
import numpy as np
import sys
from math import floor

parsing_regex = re.compile("^\[(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2}) (?P<hour>\d{2}):(?P<minute>\d{2})\] (?P<command>.+)")

ordered_list = []

with open("input") as input_file:
    for _, raw_command in enumerate(input_file):
        regex_command = parsing_regex.match(raw_command.replace("\n", ""))

        command_year = regex_command.group("year")
        command_month = regex_command.group("month")
        command_day = regex_command.group("day")
        command_hour = int(regex_command.group("hour"))
        command_minute = int(regex_command.group("minute"))
        command_command = regex_command.group("command")

        ordered_list.append({
            "year": command_year,
            "month": command_month,
            "day": command_day,
            "hour": command_hour,
            "minute": command_minute,
            "command": command_command,
        })

        if not command_hour in [0, 23]:
            raise Exception("Edge case we don't handle")

ordered_commands = pd.DataFrame(ordered_list, columns=["year", "month", "day", "hour", "minute", "command"])

ordered_commands.sort_values(by=["year", "month", "day", "hour", "minute"], inplace = True)

computed_durations = {}

computation_regex = re.compile("^(?P<type>(?:Guard)|(?:wakes)|(?:falls)) (?P<misc>.+)")
id_regex = re.compile("#(?P<id>\d+)")
command_id = None
curr_day = None
curr_dyear = None
curr_dmonth = None
curr_dday = None
command_id = None

last_index = ordered_commands.index.values.tolist()[-1]
for index, row in ordered_commands.iterrows():
    computed_command = computation_regex.match(row["command"])

    command_type = computed_command.group("type")

    if (not curr_day is None) and ((curr_dyear != row["year"]) or (curr_dmonth != row["month"]) or (curr_dday != row["day"]) or (command_type == "Guard")):
        if new_key in computed_durations:
            computed_durations[new_key]+= curr_day
        else:
            computed_durations[new_key] = curr_day
        curr_day = None

    if command_type == "Guard":
        command_id = int(id_regex.match(computed_command.group("misc")).group("id"))

    if curr_day is None:
        curr_dyear = row["year"]
        curr_dmonth = row["month"]
        curr_dday = row["day"]
        new_key = "{}{}{}-{}".format(curr_dyear, curr_dmonth, curr_dday, command_id)
        curr_day = []

    #command_type = "wakes" if command_type=="Guard" else command_type
    curr_day.append((command_type, row["hour"], row["minute"]))
    if last_index == index:
        if new_key in computed_durations:
            computed_durations[new_key]+= curr_day
        else:
            computed_durations[new_key] = curr_day

indexes_for_range = [[], []]
for key in computed_durations:
    datestamp, guard = key.split("-")
    indexes_for_range[0].append(int(datestamp))
    indexes_for_range[1].append(int(guard))

columns_for_range = [[], []]
for h in range(24):
    for m in range(60):
        columns_for_range[0].append(h)
        columns_for_range[1].append(m)

full_range_per_day = pd.DataFrame(np.zeros((len(indexes_for_range[0]), len(columns_for_range[0]))), index = indexes_for_range, columns = columns_for_range)

for index, item in computed_durations.items():
    datestamp, guard = index.split("-")
    datestamp = int(datestamp)
    guard = int(guard)
    beginning_of_sleep = None
    for command, hour, minute in item:
        if command == "falls":
            beginning_of_sleep = (hour, minute)
        elif (command == "wakes") and (not beginning_of_sleep is None):
            for h in range(beginning_of_sleep[0], hour+1):
                for m in range(beginning_of_sleep[1], minute):
                    full_range_per_day[h, m][datestamp, guard] = 1

full_range_per_day.index.names = ("datestamp", "guard")
full_range_per_day.columns.names = ("hour", "minute")

range_per_guard = full_range_per_day.groupby("guard")

#max_guard = range_per_guard.sum().T.sum().idxmax()
#max_minute = full_range_per_day.T.groupby("minute").sum().T.groupby("guard").sum().loc[max_guard].idxmax()

max_minute = full_range_per_day.T.groupby("minute").sum().T.groupby("guard").sum().max().idxmax()
max_guard = full_range_per_day.T.groupby("minute").sum().loc[max_minute].groupby("guard").sum().idxmax()

result = max_guard*max_minute

print("Answer for puzzle #8: {}*{}={}".format(max_guard, max_minute, result))
