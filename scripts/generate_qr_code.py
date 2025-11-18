#!/usr/bin/env python3
"""
Generate QR code for recruiter resume link
"""
try:
    import qrcode
    from PIL import Image
except ImportError:
    print("Installing qrcode and pillow...")
    import subprocess
    try:
        subprocess.run(["pip3", "install", "--user", "qrcode", "pillow"], check=True)
    except:
        subprocess.run(["pip3", "install", "--break-system-packages", "qrcode", "pillow"], check=True)
    import qrcode
    from PIL import Image

def generate_qr_code(url, filename="resume_qr_code.png"):
    """Generate QR code for resume URL."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print(f"✅ QR code saved to {filename}")
    return filename

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        # Try to get from ngrok
        import subprocess
        result = subprocess.run(
            ["curl", "-s", "http://localhost:4040/api/tunnels"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            import json
            try:
                data = json.loads(result.stdout)
                tunnels = data.get('tunnels', [])
                if tunnels:
                    url = tunnels[0].get('public_url', '')
                    if url:
                        url = f"{url}/"
                        print(f"Using ngrok URL: {url}")
                    else:
                        url = input("Enter your resume URL: ")
                else:
                    url = input("Enter your resume URL: ")
            except:
                url = input("Enter your resume URL: ")
        else:
            url = input("Enter your resume URL: ")
    
    generate_qr_code(url)

