import subprocess
import datetime


def parse_ps_aux():
    # Инициализируем переменные для хранения информации
    users = set()
    user_processes = {}
    total_processes = 0
    max_mem = 0.0
    max_cpu = 0.0
    total_mem = 0.0
    total_cpu = 0.0
    max_mem_process = ""
    max_cpu_process = ""

    # Запускаем 'ps aux' и получаем вывод
    output = subprocess.check_output(["ps", "aux"])

    # Разделяем вывод на строки
    lines = output.decode().split("\n")

    # Обрабатываем каждую строку вывода исключая первую с названиями столбцов
    for line in lines[1:]:
        # Пропускаем пустые строки
        if not line:
            continue
        # Разделяем строку на части
        parts = line.split()
        # ['USER', 'PID', '%CPU', '%MEM', 'VSZ', 'RSS', 'TT', 'STAT', 'STARTED', 'TIME', 'COMMAND']
        user = parts[0]
        cpu = float(parts[2])
        mem = float(parts[3])
        command = parts[10] if len(parts) > 10 else ""

        # Обновляем информацию
        users.add(user)
        total_processes += 1
        # !!!!!!! я хз, объяснение внизу, я сам еще не осознал
        user_processes[user] = user_processes.get(user, 0) + 1
        total_mem += mem
        total_cpu += cpu

        # Проверяем, является ли этот процесс максимальным по использованию памяти или CPU
        if mem > max_mem:
            max_mem = mem
            max_mem_process = command[:20]

        if cpu > max_cpu:
            max_cpu = cpu
            max_cpu_process = command[:20]

    # Сортирую пользователей и процессы, что бы в начале были пользователи начинающиеся не с _
    sorted_users = sorted(users, reverse=True)
    sorted_user_processes = dict(sorted(user_processes.items(), reverse=True))

    # Формируем отчет
    report = []
    report.append("Отчёт о состоянии системы:")
    report.append("")
    report.append("Пользователи системы: " + ", ".join(sorted_users))
    report.append("Процессов запущено: " + str(total_processes))
    report.append("")
    report.append("Пользовательских процессов:")
    for user, count in sorted_user_processes.items():
        report.append(user + ": " + str(count))
    report.append("")
    report.append("Всего памяти используется: " + str(total_mem) + " mb")
    report.append("Всего CPU используется: " + str(total_cpu) + "%")
    report.append("Больше всего памяти использует: " + max_mem_process)
    report.append("Больше всего CPU использует: " + max_cpu_process)

    # Выводим отчет в стандартный вывод
    print("\n".join(report))

    # Сохраняем отчет в файл
    with open(datetime.datetime.now().strftime("%d-%m-%Y-%H:%M-scan.txt"), "w") as f:
        f.write("\n".join(report))


def main():
    parse_ps_aux()


if __name__ == "__main__":
    main()

# Подсчет количества процессов, запущенных каждым пользователем.
# user_processes - это словарь, где ключи - это имена пользователей, а значения - это количество процессов, которые они запустили.
# user_processes.get(user, 0) - это метод, который возвращает значение для данного ключа (user) из словаря user_processes. Если ключа нет в словаре, он возвращает значение по умолчанию, которое здесь равно 0. Это означает, что если пользователь еще не запустил ни одного процесса (и, следовательно, его имени еще нет в словаре), мы считаем его количество процессов равным 0.
# user_processes[user] = user_processes.get(user, 0) + 1 - это строка кода увеличивает количество процессов данного пользователя на 1. Если пользователя еще не было в словаре, он будет добавлен с количеством процессов, равным 1. Если пользователь уже был в словаре, его текущее количество процессов увеличивается на 1.
# Таким образом, после обработки всех строк вывода команды ‘ps aux’, словарь user_processes будет содержать количество процессов, запущенных каждым пользователем
