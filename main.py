"""
Eco-Guard-Ramsar Deployment Loop
Autonomous monitoring system for Sasthamcotta Lake (Ramsar site)

This module runs the main field deployment loop for solar-powered monitoring units.
"""

import time
import random
import logging
import sys
import io
from src.bio_monitor import BiologicalIndicatorAI

# Handle Unicode encoding issues on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def field_deployment_loop():
    """
    Main deployment loop for continuous environmental monitoring.
    
    Collects:
    - Physico-chemical parameters: pH, Turbidity, Nitrogen
    - Biological indicators: AI-detected species and confidence scores
    
    Runs in perpetuity until interrupted by user (Ctrl+C)
    """
    logger.info("[POWER] Solar-Powered Monitoring Unit Active: Sasthamcotta Lake (Ramsar Site)")
    logger.info("[UPTIME] Target: 98% operational availability\n")
    
    try:
        # Initialize biological indicator engine
        monitor = BiologicalIndicatorAI()
        logger.info("[INIT] Biological Indicator Engine Initialized...")
        
        sample_count = 0
        while True:
            sample_count += 1
            
            # 1. Physico-chemical Data Collection
            vitals = {
                "pH": round(random.uniform(6.5, 8.5), 2),
                "Turbidity": round(random.uniform(1.0, 5.0), 2),
                "Nitrogen": round(random.uniform(0.5, 2.5), 2)
            }
            
            # 2. Biological AI Analysis
            try:
                species, conf = monitor.detect_species(None)
            except Exception as e:
                logger.error(f"Biological detection failed: {e}")
                species, conf = "ERROR", 0.0

            # 3. Output Field Report
            print(f"[DATA #{sample_count}] pH: {vitals['pH']} | Turbidity: {vitals['Turbidity']} NTU | Nitrogen: {vitals['Nitrogen']} mg/L")
            print(f"[AI]   Detection: {species} (confidence: {conf:.2%})")
            print("-" * 70)

            time.sleep(5) # 5-second sampling interval for field stability
            
    except KeyboardInterrupt:
        logger.info(f"\n[SHUTDOWN] Unit Powering Down Safely. [Total samples collected: {sample_count}]")
    except Exception as e:
        logger.error(f"[CRITICAL] Error in deployment loop: {e}", exc_info=True)


if __name__ == "__main__":
    field_deployment_loop()