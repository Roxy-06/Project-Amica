import speedtest
import threading
import time

def test_wifi_speed():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000      # Convert to Mbps
        ping = st.results.ping

        print(f"Download Speed: {download_speed:.2f} Mbps")
        print(f"Upload Speed: {upload_speed:.2f} Mbps")
        print(f"Ping: {ping:.2f} ms")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    threading.Thread(target=test_wifi_speed,daemon=True).start()
    i=0
    while True:
        i+=1
        print(i)
        time.sleep(1)
    


