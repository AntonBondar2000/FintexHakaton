from django.db import models

class TypeRisk(models.Model):
    name = models.CharField(max_length=255)
    class Meta:
        verbose_name = ('Type Risk')
        verbose_name_plural = ('Type Risks')

    def __str__(self):
        return self.name

class Profile(models.Model):
    name = models.CharField(max_length=255)
    type_risk = models.ForeignKey(
        TypeRisk,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    class Meta:
        verbose_name = ('Profile')
        verbose_name_plural = ('Profiles')
    def __str__(self):
        return self.name

class Branch(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self):
        return self.name

class Currency(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self):
        return self.name

class TypeStock(models.Model):
    name = models.CharField(max_length=255)
    class Meta:
        verbose_name = ('Type Stock')
        verbose_name_plural = ('Type Stocks')

    def __str__(self):
        return self.name

class Stock(models.Model):
    name = models.CharField(max_length=255)
    volume = models.PositiveIntegerField()
    price = models.FloatField()
    type = models.ForeignKey(
        TypeStock,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    start_price = models.FloatField()
    currency = models.ForeignKey(
        Currency,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    branch = models.ForeignKey(
        Branch,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    class Meta:
        verbose_name = ('Stock')
        verbose_name_plural = ('Stocks')

    def __str__(self):
        return self.name


class Package(models.Model):
    count = models.PositiveIntegerField()
    stock = models.ForeignKey(
        Stock,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    profile = models.ForeignKey(
            Profile,
            blank=True,
            null=True,
            on_delete=models.CASCADE,
    )
    class Meta:
        verbose_name = ('Package')
        verbose_name_plural = ('Packages')

    def __str__(self):
        return str(self.id)
    
    def get_divers_branch(self):
        
        print("a;egadmgpoag")
        return None


class DeltaPrice(models.Model):
    date = models.DateField()
    price = models.FloatField()
    stock = models.ForeignKey(
        Stock,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    class Meta:
        verbose_name = ('Delta Price')
        verbose_name_plural = ('Delta Prices')

    def __str__(self):
        return str(self.id)