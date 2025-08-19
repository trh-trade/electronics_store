from django.shortcuts import redirect

class RedirectToWWW:
    """
    Редирект с trh-trade.sk -> www.trh-trade.sk
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        if host == 'trh-trade.sk':
            return redirect(f"https://www.trh-trade.sk{request.get_full_path()}", permanent=True)
        return self.get_response(request)