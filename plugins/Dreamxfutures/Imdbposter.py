import re
import aiohttp
import warnings
import logging
from io import BytesIO
from PIL import Image
from info import DREAMXBOTZ_IMAGE_FETCH, TMDB_API_KEY
from imdb import Cinemagoer


logger = logging.getLogger(__name__)
ia = Cinemagoer()
LONG_IMDB_DESCRIPTION = False

Image.MAX_IMAGE_PIXELS = None
warnings.simplefilter("ignore", Image.DecompressionBombWarning)

_session: aiohttp.ClientSession | None = None

TMDB_BASE = "https://api.themoviedb.org/3"
TMDB_IMG  = "https://image.tmdb.org/t/p/w1280"


async def get_session():
    global _session
    if _session is None or _session.closed:
        _session = aiohttp.ClientSession()
    return _session


async def fetch_image(url, size=(860, 1200)):
    if not DREAMXBOTZ_IMAGE_FETCH:
        logger.info("Image fetching is disabled.")
        return url

    try:
        session = await get_session()
        async with session.get(url) as response:
            if response.status != 200:
                logger.error(f"Failed to fetch image: {response.status} for {url}")
                return None

            data = await response.read()
            img = Image.open(BytesIO(data))
            img = img.resize(size, Image.LANCZOS)

            out = BytesIO()
            img.save(out, format="JPEG")
            out.seek(0)
            return out

    except aiohttp.ClientError as e:
        logger.error(f"HTTP request error in fetch_image: {e}")
    except IOError as e:
        logger.error(f"I/O error in fetch_image: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in fetch_image: {e}")

    return None


async def close_session():
    global _session
    if _session and not _session.closed:
        await _session.close()


def list_to_str(lst):
    if lst:
        return ", ".join(map(str, lst))
    return ""


# ──────────────────────────────────────────────
# IMDB via Cinemagoer  (unchanged)
# ──────────────────────────────────────────────
async def get_movie_details(query, id=False, file=None):
    try:
        if not id:
            query = query.strip().lower()
            title = query
            year = re.findall(r'[1-2]\d{3}$', query, re.IGNORECASE)
            if year:
                year = list_to_str(year[:1])
                title = query.replace(year, "").strip()
            elif file is not None:
                year = re.findall(r'[1-2]\d{3}', file, re.IGNORECASE)
                if year:
                    year = list_to_str(year[:1])
            else:
                year = None

            movieid = ia.search_movie(title.lower(), results=10)
            if not movieid:
                return None

            if year:
                filtered = list(filter(lambda k: str(k.get('year')) == str(year), movieid))
                if not filtered:
                    filtered = movieid
            else:
                filtered = movieid

            filtered_kind = list(filter(lambda k: k.get('kind') in ['movie', 'tv series'], filtered))
            movieid = filtered_kind[0].movieID if filtered_kind else filtered[0].movieID
        else:
            movieid = query

        movie = ia.get_movie(movieid)
        ia.update(movie, info=['main', 'vote details'])

        if movie.get("original air date"):
            date = movie["original air date"]
        elif movie.get("year"):
            date = movie.get("year")
        else:
            date = "N/A"

        plot = movie.get('plot')
        if plot and len(plot) > 0:
            plot = plot[0]
        else:
            plot = movie.get('plot outline')
        if plot and len(plot) > 800:
            plot = plot[:800] + "..."

        poster_url = movie.get('full-size cover url')
        if poster_url and poster_url.endswith("@.jpg"):
            poster_url = poster_url + "._V1_SX1440.jpg"

        return {
            'title': movie.get('title'),
            'votes': movie.get('votes'),
            "aka": list_to_str(movie.get("akas")),
            "seasons": movie.get("number of seasons"),
            "box_office": movie.get('box office'),
            'localized_title': movie.get('localized title'),
            'kind': movie.get("kind"),
            "imdb_id": f"tt{movie.get('imdbID')}",
            "cast": list_to_str(movie.get("cast")),
            "runtime": list_to_str(movie.get("runtimes")),
            "countries": list_to_str(movie.get("countries")),
            "certificates": list_to_str(movie.get("certificates")),
            "languages": list_to_str(movie.get("languages")),
            "director": list_to_str(movie.get("director")),
            "writer": list_to_str(movie.get("writer")),
            "producer": list_to_str(movie.get("producer")),
            "composer": list_to_str(movie.get("composer")),
            "cinematographer": list_to_str(movie.get("cinematographer")),
            "music_team": list_to_str(movie.get("music department")),
            "distributors": list_to_str(movie.get("distributors")),
            'release_date': date,
            'year': movie.get('year'),
            'genres': list_to_str(movie.get("genres")),
            'poster_url': poster_url,
            'plot': plot,
            'rating': str(movie.get("rating", "N/A")),
            'url': f'https://www.imdb.com/title/tt{movieid}'
        }
    except Exception as e:
        logger.exception(f"An error occurred in get_movie_details: {e}")
        return None


