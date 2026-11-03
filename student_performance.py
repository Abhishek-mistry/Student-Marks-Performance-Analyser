from os import system, name as os_name

WIDTH = 72
MAX_MARKS = 100
PASS_MARK = 40
IMPROVE_BELOW = 50

subjects = []
students = {}


def clear_screen():
    system("cls" if os_name == "nt" else "clear")


def line(ch="="):
    print(ch * WIDTH)


def title(text):
    clear_screen()
    line()
    print(text.center(WIDTH))
    line()


def ask_number(prompt, low, high):
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
        except ValueError:
            print("  ! Please enter a number.")
            continue
        if low <= value <= high:
            return value
        print(f"  ! Value must be between {low} and {high}.")


def pause():
    input("\nPress Enter to continue...")


def need_data():
    if not subjects or not students:
        print("\n  ! No data yet. Enter marks first (option 1) or load sample data (option 9).")
        return False
    return True


def total(name):
    return sum(students[name].values())


def percentage(name):
    return total(name) / (MAX_MARKS * len(subjects)) * 100


def grade(pct):
    if pct >= 90: return "A+"
    if pct >= 80: return "A"
    if pct >= 70: return "B"
    if pct >= 60: return "C"
    if pct >= 50: return "D"
    if pct >= PASS_MARK: return "E"
    return "F"


def failed_subjects(name):
    return [s for s, m in students[name].items() if m < PASS_MARK]


def class_average():
    return sum(percentage(n) for n in students) / len(students)


def needs_improvement(name):
    return percentage(name) < IMPROVE_BELOW or bool(failed_subjects(name))


def setup_subjects():
    global subjects
    title("SET UP SUBJECTS")
    if students:
        print("Changing subjects will erase all existing student records.")
        if input("Continue? (y/n): ").strip().lower() != "y":
            return
        students.clear()
    count = int(ask_number("How many subjects? ", 1, 10))
    subjects = []
    for i in range(1, count + 1):
        while True:
            name = input(f"  Subject {i} name: ").strip().title()
            if name and name not in subjects:
                subjects.append(name)
                break
            print("  ! Name must be non-empty and unique.")
    print("\nSubjects saved:", ", ".join(subjects))


def enter_marks():
    if not subjects:
        setup_subjects()
        if not subjects:
            return
    title("ENTER MARKS")
    print(f"Marks are out of {MAX_MARKS}. Leave the name blank to stop.\n")
    while True:
        name = input("Student name: ").strip().title()
        if not name:
            break
        if name in students:
            print(f"  ({name} already exists - marks will be overwritten)")
        marks = {}
        for sub in subjects:
            marks[sub] = ask_number(f"  {sub:<15}: ", 0, MAX_MARKS)
        students[name] = marks
        print(f"  Saved {name}: total {total(name):g}, {percentage(name):.1f}%, "
              f"grade {grade(percentage(name))}\n")


def show_all_results():
    title("ALL STUDENT RESULTS")
    header = f"{'Name':<14}{'Total':>8}{'%':>8}{'Grade':>7}  Marks"
    print(header)
    line("-")
    for name in sorted(students):
        pct = percentage(name)
        marks = " ".join(f"{m:g}" for m in students[name].values())
        print(f"{name:<14}{total(name):>8g}{pct:>8.1f}{grade(pct):>7}  {marks}")
    line("-")
    print("Subject order:", ", ".join(subjects))


def highest_lowest():
    title("HIGHEST AND LOWEST MARKS")
    print(f"{'Subject':<15}{'Highest':<24}{'Lowest':<24}")
    line("-")
    for sub in subjects:
        hi = max(students, key=lambda n: students[n][sub])
        lo = min(students, key=lambda n: students[n][sub])
        print(f"{sub:<15}{hi + ' (' + format(students[hi][sub], 'g') + ')':<24}"
              f"{lo + ' (' + format(students[lo][sub], 'g') + ')':<24}")
    line("-")
    top = max(students, key=total)
    bottom = min(students, key=total)
    print(f"Overall topper : {top} with {total(top):g} marks")
    print(f"Overall lowest : {bottom} with {total(bottom):g} marks")


def show_average():
    title("CLASS AVERAGE")
    for sub in subjects:
        avg = sum(students[n][sub] for n in students) / len(students)
        bar = "#" * int(avg / MAX_MARKS * 40)
        print(f"{sub:<15}{avg:>6.1f}  {bar}")
    line("-")
    print(f"Class average percentage: {class_average():.2f}%  "
          f"(grade {grade(class_average())})")


def show_improvement():
    title("STUDENTS NEEDING IMPROVEMENT")
    print(f"Criteria: overall < {IMPROVE_BELOW}% or any subject < {PASS_MARK} marks\n")
    found = False
    for name in sorted(students):
        if needs_improvement(name):
            found = True
            weak = failed_subjects(name)
            note = f"weak in: {', '.join(weak)}" if weak else "low overall score"
            print(f"  * {name:<14}{percentage(name):>6.1f}%   {note}")
    if not found:
        print("  Great news - every student is meeting the standard!")


def summary():
    title("RESULT SUMMARY")
    total_students = len(students)
    passed = [n for n in students if not failed_subjects(n)]
    grades = {}
    for n in students:
        g = grade(percentage(n))
        grades[g] = grades.get(g, 0) + 1
    top = max(students, key=total)

    print(f"Students        : {total_students}")
    print(f"Subjects        : {', '.join(subjects)}")
    print(f"Passed all      : {len(passed)}  "
          f"({len(passed) / total_students * 100:.0f}%)")
    print(f"Need improvement: {sum(needs_improvement(n) for n in students)}")
    print(f"Class average   : {class_average():.2f}%")
    print(f"Topper          : {top} ({percentage(top):.1f}%)")
    print("\nGrade distribution:")
    for g in ["A+", "A", "B", "C", "D", "E", "F"]:
        print(f"  {g:<3}{'*' * grades.get(g, 0)} {grades.get(g, 0) or ''}")


def load_sample():
    global subjects
    subjects = ["Maths", "Science", "English", "History"]
    students.clear()
    students.update({
        "Asha":   dict(zip(subjects, [92, 88, 95, 90])),
        "Ben":    dict(zip(subjects, [45, 38, 60, 52])),
        "Chitra": dict(zip(subjects, [76, 81, 70, 68])),
        "Dev":    dict(zip(subjects, [30, 42, 55, 35])),
        "Esha":   dict(zip(subjects, [64, 59, 72, 66])),
    })
    print("\nSample data for 5 students loaded.")


MENU = """
  1. Enter marks for students
  2. View results (total, percentage, grade)
  3. Highest and lowest marks
  4. Class average
  5. Students who need improvement
  6. Result summary
  7. Set up / change subjects
  9. Load sample data
  0. Exit
"""


def main():
    while True:
        title("STUDENT PERFORMANCE ANALYSER")
        print(MENU)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            enter_marks()
        elif choice == "7":
            setup_subjects()
        elif choice == "9":
            load_sample()
        elif choice == "0":
            print("\nExited Successfully")
            break
        elif choice in {"2", "3", "4", "5", "6"}:
            if need_data():
                {"2": show_all_results, "3": highest_lowest, "4": show_average,
                 "5": show_improvement, "6": summary}[choice]()
        else:
            print("\n  ! Invalid option.")
        pause()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nExited.")
