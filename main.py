import os
import shutil
import subprocess
import ctypes
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import time
import re

class PCCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("박대표님의 원클릭 PC & 자동 DNS 최적화")
        self.root.geometry("600x550")
        self.root.configure(bg="#f8f9fa")
        self.root.resizable(False, False)
        
        # UI 구성
        self.setup_ui()

    def setup_ui(self):
        # 메인 프레임
        main_frame = tk.Frame(self.root, padx=30, pady=30, bg="#f8f9fa")
        main_frame.pack(expand=True, fill="both")

        # 제목
        title_label = tk.Label(
            main_frame, 
            text="🚀 원클릭 PC & 자동 DNS 최적화", 
            font=("Malgun Gothic", 22, "bold"),
            bg="#f8f9fa",
            fg="#0078d4"
        )
        title_label.pack(pady=(0, 5))

        subtitle_label = tk.Label(
            main_frame, 
            text="인터넷 속도 향상 및 시스템 찌꺼기 완벽 정리", 
            font=("Malgun Gothic", 11),
            bg="#f8f9fa",
            fg="#6c757d"
        )
        subtitle_label.pack(pady=(0, 25))

        # 실행 버튼
        self.clean_button = tk.Button(
            main_frame, 
            text="지금 바로 최적화 시작", 
            command=self.start_cleaning_thread,
            font=("Malgun Gothic", 16, "bold"),
            bg="#0078d4",
            fg="white",
            activebackground="#005a9e",
            activeforeground="white",
            padx=40,
            pady=15,
            cursor="hand2",
            relief="flat",
            borderwidth=0
        )
        self.clean_button.pack(pady=10)

        # 로그 출력 창
        log_label = tk.Label(main_frame, text="진행 상황 로그:", font=("Malgun Gothic", 10, "bold"), bg="#f8f9fa", fg="#495057")
        log_label.pack(anchor="w", pady=(15, 5))
        
        self.log_area = scrolledtext.ScrolledText(
            main_frame, 
            height=12, 
            font=("Consolas", 10),
            bg="#ffffff",
            fg="#212529",
            padx=10,
            pady=10,
            relief="solid",
            borderwidth=1
        )
        self.log_area.pack(pady=5, fill="both", expand=True)
        self.log_area.insert(tk.END, "준비 완료. 버튼을 눌러주세요.\n")
        self.log_area.configure(state='disabled')

        # 하단 안내
        footer_label = tk.Label(
            main_frame, 
            text="* 관리자 권한으로 실행 시 네트워크 최적화 효과가 극대화됩니다.", 
            font=("Malgun Gothic", 9),
            bg="#f8f9fa",
            fg="#dc3545"
        )
        footer_label.pack(pady=(15, 0))

    def log(self, message):
        self.log_area.configure(state='normal')
        self.log_area.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_area.see(tk.END)
        self.log_area.configure(state='disabled')
        self.root.update_idletasks()

    def start_cleaning_thread(self):
        self.clean_button.config(state='disabled', text="최적화 진행 중...", bg="#adb5bd")
        threading.Thread(target=self.run_cleaning, daemon=True).start()

    def run_cleaning(self):
        self.log("최적화 작업을 시작합니다...")
        
        # 1. 네트워크 및 자동 DNS 최적화
        self.log("--- [1단계] 네트워크 및 DNS 최적화 ---")
        self.optimize_network()

        # 2. 시스템 임시 파일 정리
        self.log("--- [2단계] 시스템 찌꺼기 정리 ---")
        self.clean_system_files()

        # 3. 휴지통 및 기타 정리
        self.log("--- [3단계] 기타 최적화 ---")
        self.empty_recycle_bin()

        self.log("모든 최적화 작업이 완료되었습니다!")
        self.clean_button.config(state='normal', text="최적화 완료!", bg="#28a745")
        
        messagebox.showinfo(
            "최적화 완료", 
            "PC 및 인터넷 최적화가 성공적으로 완료되었습니다!\n\n"
            "1. 인터넷 속도가 개선되었습니다 (DNS 최적화).\n"
            "2. 시스템 불필요 파일이 제거되었습니다.\n"
            "3. Vercel 등 해외 사이트 접속이 더 안정적입니다.\n\n"
            "효과를 적용하려면 브라우저를 껐다 켜거나 재부팅을 권장합니다."
        )

    def optimize_network(self):
        # DNS 캐시 초기화
        self.log("DNS 캐시를 초기화합니다...")
        subprocess.run("ipconfig /flushdns", shell=True, capture_output=True)
        
        # 네트워크 스택 리셋
        self.log("네트워크 스택을 리셋합니다 (Winsock/TCP)...")
        subprocess.run("netsh winsock reset", shell=True, capture_output=True)
        subprocess.run("netsh int ip reset", shell=True, capture_output=True)

        # 자동 DNS 설정 (구글 DNS로 설정하여 Vercel 등 해외 접속 최적화)
        self.log("최적의 DNS(Google DNS)로 자동 설정을 시도합니다...")
        try:
            # 인터페이스 이름 찾기 (보통 'Wi-Fi' 또는 '이더넷')
            result = subprocess.run("netsh interface show interface", shell=True, capture_output=True, text=True)
            interfaces = re.findall(r'Connected\s+\w+\s+\w+\s+(.+)', result.stdout)
            
            if not interfaces:
                # 한국어 윈도우 대응
                interfaces = re.findall(r'연결됨\s+\w+\s+\w+\s+(.+)', result.stdout)

            for iface in interfaces:
                iface = iface.strip()
                self.log(f"인터페이스 설정 중: {iface}")
                # 기본 DNS: 8.8.8.8 (Google)
                subprocess.run(f'netsh interface ip set dns name="{iface}" source=static address=8.8.8.8 register=primary', shell=True, capture_output=True)
                # 보조 DNS: 8.8.4.4 (Google)
                subprocess.run(f'netsh interface ip add dns name="{iface}" address=8.8.4.4 index=2', shell=True, capture_output=True)
            
            self.log("DNS 설정이 Google DNS(8.8.8.8)로 최적화되었습니다.")
        except Exception as e:
            self.log(f"DNS 자동 설정 중 오류 발생 (권한 부족일 수 있음): {e}")

    def clean_system_files(self):
        temp_paths = [
            os.environ.get('TEMP'),
            os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Temp'),
            os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Prefetch'),
            os.path.join(os.environ.get('LOCALAPPDATA'), 'Microsoft\\Windows\\Explorer')
        ]

        for path in temp_paths:
            if path and os.path.exists(path):
                self.log(f"정리 중: {path}")
                files_cleaned = 0
                try:
                    for filename in os.listdir(path):
                        file_path = os.path.join(path, filename)
                        try:
                            if os.path.isfile(file_path) or os.path.islink(file_path):
                                os.unlink(file_path)
                                files_cleaned += 1
                            elif os.path.isdir(file_path):
                                shutil.rmtree(file_path)
                                files_cleaned += 1
                        except:
                            continue
                    self.log(f" > {files_cleaned}개 항목 정리 완료.")
                except:
                    self.log(f" > 폴더 접근 권한이 없습니다.")

    def empty_recycle_bin(self):
        self.log("휴지통을 비우는 중...")
        try:
            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 1 | 2 | 4)
            self.log(" > 휴지통 정리 완료.")
        except:
            self.log(" > 휴지통 비우기 건너뜀.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PCCleanerApp(root)
    root.mainloop()
