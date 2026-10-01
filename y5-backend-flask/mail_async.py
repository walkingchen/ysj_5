"""
异步邮件发送工具模块
提供统一的异步邮件发送功能
"""
import threading
import logging
from html import escape
from concurrent.futures import ThreadPoolExecutor
from flask import current_app
from flask_mail import Message
from extensions import mail

# 创建线程池用于异步邮件发送
mail_executor = ThreadPoolExecutor(max_workers=5, thread_name_prefix="mail_sender")
logger = logging.getLogger(__name__)

def send_email_async(recipients, subject, body, html_body=None, sender=("Chattera Team", "chattera.platform@gmail.com")):
    """
    异步发送邮件
    
    Args:
        recipients: 收件人邮箱列表
        subject: 邮件主题
        body: 邮件正文
        html_body: HTML格式邮件正文（可选）
        sender: 发件人信息
    """
    # 抓取当前应用实例，供后台线程使用应用上下文
    app = None
    try:
        app = current_app._get_current_object()
    except Exception:
        app = None

    def send_email():
        try:
            def _do_send():
                logger.info(f"[mail_async] Preparing email: recipients={recipients}, subject='{subject}'")
                msg = Message(
                    recipients=recipients,
                    body=body,
                    subject=subject,
                    sender=sender
                )
                if html_body:
                    msg.html = html_body
                mail.send(msg)
                logger.info(f"[mail_async] Successfully sent email to {recipients}, subject='{subject}'")

            if app is not None:
                logger.info("[mail_async] Using captured Flask app context in background thread")
                with app.app_context():
                    _do_send()
            else:
                logger.warning("[mail_async] No Flask app context available; attempting to send without context")
                _do_send()
        except Exception as e:
            logger.exception(f"[mail_async] Failed to send email to {recipients}: {str(e)}")
    
    # 提交到线程池异步执行
    try:
        future = mail_executor.submit(send_email)
        logger.info(f"[mail_async] Submitted email task to thread pool, thread_name_prefix='mail_sender'")
        return future
    except Exception as e:
        logger.exception(f"[mail_async] Failed to submit email task: {str(e)}")
        return None

def send_bulk_emails_async(email_list):
    """
    异步批量发送邮件
    
    Args:
        email_list: 邮件信息列表，每个元素包含：
            - recipients: 收件人邮箱列表
            - subject: 邮件主题
            - body: 邮件正文
            - html_body: HTML格式邮件正文（可选）
            - sender: 发件人信息（可选）
    """
    # 抓取当前应用实例，供后台线程使用应用上下文
    app = None
    try:
        app = current_app._get_current_object()
    except Exception:
        app = None

    def send_bulk_emails():
        def _do_send_one(email_info):
            recipients = email_info.get('recipients')
            subject = email_info.get('subject')
            body = email_info.get('body')
            html_body = email_info.get('html_body')
            sender = email_info.get('sender', ("Chattera Team", "chattera.platform@gmail.com"))

            logger.info(f"[mail_async] Preparing bulk email: recipients={recipients}, subject='{subject}'")
            msg = Message(
                recipients=recipients,
                body=body,
                subject=subject,
                sender=sender
            )
            if html_body:
                msg.html = html_body
            mail.send(msg)
            logger.info(f"[mail_async] Successfully sent email to {recipients}, subject='{subject}'")

        try:
            if app is not None:
                logger.info("[mail_async] Using captured Flask app context for bulk email in background thread")
                with app.app_context():
                    for email_info in email_list:
                        try:
                            _do_send_one(email_info)
                        except Exception as e:
                            logger.exception(f"[mail_async] Failed to send email to {email_info.get('recipients', 'unknown')}: {str(e)}")
            else:
                logger.warning("[mail_async] No Flask app context available for bulk email; attempting to send without context")
                for email_info in email_list:
                    try:
                        _do_send_one(email_info)
                    except Exception as e:
                        logger.exception(f"[mail_async] Failed to send email to {email_info.get('recipients', 'unknown')}: {str(e)}")
        except Exception as e:
            logger.exception(f"[mail_async] Failed bulk email sending due to context error: {str(e)}")
    
    # 提交到线程池异步执行
    try:
        future = mail_executor.submit(send_bulk_emails)
        logger.info(f"[mail_async] Submitted bulk email task to thread pool, size={len(email_list)}")
        return future
    except Exception as e:
        logger.exception(f"[mail_async] Failed to submit bulk email task: {str(e)}")
        return None

