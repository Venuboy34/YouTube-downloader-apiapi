from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import urllib.request
import urllib.error

class handler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        """Set CORS headers to allow cross-origin requests"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def do_OPTIONS(self):
        """Handle preflight CORS requests"""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests for YouTube downloads"""
        try:
            # Parse URL and query parameters
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            
            # Get parameters from query string
            video_url = params.get('url', [''])[0]
            format_type = params.get('format', ['mp4'])[0]  # mp3 or mp4
            audio_quality = params.get('quality', ['128'])[0]
            
            if not video_url:
                self.send_response(400)
                self._set_cors_headers()
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': 'Missing required parameter: url',
                    'usage': '/api/download?url=YOUTUBE_URL&format=mp3&quality=128'
                }).encode())
                return
            
            # Build RapidAPI request
            api_url = (
                f"https://youtube-info-download-api.p.rapidapi.com/ajax/download.php"
                f"?format={format_type}"
                f"&add_info=0"
                f"&url={video_url}"
                f"&audio_quality={audio_quality}"
                f"&allow_extended_duration=false"
                f"&no_merge=false"
                f"&audio_language=en"
            )
            
            # Create request with headers
            req = urllib.request.Request(api_url)
            req.add_header('x-rapidapi-host', 'youtube-info-download-api.p.rapidapi.com')
            req.add_header('x-rapidapi-key', 'e239f85679msh1175aa87c891e18p1557f0jsnb52f646bd75c')
            
            # Make request to RapidAPI
            with urllib.request.urlopen(req) as response:
                data = response.read()
                result = json.loads(data.decode())
            
            # Send successful response
            self.send_response(200)
            self._set_cors_headers()
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': True,
                'data': result,
                'requested_format': format_type,
                'video_url': video_url
            }).encode())
            
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self._set_cors_headers()
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': f'RapidAPI Error: {e.reason}',
                'status_code': e.code
            }).encode())
            
        except Exception as e:
            self.send_response(500)
            self._set_cors_headers()
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': str(e),
                'message': 'Internal server error'
            }).encode())
    
    def do_POST(self):
        """Handle POST requests for YouTube downloads"""
        try:
            # Get content length and read body
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body.decode())
            
            video_url = data.get('url', '')
            format_type = data.get('format', 'mp4')
            audio_quality = data.get('quality', '128')
            
            if not video_url:
                self.send_response(400)
                self._set_cors_headers()
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': 'Missing required field: url'
                }).encode())
                return
            
            # Build RapidAPI request
            api_url = (
                f"https://youtube-info-download-api.p.rapidapi.com/ajax/download.php"
                f"?format={format_type}"
                f"&add_info=0"
                f"&url={video_url}"
                f"&audio_quality={audio_quality}"
                f"&allow_extended_duration=false"
                f"&no_merge=false"
                f"&audio_language=en"
            )
            
            # Create request with headers
            req = urllib.request.Request(api_url)
            req.add_header('x-rapidapi-host', 'youtube-info-download-api.p.rapidapi.com')
            req.add_header('x-rapidapi-key', 'e239f85679msh1175aa87c891e18p1557f0jsnb52f646bd75c')
            
            # Make request to RapidAPI
            with urllib.request.urlopen(req) as response:
                api_data = response.read()
                result = json.loads(api_data.decode())
            
            # Send successful response
            self.send_response(200)
            self._set_cors_headers()
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': True,
                'data': result,
                'requested_format': format_type,
                'video_url': video_url
            }).encode())
            
        except Exception as e:
            self.send_response(500)
            self._set_cors_headers()
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': str(e),
                'message': 'Internal server error'
            }).encode())
