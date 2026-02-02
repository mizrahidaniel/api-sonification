"""Log parser for various HTTP log formats."""
import re
from datetime import datetime
from typing import Dict, Optional
import json


class LogParser:
    """Parse HTTP access logs into structured events."""
    
    # Nginx combined log format
    NGINX_PATTERN = re.compile(
        r'(?P<ip>[\d.]+) - (?P<user>\S+) \[(?P<time>[^\]]+)\] '
        r'"(?P<method>\S+) (?P<path>\S+) (?P<protocol>\S+)" '
        r'(?P<status>\d+) (?P<bytes>\d+) '
        r'"(?P<referer>[^"]*)" "(?P<agent>[^"]*)"'
    )
    
    # Apache common log format
    APACHE_PATTERN = re.compile(
        r'(?P<ip>[\d.]+) - (?P<user>\S+) \[(?P<time>[^\]]+)\] '
        r'"(?P<method>\S+) (?P<path>\S+) (?P<protocol>\S+)" '
        r'(?P<status>\d+) (?P<bytes>\d+)'
    )
    
    def parse_line(self, line: str) -> Optional[Dict]:
        """Parse a single log line into structured data."""
        line = line.strip()
        if not line:
            return None
            
        # Try JSON format first
        if line.startswith('{'):
            try:
                return self._parse_json(line)
            except json.JSONDecodeError:
                pass
        
        # Try Nginx format
        match = self.NGINX_PATTERN.match(line)
        if match:
            return self._extract_event(match)
        
        # Try Apache format
        match = self.APACHE_PATTERN.match(line)
        if match:
            return self._extract_event(match)
        
        return None
    
    def _parse_json(self, line: str) -> Dict:
        """Parse JSON log format."""
        data = json.loads(line)
        return {
            'timestamp': datetime.now(),
            'method': data.get('method', 'GET'),
            'path': data.get('path', '/'),
            'status': int(data.get('status', 200)),
            'bytes': int(data.get('bytes', 0)),
            'response_time': float(data.get('response_time', 0))
        }
    
    def _extract_event(self, match) -> Dict:
        """Extract event from regex match."""
        groups = match.groupdict()
        return {
            'timestamp': datetime.now(),
            'method': groups['method'],
            'path': groups['path'],
            'status': int(groups['status']),
            'bytes': int(groups['bytes']),
            'response_time': 0.0  # Not available in standard logs
        }
    
    def stream_file(self, filepath: str):
        """Stream log file line by line."""
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    event = self.parse_line(line)
                    if event:
                        yield event
        except FileNotFoundError:
            print(f"Log file not found: {filepath}")
