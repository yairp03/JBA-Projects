from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta

TODAY_TASKS = 1
WEEK_TASKS = 2
ALL_TASKS = 3
MISSED_TASKS = 4
ADD_TASK = 5
DELETE_TASK = 6
EXIT = 0

MENU = """\
1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit"""

Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='Default Task')
    deadline = Column(Date, default=datetime.today().date())

    def __repr__(self):
        return self.task


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def main():
    choice = 1
    while choice != EXIT:
        print(MENU)
        choice = safe_input('', int)
        print()
        if choice == TODAY_TASKS:
            print_today_tasks()
        elif choice == WEEK_TASKS:
            print_week_tasks()
        elif choice == ALL_TASKS:
            print_all_tasks()
        elif choice == MISSED_TASKS:
            print_missed_tasks()
        elif choice == ADD_TASK:
            add_task()
        elif choice == DELETE_TASK:
            delete_task()


def safe_input(text, func):
    while True:
        try:
            return func(input(text))
        except Exception as e:
            print(e)


def print_tasks_list(tasks, nothing="Nothing to do!"):
    if tasks:
        for i, task in enumerate(tasks):
            print(f'{i + 1}. {task}')
    else:
        print(nothing)
    print()


def print_today_tasks():
    print("Today", datetime.today().strftime("%d %b:").lstrip('0'))
    rows = session.query(Task).filter(Task.deadline == datetime.today().date()).all()
    print_tasks_list(rows)


def print_week_tasks():
    for day in range(7):
        curr_day = datetime.today().date() + timedelta(days=day)
        print(curr_day.strftime("%A"), curr_day.strftime("%d %b:").lstrip('0'))
        rows = session.query(Task).filter(Task.deadline == curr_day).all()
        print_tasks_list(rows)


def print_all_tasks():
    print("All tasks:")
    rows = session.query(Task).order_by(Task.deadline).all()
    print_tasks_list([r.task + ". " + r.deadline.strftime('%d %b').lstrip('0') for r in rows])


def print_missed_tasks():
    print("Missed tasks:")
    rows = session.query(Task).filter(Task.deadline < datetime.today().date()).order_by(Task.deadline).all()
    print_tasks_list(rows, nothing="Nothing is missed!")


def add_task():
    task = input("Enter task\n")
    deadline = safe_input("Enter deadline (YYYY-MM-DD)\n", lambda date_str: datetime.strptime(date_str, "%Y-%m-%d"))
    new_row = Task(task=task, deadline=deadline)
    session.add(new_row)
    session.commit()
    print("The task has been added!\n")


def delete_task():
    rows = session.query(Task).order_by(Task.deadline).all()
    if not rows:
        print("Nothing to delete!\n")
        return
    print("Choose the number of the task you want to delete:")
    print_tasks_list(rows)
    session.delete(safe_input('', lambda x: rows[int(x) - 1]))
    session.commit()




if __name__ == '__main__':
    main()
