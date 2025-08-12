import pyautogui
import time
import sys
import subprocess
import os
import re

def get_clipboard_content():
    """
    Get clipboard content using multiple methods for better Linux compatibility.
    """
    methods = [
        # Method 1: Try pyperclip first
        lambda: __import__('pyperclip').paste(),
        
        # Method 2: Use xclip (common on Linux)
        lambda: subprocess.check_output(['xclip', '-selection', 'clipboard', '-o'], 
                                      universal_newlines=True),
        
        # Method 3: Use xsel (alternative to xclip)
        lambda: subprocess.check_output(['xsel', '--clipboard', '--output'], 
                                      universal_newlines=True),
        
        # Method 4: Use wl-paste (for Wayland)
        lambda: subprocess.check_output(['wl-paste'], universal_newlines=True),
        
        # Method 5: Use pbpaste (for macOS)
        lambda: subprocess.check_output(['pbpaste'], universal_newlines=True),
    ]
    
    for i, method in enumerate(methods):
        try:
            content = method()
            if content:
                if i > 0:  # If not pyperclip
                    print(f"Using clipboard method: {['pyperclip', 'xclip', 'xsel', 'wl-paste', 'pbpaste'][i]}")
                return content
        except (ImportError, subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    return None

def safe_type_text(text, typing_speed='medium'):
    """
    Type text with enhanced reliability for code and special characters.
    """
    # Speed settings
    speeds = {
        'slow': 0.05,      # 50ms between characters - most reliable
        'medium': 0.02,    # 20ms between characters - good balance
        'fast': 0.01,      # 10ms between characters - faster but less reliable
        'instant': 0       # No delay - fastest but may have errors
    }
    
    interval = speeds.get(typing_speed, 0.02)
    
    # Split text into chunks for better handling
    lines = text.split('\n')
    total_lines = len(lines)
    
    print(f"Typing {len(text)} characters across {total_lines} lines...")
    
    try:
        for line_num, line in enumerate(lines, 1):
            if line_num > 1:
                # Press Enter for new line instead of typing \n
                pyautogui.press('enter')
                time.sleep(interval * 2)  # Extra pause after Enter
            
            if line.strip():  # Only type non-empty lines
                # Type the line character by character for reliability
                for char in line:
                    # Handle special characters that might cause issues
                    if char in ['{', '}', '[', ']', '(', ')', ';', ':', '"', "'", '\\']:
                        # Add extra small delay for special programming characters
                        time.sleep(interval * 1.5)
                    
                    pyautogui.write(char)
                    time.sleep(interval)
            
            # Show progress for long texts
            if total_lines > 10 and line_num % 5 == 0:
                print(f"Progress: {line_num}/{total_lines} lines typed")
        
        print("Typing completed successfully!")
        
    except Exception as e:
        print(f"Error during typing at line {line_num}: {e}")
        print("You can move mouse to top-left corner to stop typing.")

def verify_typing_environment():
    """
    Check if the typing environment is suitable.
    """
    print("\n=== Pre-flight Check ===")
    print("1. Make sure you have a text editor or input field ready")
    print("2. Position your cursor where you want to start typing")
    print("3. Ensure no caps lock or special input modes are active")
    print("4. Close any applications that might interfere (like clipboard managers)")
    
    ready = input("\nIs your typing environment ready? (y/n): ").lower()
    return ready.startswith('y')

def choose_typing_speed():
    """
    Let user choose typing speed based on their needs.
    """
    print("\n=== Choose Typing Speed ===")
    print("1. Slow (50ms/char) - Most reliable, best for complex code")
    print("2. Medium (20ms/char) - Good balance (recommended)")
    print("3. Fast (10ms/char) - Faster but may have occasional errors")
    print("4. Instant (0ms/char) - Fastest but error-prone")
    
    choice = input("Choose speed (1-4, default=2): ").strip()
    
    speed_map = {
        '1': 'slow',
        '2': 'medium', 
        '3': 'fast',
        '4': 'instant',
        '': 'medium'  # default
    }
    
    return speed_map.get(choice, 'medium')

def autotype_clipboard():
    """
    Enhanced auto-typing with better reliability for code.
    """
    print("=== Enhanced Auto-Type Mode ===")
    
    # Get clipboard content
    clipboard_text = get_clipboard_content()
    
    if not clipboard_text:
        print("No text found in clipboard!")
        install_clipboard_tools()
        return
    
    # Show preview
    print(f"\nClipboard contains {len(clipboard_text)} characters, {len(clipboard_text.splitlines())} lines")
    print("Preview (first 100 characters):")
    print("-" * 50)
    print(repr(clipboard_text[:100]))
    if len(clipboard_text) > 100:
        print("...")
    print("-" * 50)
    
    # Verify environment
    if not verify_typing_environment():
        print("Setup your environment first, then try again.")
        return
    
    # Choose typing speed
    speed = choose_typing_speed()
    
    # Final countdown
    print(f"\nStarting in 5 seconds with '{speed}' speed...")
    print("Move mouse to top-left corner anytime to emergency stop!")
    
    for i in range(5, 0, -1):
        print(f"Starting in {i} seconds...", end='\r')
        time.sleep(1)
    
    print("\nTyping now!                     ")
    
    # Start typing with enhanced reliability
    safe_type_text(clipboard_text, speed)

def preview_clipboard():
    """
    Preview clipboard content with detailed analysis.
    """
    try:
        clipboard_text = get_clipboard_content()
        
        if not clipboard_text:
            print("No text found in clipboard!")
            return
        
        print("\n=== Detailed Clipboard Analysis ===")
        print(f"Total characters: {len(clipboard_text)}")
        print(f"Total lines: {len(clipboard_text.splitlines())}")
        print(f"Non-empty lines: {len([line for line in clipboard_text.splitlines() if line.strip()])}")
        
        # Check for potentially problematic characters
        problematic = []
        for char in clipboard_text:
            if ord(char) > 127:  # Non-ASCII
                if char not in problematic:
                    problematic.append(char)
        
        if problematic:
            print(f"Non-ASCII characters found: {problematic[:10]}")  # Show first 10
            print("These might cause typing issues on some systems.")
        
        # Show content
        print("\nContent preview:")
        print("=" * 60)
        lines = clipboard_text.splitlines()
        for i, line in enumerate(lines[:20], 1):  # Show first 20 lines
            print(f"{i:2d}: {line}")
        
        if len(lines) > 20:
            print(f"... and {len(lines) - 20} more lines")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error previewing clipboard: {e}")

def install_clipboard_tools():
    """
    Provide instructions for installing clipboard tools on Linux.
    """
    print("\n=== Clipboard Tool Installation ===")
    print("It looks like you need to install clipboard tools. Try one of these:")
    print("\nFor Ubuntu/Debian:")
    print("  sudo apt-get install xclip")
    print("  # OR")
    print("  sudo apt-get install xsel")
    print("\nFor Fedora/RHEL:")
    print("  sudo dnf install xclip")
    print("  # OR") 
    print("  sudo dnf install xsel")
    print("\nFor Arch Linux:")
    print("  sudo pacman -S xclip")
    print("  # OR")
    print("  sudo pacman -S xsel")
    print("\nFor Wayland users:")
    print("  sudo apt-get install wl-clipboard  # Ubuntu/Debian")
    print("  sudo dnf install wl-clipboard      # Fedora")
    print("  sudo pacman -S wl-clipboard        # Arch")

def main():
    print("=== Enhanced Auto-Type Script for Code ===")
    print("Specially designed for reliable code typing!")
    print("Press Ctrl+C to cancel at any time.\n")
    
    try:
        while True:
            print("\nOptions:")
            print("1. Auto-type clipboard (Enhanced for code)")
            print("2. Preview clipboard content")
            print("3. Test typing (type 'Hello World!')")
            print("4. Exit")
            
            choice = input("\nChoose option (1-4): ").strip()
            
            if choice == '1':
                autotype_clipboard()
            elif choice == '2':
                preview_clipboard()
            elif choice == '3':
                test_typing()
            elif choice == '4':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
            
            print("-" * 60)
            
    except KeyboardInterrupt:
        print("\nScript terminated by user.")
        sys.exit(0)

def test_typing():
    """
    Test the typing functionality with a simple message.
    """
    print("Testing typing functionality...")
    print("Position your cursor and press Enter when ready.")
    input()
    
    print("Typing test message in 3 seconds...")
    for i in range(3, 0, -1):
        print(f"{i}...", end=' ')
        time.sleep(1)
    print("\nTyping now!")
    
    test_text = "Hello World! This is a typing test.\n// Testing special characters: {}[]();\"'\nTest complete!"
    safe_type_text(test_text, 'medium')

if __name__ == "__main__":
    # Check if pyautogui is available
    try:
        import pyautogui
    except ImportError as e:
        print(f"Required module not found: {e}")
        print("Install pyautogui with: pip install pyautogui")
        sys.exit(1)
    
    # Enhanced safety settings for code typing
    pyautogui.FAILSAFE = True  # Move mouse to top-left corner to abort
    pyautogui.PAUSE = 0  # We'll handle pauses manually for better control
    
    main()


    