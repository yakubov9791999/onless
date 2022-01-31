from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class AllowedRolesMixin(LoginRequiredMixin):
    allowed_roles = None

    def dispatch(self, *args, **kwargs):
        if not self.request.user.role in self.allowed_roles:
            return redirect(reverse_lazy('error_403'))
        return super().dispatch(*args, **kwargs)
