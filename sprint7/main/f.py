from __future__ import annotations


def get_jumps_ways_count(stairs_count: int, max_jump: int, *, module: int) -> int:
    if module < 2:
        return 0

    if stairs_count < 1 or max_jump < 1:
        return 0

    if max_jump > stairs_count:
        max_jump = stairs_count

    jumps_ways_counts = [0] * stairs_count
    jumps_ways_counts[0] = 1

    for stair_num in range(1, len(jumps_ways_counts)):
        jumps_way_count = 0

        for jump in range(1, min(stair_num, max_jump) + 1):
            jumps_way_count += jumps_ways_counts[stair_num - jump]

        jumps_ways_counts[stair_num] = jumps_way_count % module

    return jumps_ways_counts[-1]


def main() -> None:
    stairs_count, max_jump = map(int, input().split())

    jumps_ways_count = get_jumps_ways_count(stairs_count, max_jump, module=10 ** 9 + 7)
    print(jumps_ways_count)


if __name__ == '__main__':
    main()
