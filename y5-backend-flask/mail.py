from utils.mail_async import send_email_async


def mail_notify(users, status):
    """
    异步发送房间状态通知邮件
    """
    email_list = []
    for user in users:
        if user.email is None:
            continue
        if status == 1:
            message = 'room activated'
        else:
            message = 'room deactivated'
        subject = "hello, %s" % user.nickname
        
        email_list.append({
            'recipients': [user.email],
            'subject': subject,
            'body': message
        })
    
    # 异步批量发送邮件
    if email_list:
        from utils.mail_async import send_bulk_emails_async
        send_bulk_emails_async(email_list)


def mail_morning(users):
    """
    异步发送晨间邮件
    """
    email_list = []
    for user in users:
        if user.email is None:
            continue
        message = '...'
        subject = "hello, %s" % user.nickname
        
        email_list.append({
            'recipients': [user.email],
            'subject': subject,
            'body': message
        })
    
    # 异步批量发送邮件
    if email_list:
        from utils.mail_async import send_bulk_emails_async
        send_bulk_emails_async(email_list)


def mail_night(users):
    """
    异步发送夜间邮件
    """
    email_list = []
    for user in users:
        if user.email is None:
            continue
        message = '...'
        subject = "hello, %s" % user.nickname
        
        email_list.append({
            'recipients': [user.email],
            'subject': subject,
            'body': message
        })
    
    # 异步批量发送邮件
    if email_list:
        from utils.mail_async import send_bulk_emails_async
        send_bulk_emails_async(email_list)