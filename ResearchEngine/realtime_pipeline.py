import asyncio
import random
import time
from collections import deque

class StreamConnector:
    """Base class for streaming data sources."""
    async def stream(self, queue):
        raise NotImplementedError

class MockWeatherStream(StreamConnector):
    """Simulates real-time weather data."""
    async def stream(self, queue):
        while True:
            # Generate temperature with cycle + noise
            t = time.time()
            val = 15.0 + 2.0 * math.sin(t / 10.0) + random.gauss(0, 0.5)
            await queue.put({'timestamp': t, 'value': val})
            await asyncio.sleep(1) # Data arrives every second

class RealtimeAnalysisEngine:
    """Maintains a sliding window and performs incremental spectral updates."""
    def __init__(self, window_size=50):
        self.buffer = deque(maxlen=window_size)
        self.count = 0
        
    async def process(self, queue):
        while True:
            data = await queue.get()
            self.buffer.append(data['value'])
            self.count += 1
            
            if len(self.buffer) == self.buffer.maxlen and self.count % 10 == 0:
                # Perform analysis on current window
                self.analyze()
            queue.task_done()
            
    def analyze(self):
        # Placeholder: Call Lomb-Scargle on self.buffer
        print(f"[{self.count}] Analyzing buffer of size {len(self.buffer)}, latest: {self.buffer[-1]:.2f}")

async def main():
    queue = asyncio.Queue()
    connector = MockWeatherStream()
    engine = RealtimeAnalysisEngine()
    
    # Run in parallel
    await asyncio.gather(connector.stream(queue), engine.process(queue))

if __name__ == "__main__":
    import math
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopping stream...")
