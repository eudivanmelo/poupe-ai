from django.http import JsonResponse, HttpResponseBadRequest
from django.forms.models import model_to_dict
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


class CreateJsonView(LoginRequiredMixin, CreateView):
    '''
    View for creating a new object and returning a JSON response
    '''
    success_message = 'Objeto criado com sucesso'
    error_message = 'Erro ao criar objeto'

    def form_valid(self, form):
        form.instance.user = self.request.user
        
        self.object = form.save()
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'id': self.object.id, 'message': self.success_message})
        return HttpResponseBadRequest('Requisição inválida')

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': self.error_message, 'errors': form.errors}, status=400)
        return HttpResponseBadRequest('Requisição inválida')
    
class DetailJsonView(LoginRequiredMixin, DetailView):
    '''
    View for returning a JSON response with the object details
    '''
    context_object_name = 'object'
    fields = None
    
    def get_object_data(self, obj):
        '''
        Get the object data to be returned in the JSON response
        '''
        if self.fields:
            data = obj.__dict__.copy()
            data = {key: data[key] for key in self.fields if key in data}
        else:
            data = model_to_dict(obj)
        
        # Adicionar também as propertys
        for attr_name in dir(obj):
            attr_value = getattr(obj.__class__, attr_name, None)
            if isinstance(attr_value, property):
                if self.fields is None or attr_name in self.fields:
                    data[attr_name] = getattr(obj, attr_name)
                
        return data
    
    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            obj = self.get_object()
            data = self.get_object_data(obj)
                    
            return JsonResponse({'success': True, self.context_object_name: data})
        
        return HttpResponseBadRequest('Requisição inválida')
    
class DeleteJsonView(LoginRequiredMixin, DeleteView):
    '''
    View for deleting an object and returning a JSON response
    '''
    success_message = 'Objeto excluído com sucesso'
    error_message = 'Erro ao excluir objeto'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            self.object.delete()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': self.success_message})
            return HttpResponseBadRequest('Requisição inválida')

        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': f"{self.error_message}: {str(e)}"}, status=400)
            return HttpResponseBadRequest('Requisição inválida')

class UpdateJsonView(LoginRequiredMixin, UpdateView):
    '''
    View for updating an object and returning a JSON response
    '''
    success_message = 'Objeto atualizado com sucesso'
    error_message = 'Erro ao atualizar objeto'

    def get_object_data(self, obj):
        '''
        Get the object data to be returned in the JSON response
        '''
        if self.fields:
            data = obj.__dict__.copy()
            data = {key: data[key] for key in self.fields if key in data}
        else:
            data = model_to_dict(obj)
        
        # Adicionar também as propertys
        for attr_name in dir(obj):
            attr_value = getattr(obj.__class__, attr_name, None)
            if isinstance(attr_value, property):
                if self.fields is None or attr_name in self.fields:
                    data[attr_name] = getattr(obj, attr_name)
                
        return data

    def get(self, request, *args, **kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            obj = self.get_object_data(self.get_object())
            return JsonResponse({'success': True, self.context_object_name: obj})
        
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': self.success_message})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': self.error_message, 'errors': form.errors}, status=400)
        return super().form_invalid(form)