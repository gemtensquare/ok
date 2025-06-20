import os, base64
from django.db import models
from cryptography.fernet import Fernet


# Fernet.generate_key().decode()
FERNET_KEY = "JurrhiWVlgVSA89BiQ5-ya9GDxeowe6bjrOxbrnSB6o="
cipher = Fernet(FERNET_KEY.encode())


class GemtenPage(models.Model):
    page_name = models.CharField(max_length=100)
    page_id = models.TextField()
    page_token = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.page_name}"
    

    def save(self, *args, **kwargs):
        try:
            cipher.decrypt(self.page_token.encode())
            print("\n*** page_token Already encrypted.")
        except Exception:
            print("\n***Encrypting page_token...\n")
            self.page_token = cipher.encrypt(self.page_token.encode()).decode()

        try:
            cipher.decrypt(self.page_id.encode())
            print("\n*** page_id Already encrypted.")
        except Exception:
            print("\n***Encrypting page_id...\n")
            self.page_id = cipher.encrypt(self.page_id.encode()).decode()
        super().save(*args, **kwargs)


    def get_token(self):
        return cipher.decrypt(self.page_token.encode()).decode()
    
    def get_id(self):
        return cipher.decrypt(self.page_id.encode()).decode()
    
    def get_name(self):
        return self.page_name