#!/usr/bin/env python3
"""
KHAWRIZM CLI - Command-line interface for Sovereign AI Security
Version: 0.4.0
Usage: khawrizm <command> [options]
"""

import sys
import argparse
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from security.ipi_detector import scan_for_ipi
from security.dlp_guardian import DLPGuardian
from security.zero_trust_ai import validate_zero_trust
from security.cst_compliance import CSTValidator
from src.sarc_processor import process_arabic_intent_advanced
from src.tools import verify_sovereignty


def print_banner():
    """Print ASCII banner"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ██╗  ██╗██╗  ██╗ █████╗ ██╗    ██╗██████╗ ██╗███████╗ ║
║   ██║ ██╔╝██║  ██║██╔══██╗██║    ██║██╔══██╗██║╚══███╔╝ ║
║   █████╔╝ ███████║███████║██║ █╗ ██║██████╔╝██║  ███╔╝  ║
║   ██╔═██╗ ██╔══██║██╔══██║██║███╗██║██╔══██╗██║ ███╔╝   ║
║   ██║  ██╗██║  ██║██║  ██║╚███╔███╔╝██║  ██║██║███████╗ ║
║   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝╚══════╝ ║
║                                                           ║
║           Sovereign AI Security Framework                 ║
║                    v0.4.0                                 ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)


def cmd_scan_ipi(args):
    """Scan text for Indirect Prompt Injection"""
    print("🔍 Scanning for Indirect Prompt Injection...")
    
    # Read input
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = args.text
    
    # Scan
    result = scan_for_ipi(text, strict=args.strict)
    
    # Output
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"\n{'='*60}")
        print(f"🛡️  Threat Level: {result['threat_level'].upper()}")
        print(f"✅ Safe: {result['is_safe']}")
        print(f"📊 Confidence: {result['confidence']:.2%}")
        print(f"{'='*60}\n")
        
        if result['detected_patterns']:
            print("⚠️  Detected Threats:")
            for pattern in result['detected_patterns']:
                print(f"  • {pattern}")
            print()
        
        if result['recommendations']:
            print("💡 Recommendations:")
            for rec in result['recommendations']:
                print(f"  {rec}")
            print()
    
    return 0 if result['is_safe'] else 1


def cmd_scan_pii(args):
    """Scan for Saudi PII (Iqama, National ID)"""
    print("🔍 Scanning for Saudi Personal Identifiable Information...")
    
    # Read input
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = args.text
    
    # Scan
    dlp = DLPGuardian()
    result = dlp.scan(text)
    
    # Output
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"\n{'='*60}")
        print(f"🛡️  PII Found: {result['has_pii']}")
        print(f"📊 Iqama Numbers: {result['iqama_count']}")
        print(f"📊 National IDs: {result['national_id_count']}")
        print(f"📊 Total PII: {result['total_pii']}")
        print(f"{'='*60}\n")
        
        if args.mask and result['has_pii']:
            masked = dlp.mask(text)
            print("🔒 Masked Output:")
            print(masked)
            print()
    
    return 0 if not result['has_pii'] else 1


def cmd_validate_zero_trust(args):
    """Validate Zero Trust access decision"""
    print("🔍 Validating Zero Trust Access...")
    
    result = validate_zero_trust(
        user_id=args.user,
        prompt=args.prompt,
        data_class=args.data_class,
        action=args.action,
        device_posture=args.device_posture
    )
    
    # Output
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"\n{'='*60}")
        print(f"🛡️  Decision: {result['decision'].upper()}")
        print(f"⚠️  Risk Score: {result['risk_score']:.2%}")
        print(f"✅ Allowed: {result['allowed']}")
        print(f"🔐 MFA Required: {result['requires_mfa']}")
        print(f"{'='*60}\n")
    
    return 0 if result['allowed'] else 1


def cmd_check_compliance(args):
    """Check Saudi CST Class C compliance"""
    print("🔍 Checking CST Class C Compliance...")
    
    # Read config
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    else:
        config = {
            "region": args.region,
            "encryption_at_rest": args.encryption,
            "cross_border_transfer": args.cross_border
        }
    
    # Validate
    validator = CSTValidator()
    result = validator.validate(config)
    
    # Output
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"\n{'='*60}")
        print(f"✅ Compliant: {result['is_compliant']}")
        print(f"📊 Compliance Score: {result['compliance_score']:.2%}")
        print(f"{'='*60}\n")
        
        if result['violations']:
            print("❌ Violations:")
            for violation in result['violations']:
                print(f"  • {violation}")
            print()
    
    return 0 if result['is_compliant'] else 1


def cmd_extract_intent(args):
    """Extract Arabic intent using SARC"""
    print("🔍 Extracting Arabic Intent (SARC)...")
    
    # Read input
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = args.text
    
    # Process
    result = process_arabic_intent_advanced(text)
    
    # Output
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"\n{'='*60}")
        print(f"📊 Confidence: {result['confidence']:.2%}")
        print(f"📊 Match Rate: {result['match_rate']:.2%}")
        print(f"{'='*60}\n")
        
        if result['roots']:
            print("🌳 Extracted Roots:")
            for i, root in enumerate(result['roots']):
                pred = result['predicates'][i] if i < len(result['predicates']) else "N/A"
                print(f"  • {root} → {pred}")
            print()
        
        if result['entities']:
            print("🎯 Entities:")
            for entity in result['entities']:
                print(f"  • {entity}")
            print()
    
    return 0


def cmd_check_sovereignty(args):
    """Verify zero Big Tech dependencies"""
    print("🔍 Checking Sovereignty (Big Tech Dependencies)...")
    
    directory = args.directory or "."
    result = verify_sovereignty(directory)
    
    # Output
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"\n{'='*60}")
        print(f"✅ Is Sovereign: {result['is_sovereign']}")
        print(f"📊 Files Scanned: {result['files_scanned']}")
        print(f"{'='*60}\n")
        
        if result['violations']:
            print("❌ Big Tech Dependencies Found:")
            for violation in result['violations']:
                print(f"  • {violation}")
            print()
    
    return 0 if result['is_sovereign'] else 1


def cmd_interactive(args):
    """Interactive mode - security shell"""
    print_banner()
    print("\n🚀 Welcome to KHAWRIZM Interactive Shell")
    print("Type 'help' for available commands, 'exit' to quit.\n")
    
    while True:
        try:
            cmd = input("khawrizm> ").strip()
            
            if not cmd:
                continue
            
            if cmd in ['exit', 'quit', 'q']:
                print("👋 Goodbye!")
                break
            
            if cmd in ['help', 'h', '?']:
                print("""
