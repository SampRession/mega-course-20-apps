from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from .forms import JobForm
from .models import Form


def index(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"].title()
            last_name = form.cleaned_data["last_name"].title()
            email = form.cleaned_data["email"].lower()
            date = form.cleaned_data["date"]
            occupation = form.cleaned_data["occupation"].capitalize()
            
            Form.objects.create(first_name=first_name,
                                last_name=last_name,
                                email=email,
                                date=date,
                                occupation=occupation)

            message_body = f"Thank you for your submission, {first_name}.\n\n"\
                        f"Here are your data:\n" \
                        f"- Name: {first_name} {last_name}\n" \
                        f"- Available start date: {date}\n" \
                        f"- Current occupation: {occupation}\n\n" \
                        f"I will contact you later, have a great day!"
            email_message = EmailMessage(
                subject="Form submission confirmation",
                body=message_body,
                to=[email]
            )
            email_message.send()
            
            messages.success(
                request, 
                f"Hey {first_name}, your form was successfully submitted!"
            )
        return redirect("/")
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")