def send_room_activation_email_async(user_email, user_nickname, condition=None):
    """
    异步发送房间激活邮件
    """
    video_url = "https://youtu.be/TgDJWI6QTmA" if condition in ('1', 1) else "https://youtu.be/D4U0Eajnb-Q"
    login_url = "https://camer-covid.journalism.wisc.edu/#/login"
    safe_nickname = escape(str(user_nickname))
    message = f'''Hi {user_nickname},

Thank you for signing up to join Chattera and share your memories and stories about the COVID-19 pandemic. Your Chattera room is now active!

The COVID-19 pandemic has significantly impacted our lives over the past few years. Although the pandemic has ended, reflecting on our experiences can provide valuable insights. We all went through this unprecedented time together, and your feelings matter. We invite you to join the conversation on Chattera and share your memories of the COVID-19 pandemic.

What You Will Do:

Your Chattera room will be open for at least eight days. Each day, you will be invited to read and respond to posts on the platform, share your thoughts, and interact with your Chattera buddies.

You'll find a variety of popular social media posts about COVID-19 on Chattera. Some of these posts may contain information that differs from what you currently know or contradict the best available evidence. Note that they do not imply endorsement of the Chattera team.

In today's complex information environment, it's important to verify the accuracy of what we read and share, and individual efforts are particularly vital in maintaining a well-informed community. Therefore, we encourage you to fact-check the information on the platform and share your opinions with others. As you participate in discussions, please remember to stay civil, respect differing viewpoints, and foster a supportive and constructive community.

Here is a video to walk you through Chattera:
{video_url}

What You Will Receive:

We encourage you to dive into the conversations on Chattera! Each day, if you contribute at least one thoughtful post, comment, or share, you'll earn $0.25 as a reward. Plus, if you're one of the two most active users in your Chattera room for a particular day, you'll score an extra $1 for that day.

Stay engaged and share your insights! The top participants in your room will earn up to $10 and we hope you will be one of them!

In addition to engaging on Chattera, you will be invited to complete a short daily survey about your experience on the platform. Each completed daily survey will earn you an additional $0.25, for a total of up to $2 for all eight daily surveys.

The table below summarizes the activities and compensation available throughout the project.

Take pre-survey: $1
Interact with your Chattera friends: $0.25 per day for at least one thoughtful post, comment, or share (up to $2); $1 bonus per day for being one of the two most active users (up to $8).
Take daily surveys: $0.25 per completed survey (up to $2 for all eight).
Take post-survey: $4
Total: Up to $17

Join your Chattera room now and start sharing your experiences!
Log in: {login_url}

Best regards,
Your Chattera Team'''
    html_message = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chattera Participation Information</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 20px;
                color: #333;
            }}
            table {{
                width: 80%;
                border-collapse: collapse;
                margin: 20px auto;
            }}
            th, td {{
                border: 1px solid #ddd;
                text-align: left;
                padding: 8px;
            }}
            th {{
                background-color: #f4f4f4;
            }}
            .content {{
                max-width: 800px;
                margin: 0 auto;
            }}
            .content p {{
                margin: 10px 0;
            }}
            .button {{
                display: inline-block;
                padding: 10px 20px;
                font-size: 16px;
                color: #fff;
                background-color: #007bff;
                text-align: center;
                text-decoration: none;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }}
            .button:hover {{
                background-color: #0056b3;
            }}
        </style>
    </head>
    <body>
        <div class="content">
            <p><img src="https://camer-covid.journalism.wisc.edu/logo.png" alt="Chattera logo" width="132" height="101"></p>
            <p><strong>Hi {safe_nickname},</strong></p>
            <p>Thank you for signing up to join Chattera and share your memories and stories about the COVID-19 pandemic. Your Chattera room is now active!</p>
            <p>The COVID-19 pandemic has significantly impacted our lives over the past few years. Although the pandemic has ended, reflecting on our experiences can provide valuable insights. We all went through this unprecedented time together, and your feelings matter. We invite you to join the conversation on Chattera and share your memories of the COVID-19 pandemic.</p>
            <p><strong>What You Will Do:</strong></p>
            <p>Your Chattera room will be open for at least eight days. Each day, you will be invited to read and respond to posts on the platform, share your thoughts, and interact with your Chattera buddies.</p>
            <p>You'll find a variety of popular social media posts about COVID-19 on Chattera. Some of these posts may contain information that differs from what you currently know or contradict the best available evidence. Note that <strong>they do not imply endorsement of the Chattera team</strong>.</p>
            <p>In today's complex information environment, it's important to verify the accuracy of what we read and share, and individual efforts are particularly vital in maintaining a well-informed community. Therefore, we encourage you to fact-check the information on the platform and share your opinions with others. As you participate in discussions, please remember to stay civil, respect differing viewpoints, and foster a supportive and constructive community.</p>
            <p>Here is a video to walk you through Chattera:</p>
            <p><a href="{video_url}">{video_url}</a></p>
            <p><strong>What You Will Receive:</strong></p>
            <p>We encourage you to dive into the conversations on Chattera! Each day, if you contribute at least one thoughtful post, comment, or share, you'll earn $0.25 as a reward. Plus, if you're one of the two most active users in your Chattera room for a particular day, you'll score an extra $1 for that day.</p>
            <p>Stay engaged and share your insights! The top participants in your room will earn up to $10 and we hope you will be one of them!</p>
            <p>In addition to engaging on Chattera, you will be invited to complete a short daily survey about your experience on the platform. Each completed daily survey will earn you an additional $0.25, for a total of up to $2 for all eight daily surveys.</p>
            <p>The table below summarizes the activities and compensation available throughout the project.</p>
        <table>
            <thead>
                <tr>
                    <th><strong>Activity</strong></th>
                    <th><strong>Compensation</strong></th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Take pre-survey</strong></td>
                    <td>
                        <strong>Base:</strong> $1
                    </td>
                </tr>
                <tr>
                    <td><strong>Interact with your Chattera friends</strong></td>
                    <td>
                        <strong>Base:</strong>
                        <ul>
                            <li>Earn $0.25 per day for contributing at least one thoughtful post, comment, or share.</li>
                            <li>Earn up to $2 over the course of your participation on Chattera.</li>
                        </ul>
                        <strong>Bonus:</strong>
                        <ul>
                            <li>Earn a $1 bonus per day if you are one of the two most active users in your Chattera group.</li>
                            <li>Earn up to an $8 bonus over the course of your participation on Chattera.</li>
                        </ul>
                    </td>
                </tr>
                <tr>
                    <td><strong>Take daily surveys</strong></td>
                    <td>
                        <ul>
                            <li>Earn $0.25 for each completed daily survey.</li>
                            <li>Earn a total of $2 by completing all 8 daily surveys.</li>
                        </ul>
                    </td>
                </tr>
                <tr>
                    <td><strong>Take post-survey</strong></td>
                    <td>
                        <strong>Base:</strong> $4
                    </td>
                </tr>
                <tr>
                    <td><strong>Total</strong></td>
                    <td>Up to $17</td>
                </tr>
            </tbody>
        </table>
        <p>Join your Chattera room now and start sharing your experiences!</p>
        <a type="button" class="button" href="{login_url}">Log in</a>
        <p>Best regards,<br>Your Chattera Team</p>
        </div>
    </body>
    </html>
    '''
    
    subject = "Your Room is Now Active – Welcome to Chattera!"
    send_email_async([user_email], subject, message, html_message)

def send_registration_email_async(user_email, user_nickname):
    """
    异步发送注册确认邮件
    """
    message = f'''
Dear {user_nickname},

Thank you for registering with Chattera! We're excited to have you join our community.

Your account has been successfully created and you can now start participating in conversations about COVID-19 experiences and memories.

Thank you again for your participation, and we'll be in touch soon!

Best regards,
Your Chattera Team
    '''
    
    subject = "Registration Confirmation"
    send_email_async([user_email], subject, message)
