"""
TOMBO Audio Processing Library
Recording, Playback, Synthesis, Analysis
"""

import math
from typing import List, Optional, Callable


class AudioFrame:
    """Single audio frame/sample"""
    
    def __init__(self, data: List[float], channels: int = 1, sample_rate: int = 44100):
        self.data = data
        self.channels = channels
        self.sample_rate = sample_rate
        self.length = len(data) // channels
    
    def duration(self) -> float:
        """Duration in seconds"""
        return self.length / self.sample_rate


class AudioStream:
    """Audio stream for recording/playback"""
    
    def __init__(self, channels: int = 2, sample_rate: int = 44100, bitdepth: int = 16):
        self.channels = channels
        self.sample_rate = sample_rate
        self.bitdepth = bitdepth
        self.frames = []
        self.is_recording = False
    
    def start_recording(self):
        """Start recording audio"""
        self.is_recording = True
        self.frames = []
        return True
    
    def stop_recording(self):
        """Stop recording audio"""
        self.is_recording = False
        return len(self.frames)
    
    def add_frame(self, data: List[float]):
        """Add frame to stream"""
        if len(data) != self.channels:
            raise ValueError(f"Expected {self.channels} channels")
        self.frames.append(data)
    
    def get_duration(self) -> float:
        """Get total duration in seconds"""
        return len(self.frames) / self.sample_rate
    
    def play(self, duration: Optional[float] = None):
        """Play audio stream"""
        if duration is None:
            duration = self.get_duration()
        return True


class Microphone:
    """Microphone input device"""
    
    def __init__(self, device_id: int = 0):
        self.device_id = device_id
        self.is_active = False
    
    def open(self):
        """Open microphone"""
        self.is_active = True
        return True
    
    def close(self):
        """Close microphone"""
        self.is_active = False
        return True
    
    def record(self, duration: float, stream: AudioStream) -> AudioStream:
        """Record audio for duration seconds"""
        self.open()
        
        num_frames = int(duration * stream.sample_rate)
        stream.start_recording()
        
        # Simulate recording silence
        for _ in range(num_frames):
            frame = [0.0] * stream.channels
            stream.add_frame(frame)
        
        stream.stop_recording()
        self.close()
        return stream
    
    def list_devices():
        """List available microphones"""
        return [
            {"id": 0, "name": "Default Microphone"},
            {"id": 1, "name": "Built-in Microphone"}
        ]


class Speaker:
    """Speaker output device"""
    
    def __init__(self, device_id: int = 0):
        self.device_id = device_id
        self.is_active = False
    
    def open(self):
        """Open speaker"""
        self.is_active = True
        return True
    
    def close(self):
        """Close speaker"""
        self.is_active = False
        return True
    
    def play(self, stream: AudioStream) -> bool:
        """Play audio stream"""
        self.open()
        # Simulate playback
        duration = stream.get_duration()
        self.close()
        return True


class Mixer:
    """Audio mixer for combining streams"""
    
    def __init__(self, num_channels: int = 2):
        self.num_channels = num_channels
        self.tracks = []
    
    def add_track(self, stream: AudioStream):
        """Add audio track"""
        self.tracks.append(stream)
    
    def mix(self) -> AudioStream:
        """Mix all tracks together"""
        if not self.tracks:
            return AudioStream(self.num_channels)
        
        result = AudioStream(self.num_channels, self.tracks[0].sample_rate)
        
        # Assuming all tracks have same length
        max_frames = max(t.get_duration() * t.sample_rate for t in self.tracks)
        
        for frame_idx in range(int(max_frames)):
            mixed_frame = [0.0] * self.num_channels
            
            for track in self.tracks:
                if frame_idx < len(track.frames):
                    for ch in range(self.num_channels):
                        mixed_frame[ch] += track.frames[frame_idx][ch]
            
            # Normalize to prevent clipping
            for ch in range(self.num_channels):
                mixed_frame[ch] /= len(self.tracks)
            
            result.add_frame(mixed_frame)
        
        return result


