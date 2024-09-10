from apscheduler.schedulers.background import BackgroundScheduler
from accounts.models import CustomUser
from .models import TestingModel, FG
from django.utils import timezone
from datetime import timedelta


def function():
    print("good morning")
    users = CustomUser.objects.filter(is_submit=True)
    test_model = TestingModel.objects.filter(test=True).first()
    fgs = FG.objects.all()
    current_time = timezone.now()
    current_date = timezone.now().date()
    yesterday = timezone.now() - timezone.timedelta(seconds=5)

    for user in users:
        user_time = user.is_submit_time
        if user_time is not None:
            if current_time > user_time:
                user.is_submit = False
                user.save()
                print('updated')

    if test_model:
        test_time = test_model.test_time
        if current_time > test_time:
            test_model.test = False
            test_model.test_time = timezone.now()
            test_model.save()

    if fgs:
        for f in fgs:
            if f.today_submit_timestamp and f.today_submit_timestamp < yesterday:
                f.today_submit_timestamp = None
                f.today_submit_user.clear()
                f.save()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(function, 'interval', seconds=5)
    scheduler.start()
