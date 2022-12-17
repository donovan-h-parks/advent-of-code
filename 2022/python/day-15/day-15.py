#! /usr/bin/env python3

from dataclasses import dataclass


@dataclass
class Sensor:
    """Position of sensor and closest beacon."""
    sx: int
    sy: int
    bx: int
    by: int


def part1(input_file: str, target_row: int) -> int:
    """Determine positions where beacon cannot be present along the given row."""

    # read position of sensors and closest beacon
    sensors = []
    with open(input_file) as f:
        for line in f:
            st, bt = line.split(':')
            sensor_x = int(st[st.find('x=')+2:st.find(',')])
            sensor_y = int(st[st.find('y=')+2:])
            beacon_x = int(bt[bt.find('x=')+2:bt.find(',')])
            beacon_y = int(bt[bt.find('y=')+2:])

            sensors.append(Sensor(sensor_x, sensor_y, beacon_x, beacon_y))

    # determine squares covered by sensors along row of interest
    covered_x = set()
    for sensor in sensors:
        sensor_dist = abs(sensor.sx-sensor.bx) + abs(sensor.sy-sensor.by)
        dx = sensor_dist - abs(sensor.sy-target_row)
        if dx < 0:
            continue

        for x in range(-dx, dx+1):
            covered_x.add(sensor.sx+x)

    # determine number of beacons along row of interest as these
    # don't count as being covered by a sensor
    beacon_x = set()
    for sensor in sensors:
        if sensor.by == target_row:
            beacon_x.add(sensor.bx)

    return len(covered_x) - len(beacon_x)


def part2(input_file: str, search_extent: int) -> int:
    """Determine tuning frequency of distress beacon."""

    # read position of sensors and closest beacon
    sensors = []
    with open(input_file) as f:
        for line in f:
            st, bt = line.split(':')
            sensor_x = int(st[st.find('x=')+2:st.find(',')])
            sensor_y = int(st[st.find('y=')+2:])
            beacon_x = int(bt[bt.find('x=')+2:bt.find(',')])
            beacon_y = int(bt[bt.find('y=')+2:])

            sensors.append(Sensor(sensor_x, sensor_y, beacon_x, beacon_y))

    # find position of distress beacon
    for x in range(0, search_extent+1):
        print(x)
        for y in range(0, search_extent+1):
            is_distress_beacon = True
            for sensor in sensors:
                sensor_dist = abs(sensor.sx-sensor.bx) + \
                    abs(sensor.sy-sensor.by)
                pos_dist = abs(sensor.sx-x) + abs(sensor.sy-y)

                if pos_dist <= sensor_dist:
                    is_distress_beacon = False
                    break

            if is_distress_beacon:
                return x*4000000 + y

    print('?')


if __name__ == '__main__':
    #assert part1('test.dat', 10) == 26
    #print(f'Part 1: {part1("input.dat", 2000000)}')

    assert part2('test.dat', 20) == 56000011
    print(f'Part 2: {part2("input.dat", 4000000)}')
