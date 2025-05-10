from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages


# Create your views here.
def transfer_view(request):
    if request.method == 'POST':
        sender_account_no = request.POST.get('sender_account_no')
        receiver_account_no = request.POST.get('receiver_account_no')
        amount = request.POST.get('amount')

        print("SENDER", sender_account_no)
        print("RECEIVER", receiver_account_no)
        print("AMOUNT", amount)

        try:
            amount = float(amount)
            if amount <= 0:
                messages.error(request, 'Amount must be greater than 0')
                return render(request, 'transfer_form.html')
        except ValueError:
            messages.error(request, 'Invalid amount')
            return render(request, 'transfer_form.html')
                
        with connection.cursor() as cursor:
            # Set the isolation level to SERIALIZABLE
            cursor.execute('SET TRANSACTION ISOLATION LEVEL SERIALIZABLE')
            cursor.callproc('transfer_funds', [sender_account_no, receiver_account_no, amount])
            result = cursor.fetchone()
            if result[0]:
                messages.success(request, 'Funds transferred successfully.')
            else:
                messages.error(request, 'Funds transfer failed.')
            return redirect('transfer_form')
    else:
        return render(request, 'transfer_form.html') 