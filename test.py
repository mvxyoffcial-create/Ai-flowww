#!/usr/bin/env python3
"""
Test script for AI Flow Video Generator
Run this to verify everything works before deploying
"""

import sys
import os

def test_imports():
    """Test if all required packages are installed"""
    print("🔍 Testing imports...")
    
    required_packages = [
        ('flask', 'Flask'),
        ('flask_cors', 'Flask-CORS'),
        ('PIL', 'Pillow'),
        ('cv2', 'OpenCV'),
        ('numpy', 'NumPy'),
    ]
    
    missing = []
    for module, name in required_packages:
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} - Not installed")
            missing.append(name)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("\nInstall with:")
        print("  pip install -r requirements-lite.txt")
        return False
    
    print("\n✅ All packages installed!\n")
    return True

def test_files():
    """Test if all required files exist"""
    print("📁 Testing file structure...")
    
    required_files = [
        'app_lite.py',
        'requirements-lite.txt',
        'Dockerfile.lite',
        'templates/index.html',
        'README.md',
        'DEPLOYMENT.md'
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - Missing")
            missing.append(file)
    
    if missing:
        print(f"\n❌ Missing files: {', '.join(missing)}")
        return False
    
    print("\n✅ All files present!\n")
    return True

def test_flask_app():
    """Test if Flask app can be initialized"""
    print("🌐 Testing Flask app initialization...")
    
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Try importing the lite version
        import app_lite
        print("  ✅ App imported successfully")
        
        # Test Flask app creation
        app = app_lite.app
        print("  ✅ Flask app created")
        
        # Test routes exist
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        expected_routes = ['/', '/generate', '/health']
        
        for route in expected_routes:
            if route in routes:
                print(f"  ✅ Route {route} exists")
            else:
                print(f"  ❌ Route {route} missing")
                return False
        
        print("\n✅ Flask app working!\n")
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_opencv():
    """Test OpenCV functionality"""
    print("🎨 Testing OpenCV...")
    
    try:
        import cv2
        import numpy as np
        from PIL import Image
        
        # Create test images
        img1 = np.zeros((512, 512, 3), dtype=np.uint8)
        img1[:, :] = (255, 0, 0)  # Red
        
        img2 = np.zeros((512, 512, 3), dtype=np.uint8)
        img2[:, :] = (0, 0, 255)  # Blue
        
        # Test blending
        blended = cv2.addWeighted(img1, 0.5, img2, 0.5, 0)
        print("  ✅ Image blending works")
        
        # Test conversion
        pil_img = Image.fromarray(blended)
        print("  ✅ PIL conversion works")
        
        print("\n✅ OpenCV working!\n")
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def run_quick_test():
    """Run a quick functional test"""
    print("🚀 Running quick functional test...")
    
    try:
        import numpy as np
        from PIL import Image
        import app_lite
        
        # Create test images
        img1 = Image.new('RGB', (512, 512), color='red')
        img2 = Image.new('RGB', (512, 512), color='blue')
        
        # Test interpolation
        frames = app_lite.interpolate_frames_smooth(img1, img2, num_frames=4)
        
        if len(frames) == 4:
            print(f"  ✅ Generated {len(frames)} frames")
        else:
            print(f"  ❌ Expected 4 frames, got {len(frames)}")
            return False
        
        print("\n✅ Functional test passed!\n")
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("🧪 AI Flow Video Generator - Test Suite")
    print("=" * 50)
    print()
    
    tests = [
        ("Package Imports", test_imports),
        ("File Structure", test_files),
        ("Flask App", test_flask_app),
        ("OpenCV", test_opencv),
        ("Quick Functional Test", run_quick_test),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} failed with error: {e}\n")
            results.append((name, False))
    
    # Summary
    print("=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 50)
    
    if passed == total:
        print("\n🎉 All tests passed! Ready to deploy!")
        print("\nNext steps:")
        print("1. Push to GitHub: git push origin main")
        print("2. Deploy to Koyeb (see DEPLOYMENT.md)")
        print("3. Or run locally: python app_lite.py")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix issues before deploying.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