# ──────────────────────────────────────────────
# TMDB official API  (replaces broken 3rd-party)
# ──────────────────────────────────────────────
async def get_movie_detailsx(query, id=False, file=None):
    """
    Fetch movie/series details from the official TMDB API.
    Returns a dict with the same keys channel.py expects:
      poster_url, backdrop_url, rating, genres, year,
      tmdb_url, title, plot, runtime, votes, languages, countries,
      director, cast, imdb_id, tmdb_id
    Returns {} on any failure (never None, so .get() is always safe).
    """
    if not TMDB_API_KEY:
        logger.warning("TMDB_API_KEY not set — skipping TMDB lookup")
        return {}

    try:
        session = await get_session()
        params = {
            "api_key": TMDB_API_KEY,
            "query": str(query).strip(),
            "include_adult": "false",
        }

        # ── 1. Search (try movie first, then tv) ──────────────────────
        tmdb_id = media_type = None

        for mtype in ("movie", "tv"):
            url = f"{TMDB_BASE}/search/{mtype}"
            async with session.get(url, params=params) as resp:
                if resp.status != 200:
                    logger.error(f"TMDB search/{mtype} failed: {resp.status}")
                    continue
                data = await resp.json()
                results = data.get("results", [])
                if results:
                    tmdb_id = results[0]["id"]
                    media_type = mtype
                    break

        if not tmdb_id:
            logger.info(f"TMDB: no results for '{query}'")
            return {}

        # ── 2. Details + credits + images ─────────────────────────────
        detail_params = {
            "api_key": TMDB_API_KEY,
            "append_to_response": "credits,images",
            "include_image_language": "en,null",
        }
        detail_url = f"{TMDB_BASE}/{media_type}/{tmdb_id}"
        async with session.get(detail_url, params=detail_params) as resp:
            if resp.status != 200:
                logger.error(f"TMDB detail fetch failed: {resp.status}")
                return {}
            d = await resp.json()

        # ── 3. Normalise ───────────────────────────────────────────────
        details = {}

        details['title'] = d.get('title') or d.get('name')
        details['year'] = (
            int(d['release_date'][:4]) if d.get('release_date')
            else int(d['first_air_date'][:4]) if d.get('first_air_date')
            else None
        )
        details['release_date'] = d.get('release_date') or d.get('first_air_date')
        details['rating'] = round(float(d.get('vote_average', 0)), 1) or None
        details['votes'] = d.get('vote_count', 0)
        details['runtime'] = (
            d.get('runtime') or
            (d.get('episode_run_time') or [None])[0]
        )
        details['plot'] = d.get('overview')
        details['tagline'] = d.get('tagline')
        details['tmdb_id'] = tmdb_id
        details['imdb_id'] = d.get('imdb_id')
        details['tmdb_url'] = (
            f"https://www.themoviedb.org/movie/{tmdb_id}" if media_type == "movie"
            else f"https://www.themoviedb.org/tv/{tmdb_id}"
        )

        # Genres
        details['genres'] = [g['name'] for g in d.get('genres', [])]

        # Languages / countries
        details['languages'] = [
            l.get('english_name', l.get('name', ''))
            for l in d.get('spoken_languages', [])
        ]
        details['countries'] = [
            c.get('name', '') for c in d.get('production_countries', [])
        ]

        # Credits
        crew = d.get('credits', {}).get('crew', [])
        cast = d.get('credits', {}).get('cast', [])
        details['director'] = [p['name'] for p in crew if p.get('job') == 'Director']
        details['writer']   = [p['name'] for p in crew if p.get('job') in ('Writer', 'Screenplay')]
        details['producer'] = [p['name'] for p in crew if p.get('job') == 'Producer']
        details['composer'] = [p['name'] for p in crew if p.get('department') == 'Sound']
        details['cinematographer'] = [p['name'] for p in crew if p.get('job') == 'Director of Photography']
        details['cast'] = [p['name'] for p in cast[:10]]

        # Poster
        poster_path = d.get('poster_path')
        details['poster_url'] = f"{TMDB_IMG}{poster_path}" if poster_path else None

        # Backdrop (landscape)
        backdrop_path = d.get('backdrop_path')
        # prefer an English-language backdrop from images if available
        img_backdrops = d.get('images', {}).get('backdrops', [])
        if img_backdrops:
            # pick first English or language-neutral backdrop
            for bd in img_backdrops:
                if bd.get('iso_639_1') in ('en', None, ''):
                    backdrop_path = bd.get('file_path', backdrop_path)
                    break
        details['backdrop_url'] = f"{TMDB_IMG}{backdrop_path}" if backdrop_path else None

        return details

    except Exception as e:
        logger.exception(f"An error occurred in get_movie_detailsx: {e}")
        return {}
