import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd

ROOT_DIR = Path(__file__).parent.parent


def find_file_pattern(base_path: Path, patterns: list[str]) -> Optional[Path]:
    """Find first file matching any of the patterns."""
    if not base_path.exists():
        return None
    
    for f in base_path.rglob('*'):
        if not f.is_file():
            continue
        name_lower = f.name.lower()
        for p in patterns:
            if p.replace('*', '').lower() in name_lower:
                if f.suffix.lower() in ['.csv', '.xlsx', '.xls', '.parquet']:
                    return f
    return None


def scan_period_coverage(year: str, month: str) -> dict:
    """
    Scan coverage for a specific period.
    Returns coverage info with file paths.
    """
    raw_dir = ROOT_DIR / '01_Raw'
    
    ml_path = raw_dir / 'ML' / year / month
    sap_path = raw_dir / 'SAP' / year / month
    
    ml_file = find_file_pattern(ml_path, ['liberaciones', 'ventas', 'orders'])
    sap_file = find_file_pattern(sap_path, ['sap_report', 'sap_export', 'sap'])
    
    coverage = {
        'period': f'{year}/{month}',
        'year': year,
        'month': month,
        'ml': {
            'required_pattern': '01_Raw/ML/YYYY/MM/**/Liberaciones*.csv|xlsx',
            'found': ml_file is not None,
            'file_path': str(ml_file) if ml_file else None,
            'file_name': ml_file.name if ml_file else None
        },
        'sap': {
            'required_pattern': '01_Raw/SAP/YYYY/MM/**/sap_report*.csv|xlsx',
            'found': sap_file is not None,
            'file_path': str(sap_file) if sap_file else None,
            'file_name': sap_file.name if sap_file else None
        }
    }
    
    coverage['status'] = 'OK' if (coverage['ml']['found'] and coverage['sap']['found']) else 'WAITING_FOR_DATA'
    
    return coverage


def run_coverage_gate(year: str = None, month: str = None) -> dict:
    """
    Run coverage gate - Stage 0 (PROD V1: ML + SAP only).
    """
    if year is None:
        year = datetime.now().strftime('%Y')
    if month is None:
        month = datetime.now().strftime('%m')
    
    output_dir = ROOT_DIR / '00_Config'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    period_id = f'{year}{month.zfill(2)}'
    coverage = scan_period_coverage(year, month)
    
    coverage_report = {
        'generated_at': datetime.now().isoformat(),
        'period': coverage['period'],
        'period_id': period_id,
        'status': coverage['status'],
        'ml': coverage['ml'],
        'sap': coverage['sap'],
        'version': 'PROD_V1'
    }
    
    with open(output_dir / f'coverage_report_{period_id}.json', 'w', encoding='utf-8') as f:
        json.dump(coverage_report, f, indent=2, ensure_ascii=False)
    
    health_status = {
        'status': coverage['status'],
        'stage': 'COVERAGE_GATE',
        'timestamp': datetime.now().isoformat(),
        'period': coverage['period'],
        'version': 'PROD_V1',
        'message': 'ML and SAP data present - proceeding to reconciliation' if coverage['status'] == 'OK' else 'Missing required data files',
        'ml_file': coverage['ml']['file_name'],
        'sap_file': coverage['sap']['file_name']
    }
    
    with open(output_dir / f'health_status_{period_id}.json', 'w', encoding='utf-8') as f:
        json.dump(health_status, f, indent=2, ensure_ascii=False)
    
    return coverage


def should_continue_pipeline(year: str = None, month: str = None) -> bool:
    """Check if pipeline should continue based on coverage gate."""
    coverage = run_coverage_gate(year, month)
    return coverage['status'] == 'OK'


def get_period_id(year: str = None, month: str = None) -> str:
    """Get period ID string (YYYYMM)."""
    if year is None:
        year = datetime.now().strftime('%Y')
    if month is None:
        month = datetime.now().strftime('%m')
    return f'{year}{month.zfill(2)}'
