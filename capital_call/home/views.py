from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.conf import settings
from django.core.management import call_command
from django.db.models import Q

from .models import *

from decimal import Decimal
import json
import requests
import re
from io import StringIO


def index_home(request):
    """
    Landing page showing a link to the dashboard
    """
    return render(request, 'home/index.html', { })


def dashboard(request):
    """
    Dashboard showing the Investors which need to be contacted and for how much.
    This is currently very fragile and relies on Django maintaining dicts
    in a specific order. This is not ideal.
    """
    title = 'Capital Call Dashboard'

    funding_calls_composition = FundingCallsComposition.objects.all()

    # Create a dict showing allocated amount per fund. Default it to 0
    # Create a list of fund names at the same time
    funds_dict = {}
    funds_lists = Funds.objects.values_list('name', flat=True)
    for item in funds_lists:
        funds_dict[item] = 0

    # Create an object which summarises the necessary data for the dashboard
    fund_events = []
    for item in funding_calls_composition:
        # Buld return data object funding_calls_composition
        dict_obj = {"date":item.funding_call.date,
                    "call_id":item.funding_call.id,
                    }

        # Update the fund_name dict with the running total used for each fund
        fund_name = item.fund.name
        funds_dict[fund_name] = funds_dict[fund_name] + item.amount

        # Build a list of funds allocation data and merge into dict_obj
        new_list = []
        for key, value in funds_dict.items():
            new_list.append(value)
        dict_obj.update({"data":new_list})

        # Message for this item
        message = str(fund_name) + " allocate $" + format(item.amount,',') + " USD"
        dict_obj.update({"message":message})

        # Append new dictionary to the output
        fund_events.append(dict_obj)

    return render(request, 'home/dashboard.html', {
                        'title':title,
                        'funds_lists':funds_lists,
                        'fund_events':fund_events,
                        })


def new_call(request):
    """
    Create New Call Page
    1) View to Create Call
    2) POST to process call data (date, rules, investment_name, capital_required)
    """
    title = 'Create New Call'
    # Calculate how much committed funds are still available
    funds_available = 0
    commitments_data = Commitments.objects.filter(is_exhausted=False)
    for item in commitments_data:
        remaining = item.amount - item.amount_assigned
        if remaining < 0:
            # An error has occured in the past, return error
            return JsonResponse({"status":"error",
                                "msg":"Assigned Funds > Funds Available"},
                                safe = False,
                                status = 500)
        funds_available = funds_available + remaining


    if request.method == 'POST':
        date = request.POST.get("date", False)
        rules = request.POST.get("rules", False)
        investment_name = request.POST.get("investment_name", False)
        capital_required = request.POST.get("capital_required", False)

        # Clean the Inputs
        if date == "":
            date = False
        if rules == "":
            rules = False
        if investment_name == "":
            investment_name = False
        if capital_required == "":
            capital_required = False

        # Perform validation on the POST inputs
        # If validation fails, return the user to the page with a message
        if date == False or rules == False or investment_name == False or \
                                            capital_required == False:
            message = "Invalid Inputs, please try again"
            return render(request, 'home/new_call.html', {
                                    'title':title,
                                    'funds_available':funds_available,
                                    'message':message
                                    })

        ### TODO ###
        # Validate "date" is a valid date

        # Validate "rules" value of rules corresponds to the right method

        # Validate "investment_name" has no offensive special characters

        # Validate "capital_required" is a 2dp decimcal number

        # Validate sufficient unallocated funds are available


        # Create new entry for the funding call
        new_call = FundingCalls(date = date,
                                investment_name = investment_name,
                                capital_required = capital_required)
        new_call.save()

        # Process the funding call

        # Get the available funding, and order by necessary matching rule
        commits = Commitments.objects.filter(is_exhausted=False)
        commits = list(commits.order_by('date_committed', 'id' ))

        ### TO DO ###
        # Validate that this order_by is correct vs the rules

        # Loop over the funding commits and allocate capital until done
        net_capital_required = Decimal(capital_required)
        for item in commits:
            funds_available = item.funds_available()
            if funds_available:
                # 3 unique cases which can exist for this matching
                if funds_available >= net_capital_required:
                    item.amount_assigned = item.amount_assigned + net_capital_required
                    if funds_available == net_capital_required:
                        item.is_exhausted = True
                    item.save()
                    new_comp = FundingCallsComposition(funding_call=new_call,
                                                        commitment=item,
                                                        fund=item.fund,
                                                        amount=net_capital_required
                                                        )
                    new_comp.save()
                    net_capital_required = 0
                    break
                else:
                    item.amount_assigned = item.amount_assigned + funds_available
                    item.is_exhausted = True
                    item.save()
                    net_capital_required = net_capital_required - funds_available
                    new_comp = FundingCallsComposition(funding_call=new_call,
                                                        commitment=item,
                                                        fund=item.fund,
                                                        amount=funds_available
                                                        )
                    new_comp.save()

        # Call successfully allocated

        ### TO DO ###
        # Create a page to confirm the call was processed and show details

        return redirect("/dashboard")


    # Render the new call page if method is not POST
    return render(request, 'home/new_call.html', {
                        'title':title,
                        'funds_available':funds_available,
                        })


def summary(request):
    """
    A summary page which shows all of the data in the database
    """
    title = 'Database Summary'

    investor_data = Investors.objects.all()
    funds_data = Funds.objects.all()
    commitments_data = Commitments.objects.all()
    funding_calls = FundingCalls.objects.all()
    funding_calls_composition = FundingCallsComposition.objects.all()

    return render(request, 'home/summary.html', {
                        'title':title,
                        'investor_data':investor_data,
                        'funds_data':funds_data,
                        'commitments_data':commitments_data,
                        'funding_calls':funding_calls,
                        'funding_calls_composition':funding_calls_composition,
                        })


def reset_data(request):
    """
    Clears all of the database tables
    Reloads the fixture data
    """

    # Clear all tables
    call_command('flush', interactive=False)

    # Reload the Fixtures
    out = StringIO()
    call_command("loaddata", "home/fixtures.json", stdout=out)

    return JsonResponse({"status":"ok",
                            "msg":out.getvalue(),
                            "fixture":"home/fixtures.json"},
                            safe = False,
                            status = 200)
