from app.models.users.user_model import User

def user(request=None) -> User:
    """
    Returns the current user object.
    For now, this is a mock with hardcoded ID.
    Replace with actual authentication logic in production.
    """
    return User(id=1)
