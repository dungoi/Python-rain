import os
import time
import random
import sys 

# --- Cấu hình Mưa trên Terminal ---
# Cố gắng tự động lấy kích thước terminal, mặc định là 80x25 nếu không lấy được
try:
    RONG, CAO = os.get_terminal_size()
except OSError:
    RONG = 100
    CAO = 50
SO_LUONG_HAT_MUA = 90 # Điều chỉnh mật độ mưa tại đây (tăng số này để mưa dày hơn)
# Tốc độ khung hình (sps) là 0.0005s, tương đương 2000 FPS (giá trị rất cao)
TOC_DO_KHUNG_HINH = 0.0005 # Đã đặt theo yêu cầu

# --- Cấu hình Tốc độ Rơi (Đã chuyển sang Float) ---
TOC_DO_ROI_MUA_LON = 0.0600 # Tốc độ rơi hạt lớn
TOC_DO_ROI_MUA_NHO = 0.0600  # Tốc độ rơi hạt nhỏ

# --- Cấu hình Màu sắc (Sử dụng RGB) ---
# Format: (R, G, B) với giá trị từ 0 đến 255
# Bạn đã chọn: (225, 0, 225) - Màu Magenta/Tím
MAU_MUA_LON_RGB = (0,100,150) 
# Bạn đã chọn: (0, 255, 0) - Màu Xanh lá cây
MAU_MUA_NHO_RGB = (200,200,200) 

# Hàm chuyển đổi RGB sang mã ANSI 24-bit True Color
def tao_mau_rgb(r, g, b):
    """Tạo chuỗi mã màu ANSI 24-bit (Foreground) cho màu RGB."""
    # Định dạng chuẩn True Color: \033[38;2;<r>;<g>;<b>m
    return f"\033[38;2;{r};{g};{b}m"

# Tạo mã màu ANSI True Color cho hạt mưa từ giá trị RGB
ANSI_MAU_MUA_LON = tao_mau_rgb(*MAU_MUA_LON_RGB)
ANSI_MAU_MUA_NHO = tao_mau_rgb(*MAU_MUA_NHO_RGB)
ANSI_RESET = "\033[0m"

# Mã ANSI để ẩn/hiện con trỏ và xóa màn hình
ANSI_AN_CON_TRO = "\033[?25l" 
ANSI_HIEN_CON_TRO = "\033[?25h" 
ANSI_XOA_MAN_HINH = "\033[2J"  # Xóa toàn bộ màn hình
ANSI_VE_GO_HOME = "\033[H"     # Đưa con trỏ về vị trí (1, 1)

# --- Định nghĩa Hạt Mưa ---
class HatMua:
    """Đại diện cho một hạt mưa trên Terminal."""
    def __init__(self):
        # Tỉ lệ hạt dài : hạt ngắn là 1:1 theo yêu cầu
        self.la_hat_lon = random.choice([True, False]) 

        if self.la_hat_lon:
            self.ky_tu = '|'
            self.toc_do = TOC_DO_ROI_MUA_LON 
            self.mau_sac_ansi = ANSI_MAU_MUA_LON
        else:
            self.ky_tu = '.'
            self.toc_do = TOC_DO_ROI_MUA_NHO
            self.mau_sac_ansi = ANSI_MAU_MUA_NHO

        # Vị trí ban đầu (sử dụng float)
        self.x = random.randint(0, RONG - 1)
        self.y = random.uniform(-CAO * 3, 0) # Bắt đầu từ trên cao hơn

    def cap_nhat(self):
        """Cập nhật vị trí của hạt mưa (dùng float)."""
        # Thêm một chút ngẫu nhiên để trông tự nhiên hơn
        self.y += self.toc_do * random.uniform(0.9, 1.1) 

        # Nếu hạt mưa ra khỏi màn hình, đưa nó trở lại đỉnh
        if self.y >= CAO:
            self.y = random.uniform(-CAO * 2, 0)
            self.x = random.randint(0, RONG - 1)
            # Tái tạo lại để có thể thay đổi kích thước/tốc độ ngẫu nhiên
            self.__init__()

# --- Chức năng ẩn/hiện con trỏ và xóa màn hình bằng ANSI ---

def an_con_tro():
    """Ẩn con trỏ Terminal."""
    sys.stdout.write(ANSI_AN_CON_TRO)
    sys.stdout.flush()

def hien_con_tro():
    """Hiện con trỏ Terminal."""
    sys.stdout.write(ANSI_HIEN_CON_TRO)
    sys.stdout.flush()

def chuan_bi_khung_hinh():
    """Đưa con trỏ về góc trên cùng và xóa màn hình."""
    # Kết hợp ANSI_XOA_MAN_HINH và ANSI_VE_GO_HOME để đảm bảo sạch và ổn định
    sys.stdout.write(ANSI_XOA_MAN_HINH + ANSI_VE_GO_HOME)

# --- Chức năng chính ---

def main():
    """Chạy mô phỏng mưa trên Terminal."""
    
    danh_sach_hat_mua = [HatMua() for _ in range(SO_LUONG_HAT_MUA)]

    an_con_tro()

    print(f"Python-rain . FPS: {1/TOC_DO_KHUNG_HINH:.0f}. Size: {RONG}x{CAO}. Ctrl+C to exit.")
    time.sleep(1)
    
    try:
        while True:
            # 1. Cập nhật vị trí của tất cả hạt mưa
            for hat in danh_sach_hat_mua:
                hat.cap_nhat()

            # 2. Xóa và chuẩn bị khung hình (Sử dụng ANSI thay vì os.system)
            chuan_bi_khung_hinh()

            # 3. Tạo khung hình (Grid/Buffer)
            khung_hinh = [[' ' for _ in range(RONG)] for _ in range(CAO)]

            # Đặt các hạt mưa vào khung hình
            for hat in danh_sach_hat_mua:
                y_ve = int(hat.y) 

                if 0 <= y_ve < CAO and 0 <= hat.x < RONG:
                    # Gán màu và ký tự vào vị trí vẽ
                    khung_hinh[y_ve][hat.x] = f"{hat.mau_sac_ansi}{hat.ky_tu}{ANSI_RESET}"

            # 4. In khung hình ra Terminal
            # Không sử dụng print() để tránh in xuống dòng thừa. Sử dụng sys.stdout.write()
            output = "\n".join(["".join(hang) for hang in khung_hinh])
            sys.stdout.write(output)
            sys.stdout.flush()

            # 5. Chờ (tạo hiệu ứng chuyển động)
            time.sleep(TOC_DO_KHUNG_HINH)

    except KeyboardInterrupt:
        pass 

    finally:
        hien_con_tro()
        # Đảm bảo terminal được làm sạch khi kết thúc
        os.system('cls' if os.name == 'nt' else 'clear') 
        print("\n\n Exit python-rain.")

if __name__ == "__main__":
    main()

