# ai_assistant/views.py

import json
from datetime import date

import openai
from decouple import config
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from products.models import Product
from .models import ChatSession, ChatMessage, DailyUsage

# =======================
# تنظیم کلید API OpenAI
# =======================
DEEPSEEK_API_KEY = config("DEEPSEEK_API_KEY", default="")
openai.api_key = DEEPSEEK_API_KEY

# =======================
# توابع کمکی
# =======================

def get_product_context():
    """
    گرفتن اطلاعات محصولات از دیتابیس برای Context دادن به AI
    """
    products = Product.objects.filter(active=True)[:20]  # 20 محصول فعال
    
    context = "اطلاعات محصولات فروشگاه:\n\n"
    for product in products:
        context += f"""
محصول: {product.title}
قیمت: {product.price:,} تومان
توضیحات: {product.short_description or product.description[:200]}
وضعیت: {'موجود' if product.active else 'ناموجود'}
---
"""
    return context


def check_daily_limit(user=None, session_key=None):
    MAX_DAILY_MESSAGES = 20
    today = date.today()
    
    usage, _ = DailyUsage.objects.get_or_create(
        user=user if user and user.is_authenticated else None,
        session_key=session_key if not (user and user.is_authenticated) else None,
        date=today,
        defaults={'count': 0}
    )
    
    if usage.count >= MAX_DAILY_MESSAGES:
        return False, usage.count
    return True, usage.count


def increment_usage(user=None, session_key=None):
    today = date.today()
    
    usage, _ = DailyUsage.objects.get_or_create(
        user=user if user and user.is_authenticated else None,
        session_key=session_key if not (user and user.is_authenticated) else None,
        date=today,
        defaults={'count': 0}
    )
    
    usage.count += 1
    usage.save()
    
    return usage.count


def get_or_create_session(user, session_key):
    if user and user.is_authenticated:
        session, _ = ChatSession.objects.get_or_create(user=user, session_key=None)
    else:
        session, _ = ChatSession.objects.get_or_create(user=None, session_key=session_key)
    return session


def call_deepseek_api(messages):
    """
    فراخوانی OpenAI ChatCompletion در نسخه جدید openai>=1.0.0
    """
    if not DEEPSEEK_API_KEY:
        return {
            "success": False,
            "error": "API Key تنظیم نشده است. لطفاً DEEPSEEK_API_KEY را در .env قرار دهید."
        }
    
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500,
        )
        # دسترسی به پاسخ AI در نسخه جدید:
        reply_text = response.choices[0].message.content
        return {"success": True, "reply": reply_text}
    
    except Exception as e:
        return {"success": False, "error": f"خطای API: {str(e)}"}



# =======================
# ویوها
# =======================

@csrf_exempt
@require_http_methods(["POST"])
def chat_widget(request):
    try:
        # دریافت پیام کاربر
        if request.content_type == "application/json":
            data = json.loads(request.body.decode("utf-8"))
        else:
            data = request.POST

        user_message = data.get("message", "").strip()
        if not user_message:
            return JsonResponse({"error": "لطفاً پیامی وارد کنید"}, status=400)

        # گرفتن user و session
        user = request.user if request.user.is_authenticated else None
        if not user:
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
        else:
            session_key = None

        # بررسی محدودیت روزانه
        can_use, current_count = check_daily_limit(user, session_key)
        if not can_use:
            return JsonResponse({
                "error": f"شما به حد مجاز روزانه ({current_count} پیام) رسیده‌اید.",
                "limit_reached": True
            }, status=429)

        # گرفتن session
        chat_session = get_or_create_session(user, session_key)

        # ذخیره پیام کاربر
        ChatMessage.objects.create(session=chat_session, is_user=True, message=user_message)

        # گرفتن context محصولات
        product_context = get_product_context()

        # ساخت پیام‌ها برای OpenAI
        system_prompt = f"""شما یک دستیار فروش هوشمند هستید که در یک فروشگاه آنلاین محصولات دیجیتال کار می‌کنید.
وظایف: پاسخ به سوالات، پیشنهاد محصولات، توضیح قیمت و ویژگی‌ها با لحنی دوستانه و فارسی.
{product_context}"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]

        # فراخوانی OpenAI
        api_response = call_deepseek_api(messages)
        if not api_response["success"]:
            return JsonResponse({"error": api_response["error"]}, status=500)

        ai_reply = api_response["reply"]

        # ذخیره پاسخ AI
        ChatMessage.objects.create(session=chat_session, is_user=False, message=ai_reply)

        # افزایش شمارنده استفاده
        new_count = increment_usage(user, session_key)

        return JsonResponse({
            "reply": ai_reply,
            "usage_count": new_count,
            "remaining": 20 - new_count
        })

    except Exception as e:
        return JsonResponse({"error": f"خطای سرور: {str(e)}"}, status=500)


@csrf_exempt
def get_chat_history(request):
    # برای نمونه فعلاً خالی
    return JsonResponse({"success": True, "history": []})


@csrf_exempt
def clear_chat(request):
    return JsonResponse({"success": True, "message": "چت پاک شد."})
