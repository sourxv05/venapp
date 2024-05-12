


from django.db import models

class profile(models.Model):
    name = models.CharField(max_length=100)  #  name
    address = models.TextField()  #  address
    # <Contact details>
    phone =models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    code = models.CharField(max_length=20, unique=True)  # Unique code
    # on_time_delivery_rate = models.FloatField(default=0.0)  # Historical on-time delivery rate
    # quality_rating_avg = models.FloatField(default=0.0)  # Historical quality rating average
    # average_response_time = models.FloatField(default=0.0)  # Historical average response time
    # fulfillment_rate = models.FloatField(default=0.0)  # Historical fulfillment rate



    def __str__(self):
        return self.name






#po





class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey('profile', on_delete=models.CASCADE)


    items = models.TextField()  # Details of items ordered
    quantitye = models.IntegerField()
    status = models.CharField(max_length=100)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateField(null=True)
    acknowledgment_date = models.DateField(null=True)
    od = models.DateField(null=True)
    dd = models.DateField(null=True)

    def __str__(self):
        return f"PO {self.po_number} for {self.vendor.name}"





class VendorProfile(models.Model):
    vendor = models.OneToOneField(profile, on_delete=models.CASCADE, related_name="evaluation")
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.vendor.name} evaluation"
