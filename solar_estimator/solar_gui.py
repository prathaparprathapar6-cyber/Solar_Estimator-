"""VoltRoof Solar PV Estimator - GUI & Application Entry Point
Launches the integrated Solar PV Estimator Web GUI with dynamic sizing,
sanctioned load validation, KERC 20 kW LT compliance, and PDF generation.
"""

import sys
import os
import webbrowser
from solar_pv_estimator import run_server, calculate_system, build_system_report, build_multi_site_report, export_pdf

def main():
    port = 5050
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    print("\n" + "=" * 60)
    print(" VoltRoof Solar PV Estimator GUI")
    print(" LT Applications (1 kW - 20 kW Ceiling per KERC / ESCOM)")
    print("=" * 60)
    print(f" Starting application interface on port {port}...")
    run_server(port)

if __name__ == "__main__":
    main()
