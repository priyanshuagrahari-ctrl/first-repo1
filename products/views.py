from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from .models import Product


def product_list(request):
    try:
        limit = int(request.GET.get("limit", 10))
        page = int(request.GET.get("page", 1))
        flag = int(request.GET.get("flag", 0))
        Published=int(request.GET.get("Published",0))
    except ValueError:
      return JsonResponse({'status': 400, 'Error': "limit, page, and flag must be integers"})

    if page <= 0 or limit <= 0:
       return JsonResponse({'status': 400, 'error': "Error: page and limit must be greater than 0"})


    offset_start = limit * (page - 1)
    offset_end = offset_start + limit

    cache_key = f"products:page:{page}:limit:{limit}"

    products = None
    if not flag:
        products = cache.get(cache_key)
        print('product',products)
    if products is None:
        if Published :
          products = list(
            Product.objects.filter(status='Published').values(
                "id", "name", "price", "created_at"
            ).order_by('created_at')[offset_start:offset_end]
                  )
          print(
    Product.objects
    .filter(status='Published')
    .order_by('created_at')
    .query
)

        else :
           products = list(
            Product.objects.values(
                "id", "name", "price", "created_at"
            )[offset_start:offset_end] )
           
    cache.set(cache_key, products, timeout=3600)

   
    return JsonResponse({'status': 200, 'product': products})








def product_list_cursor(request):
    try:
        limit = int(request.GET.get("limit", 10))
        next_id = request.GET.get("next_id")
        flag = int(request.GET.get("flag", 0))
        published = int(request.GET.get("Published", 0))
    except ValueError:
        return JsonResponse({
            'status': 400,
            'error': "limit, flag, and next_id must be valid integers"
        })

    if limit <= 0:
        return JsonResponse({
            'status': 400,
            'error': "limit must be greater than 0"
        })

    cache_key = f"products:cursor:asc:last_id:{next_id}:limit:{limit}:published:{published}"

    products = None

   
    if not flag:
        products = cache.get(cache_key)

    print('cached_product:', products)

    if products is None:
       
        qs = Product.objects.all()

        if published:
            qs = qs.filter(status='Published')

        qs = qs.order_by("created_at")

        if next_id:
            qs = qs.filter(id__gt=int(next_id))

        products = list(
            qs.values("id", "name", "price", "created_at")[:limit]
        )

        cache.set(cache_key, products, timeout=3600)

    print('real_product:', products)

    return JsonResponse({
        'status': 200,
        'product': products,
        'next_last_id': products[-1]["id"] if products else None
    })






def product_by_id(request):
    search_id = request.GET.get("id")

    if not search_id:
        return HttpResponse(
            "<h3>Error: id parameter is required</h3>",
            status=400
        )

    product = Product.objects.filter(id=search_id).values(
        "id", "name", "price", "created_at"
    ).first()

    if not product:
        return HttpResponse(
            "<h3>Error: Product not found</h3>",
            status=404
        )

    html = "<html><body>"
    html += "<h2>Product Details</h2>"
    html += f"<p><b>ID:</b> {product['id']}</p>"
    html += f"<p><b>Name:</b> {product['name']}</p>"
    html += f"<p><b>Price:</b> {product['price']}</p>"
    html += f"<p><b>Created At:</b> {product['created_at']}</p>"
    html += "</body></html>"

    return JsonResponse(html)
