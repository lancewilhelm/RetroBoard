#!/usr/bin/env python3
import asyncio
# Import the quart api object
from quartUtils import api

# Start the quart server if this file was called
if __name__ == '__main__':
    api.run(host='0.0.0.0')
