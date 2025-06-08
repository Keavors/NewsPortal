from datetime import datetime, time

def theme_mode(request):
    user_time = datetime.now().astimezone(
        request.user.timezone if request.user.is_authenticated else None
    )
    is_night = time(20) <= user_time.time() or user_time.time() <= time(6)
    return {'is_night_mode': is_night}