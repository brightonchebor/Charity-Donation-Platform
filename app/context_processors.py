from .models import Campaign


def campaign(request):
    id = request.resolver_match.kwargs.get('id')
    if id:
        try:
            campaign = Campaign.objects.get(id=id)
            transactions = campaign.transactions.all()
            total_transactions = transactions.count()
            return {
                'campaign': campaign, 
                'transactions':transactions,
                'total_transactions': total_transactions
            }
        except Campaign.DoesNotExist:
            return {}
    return {}




