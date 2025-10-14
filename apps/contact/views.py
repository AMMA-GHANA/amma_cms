from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactInquiry
from apps.core.models import SiteSettings


def contact_page(request):
    """Display contact page with form and contact information."""
    site_settings = SiteSettings.load()

    context = {
        'site_settings': site_settings,
    }
    return render(request, 'contact/page.html', context)


def contact_submit(request):
    """Handle contact form submission."""
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', 'general')
        message_text = request.POST.get('message', '').strip()

        # Basic validation
        if not name or not email or not message_text:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('contact:page')

        try:
            # Create contact inquiry
            inquiry = ContactInquiry.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message_text
            )

            # Send email notification to site administrators
            try:
                admin_email = settings.DEFAULT_FROM_EMAIL
                send_mail(
                    subject=f'New Contact Inquiry: {inquiry.get_subject_display()}',
                    message=f'''
New contact inquiry from {name}

Email: {email}
Phone: {phone}
Subject: {inquiry.get_subject_display()}

Message:
{message_text}

Submitted: {inquiry.submitted_date}
                    '''.strip(),
                    from_email=admin_email,
                    recipient_list=[admin_email],
                    fail_silently=True,
                )
            except Exception:
                pass  # Don't fail if email doesn't send

            messages.success(
                request,
                'Thank you for contacting us! We have received your message and will respond as soon as possible.'
            )
            return redirect('contact:page')

        except Exception as e:
            messages.error(request, 'An error occurred while submitting your message. Please try again.')
            return redirect('contact:page')

    else:
        # If not POST, redirect to contact page
        return redirect('contact:page')
