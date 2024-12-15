import random

# Список водителей
drivers_A = ["Driver A1", "Driver A2", "Driver A3"]
drivers_B = ["Driver B1", "Driver B2", "Driver B3"]

# Время начала маршрутов
route_times = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
# Продолжительность маршрута в часах
traffic_route_time = 1


# Проверка пересечения временных интервалов
def check_time_overlap(start1, end1, existing_routes):
    for start2, end2 in existing_routes:
        if start1 < end2 and start2 < end1:
            return True
    return False

# Проверка на соответствие рабочего времени водителя
def is_within_work_hours(start_time, end_time, work_start, work_end):
    return work_start <= start_time < work_end and work_start < end_time <= work_end

# Расчёт времени окончания маршрута
def calculate_end_time(start_time, duration):
    return start_time + duration

# Распределение маршрутов между водителями с учётом рабочего времени
def distribute_routes(driver_list, num_routes, route_duration, work_hours):
    schedule = {driver: [] for driver in driver_list}  # Создаём расписание для каждого водителя
    all_routes = []

    # Генерация всех маршрутов
    for _ in range(num_routes):
        start_time = random.choice(route_times)
        end_time = calculate_end_time(start_time, route_duration)
        all_routes.append((start_time, end_time))

    # Распределение маршрутов по кругу
    driver_index = 0
    for route in all_routes:
        assigned = False
        attempts = 0  # Счётчик попыток для предотвращения бесконечного цикла
        while not assigned and attempts < len(driver_list):
            driver = driver_list[driver_index]
            work_start, work_end = work_hours[driver]

            if (
                not check_time_overlap(route[0], route[1], schedule[driver]) and
                is_within_work_hours(route[0], route[1], work_start, work_end)
            ):
                schedule[driver].append(route)
                assigned = True

            driver_index = (driver_index + 1) % len(driver_list)  # Переход к следующему водителю
            attempts += 1

        if not assigned:
            print(f"Маршрут с {route[0]} до {route[1]} невозможно распределить!")

    return schedule

# Жадное распределение маршрутов
def greedy_distribute_routes(driver_list, num_routes, route_duration):
    schedule = {driver: [] for driver in driver_list}
    scheduled_routes = []

    all_routes = []
    for _ in range(num_routes):
        start_time = random.choice(route_times)
        end_time = calculate_end_time(start_time, route_duration)
        all_routes.append((start_time, end_time))

    for route in all_routes:
        if route in scheduled_routes:
            continue

        best_driver = None
        best_penalty = float('inf')

        for driver, routes in schedule.items():
            if not check_time_overlap(route[0], route[1], routes):
                penalty = len(routes)
                if penalty < best_penalty:
                    best_penalty = penalty
                    best_driver = driver

        if best_driver is not None:
            schedule[best_driver].append(route)
            scheduled_routes.append(route)

    return schedule

# Генерация расписания для водителей типа A
def generate_schedule_A(num_routes):
    if not drivers_A:
        print("Нет водителей типа A для создания расписания.")
        return

    work_hours_A = {driver: (8, 16) for driver in drivers_A}
    schedule = distribute_routes(drivers_A, num_routes, traffic_route_time, work_hours_A)
    display_schedule(schedule)

# Генерация расписания для водителей типа B
def generate_schedule_B(num_routes):
    if not drivers_B:
        print("Нет водителей типа B для создания расписания.")
        return

    work_hours_B = {driver: (0, 24) for driver in drivers_B}
    schedule = distribute_routes(drivers_B, num_routes, traffic_route_time, work_hours_B)
    display_schedule(schedule)

# Вывод расписания
def display_schedule(schedule):
    for driver, routes in schedule.items():
        print(f"Водитель: {driver}")
        for start, end in routes:
            print(f"  Рейс с {start}:00 до {end}:00")
        print()

# Пример вызова функций
if __name__ == "__main__":
    num_routes = 10
    print("Расписание для водителей типа A:")
    generate_schedule_A(num_routes)

    print("Расписание для водителей типа B:")
    generate_schedule_B(num_routes)
