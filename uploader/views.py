from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import os
from .models import ImageEntry

# These will be set by the user in the environment
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHANNEL_ID = os.environ.get('TELEGRAM_CHANNEL_ID', '')

def index(request):
    return render(request, 'index.html')

UPLOAD_API_KEY = os.environ.get('UPLOAD_API_KEY', '')

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Check API Key
        client_key = request.POST.get('api_key', '')
        if UPLOAD_API_KEY and client_key != UPLOAD_API_KEY:
            return JsonResponse({'error': 'Unauthorized. Invalid API Key.'}, status=403)
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHANNEL_ID:
            return JsonResponse({'error': 'Telegram Bot Token or Channel ID is missing in server config.'}, status=500)
            
                image_file = request.FILES['image']
        
        # Check file type for Video/GIF support
        is_document = image_file.name.lower().endswith(('.mp4', '.gif', '.webm', '.pdf', '.zip'))
        api_method = "sendDocument" if is_document else "sendPhoto"
        file_key = 'document' if is_document else 'photo'
        
        # Send to Telegram
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/{api_method}"
        files = {file_key: image_file.read()}
        data = {'chat_id': TELEGRAM_CHANNEL_ID}
        
        try:
            response = requests.post(url, data=data, files=files)
            result = response.json()
            
            if result.get('ok'):
                if is_document:
                    file_id = result['result']['document']['file_id']
                else:
                    file_id = result['result']['photo'][-1]['file_id']
                message_id = result['result']['message_id']
                
                entry = ImageEntry.objects.create(
                    telegram_file_id=file_id,
                    telegram_message_id=message_id,
                    file_name=image_file.name
                )
                
                # Return the custom URL
                file_url = request.build_absolute_uri(f'/img/{entry.short_id}')
                return JsonResponse({'success': True, 'url': file_url, 'short_id': entry.short_id})
            else:
                return JsonResponse({'error': f"Telegram API Error: {result.get('description')}"}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Invalid request'}, status=400)

def serve_image(request, short_id):
    entry = get_object_or_404(ImageEntry, short_id=short_id)
    
    # 1. Get file path from Telegram
    file_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getFile?file_id={entry.telegram_file_id}"
    res = requests.get(file_url).json()
    
    if not res.get('ok'):
        return HttpResponse("Image not found on Telegram servers.", status=404)
        
    file_path = res['result']['file_path']
    
        # 2. Download the actual file bytes
    download_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
    img_res = requests.get(download_url)
    
    # 3. Stream back to user with caching
    content_type = img_res.headers.get('Content-Type', 'application/octet-stream')
    if entry.file_name.lower().endswith('.mp4'): content_type = 'video/mp4'
    if entry.file_name.lower().endswith('.gif'): content_type = 'image/gif'
    
    response = HttpResponse(img_res.content, content_type=content_type)
    response['Cache-Control'] = 'public, max-age=31536000' # Cache for 1 year
    return response

def gallery_view(request):
    images = ImageEntry.objects.all().order_by('-uploaded_at')
    return render(request, 'gallery.html', {'images': images})

@csrf_exempt
def delete_image(request, short_id):
    if request.method == 'POST':
        entry = get_object_or_404(ImageEntry, short_id=short_id)
        
        if entry.telegram_message_id:
            delete_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/deleteMessage"
            requests.post(delete_url, data={'chat_id': TELEGRAM_CHANNEL_ID, 'message_id': entry.telegram_message_id})
            
        entry.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)



