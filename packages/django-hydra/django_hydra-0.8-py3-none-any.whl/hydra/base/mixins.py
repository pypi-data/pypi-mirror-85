# Python
import operator
from functools import reduce

# Django
from django.urls import reverse, reverse_lazy, NoReverseMatch
from django.utils.html import format_html

# Shortcuts
from hydra.shortcuts import get_urls_of_site, get_slug_or_pk

# Utils
from hydra.utils import import_class


class UrlMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        object = None
        if self.action != "list":
            object = self.object

        urls = get_urls_of_site(self.site, object)

        if "site" in context:
            context["site"].update(urls)
        else:
            context.update({
                "site": urls
            })
        return context


class TemplateMixin:
    def get_template_names(self):
        action = self.template_name_suffix.split("_")[-1]
        self.template_name = getattr(self.site, "%s_template_name" % action)
        return super().get_template_names()


class BreadcrumbMixin:
    """Clase base que contiene la información común de todas las subclases"""

    def get_menu_in_path(self, path):
        Menu = import_class("hydra.models", "Menu")
        if not Menu: return
        if not path: return

        try:
            menu = Menu.objects.get(route=path)
            return menu
        except Menu.DoesNotExist:
            path = "/".join(path.split("/")[0: -1])
            return self.get_menu_in_path(path)

    def get_breadcrumb_text(self, action):
        text = getattr(self.site, "breadcrumb_%s_text" % action)
        if not text: return None
        return format_html(text)

    def get_base(self, menu):
        base = [(menu.name, f"/{menu.route}/")]
        if menu.parent:
            base =  self.get_base(menu.parent) + base
        return base

    def get_base_breadcrumbs(self):
        base_breadcrumbs = [(self.get_breadcrumb_text("home"), "/")]

        menu = self.get_menu_in_path(self.request.path[1:-1])
        if not menu: return base_breadcrumbs
        base_breadcrumbs.extend(self.get_base(menu))
        return base_breadcrumbs

    def get_form_breadcrumbs(self):
        breadcrumbs = self.get_base_breadcrumbs()
        breadcrumbs.append((self.get_breadcrumb_text(self.action), "#"))
        return breadcrumbs

    def get_create_breadcrumbs(self):
        return self.get_form_breadcrumbs()

    def get_update_breadcrumbs(self):
        return self.get_form_breadcrumbs()

    def get_list_breadcrumbs(self):
        return self.get_base_breadcrumbs()

    def get_detail_breadcrumbs(self):
        """Obtiene el breadcumb para Detail View"""
        url_name = self.site.get_url_name(self.action)
        breadcrumbs = self.get_list_breadcrumbs()
        breadcrumbs.append(
            (
                self.get_breadcrumb_text(self.action) or str(self.object),
                reverse_lazy(url_name, args=[get_slug_or_pk(self.object)],),
            )
        )
        return breadcrumbs

    def get_delete_breadcrumbs(self):
        breadcrumbs = self.get_detail_breadcrumbs()
        breadcrumbs.append((self.get_breadcrumb_text(self.action), "#"))
        return breadcrumbs

    def get_breadcrumbs(self):
        attr = getattr(self, "get_%s_breadcrumbs" % self.action)
        return attr()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        breadcrumbs = {
            "breadcrumbs" : self.get_breadcrumbs()
        }

        if "site" in context:
            context["site"].update(breadcrumbs)
        else:
            context.update({
                "site": breadcrumbs
            })
        return context


class FilterMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        opts = {
            "order_by": self._get_headers(),
            "search_fields": self._get_search_fields_with_labels(),
            "active_searches": self._clean_search_params(),
        }

        if "site" in context:
            context["site"].update(opts)
        else:
            context.update({
                "site": opts
            })
    
        return context

    def reduce_queryset(self, params, queryset, op):
        args = []
        for field, value, verbose_name in params:
            action = '__icontains'
            if self.model._meta.get_field(field).__class__.__name__ in (
                'CharField',
                'TextField',
            ):
                action = '__unaccent' + action
            args.append(Q(**{field + action: value}))
        if args:
            queryset = queryset.filter(reduce(op, args))
        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()

        params = self._clean_search_params()
        if 'sf' in self.request.GET:
            return self.reduce_queryset(params, queryset, operator.__or__)

        queryset = self.reduce_queryset(params, queryset, operator.__and__)
        return queryset

    def _clean_search_params(self):
        params = []
        if 'sf' in self.request.GET:
            value = self.request.GET.get('sf')
            for field in self.site.search_fields:
                verbose_name = get_field_label_of_model(
                    self.site.model, '.'.join(field.split('__'))
                )
                params.append((field, value, verbose_name))
            return params

        for key in self.request.GET.keys():
            if key.startswith('sf_') and key[3:] in self.site.search_fields:
                field = key[3:]
                verbose_name = get_field_label_of_model(
                    self.site.model, '.'.join(field.split('__'))
                )
                params.append((field, self.request.GET.get(key), verbose_name))
        return params

    def _get_search_fields_with_labels(self):
        fields = []
        for field in self.site.search_fields:
            point_field = '.'.join(field.split('__'))
            fields.append(
                (
                    f'sf_{field}',
                    get_field_label_of_model(self.model, point_field),
                )
            )
        return fields
