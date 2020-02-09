from django.db import models
from decimal import Decimal

class Investors(models.Model):
    """
    A list of investors with their contact information
    """
    name = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=256)

    ### TO DO ###
    # Expand this model to capture all of the investors critical information

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(null=True, blank=True, auto_now=True)

    def __str__(self):
        return str(self.id)


class Funds(models.Model):
    """
    A list of investment funds which have been setup.
    """
    name = models.CharField(max_length=256)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(null=True, blank=True, auto_now=True)

    def __str__(self):
        return str(self.id)


class Commitments(models.Model):
    """
    The amount of money commited to each fund by specific investors
    After each request for funds, the amount_assigned value is increased.
    After all of the funds are assigned, set the is_exhausted flag to True
    """
    fund = models.ForeignKey(Funds,
                                related_name='commitments_funds',
                                on_delete=models.PROTECT)
    date_committed = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    amount_assigned = models.DecimalField(max_digits=15,
                                decimal_places=2,
                                default=Decimal('0.00'))
    is_exhausted = models.BooleanField(default=False)

    ### TO DO ###
    # Add Currency model to specify which currency , and link to the commitment

    investor = models.ForeignKey(Investors,
                                related_name='commitments_investors',
                                on_delete=models.PROTECT)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(null=True, blank=True, auto_now=True)

    def funds_available(self):
        """
        Returns the amount of funds available
        Returns False if nothing available
        """
        if self.is_exhausted:
            return False
        remaining = self.amount - self.amount_assigned
        if remaining == 0:
            self.is_exhausted = True
            self.save()
            return False

        ### TO DO ###
        # Catch exceptions where remaining is < 0
        return remaining

    def __str__(self):
        return str(self.id)


class FundingCalls(models.Model):
    """
    Details of each funding call requested
    id_tag denotes a custom call id number/string if required
    """
    id_tag = models.CharField(null=True, blank=True, max_length=256)
    date = models.DateField()
    investment_name = models.CharField(max_length=256)
    capital_required = models.DecimalField(max_digits=15, decimal_places=2)

    ### TO DO ###
    # Add a rules model, and add a foreign key here for the matching rules

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(null=True, blank=True, auto_now=True)

    def __str__(self):
        return str(self.id)


class FundingCallsComposition(models.Model):
    """
    Breaks down each funding call into the source of funds for each
    For example, if a call required 10M, then it might take 7M from one investor
    and 3M from another investor. itemise each separately
    """

    funding_call = models.ForeignKey(FundingCalls,
                            related_name='fundingcallscomposition_fundingcalls',
                            on_delete=models.PROTECT)
    commitment = models.ForeignKey(Commitments,
                            related_name='fundingcallscomposition_commitments',
                            on_delete=models.PROTECT)

    # Not essential but added to simplify queries
    fund = models.ForeignKey(Funds,
                            related_name='fundingcallscomposition_funds',
                            on_delete=models.PROTECT)

    amount = models.DecimalField(max_digits=15, decimal_places=2)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(null=True, blank=True, auto_now=True)

    def __str__(self):
        return str(self.id)
