from django.db import models
from users.models import Profile, User
from PIL import Image, ImageOps
from tinymce.models import HTMLField
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.apps import apps


class AreaConhecimento(models.Model):
    area = models.CharField(max_length=150)

    def __str__(self):
        return self.area


class Projeto(models.Model):
    STATUS_CHOICES = [
        ("Proposta", "Proposta"),
        ("Em andamento", "Em andamento"),
        ("Pausado", "Pausado"),
        ("Concluído", "Concluído"),
    ]
    MODALIDADE_CHOICES = [
        ("Ensino", "Ensino"),
        ("Pesquisa", "Pesquisa"),
        ("Extensão", "Extensão"),
        ("Interdisciplinar", "Interdisciplinar"),
    ]

    titulo = models.CharField(max_length=100)
    descricao = HTMLField(_("Descricao"), blank=True)
    resumo = HTMLField(_("Resumo"), blank=True)
    justificativa = HTMLField(_("Justificativa"), blank=  True)
    area_conhecimento = models.ForeignKey(AreaConhecimento, on_delete=models.CASCADE, related_name='areas_projetos', null=True, blank=True)
    objetivo = HTMLField(_("Objetivo"), blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    resultados = HTMLField(_("Resultados"), blank=True)
    capa = models.ImageField(upload_to='projetos/', null=True, blank=True)
    doc = models.FileField(upload_to='docs/', blank=True, null=True)
    palavras_chave = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    modalidade = models.CharField(max_length=20, choices=MODALIDADE_CHOICES)
    componentes = models.ManyToManyField(User, related_name='projetos', blank=True)
    colab = models.ManyToManyField('self', symmetrical=False, related_name='colaboradores', blank=True)
    views = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.capa:
            img = Image.open(self.capa.path)
            output_size = (520, 320)
            img = ImageOps.fit(img, output_size, Image.LANCZOS)
            img.save(self.capa.path)

    
class FotoProjeto(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='photos')
    foto = models.ImageField()

    def __str__(self):
        return f"Foto do projeto {self.projeto.titulo}"


class Noticia(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = HTMLField(_("Descricao"), blank=True)
    conteudo = HTMLField(_("Conteudo"), blank=True)
    data_publicacao = models.DateTimeField(auto_now_add=True, null=True)
    imagem = models.ImageField(upload_to='noticias/', null=True, blank=True)
    area_conhecimento = models.ForeignKey(AreaConhecimento, on_delete=models.CASCADE, related_name='area_conhecimento_noticia', null=True, blank=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='noticias', null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class RedeSocial(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    url_base = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nome
    

class UserSocialLink(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="social_links"
    )
    rede = models.ForeignKey(
        RedeSocial,
        on_delete=models.CASCADE,
        related_name="rede"
        )
    url = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Link de rede social"
        verbose_name_plural = "Links de redes sociais"

    def __str__(self):
        return f"{self.user.nome_usual} - {self.rede.nome}"

class IdentidadeVisual(models.Model):
    logo = models.ImageField(upload_to='media/', null=True, blank=True)
    pagina_inicial_frase = models.CharField(max_length=300, default="Repositório IFSPP, aqui é o lar de todos os nossos projetos!")
    imagem = models.ImageField(upload_to='media/', null=True, blank=True)
    cor_sistema = models.CharField(max_length=7, default="#005EFF")
    cor_suplente = models.CharField(max_length=7, blank=True, null=True)
    cor_titulo = models.CharField(max_length=7, default="#FF9823")

    def __str__(self):
        return f"Cores{self.cor_sistema, self.cor_suplente, self.cor_titulo}"
 

class Instituicao(models.Model):
    logo = models.ImageField(upload_to='media/', null=True, blank=True)
    nome = models.CharField(max_length=150)
    cep = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.CharField(max_length=250, blank=True, null=True)
    site = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nome