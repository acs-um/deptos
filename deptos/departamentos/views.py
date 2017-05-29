from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect


#@login_required()
def home(request):
    return render_to_response('departamentos/home.html', {'user': request.user}, context_instance=RequestContext(request))
