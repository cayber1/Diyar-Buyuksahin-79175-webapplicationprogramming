from celery import shared_task
import time

@shared_task
def send_post_notification(post_id):
    print(f"📨 Görev başladı: Post ID = {post_id}")
    time.sleep(3)  # simülasyon gecikmesi
    print("✅ E-posta gönderildi (simülasyon)")
    return True
