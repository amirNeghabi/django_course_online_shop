import requests
import json

from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages

from orders.models import Order


def payment_process(request):
    """
    پردازش پرداخت و اتصال به درگاه زرین‌پال
    """
    # دریافت order_id از session
    order_id = request.session.get('order_id')
    
    if not order_id:
        messages.error(request, 'سفارشی یافت نشد. لطفاً دوباره سفارش ثبت کنید.')
        return redirect('cart:cart_detail')
    
    # دریافت سفارش
    order = get_object_or_404(Order, id=order_id)
    
    # محاسبه قیمت (تبدیل تومان به ریال)
    toman_total_price = order.get_total_price()
    rial_total_price = int(toman_total_price * 10)
    
    # URL درگاه زرین‌پال
    zarinpal_request_url = 'https://api.zarinpal.com/pg/v4/payment/request.json'
    
    # Headers
    request_header = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    
    # داده‌های ارسالی به زرین‌پال
    request_data = {
        'merchant_id': settings.ZARINPAL_MERCHANT_ID,
        'amount': rial_total_price,
        'description': f'سفارش #{order.id} - {order.user.first_name} {order.user.last_name}',
        'callback_url': request.build_absolute_uri('/payment/callback/'),
    }
    
    try:
        # ارسال درخواست به زرین‌پال
        res = requests.post(
            url=zarinpal_request_url, 
            data=json.dumps(request_data), 
            headers=request_header,
            timeout=10  # تایم‌اوت 10 ثانیه
        )
        
        # بررسی status code
        if res.status_code != 200:
            messages.error(request, 'خطا در اتصال به درگاه پرداخت. لطفاً دوباره تلاش کنید.')
            return redirect('cart:cart_detail')
        
        # پارس کردن response
        response_data = res.json()
        
        # بررسی ساختار response
        if 'data' not in response_data:
            messages.error(request, 'پاسخ نامعتبر از درگاه پرداخت.')
            return redirect('cart:cart_detail')
        
        data = response_data['data']
        
        # بررسی وجود authority
        if 'authority' in data and data['authority']:
            authority = data['authority']
            
            # ذخیره authority در سفارش
            order.zarinpal_authority = authority
            order.save()
            
            # هدایت به درگاه پرداخت
            zarinpal_payment_url = f'https://www.zarinpal.com/pg/StartPay/{authority}'
            return redirect(zarinpal_payment_url)
        
        # بررسی خطاها
        elif 'errors' in data and data['errors']:
            error_message = data['errors'][0] if data['errors'] else 'خطای نامشخص'
            messages.error(request, f'خطا در ایجاد درخواست پرداخت: {error_message}')
            return redirect('cart:cart_detail')
        
        else:
            messages.error(request, 'خطا در دریافت اطلاعات پرداخت از درگاه.')
            return redirect('cart:cart_detail')
    
    except requests.exceptions.Timeout:
        messages.error(request, 'زمان اتصال به درگاه پرداخت به پایان رسید. لطفاً دوباره تلاش کنید.')
        return redirect('cart:cart_detail')
    
    except requests.exceptions.ConnectionError:
        messages.error(request, 'خطا در اتصال به درگاه پرداخت. لطفاً اتصال اینترنت خود را بررسی کنید.')
        return redirect('cart:cart_detail')
    
    except requests.exceptions.RequestException as e:
        messages.error(request, 'خطایی در فرآیند پرداخت رخ داد. لطفاً دوباره تلاش کنید.')
        return redirect('cart:cart_detail')
    
    except Exception as e:
        # لاگ کردن خطا (در production)
        print(f'Payment Error: {str(e)}')
        messages.error(request, 'خطای غیرمنتظره. لطفاً با پشتیبانی تماس بگیرید.')
        return redirect('cart:cart_detail')


def payment_callback(request):
    """
    بازگشت از درگاه پرداخت
    """
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')
    
    if not authority or status != 'OK':
        messages.error(request, 'پرداخت ناموفق بود یا توسط کاربر لغو شد.')
        return redirect('cart:cart_detail')
    
    try:
        # یافتن سفارش با authority
        order = Order.objects.get(zarinpal_authority=authority)
        
        # محاسبه مبلغ
        toman_total_price = order.get_total_price()
        rial_total_price = int(toman_total_price * 10)
        
        # URL تایید پرداخت
        zarinpal_verify_url = 'https://api.zarinpal.com/pg/v4/payment/verify.json'
        
        # Headers
        request_header = {
            "accept": "application/json",
            "content-type": "application/json"
        }
        
        # داده‌های تایید
        request_data = {
            'merchant_id': settings.ZARINPAL_MERCHANT_ID,
            'amount': rial_total_price,
            'authority': authority,
        }
        
        # ارسال درخواست تایید
        res = requests.post(
            url=zarinpal_verify_url,
            data=json.dumps(request_data),
            headers=request_header,
            timeout=10
        )
        
        if res.status_code != 200:
            messages.error(request, 'خطا در تایید پرداخت.')
            return redirect('cart:cart_detail')
        
        response_data = res.json()
        
        if 'data' in response_data:
            data = response_data['data']
            
            if data.get('code') == 100 or data.get('code') == 101:
                # پرداخت موفق
                order.is_paid = True
                order.zarinpal_ref_id = data.get('ref_id', '')
                order.save()
                
                # پاک کردن session
                if 'order_id' in request.session:
                    del request.session['order_id']
                
                messages.success(request, f'پرداخت با موفقیت انجام شد. کد پیگیری: {data.get("ref_id", "")}')
                return redirect('payment:payment_success')
            else:
                messages.error(request, 'پرداخت تایید نشد.')
                return redirect('cart:cart_detail')
        else:
            messages.error(request, 'پاسخ نامعتبر از درگاه پرداخت.')
            return redirect('cart:cart_detail')
    
    except Order.DoesNotExist:
        messages.error(request, 'سفارش یافت نشد.')
        return redirect('cart:cart_detail')
    
    except Exception as e:
        print(f'Callback Error: {str(e)}')
        messages.error(request, 'خطا در تایید پرداخت.')
        return redirect('cart:cart_detail')


def payment_success(request):
    """
    صفحه موفقیت پرداخت
    """
    return render(request, 'payment/payment_success.html')


def payment_failed(request):
    """
    صفحه شکست پرداخت
    """
    return render(request, 'payment/payment_failed.html')