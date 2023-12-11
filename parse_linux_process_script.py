import subprocess
import datetime


def parse_ps_aux():
    output = subprocess.check_output(["ps", "aux"])
    lines = output.decode().split("\n")
    return lines


def parse_data(lines):
    users = set()
    user_processes = {}
    total_processes = 0
    max_mem = 0.0
    max_cpu = 0.0
    total_mem = 0.0
    total_cpu = 0.0
    max_mem_process = ""
    max_cpu_process = ""

    for line in lines[1:]:
        if not line:
            continue
        parts = line.split()

        user, cpu, mem, command = parts[0], float(parts[2]), float(parts[3]), parts[10]

        users.add(user)

        total_processes += 1
        user_processes[user] = user_processes.get(user, 0) + 1

        total_mem += mem
        total_cpu += cpu

        if mem > max_mem:
            max_mem = mem
            max_mem_process = command[:20]

        if cpu > max_cpu:
            max_cpu = cpu
            max_cpu_process = command[:20]

    return (
        users,
        user_processes,
        total_processes,
        total_mem,
        total_cpu,
        max_mem_process,
        max_cpu_process,
    )


def make_report(*args):
    (
        users,
        user_processes,
        total_processes,
        total_mem,
        total_cpu,
        max_mem_process,
        max_cpu_process,
    ) = args

    report = [
        "Отчёт о состоянии системы:",
        "",
        f"Пользователи системы: {', '.join(sorted(users, reverse=True))}",
        f"Процессов запущено: {total_processes}",
        "",
        "Пользовательских процессов:",
    ]

    sorted_user_processes = dict(sorted(user_processes.items(), reverse=True))

    for user, count in sorted_user_processes.items():
        report.append(f"{user}: {count}")

    report.extend(
        [
            "",
            f"Всего памяти используется: {total_mem} mb",
            f"Всего CPU используется: {total_cpu}%",
            f"Больше всего памяти использует: {max_mem_process}",
            f"Больше всего CPU использует: {max_cpu_process}",
        ]
    )

    return report


def show_report(report):
    print("\n".join(report))


def save_report(report):
    with open(datetime.datetime.now().strftime("%d-%m-%Y-%H:%M-scan.txt"), "w") as f:
        f.write("\n".join(report))


def main():
    output = parse_ps_aux()
    data_for_report = parse_data(output)
    result_report = make_report(*data_for_report)

    show_report(result_report)
    save_report(result_report)


if __name__ == "__main__":
    main()
