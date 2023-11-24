import os

import django
from django.utils.timezone import localtime, now


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from datacenter.models import Passcard, Visit  # noqa: E402

if __name__ == '__main__':
    active_passcards = Passcard.objects.filter(is_active=True)
    random_passcode = active_passcards[0].passcode
    passcode_visits = Visit.objects.filter(passcard__passcode=random_passcode)
    for visit in passcode_visits:
        print(visit)
    active_visitors = Visit.objects.filter(passcard__is_active=True) \
        & Visit.objects.filter(leaved_at=None)
    for visitor in active_visitors:
        visitor_enter_time = localtime(visitor.entered_at)
        visit_time = now() - visitor_enter_time
        print("Зашёл в хранилище, время по Москве:", visitor_enter_time)
        print("Находится в хранилище: {0:02}:{1:02}:{2:02}".format(
            int(visit_time.total_seconds() // 3600),
            int((visit_time.total_seconds() % 3600) // 60),
            int(visit_time.total_seconds() % 60)
            )
        )
        print(visitor.passcard.owner_name)
    print('Количество пропусков:', Passcard.objects.count())  # noqa: T001
    print('Количество активных пропусков:', len(active_passcards))     
