from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import AnnouncementForm
from .models import Announcement
from .permissions import ModeratorOrAdminRequiredMixin, can_manage_announcements


class AnnouncementListView(ListView):
    """Список оголошень. Доступний усім; неопубліковані бачать лише мод./адмін."""

    model = Announcement
    template_name = "announcements/announcement_list.html"
    context_object_name = "announcements"
    paginate_by = 10

    def get_queryset(self):
        qs = Announcement.objects.select_related("created_by")
        if not can_manage_announcements(self.request.user):
            qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_manage"] = can_manage_announcements(self.request.user)
        return context


class AnnouncementDetailView(DetailView):
    """Детальний перегляд оголошення."""

    model = Announcement
    template_name = "announcements/announcement_detail.html"
    context_object_name = "announcement"

    def get_queryset(self):
        qs = Announcement.objects.select_related("created_by")
        if not can_manage_announcements(self.request.user):
            qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_manage"] = can_manage_announcements(self.request.user)
        return context


class AnnouncementCreateView(ModeratorOrAdminRequiredMixin, CreateView):
    """Створення оголошення — лише модератори/адміністратори."""

    model = Announcement
    form_class = AnnouncementForm
    template_name = "announcements/announcement_form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Оголошення успішно створено.")
        return super().form_valid(form)


class AnnouncementUpdateView(ModeratorOrAdminRequiredMixin, UpdateView):
    """Редагування оголошення — лише модератори/адміністратори."""

    model = Announcement
    form_class = AnnouncementForm
    template_name = "announcements/announcement_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Оголошення оновлено.")
        return super().form_valid(form)


class AnnouncementDeleteView(ModeratorOrAdminRequiredMixin, DeleteView):
    """Видалення оголошення — лише модератори/адміністратори."""

    model = Announcement
    template_name = "announcements/announcement_confirm_delete.html"
    success_url = reverse_lazy("announcements:list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Оголошення видалено.")
        return super().delete(request, *args, **kwargs)
