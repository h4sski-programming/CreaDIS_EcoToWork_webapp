from flask import Blueprint, render_template, flash, request, redirect, url_for
from models import User, Activity
from app import db
from flask_login import login_required, current_user
from datetime import date, datetime

views = Blueprint('views', __name__)


@views.route('/profile')
@login_required
def profile():
    user = current_user
    return render_template('profile.html', user=user)


@views.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    user = current_user
    today = date.today()

    if request.method == 'POST':
        distance = request.form.getlist('distance')
        activity = request.form.getlist('activity')
        for i, (d, a) in enumerate(zip(distance, activity)):
            if d != '':
                if int(d) < 0:
                    flash(
                        'Distance values must be greather than 0, please re-type your values', category='error')
                elif a == '' and int(d) != 0:
                    flash('You must select activity type', category='error')
                else:
                    new_activity_date = date(today.year, today.month, i+1)
                    if new_activity_date in user.activity:
                        user.activity.filter(date_of_activity=new_activity_date).\
                            update({'distance': d, 'activity_type': a})
                    else:
                        new_activity = Activity(
                            user_id=user.id, distance=d, date_of_activity=new_activity_date, activity_type=a)
                        db.session.add(new_activity)
                        db.session.commit()
                    flash(
                        f'At day {today.year}-{today.month}-{ i + 1 } you added value = {d} [km] with activity type {a}.', category='success')

    month = today.strftime("%Y %B")
    first_month_day_number = int(
        datetime(today.year, today.month, 1).strftime('%w'))

    # Changing first week day from Sunday into Monday
    if first_month_day_number == 0:
        first_month_day_number = 6
    else:
        first_month_day_number -= 1

    # Selecting lenght of the current month
    days_in_month = 0
    if today.month in [1, 3, 5, 7, 8, 10, 12]:
        days_in_month = 31
    elif today.month == 2:      # February
        if today.year % 400 == 0:
            days_in_month = 29
        elif today.year % 100 == 0:
            days_in_month = 28
        elif today.year % 4 == 0:
            days_in_month = 29
        else:
            days_in_month = 28
    else:
        days_in_month = 30

    distance_list = []
    activity_type_list = []
    start_date = date(2022, 10, 1)
    end_date = date(2022, 10, 31)
    for current_activity in user.activity:
        if start_date <= current_activity.date_of_activity <= end_date:
            distance_list.append(current_activity.distance)
            activity_type_list.append(current_activity.activity_type)

    return render_template('edit.html', user=user, today=today, date=date, month=month, days_in_month=days_in_month, first_month_day_number=first_month_day_number, distance_list=distance_list, activity_type_list=activity_type_list)


@ views.route('/', methods=['GET', 'POST'])
@ login_required
def home():
    user = current_user
    users = User.query.order_by('first_name')
    today = date.today()

    days_in_month = 0
    if today.month in [1, 3, 5, 7, 8, 10, 12]:
        days_in_month = 31
    elif today.month in [2]:
        days_in_month = 28
    else:
        days_in_month = 30

    list_of_days = []
    s = ''
    for i in range(1, days_in_month + 1):
        day_weekday_name = date(today.year, today.month, i).strftime("%a")
        s = str(i) + ' ' + str(day_weekday_name)
        list_of_days.append(s)

    if request.method == 'POST':
        input_value_date_str = request.form.get('inputValueDate')
        input_value = int(request.form.get('inputValue'))

        input_value_date = datetime.strptime(
            input_value_date_str, '%Y-%m-%d').date()
        print(input_value_date)
        print(today.month)
        condition = int(input_value_date.month) != today.month
        print(condition)
        if condition:
            flash(
                f'Date {input_value_date} is not in curent month, please input value again.', category='error')
        elif input_value > 0:
            flash(
                f'You add/update record at {input_value_date} with value of {input_value} [km].', category='success')
        else:
            flash(
                f'Please type value greather then 0.', category='error')
        return redirect(url_for('views.home'))

    return render_template('home.html', user=user, users=users, today=today, list_of_days=list_of_days)
