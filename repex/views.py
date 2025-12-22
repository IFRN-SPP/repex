from django.shortcuts import render, redirect
from .models import Projeto, Noticia, IdentidadeVisual, FotoProjeto, AreaConhecimento, Instituicao, RedeSocial, UserSocialLink
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponseRedirect
from .forms import ProjetoForm, IdentidadeVisualForm, UserSocialLinkForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from users.models import User, Profile
from django.db.models import Q
from users.views import is_superuser


def ta_no_grupo(user):
    return user.groups.filter(name='Professor').exists()


def index(request):
    projetos = Projeto.objects.all().order_by("-criado_em")[:9]
    projetos_random = Projeto.objects.all().order_by("?")[:9]
    projetos_mais_vistos = Projeto.objects.all().order_by("-views")[:9]
    noticias = Noticia.objects.all().order_by("-criado_em")[:9]
    context = {
        "noticias": noticias,
        "projetos": projetos,
        'projetos_random': projetos_random,
        "projetos_mais_vistos": projetos_mais_vistos
    }
    return render(request, 'index.html', context)


def explorar(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    modalidade = request.GET.get('modalidade', '')
    area_id = request.GET.get('area_conhecimento', '')

    resultado_projeto_titulo = Projeto.objects.filter(titulo__icontains=query)
    resultado_projeto_objetivo = Projeto.objects.filter(objetivo__icontains=query)
    resultado_projeto_resumo = Projeto.objects.filter(resumo__icontains=query)
    resultados_projetos = (
        resultado_projeto_titulo | resultado_projeto_objetivo | resultado_projeto_resumo
        ).distinct()
    
    if status:
        resultados_projetos = resultados_projetos.filter(status=status).distinct()
    if modalidade:
        resultados_projetos = resultados_projetos.filter(modalidade=modalidade).distinct()
    if area_id:
        resultados_projetos = resultados_projetos.filter(area_conhecimento_id=area_id)

    paginator_projetos = Paginator(resultados_projetos, 16)
    page_number_projetos = request.GET.get('page', 1)
    resultados_projetos = paginator_projetos.get_page(page_number_projetos)

    context = {
        'resultados_projetos': resultados_projetos,
        'query': query,
        'status_choices': Projeto.STATUS_CHOICES,
        'modalidade_choices': Projeto.MODALIDADE_CHOICES,
        'areas': AreaConhecimento.objects.all()
    }
    return render(request, 'explorar.html', context)


def ajax_projetos(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    modalidade = request.GET.get('modalidade', '')
    area_id = request.GET.get('area_conhecimento', '')

    resultado_projeto_titulo = Projeto.objects.filter(titulo__icontains=query)
    resultado_projeto_objetivo = Projeto.objects.filter(objetivo__icontains=query)
    resultado_projeto_resumo = Projeto.objects.filter(resumo__icontains=query)
    resultados_projetos = (
        resultado_projeto_titulo | resultado_projeto_objetivo | resultado_projeto_resumo
    ).distinct()

    if status:
        resultados_projetos = resultados_projetos.filter(status=status)
    if modalidade:
        resultados_projetos = resultados_projetos.filter(modalidade=modalidade)
    if area_id:
        resultados_projetos = resultados_projetos.filter(area_conhecimento_id=area_id)

    paginator = Paginator(resultados_projetos, 16)
    page_number_projetos = request.GET.get('page', 1)
    resultados_projetos = paginator.get_page(page_number_projetos)

    html = render_to_string(
        "partials/_ajax_projetos.html",
        {
            "resultados_projetos": resultados_projetos,
            "query": query,
            'status_choices': Projeto.STATUS_CHOICES,
            'modalidade_choices': Projeto.MODALIDADE_CHOICES,
            'areas': AreaConhecimento.objects.all()
        },
        request=request,
    )

    return JsonResponse({"html": html})


def buscar_projetos(request):
    query = request.GET.get('q', '')
    resultados = Projeto.objects.filter(nome__icontains=query) if query else []
    data = [{"id": p.id, "nome": p.nome} for p in resultados]
    return JsonResponse(data, safe=False)


class ProjetoDetailView(DetailView):
    model = Projeto
    template_name = 'projeto_detail.html'
    context_object_name = 'projeto'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        projeto = self.get_object()  

        session_key = f"viewed_projeto_{projeto.pk}"
        if not request.session.get(session_key, False):
            projeto.views += 1
            projeto.save(update_fields=["views"])
            request.session[session_key] = True

        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projeto = self.get_object()
        projetos = Projeto.objects.filter(area_conhecimento=projeto.area_conhecimento).exclude(pk=projeto.pk)[:9]

        context['projetos'] = projetos
        return context


class NoticiaDetailView(DetailView):
    model = Noticia
    template_name = 'noticia_detail.html'
    context_object_name = 'noticia'
    

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profile_detail.html'
    context_object_name = 'profile'


# ----------------- Creates -----------------

class ProjetoCreateView(LoginRequiredMixin, UserPassesTestMixin ,SuccessMessageMixin, CreateView):
    model = Projeto
    form_class = ProjetoForm
    template_name = 'projeto_form.html'
    success_message = 'Projeto criado com sucesso!'
    success_url = reverse_lazy('dashboard')
    
    def test_func(self):
        return ta_no_grupo(self.request.user) or is_superuser(self.request.user)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        self.object.componentes.add(self.request.user)

        for file in self.request.FILES.getlist("fotos"):
            FotoProjeto.objects.create(projeto=self.object, foto=file)
        return HttpResponseRedirect(self.get_success_url())


class NoticiaCreateView(LoginRequiredMixin, UserPassesTestMixin ,SuccessMessageMixin, CreateView):
    model = Noticia
    fields = ['titulo', 'descricao', 'conteudo', 'imagem', 'area_conhecimento']
    template_name = 'noticia_form.html'
    success_message = 'Notícia criada com sucesso!'
    success_url = reverse_lazy('dashboard')
    
    def test_func(self):
        return ta_no_grupo(self.request.user) or is_superuser(self.request.user)

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)
    

class AreaConhecimentoCreateView(LoginRequiredMixin, UserPassesTestMixin ,SuccessMessageMixin, CreateView):
    model = AreaConhecimento
    fields = ['area']
    template_name = 'area_conhecimento_form.html'
    success_message = 'Área de conhecimento cadastrada com sucesso!'
    success_url = reverse_lazy('painel')
    
    def test_func(self):
        return is_superuser(self.request.user)


class InstituicaoCreateView(LoginRequiredMixin, UserPassesTestMixin ,SuccessMessageMixin, CreateView):
    model = Instituicao
    fields = ['logo', 'nome', 'cep', 'endereco', 'site']
    template_name = 'instituicao_form.html'
    success_message = 'Instituição cadastrada com sucesso!'
    success_url = reverse_lazy('painel')

    def test_func(self):
        return is_superuser(self.request.user)


class IdentidadeVisualCreateView(LoginRequiredMixin, UserPassesTestMixin ,SuccessMessageMixin, CreateView):
    model = IdentidadeVisual
    template_name = 'identidade_visual_form.html'
    success_message = 'Identidade visual criada com sucesso!'
    form_class = IdentidadeVisualForm
    success_url = reverse_lazy('painel')

    def test_func(self):
        return is_superuser(self.request.user)


class RedeSocialCreateView(LoginRequiredMixin, UserPassesTestMixin ,SuccessMessageMixin, CreateView):
    model = RedeSocial
    fields = ['nome', 'url_base']
    template_name = 'rede_social_form.html'
    success_message = 'Rede social criada com sucesso!'
    success_url = reverse_lazy('painel')

    def test_func(self):
        return is_superuser(self.request.user)


class UserSocialLinkCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = UserSocialLink
    form_class = UserSocialLinkForm
    template_name = "profile_rede_social_form.html"
    success_message = "Rede social pessoal adicionada com sucesso!"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# ----------------- Updates -----------------

class ProjetoUpdateView(LoginRequiredMixin, UserPassesTestMixin ,SuccessMessageMixin, UpdateView):
    model = Projeto
    form_class = ProjetoForm
    template_name = 'projeto_form.html'
    success_message = 'Projeto atualizado com sucesso!'
    success_url = reverse_lazy('dashboard')
    
    def test_func(self):
        projeto = self.get_object()
        user = self.request.user
        return ta_no_grupo(user) and projeto.componentes.filter(id=user.id).exists()


class NoticiaUpdateView(LoginRequiredMixin, UserPassesTestMixin ,SuccessMessageMixin, UpdateView):
    model = Noticia
    fields = ['titulo', 'descricao', 'conteudo', 'imagem', 'area_conhecimento']
    template_name = 'noticia_form.html'
    success_message = 'Notícia atualizada com sucesso!'
    success_url = reverse_lazy('dashboard')
    
    def test_func(self):
        noticia = self.get_object()
        user = self.request.user
        return ta_no_grupo(user) and noticia.autor.id == user.id


class AreaConhecimentoUpdateView(LoginRequiredMixin, UserPassesTestMixin ,SuccessMessageMixin, UpdateView):
    model = AreaConhecimento
    fields = ['area']
    template_name = 'area_conhecimento_form.html'
    success_message = 'Áre de conhecimento atualizada com sucesso!'
    success_url = reverse_lazy('painel')

    def test_func(self):
        return is_superuser(self.request.user)


class InstituicaoUpdateView(LoginRequiredMixin, UserPassesTestMixin ,SuccessMessageMixin, UpdateView):
    model = Instituicao
    fields = ['logo', 'nome', 'cep', 'endereco', 'site']
    template_name = 'instituicao_form.html'
    success_message = 'Instituição atualizada com sucesso!'
    success_url = reverse_lazy('painel')

    def test_func(self):
        return is_superuser(self.request.user)

    
class IdentidadeVisualUpdateView(LoginRequiredMixin, UserPassesTestMixin ,SuccessMessageMixin, UpdateView):
    model = IdentidadeVisual
    template_name = 'identidade_visual_form.html'
    success_message = 'Identidade visual atualizada com sucesso!'
    form_class = IdentidadeVisualForm
    success_url = reverse_lazy('painel')

    def test_func(self):
        return is_superuser(self.request.user)


class RedeSocialUpdateView(LoginRequiredMixin, UserPassesTestMixin ,SuccessMessageMixin, UpdateView):
    model = RedeSocial
    fields = ["rede", "url"]
    template_name = 'rede_social_form.html'
    success_message = 'Rede social atualizada com sucesso!'
    success_url = reverse_lazy('painel')

    def test_func(self):
        return is_superuser(self.request.user)


class UserSocialLinkUpdateView(LoginRequiredMixin, UserPassesTestMixin ,SuccessMessageMixin, UpdateView):
    model = UserSocialLink
    form_class = UserSocialLinkForm
    template_name = "profile_rede_social_form.html"
    success_message = "Rede social pessoal atualizada com sucesso!"
    success_url = reverse_lazy("dashboard")
    
    def test_func(self):
        link = self.get_object()
        user = self.request.user
        return link.user.id == user.id


# ----------------- Deletes -----------------

class ProjetoDeleteView(LoginRequiredMixin, UserPassesTestMixin ,SuccessMessageMixin, DeleteView):
    model = Projeto
    success_message = 'Projeto deletado com sucesso!'
    success_url = reverse_lazy('dashboard')
    
    def test_func(self):
        projeto = self.get_object()
        user = self.request.user
        return ta_no_grupo(self.request.user) and projeto.componentes.filter(id=user.id).exists()


class NoticiaDeleteView(LoginRequiredMixin, UserPassesTestMixin ,SuccessMessageMixin, DeleteView):
    model = Noticia
    success_message = 'Notícia deletada com sucesso!'
    success_url = reverse_lazy('dashboard')
    
    def test_func(self):
        noticia = self.get_object()
        user = self.request.user
        return ta_no_grupo(user) and noticia.autor.id == user.id


class AreaConhecimentoDeleteView(LoginRequiredMixin, UserPassesTestMixin ,SuccessMessageMixin, DeleteView):
    model = AreaConhecimento
    template_name = 'area_conhecimento_confirm_delete.html'
    success_message = 'Área de conhecimento deletada com sucesso!'
    success_url = reverse_lazy('painel')
    
    def test_func(self):
        return is_superuser(self.request.user)


class InstituicaoDeleteView(LoginRequiredMixin, UserPassesTestMixin ,SuccessMessageMixin, DeleteView):
    model = Instituicao
    template_name = 'instituicao_confirm_delete.html'
    success_message = 'Instituição deletada com sucesso!'
    success_url = reverse_lazy('painel')
    
    def test_func(self):
        return is_superuser(self.request.user)


class RedeSocialDeleteView(LoginRequiredMixin, UserPassesTestMixin ,SuccessMessageMixin, DeleteView):
    model = RedeSocial
    template_name = 'rede_social_confirm_delete.html'
    success_message = 'Rede social deletada com sucesso!'
    success_url = reverse_lazy('painel')
    
    def test_func(self):
        return is_superuser(self.request.user)


class UserSocialLinkDeleteView(LoginRequiredMixin, UserPassesTestMixin ,SuccessMessageMixin, DeleteView):
    model = UserSocialLink
    success_message = 'Rede social deletada com sucesso!'
    success_url = reverse_lazy('dashboard')
    
    def test_func(self):
        link = self.get_object()
        user = self.request.user
        return link.user.id == user.id
