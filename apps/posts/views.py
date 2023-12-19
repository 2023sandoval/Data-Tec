from .models import Post, Comentario, Categoria
from .forms import  ComentarioForm, CrearPostForm, NuevaCategoriaForm
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.shortcuts import  redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
#render sacar si da problemas linea 6
# from crispy_alerts.utils import add_alert


# def my_view(request):
#     # Lógica de tu vista
#     add_alert(request, "success", "¡Éxito!", "¡La operación se completó con éxito!")

# post = Post.objects.create(title='Mi post', content='Contenido del post', id=1)
# post.image.save('imagen.jpg', open('ruta/a/la/imagen.jpg', 'rb'))

#Vistas Basadas en Clases
class PostListView(ListView):
    model = Post
    template_name = "posts/posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        orden = self.request.GET.get('orden')
        if orden == 'reciente':
            queryset = queryset.order_by('-fecha')
        elif orden == 'antiguo':
            queryset = queryset.order_by('fecha')
        elif orden == 'alfabetico':
            queryset = queryset.order_by('titulo')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orden'] = self.request.GET.get('orden', 'reciente')
        return context

#Vista basada en funciones comentada por las dudas
# def posts(request):
#     posts = Post.objects.all()
#     return render(request, 'posts.html', {'posts': posts})

class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_individual.html"
    context_object_name = "posts"
    pk_url_kwarg = "id"
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ComentarioForm()
        context['comentarios'] = Comentario.objects.filter(posts_id=self.kwargs['id'])
        return context
    
    def post(self, request, *args, **kwargs):
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.posts_id = self.kwargs['id']
            comentario.save()
            return redirect('apps.posts:post_individual', id=self.kwargs['id'])
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)
        
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CrearPostForm
    template = 'posts/crear_post.html'
    success_url = reverse_lazy('apps.posts:posts')

class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = NuevaCategoriaForm
    template_name = 'posts/crear_categoria.html'
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy('apps.posts:post_create')
        
class PostsPorCategoriaView(ListView):
    model = Post
    template_name = 'posts/posts_por_categoria.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(categoria_id=self.kwargs['pk'])
    
        
class CategoriaListView(ListView):
    model = Categoria
    template_name = 'posts/categoria_list.html'
    context_object_name = 'categorias'

class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'posts/categoria_confirm_delete.html'
    success_url = reverse_lazy('apps.posts:categoria_list')

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class =CrearPostForm
    template_name = 'posts/modificar_post.html'
    success_url = reverse_lazy('apps.posts:posts')

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/eliminar_post.html'
    success_url = reverse_lazy('apps.posts:posts')

class ComentarioCreateView(LoginRequiredMixin, CreateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'comentario/agregarComentario.html'
    success_url = 'comentario/comentarios'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.posts_id = self.kwargs['posts_id']
        return super().form_valid(form)
    
class ComentarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'comentario/comentario_form.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('apps.posts:post_individual', arg=[self.object.posts.id])
        
class ComentarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Comentario
    template_name = 'comentario/comentario_confirm_delete.html'

    def get_success_url(self):
        return reverse('apps.posts:post_individual', args=[self.object.posts.id])





def ComentarioReplyView(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)

    if request.method == 'POST':

        return redirect('comentario_detail', comentario_id==comentario.id)
    return render(request, 'comentario_reply.html', {'comentario': comentario})
