from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django import forms
from maindudu.models import Automovel, Carro, Moto, Anuncio
from django.shortcuts import render, redirect, get_object_or_404


Usuario = get_user_model()

# Formulário de Registro
class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'password']

# View para registrar o usuário
def register(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            # Use o método create_user para garantir que o usuário seja criado corretamente
            Usuario.create_user(
                email=form.cleaned_data['email'],
                nome=form.cleaned_data['nome'],
                password=form.cleaned_data['password']
            )
            return redirect('listar_usuarios')  # Nome da URL que lista os usuários
    else:
        form = UsuarioForm()

    return render(request, 'register.html', {'form': form})

# View de sucesso (pode ser um simples redirecionamento)
def success(request):
    return render(request, 'success.html')

def listar_usuarios(request):
    if request.method == 'GET':
        usuarios = Usuario.obter_todos_usuarios()
        return render(request, 'listar_usuarios.html', {'usuarios': usuarios})

# # View para listar todos os automóveis
def listar_automoveis(request):
    automoveis = Automovel().obter_todos_automoveis()  # Chamando o método do model
    return render(request, 'listar_automoveis.html', {'automoveis': automoveis})




# Formulário para Automóvel
class AutomovelForm(forms.ModelForm):
    class Meta:
        model = Automovel
        fields = ['marca', 'modelo', 'ano']  # Campos do modelo Automovel

# View para criar um Automóvel
def criar_automovel(request):
    if request.method == 'POST':
        form = AutomovelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_automoveis')
    else:
        form = AutomovelForm()
    
    return render(request, 'criar_automovel.html', {'form': form})

class CarroForm(forms.ModelForm):
    class Meta:
        model = Carro
        fields = ['automovel', 'cor', 'tipo', 'numero_portas']  # Campos do modelo Carro

def criar_carro(request):
    if request.method == 'POST':
        form = CarroForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('listar_carros')
    else:
        form = CarroForm()
    
    # Passa a lista de automóveis cadastrados para o template
    automoveis = Automovel.objects.all()
    return render(request, 'criar_carro.html', {'form': form, 'automoveis': automoveis})

def listar_carros(request):
    carros = Carro.obter_todos_carros()
    return render(request, 'listar_carros.html', {'carros': carros})

def deletar_carro(request, carro_id): # REFAZER <<<<<<<<< SOMENTE O USUARIO QUE CRIOU PODE DELETAR
    Carro.deletar_carro(carro_id)
    return redirect('listar_carros')


def criar_moto(request):
    if request.method == 'POST':
        automovel_id = request.POST.get('automovel')
        automovel = Automovel.objects.get(id=automovel_id)
        cilindradas = request.POST.get('cilindradas')
        tipo = request.POST.get('tipo')
        cor = request.POST.get('cor')
        Moto.create_moto(automovel, cilindradas, tipo, cor)
        return redirect('listar_motos')
    else:
        automoveis = Automovel.obter_todos_automoveis()  # Obter automóveis disponíveis
        return render(request, 'criar_moto.html', {'automoveis': automoveis})

def listar_motos(request):
    motos = Moto.obter_todas_motos()
    return render(request, 'listar_motos.html', {'motos': motos})

def deletar_moto(request, moto_id): # COLOCAR PRA DELETAR APENAS O USER RESPONSÁVEL
    Moto.deletar_moto(moto_id)
    return redirect('listar_motos')

# View para listar todos os anúncios
def listar_anuncios(request):
    anuncios = Anuncio.obter_todos_anuncios()
    return render(request, 'listar_anuncios.html', {'anuncios': anuncios})

# View para criar um novo anúncio
def criar_anuncio(request):
    if request.method == 'POST':
        preco_por_dia = request.POST.get('preco_por_dia')
        disponibilidade = request.POST.get('disponibilidade')
        usuario = request.user  # Supondo que o usuário esteja autenticado
        automovel = None  # Coloque a lógica de automóvel aqui
        
        if preco_por_dia and disponibilidade and usuario and automovel:
            Anuncio.create_anuncio(automovel, preco_por_dia, disponibilidade, usuario)
            return redirect('listar_anuncios')
    return render(request, 'criar_anuncio.html')

# View para editar um anúncio
def editar_anuncio(request, anuncio_id):
    anuncio = get_object_or_404(Anuncio, id=anuncio_id)
    if request.method == 'POST':
        anuncio.preco_por_dia = request.POST.get('preco_por_dia')
        anuncio.disponibilidade = request.POST.get('disponibilidade')
        anuncio.save()
        return redirect('listar_anuncios')
    return render(request, 'editar_anuncio.html', {'anuncio': anuncio})

# View para deletar um anúncio
def deletar_anuncio(request, anuncio_id):
    anuncio = get_object_or_404(Anuncio, id=anuncio_id)
    if request.method == 'POST':
        anuncio.delete()
        return redirect('listar_anuncios')
    return render(request, 'deletar_anuncio.html', {'anuncio': anuncio})

# View para consultar um anúncio por ID
def consulta_anuncio(request, anuncio_id):
    anuncio = get_object_or_404(Anuncio, id=anuncio_id)
    return render(request, 'consulta_anuncio.html', {'anuncio': anuncio})