Available commands:
  scan-ipi <text>        - Scan for prompt injection
  scan-pii <text>        - Scan for Saudi PII
  extract <arabic_text>  - Extract Arabic intent
  help                   - Show this help
  exit                   - Exit shell
                """)
                continue
            
            # Parse command
            parts = cmd.split(maxsplit=1)
            if len(parts) < 2:
                print("❌ Invalid command. Type 'help' for usage.")
                continue
            
            cmd_name, text = parts
            
            if cmd_name == "scan-ipi":
                result = scan_for_ipi(text)
                print(f"Threat: {result['threat_level']}, Safe: {result['is_safe']}")
            
            elif cmd_name == "scan-pii":
                dlp = DLPGuardian()
                result = dlp.scan(text)
                print(f"PII Found: {result['has_pii']}, Total: {result['total_pii']}")
            
            elif cmd_name == "extract":
                result = process_arabic_intent_advanced(text)
                print(f"Roots: {', '.join(result['roots'])}")
                print(f"Predicates: {', '.join(result['predicates'])}")
            
            else:
                print(f"❌ Unknown command: {cmd_name}")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return 0


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="KHAWRIZM - Sovereign AI Security Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  khawrizm scan-ipi -f email.txt --strict
  khawrizm scan-pii "الإقامة: 2456789012" --mask
  khawrizm extract "أريد بناء نظام ذكي"
  khawrizm check-compliance --region ksa-riyadh-1
  khawrizm interactive
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # scan-ipi
    ipi_parser = subparsers.add_parser('scan-ipi', help='Scan for Indirect Prompt Injection')
    ipi_parser.add_argument('-f', '--file', help='Input file path')
    ipi_parser.add_argument('-t', '--text', help='Input text')
    ipi_parser.add_argument('--strict', action='store_true', help='Use strict mode')
    ipi_parser.add_argument('--json', action='store_true', help='JSON output')
    ipi_parser.set_defaults(func=cmd_scan_ipi)
    
    # scan-pii
    pii_parser = subparsers.add_parser('scan-pii', help='Scan for Saudi PII')
    pii_parser.add_argument('-f', '--file', help='Input file path')
    pii_parser.add_argument('-t', '--text', help='Input text')
    pii_parser.add_argument('--mask', action='store_true', help='Mask PII in output')
    pii_parser.add_argument('--json', action='store_true', help='JSON output')
    pii_parser.set_defaults(func=cmd_scan_pii)
    
    # validate-zt
    zt_parser = subparsers.add_parser('validate-zt', help='Validate Zero Trust access')
    zt_parser.add_argument('-u', '--user', required=True, help='User ID')
    zt_parser.add_argument('-p', '--prompt', required=True, help='User prompt')
    zt_parser.add_argument('-d', '--data-class', required=True, help='Data classification')
    zt_parser.add_argument('-a', '--action', required=True, help='Action type')
    zt_parser.add_argument('--device-posture', default='unknown', help='Device posture')
    zt_parser.add_argument('--json', action='store_true', help='JSON output')
    zt_parser.set_defaults(func=cmd_validate_zero_trust)
    
    # check-compliance
    comp_parser = subparsers.add_parser('check-compliance', help='Check CST compliance')
    comp_parser.add_argument('-f', '--file', help='Config file (JSON)')
    comp_parser.add_argument('-r', '--region', help='Cloud region')
    comp_parser.add_argument('-e', '--encryption', action='store_true', help='Encryption at rest')
    comp_parser.add_argument('-c', '--cross-border', action='store_true', help='Cross-border transfer')
    comp_parser.add_argument('--json', action='store_true', help='JSON output')
    comp_parser.set_defaults(func=cmd_check_compliance)
    
    # extract-intent
    extract_parser = subparsers.add_parser('extract', help='Extract Arabic intent (SARC)')
    extract_parser.add_argument('-f', '--file', help='Input file path')
    extract_parser.add_argument('-t', '--text', help='Arabic text')
    extract_parser.add_argument('--json', action='store_true', help='JSON output')
    extract_parser.set_defaults(func=cmd_extract_intent)
    
    # check-sovereignty
    sov_parser = subparsers.add_parser('check-sovereignty', help='Check Big Tech dependencies')
    sov_parser.add_argument('-d', '--directory', help='Directory to scan')
    sov_parser.add_argument('--json', action='store_true', help='JSON output')
    sov_parser.set_defaults(func=cmd_check_sovereignty)
    
    # interactive
    interactive_parser = subparsers.add_parser('interactive', help='Interactive security shell')
    interactive_parser.set_defaults(func=cmd_interactive)
    
    # Parse and execute
    args = parser.parse_args()
    
    if not args.command:
        print_banner()
        parser.print_help()
        return 0
    
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
