from django.shortcuts import render, get_object_or_404, redirect
from chai.forms import chaivarityForm
from chai.models import store, storereview

def home(request):
    stores = None
    form = chaivarityForm()

    if request.method == "POST":

        # Check if this POST is a review submission
        if 'review_store_id' in request.POST:
            store_id = request.POST.get('review_store_id')
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')

            if store_id and rating and comment and request.user.is_authenticated:
                selected_store = get_object_or_404(store, pk=store_id)
                storereview.objects.create(
                    store=selected_store,
                    user=request.user,
                    rating=int(rating),
                    comment=comment,
                )
            return redirect('home')

        # Otherwise, it's the chai variety search form
        form = chaivarityForm(request.POST)
        if form.is_valid():
            chai_varity = form.cleaned_data['chai_varity']
            stores = store.objects.filter(chai_varities=chai_varity)

    return render(
        request,
        'Website/index.html',
        {
            'form': form,
            'stores': stores,
        }
    )


def store_bill(request, store_id):
    selected_store = get_object_or_404(store, pk=store_id)

    return render(
        request,
        'Website/bill.html',
        {
            'store': selected_store,
        }
    )