import random

# Данные для водителей и временных интервалов
drivers_A = ["Driver A1", "Driver A2", "Driver A3"]
drivers_B = ["Driver B1", "Driver B2", "Driver B3"]
available_slots = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]  # Временные слоты для рейсов
task_duration = 1  # Длительность рейса (в часах)
work_hours_A = 8  # часы работы для A группы
work_hours_B = 8  # часы работы для B группы


# Проверка пересечения временных интервалов
def has_overlap(start1, end1, intervals):
    for start2, end2 in intervals:
        if start1 < end2 and start2 < end1:
            return True  # Времена пересекаются
    return False


# Расчет времени окончания рейса
def get_end_time(start_time, duration):
    return start_time + duration


# Создание начальных вариантов расписания
def initialize_schedules(driver_list, task_count, pool_size=100):
    schedules = []
    for _ in range(pool_size):
        allocation = {driver: [] for driver in driver_list}
        occupied_times = []  # Занятые интервалы времени
        for _ in range(task_count):
            driver = random.choice(driver_list)
            valid_slot = False
            while not valid_slot:
                start_time = random.choice(available_slots)
                end_time = get_end_time(start_time, task_duration)
                if not has_overlap(start_time, end_time, allocation[driver]):
                    allocation[driver].append((start_time, end_time))
                    occupied_times.append((start_time, end_time))
                    valid_slot = True
        schedules.append(allocation)
    return schedules


# Объединение двух вариантов расписания
def merge_allocations(parent1, parent2, driver_list):
    offspring = {driver: [] for driver in driver_list}
    for driver in driver_list:
        if random.random() > 0.5:
            offspring[driver] = parent1[driver]
        else:
            offspring[driver] = parent2[driver]
    return offspring


# Изменение существующего расписания
def modify_allocation(allocation, driver_list):
    driver = random.choice(driver_list)
    if allocation[driver]:
        allocation[driver].pop()  # Удаляем одну задачу
    occupied_times = [time for tasks in allocation.values() for time in tasks]
    valid_slot = False
    while not valid_slot:
        start_time = random.choice(available_slots)
        end_time = get_end_time(start_time, task_duration)
        if not has_overlap(start_time, end_time, occupied_times):
            allocation[driver].append((start_time, end_time))
            valid_slot = True
    return allocation


# Алгоритм для оптимизации расписания(основной)
def optimize_schedule(driver_list, work_hours, task_count, duration, max_cycles=50, pool_size=100):
    pool = initialize_schedules(driver_list, task_count, pool_size)

    for _ in range(max_cycles):
        # Оценка текущего состояния
        pool = sorted(pool, key=lambda x: evaluate_schedule(x), reverse=True)
        next_pool = pool[:10]  # Берем 10 лучших решений

        while len(next_pool) < pool_size:
            # Выбор двух "родителей"
            parent1 = random.choice(pool[:50])
            parent2 = random.choice(pool[:50])

            # Объединение
            child = merge_allocations(parent1, parent2, driver_list)

            # Изменение (с некоторой вероятностью)
            if random.random() < 0.2:
                child = modify_allocation(child, driver_list)

            next_pool.append(child)

        pool = next_pool

    # Возврат лучшего решения
    best_allocation = max(pool, key=lambda x: evaluate_schedule(x))
    return best_allocation


# Оценка качества расписания
def evaluate_schedule(allocation):
    overlaps = 0
    all_intervals = [time for tasks in allocation.values() for time in tasks]
    for i in range(len(all_intervals)):
        for j in range(i + 1, len(all_intervals)):
            if has_overlap(all_intervals[i][0], all_intervals[i][1], all_intervals[j:j + 1]):
                overlaps += 1
    return -overlaps  # Чем меньше пересечений, тем лучше


# Печать расписания рейсов
def print_schedule(allocation):
    for driver, tasks in allocation.items():
        print(f"Водитель: {driver}")
        for start, end in tasks:
            print(f"  Рейс с {start} до {end}")
        print()


# Генерация и вывод расписания
def generate_and_show(driver_list, work_hours, task_count):
    if not driver_list:
        print("Нет доступных водителей для выполнения рейсов.")
        return
    best_allocation = optimize_schedule(driver_list, work_hours, task_count, task_duration)
    print_schedule(best_allocation)


# Основной блок программы
if __name__ == "__main__":
    print("Выберите группу водителей (A или B):")
    group_choice = input().strip().upper()

    print("Введите количество рейсов:")
    try:
        tasks = int(input().strip())
        if group_choice == "A":
            generate_and_show(drivers_A, work_hours_A, tasks)
        elif group_choice == "B":
            generate_and_show(drivers_B, work_hours_B, tasks)
        else:
            print("Некорректный выбор группы. Введите 'A' или 'B'.")
    except ValueError:
        print("Ошибка: введите числовое значение для количества рейсов.")