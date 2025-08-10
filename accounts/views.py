from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from pypaystack2 import Paystack
import uuid
import requests
from django.http import JsonResponse
import logging
import re
from datetime import datetime



logger = logging.getLogger(__name__)
# Initialize Paystack
paystack = Paystack(settings.PAYSTACK_SECRET_KEY)

def home(request):
    return render(request, 'index.html')

def appointments(request):
    return render(request, 'contact.html')

def impact_initiatives(request):
    return render(request, 'impact_initiatives.html')

def partnerships(request):
    return render(request, 'donate.html')




def donation_form(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number', '')
        donation_amount = request.POST.get('donation_amount')
        custom_amount = request.POST.get('custom_amount')
        message = request.POST.get('message', '')

        # Validate inputs
        if not full_name or not email:
            messages.error(request, 'Full name and email are required.')
            return render(request, 'donate.html')

        try:
            amount = float(custom_amount) if donation_amount == 'custom' else float(donation_amount)
            if amount <= 0:
                raise ValueError('Amount must be greater than zero.')
            amount_in_kobo = int(amount * 100)  # Convert NGN to kobo for Paystack
        except (ValueError, TypeError):
            messages.error(request, 'Invalid donation amount.')
            return render(request, 'donate.html')

        reference = str(uuid.uuid4())
        request.session['donation_details'] = {
            'full_name': full_name,
            'email': email,
            'phone_number': phone_number,
            'amount': amount,
            'message': message,
            'reference': reference,
        }

        return render(request, 'donate.html', {
            'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
            'amount_in_kobo': amount_in_kobo,
            'email': email,
            'reference': reference,
        })

    return render(request, 'donate.html', {'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})

def payment_callback(request):
    reference = request.GET.get('reference')
    if not reference:
        messages.error(request, 'No reference provided.')
        return redirect('donation_form')

    donation_details = request.session.get('donation_details')
    if not donation_details or donation_details['reference'] != reference:
        messages.error(request, 'Invalid or expired transaction reference.')
        return redirect('donation_form')

    try:
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        url = f"https://api.paystack.co/transaction/verify/{reference}"
        response = requests.get(url, headers=headers)
        result = response.json()

        if result['status'] and result['data']['status'] == 'success':
            # Admin email content
            admin_subject = 'New Donation to Auxichron Health'
            admin_plain_message = f"""
New Donation to Auxichron Health

Full Name: {donation_details['full_name']}
Email: {donation_details['email']}
Phone Number: {donation_details['phone_number'] or 'N/A'}
Amount: ₦{donation_details['amount']}
Message: {donation_details['message'] or 'N/A'}
Reference: {donation_details['reference']}

This is an automated message from the Auxichron Health donation system.
Contact: info@auxichronhealth.com | +2349059940348
"""
            admin_html_message = f"""
<html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f6f7; margin: 0; padding: 0;">
        <div style="max-width: 700px; margin: 40px auto; background: #fff; border: 1px solid #ddd; padding: 30px;">
            <div style="text-align: center; border-bottom: 1px solid #e1e1e1; padding-bottom: 15px; margin-bottom: 25px;">
                <img src="https://auxichronhealth.com/static/assets/img/logo/logo1.png" alt="Auxichron Health Logo" style="max-width: 150px;">
                <h1 style="color: #02015A; margin: 10px 0;">Auxichron Health</h1>
                <p style="font-size: 16px; color: #31353D;">New Donation Notification</p>
            </div>
            <p style="font-size: 15px; color: #31353D;">A new donation has been received with the following details:</p>
            <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
                <tr><td style="padding: 8px; font-weight: bold; width: 30%;">Full Name:</td><td style="padding: 8px;">{donation_details['full_name']}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Email:</td><td style="padding: 8px;">{donation_details['email']}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Phone Number:</td><td style="padding: 8px;">{donation_details['phone_number'] or 'N/A'}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Amount:</td><td style="padding: 8px;">₦{donation_details['amount']}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Message:</td><td style="padding: 8px;">{donation_details['message'] or 'N/A'}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Reference:</td><td style="padding: 8px;">{donation_details['reference']}</td></tr>
            </table>
            <p style="margin-top: 30px; font-size: 14px; color: #666;">
                This is an automated message from the Auxichron Health donation system.
            </p>
            <div style="text-align: center; border-top: 1px solid #e1e1e1; padding-top: 15px; margin-top: 25px;">
                <p style="font-size: 14px; color: #31353D;">Auxichron Health, 123 Health St, Wellness City, Nigeria</p>
                <p style="font-size: 14px; color: #31353D;">
                    <a href="mailto:info@auxichronhealth.com" style="color: #02015A; text-decoration: none;">info@auxichronhealth.com</a> | 
                    <a href="tel:+2349059940348" style="color: #02015A; text-decoration: none;">+2349059940348</a>
                </p>
                
            </div>
        </div>
    </body>
</html>
"""

            # Donor thank-you email content
            donor_subject = 'Thank You for Your Donation to Auxichron Health'
            donor_plain_message = f"""
Dear {donation_details['full_name']},

Thank you for your generous donation of ₦{donation_details['amount']} to Auxichron Health. Your support empowers us to deliver innovative healthcare services, provide patient care, and drive community outreach programs that transform lives.

Donation Amount: ₦{donation_details['amount']}
Reference: {donation_details['reference']}
{'Your Message: ' + donation_details['message'] if donation_details['message'] else ''}

Your contribution makes a lasting impact. Visit https://www.auxichronhealth.com/donate.html to make another donation.

Best regards,
The Auxichron Health Team

Contact: info@auxichronhealth.com | +2349059940348
"""
            donor_html_message = f"""
<html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f6f7; margin: 0; padding: 0;">
        <div style="max-width: 700px; margin: 40px auto; background: #fff; border: 1px solid #ddd; padding: 30px;">
            <div style="text-align: center; border-bottom: 1px solid #e1e1e1; padding-bottom: 15px; margin-bottom: 25px;">
                <img src="https://auxichronhealth.com/static/assets/img/logo/logo1.png" alt="Auxichron Health Logo" style="max-width: 150px;">
                <h1 style="color: #02015A; margin: 10px 0;">Thank You for Your Donation!</h1>
                <p style="font-size: 16px; color: #31353D;">Auxichron Health</p>
            </div>
            <p style="font-size: 15px; color: #31353D;">Dear {donation_details['full_name']},</p>
            <p style="font-size: 15px; color: #31353D;">We are deeply grateful for your generous donation of ₦{donation_details['amount']} to Auxichron Health. Your support empowers us to deliver innovative healthcare services, provide patient care, and drive community outreach programs that transform lives.</p>
            <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
                <tr><td style="padding: 8px; font-weight: bold; width: 30%;">Donation Amount:</td><td style="padding: 8px;">₦{donation_details['amount']}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Reference:</td><td style="padding: 8px;">{donation_details['reference']}</td></tr>
                {'<tr><td style="padding: 8px; font-weight: bold;">Your Message:</td><td style="padding: 8px;">' + donation_details['message'] + '</td></tr>' if donation_details['message'] else ''}
            </table>
            <p style="font-size: 15px; color: #31353D; margin-top: 20px;">Your contribution makes a lasting impact. Thank you for being part of our mission to improve healthcare outcomes.</p>
            <div style="text-align: center; margin-top: 20px;">
                <a href="https://www.auxichronhealth.com/donate.html" style="background: #02015A; color: #fff; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-size: 14px;">Make Another Donation</a>
            </div>
            <p style="font-size: 15px; color: #31353D; margin-top: 20px;">Best regards,<br>The Auxichron Health Team</p>
            <div style="text-align: center; border-top: 1px solid #e1e1e1; padding-top: 15px; margin-top: 25px;">
                <p style="font-size: 14px; color: #31353D;">Auxichron Health, 123 Health St, Wellness City, Nigeria</p>
                <p style="font-size: 14px; color: #31353D;">
                    <a href="mailto:info@auxichronhealth.com" style="color: #02015A; text-decoration: none;">info@auxichronhealth.com</a> | 
                    <a href="tel:+2349059940348" style="color: #02015A; text-decoration: none;">+2349059940348</a>
                </p>
                <div style="margin-top: 10px;">
                    <a href="https://facebook.com/auxichronhealth" style="margin: 0 5px;"><img src="https://www.auxichronhealth.com/static/assets/img/icons/facebook.png" alt="Facebook" style="width: 24px;"></a>
                    <a href="https://linkedin.com/company/auxichronhealth" style="margin: 0 5px;"><img src="https://www.auxichronhealth.com/static/assets/img/icons/linkedin.png" alt="LinkedIn" style="width: 24px;"></a>
                    <a href="https://instagram.com/auxichronhealth" style="margin: 0 5px;"><img src="https://www.auxichronhealth.com/static/assets/img/icons/instagram.png" alt="Instagram" style="width: 24px;"></a>
                    <a href="https://youtube.com/channel/auxichronhealth" style="margin: 0 5px;"><img src="https://www.auxichronhealth.com/static/assets/img/icons/youtube.png" alt="YouTube" style="width: 24px;"></a>
                </div>
            </div>
        </div>
    </body>
</html>
"""

            # Send email to admin
            try:
                send_mail(
                    subject=admin_subject,
                    message=admin_plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    html_message=admin_html_message,
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Error sending admin email: {str(e)}")  # Replace with logging in production

            # Send thank-you email to donor
            try:
                send_mail(
                    subject=donor_subject,
                    message=donor_plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[donation_details['email']],
                    html_message=donor_html_message,
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Error sending donor email: {str(e)}")  # Replace with logging in production

            messages.success(request, f"Thank you, {donation_details['full_name']}, for your donation of ₦{donation_details['amount']}!")
            return redirect('donation_success')
        else:
            messages.error(request, 'Payment was not successful.')
            return redirect('donation_form')
    except Exception as e:
        messages.error(request, f'Payment verification failed: {str(e)}')
        return redirect('donation_form')

def donation_success(request):
    donation_details = request.session.get('donation_details', {})
    if donation_details:
        del request.session['donation_details']  # Clean up session
    return render(request, 'success.html', {'donation_details': donation_details})
























def book_appointment(request):
    if request.method == 'POST':
        try:
            # Gather form data
            full_name = request.POST.get('full_name', '').strip()
            email = request.POST.get('email', '').strip()
            phone_number = request.POST.get('phone_number', '').strip()
            service_type = request.POST.get('service_type', 'Not specified')
            message = request.POST.get('message', '').strip()

            # Server-side validation
            required_fields = [full_name, email, phone_number, service_type]
            if not all(required_fields):
                missing_fields = [field for field, value in zip(['full_name', 'email', 'phone_number', 'service_type'], required_fields) if not value]
                logger.warning(f"Invalid submission: Missing fields - {', '.join(missing_fields)}")
                return JsonResponse({'success': False, 'message': 'Please fill in all required fields.'}, status=400)

            # Validate email format
            email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
            if not re.match(email_pattern, email):
                logger.warning(f"Invalid email format: {email}")
                return JsonResponse({'success': False, 'message': 'Please provide a valid email address.'}, status=400)

            # Validate phone format (Nigerian numbers: +234 or 0 followed by 10 digits)
            phone_pattern = r'^\+234[0-9]{10}$|^0[0-9]{10}$'
            if not re.match(phone_pattern, phone_number):
                logger.warning(f"Invalid phone format: {phone_number}")
                return JsonResponse({'success': False, 'message': 'Please provide a valid Nigerian phone number (e.g., +2349059940348 or 08034715913).'}, status=400)

            # Admin email content
            admin_subject = 'New Contact Request – Auxichron Health'
            admin_plain_message = f"""
New Contact Request for Auxichron Health

Full Name: {full_name}
Email: {email}
Phone Number: {phone_number}
Service Type: {service_type}
Message: {message or 'N/A'}

Submitted on: {datetime.now().strftime('%Y-%m-%d %I:%M %p WAT')}
This is an automated message from the Auxichron Health contact system.
Contact: info@auxichronhealth.com | +2349059940348
"""
            admin_html_message = f"""
<html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f6f7; margin: 0; padding: 0;">
        <div style="max-width: 700px; margin: 40px auto; background: #fff; border: 1px solid #ddd; padding: 30px;">
            <div style="text-align: center; border-bottom: 1px solid #e1e1e1; padding-bottom: 15px; margin-bottom: 25px;">
                <img src="https://auxichronhospital.com/static/assets/img/logo/auxichron-logo.png" alt="Auxichron Health Logo" style="max-width: 150px;">
                <h1 style="color: #02015A; margin: 10px 0;">Auxichron Health</h1>
                <p style="font-size: 16px; color: #31353D;">New Contact Request</p>
            </div>
            <p style="font-size: 15px; color: #31353D;">A new contact request has been submitted with the following details:</p>
            <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
                <tr><td style="padding: 8px; font-weight: bold; width: 30%;">Full Name:</td><td style="padding: 8px;">{full_name}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Email:</td><td style="padding: 8px;">{email}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Phone Number:</td><td style="padding: 8px;">{phone_number}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Service Type:</td><td style="padding: 8px;">{service_type}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Message:</td><td style="padding: 8px;">{message or 'N/A'}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Submitted On:</td><td style="padding: 8px;">{datetime.now().strftime('%Y-%m-%d %I:%M %p WAT')}</td></tr>
            </table>
            <p style="margin-top: 30px; font-size: 14px; color: #666;">
                This is an automated message from the Auxichron Health contact system.
            </p>
            <div style="text-align: center; border-top: 1px solid #e1e1e1; padding-top: 15px; margin-top: 25px;">
                <p style="font-size: 14px; color: #31353D;">Auxichron Health, 123 Health St, Wellness City, Nigeria</p>
                <p style="font-size: 14px; color: #31353D;">
                    <a href="mailto:info@auxichronhealth.com" style="color: #02015A; text-decoration: none;">info@auxichronhealth.com</a> | 
                    <a href="tel:+2349059940348" style="color: #02015A; text-decoration: none;">+2349059940348</a>
                </p>
                
            </div>
        </div>
    </body>
</html>
"""

            # User confirmation email content
            user_subject = 'Thank You for Contacting Auxichron Health'
            user_plain_message = f"""
Dear {full_name},

Thank you for contacting Auxichron Health. We have received your message and will get back to you as soon as possible.

Full Name: {full_name}
Email: {email}
Phone Number: {phone_number}
Service Type: {service_type}
Message: {message or 'N/A'}

For any urgent inquiries, please contact us at info@auxichronhealth.com or +2349059940348.

Best regards,
The Auxichron Health Team
"""
            user_html_message = f"""
<html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f6f7; margin: 0; padding: 0;">
        <div style="max-width: 700px; margin: 40px auto; background: #fff; border: 1px solid #ddd; padding: 30px;">
            <div style="text-align: center; border-bottom: 1px solid #e1e1e1; padding-bottom: 15px; margin-bottom: 25px;">
                <img src="https://auxichronhospital.com/static/assets/img/logo/auxichron-logo.png" alt="Auxichron Health Logo" style="max-width: 150px;">
                <h1 style="color: #02015A; margin: 10px 0;">Thank You for Contacting Us!</h1>
                <p style="font-size: 16px; color: #31353D;">Auxichron Health</p>
            </div>
            <p style="font-size: 15px; color: #31353D;">Dear {full_name},</p>
            <p style="font-size: 15px; color: #31353D;">Thank you for contacting Auxichron Health. We have received your message and will get back to you as soon as possible.</p>
            <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
                <tr><td style="padding: 8px; font-weight: bold; width: 30%;">Full Name:</td><td style="padding: 8px;">{full_name}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Email:</td><td style="padding: 8px;">{email}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Phone Number:</td><td style="padding: 8px;">{phone_number}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Service Type:</td><td style="padding: 8px;">{service_type}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Message:</td><td style="padding: 8px;">{message or 'N/A'}</td></tr>
            </table>
            <p style="font-size: 15px; color: #31353D; margin-top: 20px;">For any urgent inquiries, please contact us at <a href="mailto:info@auxichronhealth.com" style="color: #02015A; text-decoration: none;">info@auxichronhealth.com</a> or <a href="tel:+2349059940348" style="color: #02015A; text-decoration: none;">+2349059940348</a>.</p>
            <p style="font-size: 15px; color: #31353D; margin-top: 20px;">Best regards,<br>The Auxichron Health Team</p>
            <div style="text-align: center; border-top: 1px solid #e1e1e1; padding-top: 15px; margin-top: 25px;">
                <p style="font-size: 14px; color: #31353D;">Auxichron Health, 123 Health St, Wellness City, Nigeria</p>
                <p style="font-size: 14px; color: #31353D;">
                    <a href="mailto:info@auxichronhealth.com" style="color: #02015A; text-decoration: none;">info@auxichronhealth.com</a> | 
                    <a href="tel:+2349059940348" style="color: #02015A; text-decoration: none;">+2349059940348</a>
                </p>
                
            </div>
        </div>
    </body>
</html>
"""

            # Send email to admin
            try:
                send_mail(
                    subject=admin_subject,
                    message=admin_plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    html_message=admin_html_message,
                    fail_silently=True,
                )
                logger.info(f"Admin email sent to {settings.ADMIN_EMAIL} at {datetime.now().strftime('%Y-%m-%d %I:%M %p WAT')}")
            except Exception as e:
                logger.error(f"Error sending admin email to {settings.ADMIN_EMAIL}: {str(e)}")
                return JsonResponse({'success': False, 'message': 'Failed to process your request. Please try again later.'}, status=500)

            # Send confirmation email to user
            try:
                send_mail(
                    subject=user_subject,
                    message=user_plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    html_message=user_html_message,
                    fail_silently=True,
                )
                logger.info(f"User email sent to {email} at {datetime.now().strftime('%Y-%m-%d %I:%M %p WAT')}")
            except Exception as e:
                logger.error(f"Error sending user email to {email}: {str(e)}")
                # Continue with success response to avoid exposing error to user
                pass

            return JsonResponse({'success': True, 'message': f'Thank you, {full_name}, for contacting Auxichron Health! We will get back to you soon.'})

        except Exception as e:
            logger.error(f"Unexpected error in contact_us: {str(e)}")
            return JsonResponse({'success': False, 'message': 'An unexpected error occurred. Please try again later.'}, status=500)

    return render(request, 'contact.html')