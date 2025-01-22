# src/runtime/cuda_context.py

import torch
from typing import Dict, Optional
from ..common.exceptions import CUDAError

class CUDAContext:
    def __init__(self, gpu_id: int):
        self.gpu_id = gpu_id
        self.device = None
        self.stream = None
        self.memory_pool = None
        self._initialize_context()

    def _initialize_context(self):
        """Initialize CUDA context"""
        try:
            self.device = torch.device(f'cuda:{self.gpu_id}')
            self.stream = torch.cuda.Stream(device=self.gpu_id)
            self.memory_pool = torch.cuda.memory.CUDAPluggableAllocator()
            torch.cuda.set_device(self.gpu_id)
        except Exception as e:
            raise CUDAError(f"Failed to initialize CUDA context: {e}")

    def get_context_info(self) -> Dict:
        """Get context information"""
        return {
            "gpu_id": self.gpu_id,
            "device": self.device,
            "stream": self.stream,
            "memory_allocated": torch.cuda.memory_allocated(self.device),
            "memory_reserved": torch.cuda.memory_reserved(self.device)
        }

    def __enter__(self):
        """Context manager entry"""
        torch.cuda.set_device(self.gpu_id)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stream.synchronize()