from rest_framework.permissions import BasePermission

class IsApprovedProfessional(BasePermission):
    message = "Votre compte professionnel n'a pas encore été approuvé"

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated 
            and request.user.user_type == 'PRO'
            and hasattr(request.user, 'professional')
            and request.user.professional.approved
        )
    

class IsOwnerProfessional(BasePermission):
    """
    Permission pour s'assurer que seul le propriétaire (Professional.user) peut modifier un établissement.
    """

    def has_object_permission(self, request, view, obj):
        # L'utilisateur doit être égal à obj.owner.user
        return request.user == obj.owner.user