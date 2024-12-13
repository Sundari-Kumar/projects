import time
from security_system import SecuritySystem

def main():
    system = SecuritySystem()

    try:
        while True:
            print("\nMonitoring for Intruders...")
            system.detect_intruder()  # Detect intruders at random intervals
            time.sleep(5)  # Wait for 5 seconds before checking again

            # Optionally, show logs every 10 seconds
            if time.time() % 10 == 0:
                print("\nIntruder Detection Logs:")
                system.check_logs()

    except KeyboardInterrupt:
        print("\nSecurity System Shutting Down.")
    finally:
        system.close()

if __name__ == "__main__":
    main()
