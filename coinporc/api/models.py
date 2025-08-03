from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as gis_models

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('CLIENT', 'Client'),
        ('PRO', 'Professionnel'),
        ('ADMIN', 'Administrateur'),
    ]

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='CLIENT')
    phone = models.CharField(max_length=20, blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True)
    favorites = models.ManyToManyField('Establishment', blank=True)  # Établissements favoris
    email_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    

class Professional(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'PRO'}
    )
    company_name = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.company_name} ({self.user.email})"

class Establishment(models.Model):
    PORK_TYPES = [
        ('TRAD', 'Traditionnel'),
        ('FOUR', 'Au four'),
        ('AIL', 'A l\'ail'),
        ('AUTRE', 'Autre recette'),
    ]
    
    owner = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='owned_establishments')
    name = models.CharField(max_length=100)
    description = models.TextField()
    pork_type = models.CharField(max_length=10, choices=PORK_TYPES)
    location = gis_models.PointField()  # Nécessite PostGIS
    opening_hours = models.JSONField()  # Ex: {"lundi": "09:00-18:00", ...}
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    pending_deletion = models.BooleanField(default=False)
    
    @property
    def average_rating(self):
        return self.reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0
        
    def __str__(self):
        return f"{self.name} ({self.city})"
    

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    pork_quality = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    service_rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    photo = models.ImageField(upload_to='reviews/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'establishment')  # 1 avis par utilisateur/établissement
    
    def __str__(self):
        return f"Avis de {self.user} sur {self.establishment}"
    

class EstablishmentImage(models.Model):
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='establishments/')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_approved = models.BooleanField(default=False)  # Modération admin
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Photo de {self.establishment.name}"
    

class Promotion(models.Model):
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE, related_name='promotions')
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    discount = models.CharField(max_length=50, blank=True)  # "-20%", "1 acheté = 1 offert"
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} @ {self.establishment}"
    

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateTimeField()
    guests = models.PositiveSmallIntegerField(default=1)
    special_request = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Réservation #{self.id} pour {self.establishment}"

