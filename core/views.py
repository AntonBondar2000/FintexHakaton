from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView, BaseDetailView
from .models import Package, Profile, Branch, Stock, TypeStock, Currency
from django.db.models import Q

class Home(ListView):
    template_name = "core/index.html"

    def get_queryset(self):
        divers_branch = self.get_divers_branch()
        divers_type = self.get_divers_type()
        divers_currency = self.get_diver_currency()
        print(divers_currency)
        user = Profile.objects.get(id=1)
        stock = Stock.objects.filter(package__profile=user).values('name', 'type__name', 'currency__name', 'price', 'branch__name', 'package__count')
        print(stock)
        return {
            'divBranch': divers_branch,
            'divType': divers_type,
            'divCurrency': divers_currency,
            'user': user,
            'stock': stock
        }
    def get_divers_branch(self):
        user = Profile.objects.get(id=1)
        pak = Package.objects.filter(profile=user)
        branch = Branch.objects.filter(stock__package__profile_id=user.id)
        divers_branch = {}
        all_price = 0
        for item in branch:
            current_pak = pak.filter(stock__branch=item)
            for st in current_pak:
                current_stock = Stock.objects.get(id=st.stock_id)
                price = current_stock.price
                if(current_stock.currency.name!="Руб"):
                    price *= 76
                price = price * st.count
                if item.name in divers_branch:
                    divers_branch[item.name] += price
                else:
                    divers_branch.update({item.name: price})
                all_price += price
        for item in divers_branch:
            divers_branch[item] = round(divers_branch[item]/all_price*100, 2)
        return divers_branch
    
    def get_divers_type(self):
        user = Profile.objects.get(id=1)
        pak = Package.objects.filter(profile=user)
        type_stock = TypeStock.objects.filter(stock__package__profile_id=user.id)
        divers_type = {}
        all_price = 0
        for item in type_stock:
            current_pak = pak.filter(stock__type=item)
            for st in current_pak:
                current_stock = Stock.objects.get(id=st.stock_id)
                price = current_stock.price
                if(current_stock.currency.name!="Руб"):
                    price *= 76
                price = price * st.count
                if item.name in divers_type:
                    divers_type[item.name] += price
                else:
                    divers_type.update({item.name: price})
                all_price += price
        for item in divers_type:
            divers_type[item] = round(divers_type[item]/all_price*100, 2)
        return divers_type
    
    def get_diver_currency(self):
        user = Profile.objects.get(id=1)
        pak = Package.objects.filter(profile=user)
        type_currency = Currency.objects.filter(stock__package__profile_id=user.id)
        divers_currency = {}
        all_price = 0
        for item in type_currency:
            current_pak = pak.filter(stock__currency=item)
            for st in current_pak:
                current_stock = Stock.objects.get(id=st.stock_id)
                price = current_stock.price
                if(current_stock.currency.name!="Руб"):
                    price *= 76
                price = price * st.count
                if item.name in divers_currency:
                    divers_currency[item.name] += price
                else:
                    divers_currency.update({item.name: price})
                all_price += price
        for item in divers_currency:
            divers_currency[item] = round(divers_currency[item]/all_price*100, 2)
        return divers_currency
