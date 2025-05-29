import re

def parse_value(val: str):
    if val == "nan":
        return None
    elif val == "inf":
        return 1e99
    elif "%" in val:
        return float(val.strip("%"))
    elif "." in val:
        return float(val)
    else:
        return int(val)

class Gem5Stat():
    def __init__(self, line: str):
        if match := re.match(r'([a-zA-Z0-9_.:-]+)\s+([0-9.]+|nan|inf)\s+# (.*)', line):
            self.name = match.group(1)
            self.value = parse_value(match.group(2))
            self.description = match.group(3)

        elif match := re.match(r'([a-zA-Z0-9_.:-]+)\s+([0-9.]+)\s+([0-9.]+)%\s+([0-9.]+)%\s*# (.*)', line):
            self.name = match.group(1)
            self.value = parse_value(match.group(2))
            self.percentage = parse_value(match.group(3))
            self.percentage_cumulative = parse_value(match.group(4))
            self.description = match.group(5)

        else:
            raise ValueError(f"Cannot parse string into gem5 stat: {line}")


def parse_gem5_stats(file_path: str) -> "list[dict[str, Gem5Stat]]":
    with open(file_path, 'r') as f:
        lines = f.readlines()

    stat_instances = []
    current_stat_instance = {}

    in_stat_instance = False

    for line in lines:
        if line.strip() == '---------- Begin Simulation Statistics ----------':
            in_stat_instance = True
            current_stat_instance = {}
        elif line.strip() == '---------- End Simulation Statistics   ----------':
            in_stat_instance = False
            stat_instances.append(current_stat_instance)
        elif in_stat_instance:
            if line == "\n":
                continue
            stat = Gem5Stat(line)
            current_stat_instance[stat.name] = stat

    return stat_instances