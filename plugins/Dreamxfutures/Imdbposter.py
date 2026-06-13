import re
import aiohttp
import warnings
import logging
from io import BytesIO
from PIL import Image
from info import DREAMXBOTZ_IMAGE_FETCH, TMDB_API_KEY

logger = logging.getLogger(__name__)

Image.MAX_IMAGE_PIXELS = None
warnings.simplefilter("ignore", Image.DecompressionBombWarning)

_session: aiohttp.ClientSession | None = None

TMDB_BASE = "https://api.themoviedb.org/3"
TMDB_IMG  = "https://image.tmdb.org/t/p"


async def get_session():
    global _session
    if _session is None or _session.closed:
        _session = aiohttp.ClientSession()
    return _session


async def close_session():
    global _session
    if _session and not _session.closed:
        await _session.close()


def list_to_str(lst):
    if not lst:
        return ""
    if isinstance(lst, str):
        return lst
    return ", ".join(map(str, lst))


async def fetch_image(url: str, size: tuple = (860, 1200)):
    """Download image from url, resize it, return BytesIO ready for Telegram."""
    if not DREAMXBOTZ_IMAGE_FETCH:
        return url
    try:
        session = await get_session()
        async with session.get(url) as resp:
            if resp.status != 200:
                logger.error(f"fetch_image: HTTP {resp.status} for {url}")
                return None
            data = await resp.read()
        img = Image.open(BytesIO(data)).convert("RGB")
        img = img.resize(size, Image.LANCZOS)
        out = BytesIO()
        img.save(out, format="JPEG", quality=90)
        out.seek(0)
        return out
    except Exception as e:
        logger.error(f"fetch_image error: {e}")
        return None


# ─────────────────────────────────────────────────────────────
# Internal: search TMDB and return raw detail dict
# ─────────────────────────────────────────────────────────────
async def _tmdb_search_and_fetch(query: str) -> dict:
    """
    Search TMDB for query (movie or TV).
    Returns raw TMDB detail dict (with credits & images appended)
    or {} on any failure.
    """
    if not TMDB_API_KEY:
        logger.warning("TMDB_API_KEY not configured")
        return {}

    session = await get_session()

    # Strip trailing year for cleaner search
    raw_query = str(query).strip()
    year_m = re.search(r'\b((?:19|20)\d{2})\s*$', raw_query)
    search_year  = year_m.group(1) if year_m else None
    search_title = raw_query[:year_m.start()].strip() if year_m else raw_query

    async def _search(title, year=None):
        for mtype in ("movie", "tv"):
            params = {
                "api_key": TMDB_API_KEY,
                "query": title,
                "include_adult": "false",
            }
            if year:
                params["year"] = year
                params["first_air_date_year"] = year
            async with session.get(f"{TMDB_BASE}/search/{mtype}", params=params) as r:
                if r.status != 200:
                    continue
                results = (await r.json()).get("results", [])
                if results:
                    return results[0]["id"], mtype
        return None, None

    # Try with year first, then without
    tmdb_id, media_type = await _search(search_title, search_year)
    if not tmdb_id and search_year:
        logger.info(f"TMDB: retrying '{search_title}' without year {search_year}")
        tmdb_id, media_type = await _search(search_title)

    if not tmdb_id:
        logger.info(f"TMDB: no results for '{search_title}' (year={search_year})")
        return {}

    # Fetch full details
    detail_params = {
        "api_key": TMDB_API_KEY,
        "append_to_response": "credits,images,external_ids",
        "include_image_language": "en,null",
    }
    async with session.get(
        f"{TMDB_BASE}/{media_type}/{tmdb_id}", params=detail_params
    ) as r:
        if r.status != 200:
            logger.error(f"TMDB detail fetch failed: HTTP {r.status}")
            return {}
        d = await r.json()

    d["_media_type"] = media_type
    return d


