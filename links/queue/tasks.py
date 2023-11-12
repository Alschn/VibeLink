from celery import shared_task


@shared_task
def generate_link_requests() -> list[int]:
    from accounts.models import User
    from links.models import LinkRequest
    from links.emails import send_link_requests_email_notifications

    users = User.objects.all()
    link_requests = [LinkRequest.objects.create(user=user) for user in users]

    # todo: email notifications
    send_link_requests_email_notifications(users)

    return [link_request.id for link_request in link_requests]
