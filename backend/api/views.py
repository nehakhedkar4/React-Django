from twilio.rest import Client
import random 

from rest_framework.views import APIView
from rest_framework.response import Response    
# from .serializers import *
from .models import *
from django.contrib.auth import authenticate

from django.utils import timezone

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from myproject import settings
import stripe
from django.shortcuts import redirect

# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def decode_jwt_token(token):
    try:
        decoded_token = jwt.decode(token, settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=['HS256'])
        return decoded_token
    except jwt.exceptions.DecodeError:
        return None

def get_user_from_token(token):
    decoded_token = decode_jwt_token(token)
    if decoded_token:
        user_id = decoded_token['user_id']
        try:
            user = MyUser.objects.get(id=user_id)
            return user
        except MyUser.DoesNotExist:
            return None
    return None

def generate_otp():
    return random.randrange(1000,9999)

# SEND OTP TO PHONE AND EMAIL USING TWILO API
def send_otp_email(email):

    otp = generate_otp()

    message = Mail(
        from_email='nk.empiric@gmail.com',
        to_emails=f'{email}',
        # to_emails='up.empiric@gmail.com',
        subject='Sending with Twilio SendGrid is Fun',
        html_content=f'<strong>Your verification code is: {otp}</strong>'
        )
    sg = SendGridAPIClient('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')
    response = sg.send(message)
    user = MyUser.objects.get(email=email)
    update_time = timezone.now()
    user.created_at = update_time
    user.otp = otp
    user.save()
    return email

def send_otp_phone(phone):

    otp = generate_otp()

    account_sid = 'AC87b972d42fca0eba846340579d18d023'
    auth_token = 'd564969f334389033e207b056b1412b5'

    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=f"Your verification code is: {otp}",
                        from_='+13854741159',
                        to= f'+91{phone}',
                        # to='+918758691652'
                    )
    user = MyUser.objects.get(phone=phone)
    update_time = timezone.now()
    user.created_at = update_time
    user.otp = otp
    user.save()
    return phone

# STRIPE CARD PAYMENT 

stripe.api_key = settings.STRIPE_SECRET_KEY

class CardPaymentView(APIView):
    def post(self, request, token, format=None):
        user = get_user_from_token(token)
        line_items = []
        cart_product = [p for p in MyCart.objects.all() if p.user==user]
        for i in cart_product:
            line_items.append({
                'price_data' : {
                        'currency' : 'inr',
                        'unit_amount' : (i.product.selling_price)*100,
                        'product_data' : {
                            'name' : i.product.product_title,
                        }
                },
                'quantity' : i.product_qty,
            })
        checkout_session = stripe.checkout.Session.create(
            payment_method_types = ['card'],
            
            line_items=line_items,
            mode='payment',
            success_url='http://localhost:3000/orderstatus/?success=true',
            cancel_url='http://localhost:3000/msg/?canceled=true',
        ) 
        # cart = MyCart.objects.filter(user=user)
        # for c in cart:
        #     MyOrder(user=user,product=c.product,product_qty=c.product_qty).save()
        #     print("saveddddd")
        #     c.delete()
        #     print("deleteeeeeeeeeee")
        return redirect(checkout_session.url)

# RAZOR PAY PAYMENT
import razorpay

client = razorpay.Client(auth=("rzp_test_mQX5zJOEMTb076", "QZoWctpequlkR9MeUUrWOuW9"))

class RazorPayView(APIView):
    def post(self, request, format=None):

        payment = client.order.create({"amount": int(1) * 100, 
                                   "currency": "INR", 
                                   "payment_capture": "1"})
        return Response({'payment' : payment}) 
    

# razorpay
# rzp_test_mQX5zJOEMTb076 - key id
# QZoWctpequlkR9MeUUrWOuW9 - key secrete

class Test2View(APIView):
    def post(self, request, format=None):
        print("post rqst called--------------------------------------------------------------")
        print(request.data)
        serializer = Test2View(data=request.data)
        print(serializer,"------------------------------------------------------serilizer")
        print(serializer.is_valid(),"--------------------------------------------serializer is valid")
        print(serializer.validated_data['fname'])
        print(serializer.validated_data['name'])
        if not serializer.is_valid():
            print(serializer.errors)
            return Response({"msg" : "2574"})
        else:
            print("serializer true-----------------------------")
            print(serializer.validated_data['name'])
            print(serializer.validated_data['fname'])
            return Response({"msg" : "2574"})