# ─────────────────────────────────────────────────────────────
# Internal: normalise raw TMDB dict → channel.py-compatible dict
# ─────────────────────────────────────────────────────────────
def _normalise_tmdb(d: dict) -> dict:
    if not d:
        return {}

    media_type = d.get("_media_type", "movie")
    tmdb_id    = d.get("id")

    # Crew / cast
    crew = d.get("credits", {}).get("crew", [])
    cast = d.get("credits", {}).get("cast", [])

    # Poster path
    poster_path   = d.get("poster_path")
    backdrop_path = d.get("backdrop_path")

    # Prefer English-language backdrop from images list
    for bd in d.get("images", {}).get("backdrops", []):
        if bd.get("iso_639_1") in ("en", None, ""):
            backdrop_path = bd.get("file_path", backdrop_path)
            break

    poster_url   = f"{TMDB_IMG}/w1280{poster_path}"   if poster_path   else None
    backdrop_url = f"{TMDB_IMG}/w1280{backdrop_path}" if backdrop_path else None

    # Rating
    vote_avg = d.get("vote_average", 0)
    rating   = round(float(vote_avg), 1) if vote_avg else "N/A"

    # Year
    rd = d.get("release_date") or d.get("first_air_date") or ""
    year = int(rd[:4]) if rd and len(rd) >= 4 else None

    # Genres — return as comma string so channel.py split works
    genres = ", ".join(g["name"] for g in d.get("genres", []))

    # External IDs
    ext = d.get("external_ids", {})
    imdb_id = d.get("imdb_id") or ext.get("imdb_id")

    tmdb_url = (
        f"https://www.themoviedb.org/movie/{tmdb_id}"
        if media_type == "movie"
        else f"https://www.themoviedb.org/tv/{tmdb_id}"
    )
    imdb_url = f"https://www.imdb.com/title/{imdb_id}" if imdb_id else tmdb_url

    plot = (d.get("overview") or "")[:800] or None

    return {
        # Keys used by channel.py
        "poster_url":   poster_url,
        "backdrop_url": backdrop_url,
        "rating":       str(rating),
        "genres":       genres,
        "year":         year,
        "tmdb_url":     tmdb_url,
        "url":          imdb_url,        # IMDB fallback url key
        # Extra detail keys (used elsewhere / future)
        "title":        d.get("title") or d.get("name"),
        "plot":         plot,
        "tagline":      d.get("tagline"),
        "runtime":      d.get("runtime") or (d.get("episode_run_time") or [None])[0],
        "votes":        d.get("vote_count", 0),
        "release_date": rd,
        "tmdb_id":      tmdb_id,
        "imdb_id":      imdb_id,
        "languages":    ", ".join(
            l.get("english_name", l.get("name", ""))
            for l in d.get("spoken_languages", [])
        ),
        "countries":    ", ".join(
            c.get("name", "") for c in d.get("production_countries", [])
        ),
        "director":     ", ".join(p["name"] for p in crew if p.get("job") == "Director"),
        "writer":       ", ".join(p["name"] for p in crew if p.get("job") in ("Writer", "Screenplay")),
        "producer":     ", ".join(p["name"] for p in crew if p.get("job") == "Producer"),
        "composer":     ", ".join(p["name"] for p in crew if p.get("department") == "Sound"),
        "cinematographer": ", ".join(p["name"] for p in crew if p.get("job") == "Director of Photography"),
        "cast":         ", ".join(p["name"] for p in cast[:10]),
        "certificates": "",
        "distributors": "",
        "aka":          "",
        "seasons":      d.get("number_of_seasons"),
        "box_office":   None,
        "kind":         "movie" if media_type == "movie" else "tv series",
    }


# ─────────────────────────────────────────────────────────────
# PUBLIC API — both functions now use TMDB directly
# ─────────────────────────────────────────────────────────────

async def get_movie_detailsx(query, id=False, file=None) -> dict:
    """
    Primary TMDB fetch used by channel.py when TMDB_POSTER=True.
    Always returns a dict (never None). Returns {} on failure.
    """
    try:
        raw = await _tmdb_search_and_fetch(query)
        return _normalise_tmdb(raw)
    except Exception as e:
        logger.exception(f"get_movie_detailsx error: {e}")
        return {}


async def get_movie_details(query, id=False, file=None) -> dict | None:
    """
    Fallback fetch used by channel.py when TMDB_POSTER=False or TMDB has no poster.
    Now also uses TMDB (Cinemagoer removed — too slow / unreliable).
    Returns dict or None (channel.py does `or {}` on this).
    """
    try:
        raw = await _tmdb_search_and_fetch(query)
        result = _normalise_tmdb(raw)
        return result if result else None
    except Exception as e:
        logger.exception(f"get_movie_details error: {e}")
        return None
