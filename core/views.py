from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView, BaseDetailView
from .models import Package, Profile, Branch, Stock, TypeStock, Currency
from django.db.models import Q
from dateutil.parser import parse as du_parse
from dateutil.relativedelta import relativedelta
import datetime

class Home(ListView):
    template_name = "core/index.html"

    def get_queryset(self):
        id = self.kwargs.get('id')
        divers_branch = self.get_divers_branch(id)
        all_users = Profile.objects.all()
        divers_type = self.get_divers_type(id)
        divers_currency, all_price = self.get_diver_currency(id)
        user = Profile.objects.get(id=id)
        profit = self.profit_package(id)
        error, recomend = [], []
        stock = Stock.objects.filter(package__profile=user).values('name', 'type__name', 'currency__name', 'price', 'branch__name', 'package__count', 'risk')
        if user.type_risk.name == "Агрессивный":
            error, recomend = self.recomend_agressive(divers_branch, divers_type, divers_currency, stock)
        elif user.type_risk.name == "Умеренный":
            error, recomend = self.recomend_normal(divers_branch, divers_type, divers_currency, stock)
        elif user.type_risk.name == "Консервативный":
            error, recomend = self.recomend_conserv(divers_branch, divers_type, divers_currency, stock)
        return {
            'divBranch': divers_branch,
            'divType': divers_type,
            'divCurrency': divers_currency,
            'user': user,
            'stock': stock,
            'error': error,
            'recomend': recomend,
            'all_price_rub': round(all_price, 2),
            'all_price_dol': round(all_price/76, 2),
            'all_users': all_users,
            'profit': round(profit, 2)
        }
    def profit_package(self, id):
        pak = Package.objects.filter(profile_id=id)
        profit = 0
        for item in pak:
            now_price = item.now_price
            start_price = item.start_price
            count = item.count
            devident = item.stock.devidents
            delta = relativedelta(du_parse(str(datetime.datetime.now())), du_parse(str(item.date_buy))).months
            tmp = (now_price - start_price)*count + devident*delta
            tmp = tmp if item.stock.currency.name == "Руб" else tmp * 76
            profit += tmp
        return profit
        
    def recomend_conserv(self, divers_branch, divers_type, divers_currency, stock):
        error_message_container = []
        comment_message_container = []
        error_message = ""
        comment_message = ""
        if len(divers_branch) >= 7:
            error_branch = [key for key, items in divers_branch.items() if divers_branch[key] >= 20 ]
            if len(error_branch) > 0:
                error_message = 'В вашем портфеле доминируют бумаги следующих отраслей: '
                for index, item in enumerate(error_branch):
                    error_message += "'" + str(item) + "'"
                    if (index != len(error_branch) - 1):
                        error_message += ", "
                comment_message = 'Рекомендуем перераспределить активы по разным отраслям, путем покупки новых облигаций и продажи текущих ценных бумаг'
        else:
            error_message = 'Ваш портфель покрывает небольшой набор отраслей, для уменьшения риска, необходимо иметь акции хотя бы 7 отраслей'
            comment_message = 'Рекомендуем приобрести ценные бумаги из различных отраслей'
        error_message_container.append(error_message)
        comment_message_container.append(comment_message)
        if len(divers_currency) < 2:
            error_message = 'Слишком опасно иметь активы в одной валюте'
            comment_message = 'Рекомендуем приобрести активы в другой валюте'
            error_message_container.append(error_message)
            comment_message_container.append(comment_message)
        else:
            error_currency = [key for key, items in divers_currency.items() if divers_currency[key] >=60 ]
            if len(error_currency) > 0:
                error_message = 'В вашем портфеле преобладают активы в следующих валютах: '
                comment_message = 'Рекомендуем продать активы в следующих валютах: '
                for index, item in enumerate(error_currency):
                    error_message += "'" + str(item) + "'"
                    comment_message += "'" + str(item) + "'"
                    if (index != len(error_currency) - 1):
                        error_message += ", "
                    else:
                        comment_message += " и докупить активы в других валютах"
            error_message_container.append(error_message)
            comment_message_container.append(comment_message)
        error_type_obligation = divers_type.get("Облигация", True)
        if error_type_obligation < 80 and error_type_obligation:
            error_message = 'В вашем активе меньше 80% облигаций, поэтому большой риск потери инвестиции'
            comment_message = 'Докупите облигации'

            error_message_container.append(error_message)
            comment_message_container.append(comment_message)
        
        stock_without_risk = stock.filter(risk__gte=1)
        if len(stock_without_risk)!= 0:
            error_message = 'В вашем портфеле есть активы с высоким уровнем риска'
            comment_message = 'Рекомендуем продать активы, с риском больше 1'

            error_message_container.append(error_message)
            comment_message_container.append(comment_message)

        return error_message_container, comment_message_container

    def recomend_normal(self, divers_branch, divers_type, divers_currency, stock):
        error_message_container = []
        comment_message_container = []
        error_message = ""
        comment_message = ""
        if len(divers_branch) >= 5:
            error_branch = [key for key, items in divers_branch.items() if divers_branch[key] >=30 ]
            if len(error_branch) > 0:
                error_message = 'В вашем портфеле доминируют бумаги следующих отраслей: '
                for index, item in enumerate(error_branch):
                    error_message += "'" + str(item) + "'"
                    if (index != len(error_branch) - 1):
                        error_message += ", "
                comment_message = 'Рекомендуем перераспределить активы по разным отраслям, для уменьшения риска, необходимо иметь акции хотя бы 5 отраслей'
        else:
            error_message = 'Ваш портфель покрывает небольшой набор отраслей'
            comment_message = 'Рекомендуем приобрести ценные бумаги из различных отраслей'
        error_message_container.append(error_message)
        comment_message_container.append(comment_message)
        if len(divers_currency) < 2:
            error_message = 'Слишком опасно иметь активы в одной валюте'
            comment_message = 'Рекомендуем приобрести активы в другой валюте'
            error_message_container.append(error_message)
            comment_message_container.append(comment_message)
        else:
            error_currency = [key for key, items in divers_currency.items() if divers_currency[key] >= 60 ]
            if len(error_currency) > 0:
                error_message = 'В вашем портфеле преобладают активы в следующих валютах: '
                comment_message = 'Рекомендуем продать активы в следующих валютах: '
                for index, item in enumerate(error_currency):
                    error_message += "'" + str(item) + "'"
                    comment_message += "'" + str(item) + "'"
                    if (index != len(error_currency) - 1):
                        error_message += ", "
                    else:
                        comment_message += " и докупить активы в других валютах"
            error_message_container.append(error_message)
            comment_message_container.append(comment_message)
        error_type_stock = divers_type.get("Акция", True)
        error_type_obligation = divers_type.get("Облигация", True)
        if error_type_stock and (error_type_stock < 50 or error_type_stock > 60):
            if error_type_obligation and (error_type_obligation < 40 or error_type_obligation > 50):
                error_message = 'У вас не правильное распределение типов активов'
                comment_message = 'Нужно добиться следующих показателей: акции - от 50 до 60, облигации - от 40 до 50'
            else:
                error_message = 'У вас не правильные показатели акций'
                comment_message = 'Нужно добиться следующих показателей: акции - от 50 до 60'
            error_message_container.append(error_message)
            comment_message_container.append(comment_message)

        stock_without_risk = stock.filter(risk__gte=1)
        if len(stock_without_risk) > 3:
            error_message = 'В вашем портфеле много активов с высоким уровнем риска'
            comment_message = 'Рекомендуем оставить не больше 3 активов с высоким уровнем риска'

            error_message_container.append(error_message)
            comment_message_container.append(comment_message)
        elif len(stock_without_risk) == 0:
            error_message = 'В вашем портфеле нет активов с повышенным уровнем риска'
            comment_message = 'Рекомендуем купить несколько активов с повышенным уровнем риска, для увеличения прибыли'

            error_message_container.append(error_message)
            comment_message_container.append(comment_message)
        return error_message_container, comment_message_container

    def recomend_agressive(self, divers_branch, divers_type, divers_currency, stock):
        error_message_container = []
        comment_message_container = []
        error_message = ""
        comment_message = ""
        if len(divers_branch) >= 5:
            error_branch = [key for key, items in divers_branch.items() if divers_branch[key] >=40 ]
            if len(error_branch) > 0:
                error_message = 'В вашем портфеле доминируют бумаги следующих отраслей: '
                for index, item in enumerate(error_branch):
                    error_message += "'" + str(item) + "'"
                    if (index != len(error_branch) - 1):
                        error_message += ", "
                comment_message = 'Рекомендуем перераспределить активы по разным отраслям'
        else:
            error_message = 'Ваш портфель покрывает небольшой набор отраслей'
            comment_message = 'Рекомендуем приобрести ценные бумаги из различных отраслей'
        error_message_container.append(error_message)
        comment_message_container.append(comment_message)
        if len(divers_currency) < 2:
            error_message = 'Слишком опасно иметь активы в одной валюте'
            comment_message = 'Рекомендуем приобрести активы в другой валюте'
            error_message_container.append(error_message)
            comment_message_container.append(comment_message)
        else:
            error_currency = [key for key, items in divers_currency.items() if divers_currency[key] >=80 ]
            if len(error_currency) > 0:
                error_message = 'В вашем портфеле преобладают активы в следующих валютах: '
                comment_message = 'Рекомендуем продать активы в следующих валютах: '
                for index, item in enumerate(error_currency):
                    error_message += "'" + str(item) + "'"
                    comment_message += "'" + str(item) + "'"
                    if (index != len(error_currency) - 1):
                        error_message += ", "
                    else:
                        comment_message += " и докупить активы в других валютах"
            error_message_container.append(error_message)
            comment_message_container.append(comment_message)
        error_type = divers_type.get("Акция", True)
        if error_type and error_type < 80:
            error_message = 'В вашем активе меньше 80% акции, чего не достаточно для получения желаемой прибыли'
            comment_message = 'Докупите акции'
            error_message_container.append(error_message)
            comment_message_container.append(comment_message)
        stock_without_risk = stock.filter(risk__gte=1)
        if len(stock_without_risk) < 5:
            error_message = 'В вашем портфеле не хватает активов с высоким уровнем риска, из-за этого может упасть доход'
            comment_message = 'Рекомендуем купить больше активов с высоким уровнем риска'

            error_message_container.append(error_message)
            comment_message_container.append(comment_message)
        return error_message_container, comment_message_container


    def get_divers_branch(self, id):
        user = Profile.objects.get(id=id)
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
    
    def get_divers_type(self, id):
        user = Profile.objects.get(id=id)
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
    
    def get_diver_currency(self, id):
        user = Profile.objects.get(id=id)
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
        return divers_currency, all_price
