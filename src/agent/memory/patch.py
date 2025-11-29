"""
Patch to fix the ollama base URL issue in browser-use library.
This patch ensures that mem0 is configured with the correct ollama endpoint.
"""

import os
import logging
from typing import Any

logger = logging.getLogger(__name__)

def patch_embedder_config_dict():
    """
    Patch the embedder_config_dict property to include ollama_base_url when provider is ollama.
    """
    try:
        # Import the original views module
        from browser_use.agent.memory.views import MemoryConfig
        
        # Store the original method
        original_embedder_config_dict = MemoryConfig.embedder_config_dict
        
        def patched_embedder_config_dict(self) -> dict[str, Any]:
            """Patched version that includes ollama_base_url for ollama provider."""
            config = original_embedder_config_dict.fget(self)
            
            # If using ollama, add the base URL from environment variable
            if self.embedder_provider == 'ollama':
                ollama_base_url = os.getenv('OLLAMA_ENDPOINT', 'http://localhost:11434')
                if ollama_base_url:
                    config['config']['ollama_base_url'] = ollama_base_url
                    logger.info(f"Using ollama base URL: {ollama_base_url}")
            
            return config
        
        # Replace the method
        MemoryConfig.embedder_config_dict = property(patched_embedder_config_dict)
        
        logger.info("Successfully patched MemoryConfig.embedder_config_dict")
        
    except ImportError as e:
        logger.error(f"Failed to patch browser-use memory config: {e}")
        raise

# Apply the patch when this module is imported
patch_embedder_config_dict()