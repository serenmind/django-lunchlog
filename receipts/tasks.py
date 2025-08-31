import logging
from celery import shared_task
import requests

from django.conf import settings

from .models import PlaceInfo

logger = logging.getLogger(__name__)

api_key = getattr(settings, "GOOGLE_PLACES_API_KEY", None)


@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def fetch_places_for_receipt(self, receipt_id, address):
    """Fetch up to 10 lunch places using Google Places Text Search near the provided address.

    Saves unique PlaceInfo records.
    """
    
    if not api_key:
        logger.error('GOOGLE_PLACES_API_KEY not configured')
        return []

    # Use Text Search to query 'lunch near {address}' which usually returns relevant places
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    params = {
        'query': f'lunch near {address}',
        'key': api_key,
        'type': 'restaurant',
        'language': 'en',
        'radius': 5000,
    }
    # Don't call the external API if we already have places for the same address
    if address:
        addr_norm = address.strip()
        if PlaceInfo.objects.filter(address__iexact=addr_norm).exists():
            logger.info("Places already fetched for address '%s', skipping API call", addr_norm)
            return []

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        logger.exception('Google Places API request failed: %s', exc)
        try:
            raise self.retry(exc=exc)
        except Exception:
            return []

    results = data.get('results', [])[:10]
    saved = []

    for item in results:
        place_id = item.get('place_id')
        if not place_id:
            continue
        # avoid duplicates
        obj, created = PlaceInfo.objects.update_or_create(
            place_id=place_id,
            defaults={
                'name': item.get('name', ''),
                'address': item.get('formatted_address', ''),
                'types': item.get('types', []),
                'rating': item.get('rating'),
                'raw': item,
            },
        )
        saved.append(obj.place_id)

    return saved
