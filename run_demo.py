#!/usr/bin/env python3
"""
Main demo runner - Easy way to run the AI Racing Simulator
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Main demo menu"""
    print("🏎️  AI RACING SIMULATOR")
    print("=" * 40)
    print("Select a demo to run:")
    print()
    print("1. Quick Race Example")
    print("2. Custom Championship")
    print("3. Telemetry Analysis")
    print("4. Complete System Showcase")
    print("5. Grand Prix Finale")
    print("6. Run All Tests")
    print()
    
    choice = input("Enter your choice (1-6): ").strip()
    
    if choice == "1":
        os.system("python examples/quick_race.py")
    elif choice == "2":
        os.system("python examples/custom_championship.py")
    elif choice == "3":
        os.system("python examples/telemetry_analysis.py")
    elif choice == "4":
        from visualization.showcase_finale import main as showcase_main
        showcase_main()
    elif choice == "5":
        from visualization.grand_prix_finale import main as finale_main
        finale_main()
    elif choice == "6":
        run_all_tests()
    else:
        print("Invalid choice. Please select 1-6.")

def run_all_tests():
    """Run all test files"""
    print("🧪 Running all tests...")
    
    test_files = [
        "tests/test_racing.py",
        "tests/test_telemetry.py", 
        "tests/test_challenges.py",
        "tests/test_data_prizes.py",
        "tests/test_intelligence.py",
        "tests/test_personalities.py",
        "tests/test_config.py"
    ]
    
    for test_file in test_files:
        print(f"\n🔍 Running {test_file}...")
        try:
            os.system(f"python {test_file}")
            print(f"✅ {test_file} completed")
        except Exception as e:
            print(f"❌ {test_file} failed: {e}")
    
    print("\n🏁 All tests completed!")

if __name__ == "__main__":
    main()