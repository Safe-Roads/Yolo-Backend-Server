from math import radians, cos, sin, sqrt, atan2
from .supabase_client import supabase

DUPLICATE_DISTANCE_METERS = 10


def distance_meters(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def is_duplicate(lat, lon):
    try:
        response = supabase.table("potholes").select("*").limit(50).execute()

        if response.data:
            for row in response.data:
                dist = distance_meters(lat, lon, row["latitude"], row["longitude"])
                if dist < DUPLICATE_DISTANCE_METERS:
                    return True

        return False
    except Exception as e:
        print("❌ Deduplication error:", e)
        return False


def save_pothole(lat, lon, confidence):
    try:
        if is_duplicate(lat, lon):
            return False

        supabase.table("potholes").insert({
            "latitude": lat,
            "longitude": lon,
            "confidence": confidence
        }).execute()

        return True

    except Exception as e:
        print("❌ Supabase insert error:", e)
        return False
