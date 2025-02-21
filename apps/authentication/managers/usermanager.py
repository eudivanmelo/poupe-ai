from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        """
        Gerenciador de modelo de usuário personalizado, onde email são os identificadores 
        exclusivos para autenticação em vez de nomes de usuário.

        Args:
            email (string): Email do usuário.
            password (string, optional): Senha do usuário. Defaults to None.

        Raises:
            ValueError: O campo Email deve ser definido.

        Returns:
            CustomUser: Usuário criado.
        """
        if not email:
            raise ValueError('O campo Email deve ser definido.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Cria um superusuário.

        Args:
            email (string): Email do usuário.
            password (string, optional): Senha do usuário. Defaults to None.

        Raises:
            ValueError: O superusuário deve ter is_staff=True.
            ValueError: O superusuário deve ter is_superuser=True.

        Returns:
            CustomUser: Usuário criado.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("O superusuário deve ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("O superusuário deve ter is_superuser=True.")
        return self.create_user(email, password, **extra_fields)