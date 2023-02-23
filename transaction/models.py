from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import Q, Sum, Count
from django.db.models.functions import Coalesce


# Create your models here.


class Transactions(models.Model):
    CHARGE = 1
    PURCHASE = 2
    TRANSFER_RECEIVED = 3
    TRANSFER_SENT = 4

    TRANSACTION_TYPE_CHOICES = (
        (CHARGE, 'Charge'),
        (PURCHASE, 'Purchase'),
        (TRANSFER_RECEIVED, 'Transfer received'),
        (TRANSFER_SENT, 'Transfer sent'),
    )
    user = models.ForeignKey(User, related_name='transactions', on_delete=models.RESTRICT)
    transaction_type = models.PositiveSmallIntegerField(choices=TRANSACTION_TYPE_CHOICES, default=CHARGE)
    amount = models.BigIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.get_transaction_type_display()} - {self.amount}"

    def get_transaction_type_display(self):
        pass

    @classmethod
    def get_report(cls):
        positive_transactions = Sum(
            'transactions__amount',
            filter=Q(transactions__transaction_type__in=[1, 3]))

        negative_transactions = Sum(
            'transactions__amount',
            filter=Q(transactions__transaction_type__in=[2, 4]))
        users = User.objects.all().annotate(
            transaction_count=Count('transactions__id'),
            balance=Coalesce(positive_transactions, 0) - Coalesce(negative_transactions, 0)
        )

        return users

    @classmethod
    def get_total_balance(cls):
        queryset = cls.get_report()
        return queryset.aggregate(Sum('balance'))

    @classmethod
    def user_balance(cls, user):
        positive_transaction = Sum('amount', filter=Q(transaction_type__in=[1, 3]))
        negative_transaction = Sum('amount', filter=Q(transaction_type__in=[2, 4]))

        user_balance = user.transactions.all().aggregate(
            balance=Coalesce(positive_transaction, 0) - Coalesce(negative_transaction, 0)
        )

        return user_balance.get('balance', 0)


class UserBalance(models.Model):
    user = models.ForeignKey(User, related_name='balance_records', on_delete=models.RESTRICT)
    balance = models.BigIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.balance} - {self.created_time}"

    @classmethod
    def record_user_balance(cls, user):
        balance = Transactions.user_balance(user)
        instance = cls.objects.create(user=user, balance=balance)
        return instance

    @classmethod
    def record_all_users_balance(cls):
        for user in User.objects.all():
            cls.record_user_balance(user)


class TransfrerTransaction(models.Model):
    sender_transaction = models.ForeignKey(
        Transactions, related_name='sent_transfer', on_delete=models.RESTRICT)
    receiver_transaction = models.ForeignKey(
        Transactions, related_name='received_transfer', on_delete=models.RESTRICT)

    def __str__(self):
        return f"{self.sender_transaction} >> {self.receiver_transaction}"

    @classmethod
    def transfer(cls, sender, receiver, amount):
        if Transactions.user_balance(sender) < amount:
            return "Transaction not Allowed, balance not enough"

        with transaction.atomic():
            send_transaction = Transactions.objects.create(
                user=sender, amount=amount, transaction_type=Transactions.TRANSFER_SENT)

            receiver_transaction = Transactions.objects.create(
                user=receiver, amount=amount, transaction_type=Transactions.TRANSFER_RECEIVED
            )

            instance = cls.objects.create(
                send_transaction=send_transaction, receiver_transaction=receiver_transaction)

            return instance


class UserScore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()

    @classmethod
    def change_score(cls, user, score):
        instance = cls.objects.select_for_update().get(user=user)
        with transaction.atomic():
            if not instance.exists():
                instance = cls.objects.create(user=user, score=0)

            else:
                instance = instance.first()
            instance.score += score
            instance.save()
