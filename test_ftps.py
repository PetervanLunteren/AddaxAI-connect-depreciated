#!/usr/bin/env python3
from ftplib import FTP_TLS
import sys

# FTPS settings from config
FTPS_HOST = "188.166.117.22"
FTPS_PORT = 21
FTPS_USER = "camera"
FTPS_PASS = "03e750417d0ab4ae"
FTPS_REMOTE_DIR = "/opt/addaxai-connect/uploads"

# Test file to upload (change this to your test file)
test_file = sys.argv[1] if len(sys.argv) > 1 else "test.txt"

print(f"Testing FTPS connection to {FTPS_HOST}:{FTPS_PORT}")
print(f"User: {FTPS_USER}")
print(f"Test file: {test_file}")
print("-" * 50)

try:
    # Connect and authenticate
    print("1. Connecting...")
    ftps = FTP_TLS()
    ftps.connect(FTPS_HOST, FTPS_PORT, timeout=30)
    
    print("2. Authenticating...")
    ftps.auth()
    ftps.prot_p()
    
    print("3. Logging in...")
    ftps.login(FTPS_USER, FTPS_PASS)
    
    print("4. Setting passive mode...")
    ftps.set_pasv(True)
    
    # List current directory
    print("5. Current directory:")
    try:
        print(f"   PWD: {ftps.pwd()}")
    except Exception as e:
        print(f"   Could not get PWD: {e}")
    
    # Skip listing files - often restricted
    print("6. Skipping file listing (often restricted)")
    
    # Try to change directory
    print(f"\n7. Trying to change to {FTPS_REMOTE_DIR}...")
    try:
        ftps.cwd(FTPS_REMOTE_DIR)
        print(f"   Success! Now in: {ftps.pwd()}")
    except Exception as e:
        print(f"   Failed: {e}")
        print("   Trying relative path...")
        try:
            ftps.cwd(FTPS_REMOTE_DIR.lstrip('/'))
            print(f"   Success with relative! Now in: {ftps.pwd()}")
        except Exception as e2:
            print(f"   Failed relative too: {e2}")
            print(f"   Staying in: {ftps.pwd()}")
    
    # Upload test file
    print(f"\n8. Uploading {test_file}...")
    try:
        with open(test_file, 'rb') as f:
            result = ftps.storbinary(f'STOR {test_file}', f)
            print(f"   Upload result: {result}")
            print("   SUCCESS - File uploaded!")
    except Exception as e:
        print(f"   Upload failed: {e}")
    
    print("\n9. Closing connection...")
    ftps.quit()
    print("   Done!")
    
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()