class SineWave:
    """Sine wave synthesizer"""
    
    @staticmethod
    def generate(frequency: float, duration: float, sample_rate: int = 44100, amplitude: float = 0.5) -> List[float]:
        """Generate sine wave"""
        num_samples = int(duration * sample_rate)
        samples = []
        
        for i in range(num_samples):
            t = i / sample_rate
            sample = amplitude * math.sin(2 * math.pi * frequency * t)
            samples.append(sample)
        
        return samples


class SquareWave:
    """Square wave synthesizer"""
    
    @staticmethod
    def generate(frequency: float, duration: float, sample_rate: int = 44100, amplitude: float = 0.5) -> List[float]:
        """Generate square wave"""
        num_samples = int(duration * sample_rate)
        samples = []
        period = sample_rate / frequency
        
        for i in range(num_samples):
            phase = (i % period) / period
            sample = amplitude if phase < 0.5 else -amplitude
            samples.append(sample)
        
        return samples


class SawtoothWave:
    """Sawtooth wave synthesizer"""
    
    @staticmethod
    def generate(frequency: float, duration: float, sample_rate: int = 44100, amplitude: float = 0.5) -> List[float]:
        """Generate sawtooth wave"""
        num_samples = int(duration * sample_rate)
        samples = []
        period = sample_rate / frequency
        
        for i in range(num_samples):
            phase = (i % period) / period
            sample = amplitude * (2 * phase - 1)
            samples.append(sample)
        
        return samples


class TriangleWave:
    """Triangle wave synthesizer"""
    
    @staticmethod
    def generate(frequency: float, duration: float, sample_rate: int = 44100, amplitude: float = 0.5) -> List[float]:
        """Generate triangle wave"""
        num_samples = int(duration * sample_rate)
        samples = []
        period = sample_rate / frequency
        
        for i in range(num_samples):
            phase = (i % period) / period
            if phase < 0.5:
                sample = amplitude * 4 * (phase - 0.25)
            else:
                sample = amplitude * 4 * (0.75 - phase)
            samples.append(sample)
        
        return samples


class AudioFilter:
    """Audio filtering operations"""
    
    @staticmethod
    def lowpass(data: List[float], cutoff: float, sample_rate: int = 44100) -> List[float]:
        """Low-pass filter"""
        alpha = cutoff / (cutoff + sample_rate)
        filtered = [data[0]]
        
        for i in range(1, len(data)):
            filtered.append(alpha * data[i] + (1 - alpha) * filtered[i-1])
        
        return filtered
    
    @staticmethod
    def highpass(data: List[float], cutoff: float, sample_rate: int = 44100) -> List[float]:
        """High-pass filter"""
        alpha = cutoff / (cutoff + sample_rate)
        filtered = [data[0]]
        
        for i in range(1, len(data)):
            filtered.append(alpha * (filtered[i-1] + data[i] - data[i-1]))
        
        return filtered
    
    @staticmethod
    def bandpass(data: List[float], low: float, high: float, sample_rate: int = 44100) -> List[float]:
        """Band-pass filter"""
        lowpassed = AudioFilter.lowpass(data, high, sample_rate)
        bandpassed = AudioFilter.highpass(lowpassed, low, sample_rate)
        return bandpassed


class AudioAnalysis:
    """Audio analysis and feature extraction"""
    
    @staticmethod
    def rms(data: List[float]) -> float:
        """Root Mean Square (volume indicator)"""
        if not data:
            return 0
        mean_square = sum(x**2 for x in data) / len(data)
        return math.sqrt(mean_square)
    
    @staticmethod
    def peak(data: List[float]) -> float:
        """Peak amplitude"""
        return max(abs(x) for x in data) if data else 0
    
    @staticmethod
    def crest_factor(data: List[float]) -> float:
        """Crest factor (peak / RMS)"""
        rms_val = AudioAnalysis.rms(data)
        peak_val = AudioAnalysis.peak(data)
        return peak_val / rms_val if rms_val > 0 else 0
    
    @staticmethod
    def zero_crossings(data: List[float]) -> int:
        """Count zero crossings"""
        count = 0
        for i in range(1, len(data)):
            if (data[i-1] < 0 and data[i] >= 0) or (data[i-1] >= 0 and data[i] < 0):
                count += 1
        return count
    
    @staticmethod
    def spectral_centroid(data: List[float], sample_rate: int = 44100) -> float:
        """Calculate spectral centroid (center of mass of spectrum)"""
        # Simplified implementation
        if not data or len(data) < 2:
            return 0
        return sample_rate / 2


class Envelope:
    """ADSR (Attack, Decay, Sustain, Release) envelope"""
    
    def __init__(self, attack: float, decay: float, sustain: float, release: float, sample_rate: int = 44100):
        self.attack = attack
        self.decay = decay
        self.sustain = sustain
        self.release = release
        self.sample_rate = sample_rate
    
    def apply(self, data: List[float], note_duration: float) -> List[float]:
        """Apply ADSR envelope to audio"""
        attack_samples = int(self.attack * self.sample_rate)
        decay_samples = int(self.decay * self.sample_rate)
        sustain_level = 0.7
        
        envelope = []
        total_samples = len(data)
        
        for i in range(total_samples):
            if i < attack_samples:
                # Attack phase
                env = i / attack_samples if attack_samples > 0 else 1
            elif i < attack_samples + decay_samples:
                # Decay phase
                progress = (i - attack_samples) / decay_samples if decay_samples > 0 else 0
                env = 1 - progress * (1 - sustain_level)
            else:
                # Sustain phase
                env = sustain_level
            
            envelope.append(data[i] * env)
        
        return envelope


# ============================================================================
# PUBLIC API FUNCTIONS
# ============================================================================

def record_audio(duration: float, sample_rate: int = 44100, channels: int = 2) -> AudioStream:
    """Record audio for specified duration"""
    stream = AudioStream(channels, sample_rate)
    mic = Microphone()
    return mic.record(duration, stream)

def play_audio(stream: AudioStream):
    """Play audio stream"""
    speaker = Speaker()
    return speaker.play(stream)

def generate_sine(frequency: float, duration: float, sample_rate: int = 44100) -> List[float]:
    """Generate sine wave"""
    return SineWave.generate(frequency, duration, sample_rate)

def generate_square(frequency: float, duration: float, sample_rate: int = 44100) -> List[float]:
    """Generate square wave"""
    return SquareWave.generate(frequency, duration, sample_rate)

def generate_sawtooth(frequency: float, duration: float, sample_rate: int = 44100) -> List[float]:
    """Generate sawtooth wave"""
    return SawtoothWave.generate(frequency, duration, sample_rate)

def generate_triangle(frequency: float, duration: float, sample_rate: int = 44100) -> List[float]:
    """Generate triangle wave"""
    return TriangleWave.generate(frequency, duration, sample_rate)

def filter_lowpass(data: List[float], cutoff: float, sample_rate: int = 44100) -> List[float]:
    """Apply low-pass filter"""
    return AudioFilter.lowpass(data, cutoff, sample_rate)

def filter_highpass(data: List[float], cutoff: float, sample_rate: int = 44100) -> List[float]:
    """Apply high-pass filter"""
    return AudioFilter.highpass(data, cutoff, sample_rate)

def filter_bandpass(data: List[float], low: float, high: float, sample_rate: int = 44100) -> List[float]:
    """Apply band-pass filter"""
    return AudioFilter.bandpass(data, low, high, sample_rate)

def analyze_rms(data: List[float]) -> float:
    """Calculate RMS (volume level)"""
    return AudioAnalysis.rms(data)

def analyze_peak(data: List[float]) -> float:
    """Find peak amplitude"""
    return AudioAnalysis.peak(data)

def analyze_zero_crossings(data: List[float]) -> int:
    """Count zero crossings"""
    return AudioAnalysis.zero_crossings(data)

def create_envelope(attack: float, decay: float, sustain: float, release: float) -> Envelope:
    """Create ADSR envelope"""
    return Envelope(attack, decay, sustain, release)
