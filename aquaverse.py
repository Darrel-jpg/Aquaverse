import time
import os
import art
import random
import pandas as pd
from tabulate import tabulate
from datetime import datetime

# Link video demo
# https://www.youtube.com/watch?v=814mgurPxDg

file_csv_user = 'user.csv'
file_data_produk = 'data produk.csv'
file_keranjang = 'keranjang.csv'
file_riwayat_pembelian = 'riwayat.csv'


def header(text):
    slant = art.text2art(text, font='slant')
    print(slant)

def register():
    while True:
        try:
            with open(file_csv_user, 'r') as file_user:
                lines = file_user.readlines()
                email_ditemukan = False
                while True:
                    email = input('Email (@gmail.com): ')
                    if email[-10:] == '@gmail.com':
                        break
                    else:
                        print('Email harus menggunakan domain @gmail.com, silakan coba lagi')
                for i in lines:
                    data = i.strip().split(',')
                    email_copy = data[2].strip()
                    if email == email_copy:
                        email_ditemukan = True
                if email_ditemukan:
                    print('Email sudah terdaftar, gunakan email lain')
                    continue
                while True:
                    try:
                        phone = int(input('Nomor telepon: '))
                        break
                    except ValueError:
                        print('Nomor telepon harus berupa angka, silakan coba lagi')
                username = input('Username: ')
                username_ditemukan = False
                for i in lines:
                    data = i.strip().split(',')
                    username_copy = data[0].strip()
                    if username == username_copy:
                        username_ditemukan = True
                if username_ditemukan:
                    print('Username sudah digunakan, coba username lain')
                    continue
            while True:
                password = input('Password (minimal 8 karakter dan mengandung angka): ')
                if any(char.isdigit() for char in password) and len(password) >= 8:
                    if username != password:
                        re_password = input('Konfirmasi password: ')
                        if password == re_password:
                            with open(file_csv_user, 'a') as file_user:
                                file_user.write(f'{username},{password},{email},{phone},aktif\n')
                                print('REGISTRASI DIPROSES', end='', flush=True)
                                for i in range(3):
                                    time.sleep(0.5)
                                    print('.', end='', flush=True)
                                print('\nAkun berhasil dibuat! Silakan login untuk melanjutkan')
                                return
                        else:
                            print('Konfirmasi password tidak cocok. Silakan coba lagi')
                    else:
                        print('Password tidak boleh sama dengan username, silakan coba lagi')
                else:
                    print('Password tidak valid, pastikan panjang minimal 8 karakter dan mengandung angka')
        except Exception as e:
            print(f'Terjadi kesalahan: {e}')
            break

def login():
    while True:
        try:
            with open(file_csv_user, 'r') as file_user:
                global username
                username = input('Username: ')
                password = input('Password: ')
                lines = file_user.readlines()
                login_berhasil = False
                username_ditemukan = False
                for i in lines:
                    data = i.strip().split(',')
                    username_copy, password_copy, email, phone, status = data
                    if username == username_copy:
                        username_ditemukan = True
                        if password == password_copy:
                            login_berhasil = True
                            global user_profil
                            user_profil = [username_copy, password_copy, email, phone]
                            break
                if username == 'admin' and password == 'admin000':
                    admin()
                    return
                elif not username_ditemukan:
                    print('Username tidak ditemukan.')
                    pilihan_user = input('Apakah Anda ingin mendaftarkan akun baru? (y/n): ').strip().lower()
                    if pilihan_user == 'y':
                        register()
                        return
                    elif pilihan_user == 'n':
                        print('Silakan coba login kembali')
                        continue
                    else:
                        print('Perintah tidak dikenali. Silakan coba lagi')
                elif login_berhasil:
                    if status == 'aktif':
                        print('LOGIN DIPROSES', end='', flush=True)
                        for i in range(3):
                            time.sleep(0.5)
                            print('.', end='', flush=True)
                        print('\nLogin berhasil!')
                        time.sleep(1)
                        os.system('cls')
                        return
                    elif status == 'blokir':
                        os.system('cls')
                        print('Akun anda telah terblokir')
                        return
                elif not login_berhasil:
                    print('Username atau password salah, Silakan coba lagi')
                    reset_pass = input('Lupa password? (y/n): ').strip().lower()
                    if reset_pass == 'y':
                        reset_password()
                        return
                    elif reset_pass == 'n':
                        continue
                    else:
                        print('Perintah tidak dikenali, silakan coba lagi')
        except Exception as e:
            print(f'Terjadi kesalahan: {e}')
            return

def register_login():
    while True:
        try:
            os.system('cls')
            header(text='AQUAVERSE')
            reg_login = input('Menu:\n[1] Registrasi\n[2] Login\nPilih opsi: ').strip()
            if reg_login.isdigit():
                if reg_login == '1':
                    os.system('cls')
                    header(text='REGISTER\n  PAGE')
                    register()
                    login()
                    break
                elif reg_login == '2':
                    os.system('cls')
                    header(text='LOGIN\nPAGE')
                    login()
                    break
                else:
                    print('Input tidak valid, pilih antara 1 atau 2.')
            else:
                print('Input harus berupa angka')
            time.sleep(1)
        except Exception as e:
            print(f'Terjadi kesalahan: {e}')
            time.sleep(1)
            

def reset_password():
    while True:
        try:
            with open(file_csv_user, 'r') as file_user:
                lines = file_user.readlines()
                email_ditemukan = False
                list_baris = []
                user_email = input('Email: ')
                for i in lines:
                    data = i.strip().split(',')
                    username_copy, password, email, phone, status = data
                    if user_email == email and username_copy == username:
                        email_ditemukan = True
                        try:
                            kode_otp = random.randint(1000, 9999)
                            print(f'Kode OTP: {kode_otp}')
                            while True:
                                try:
                                    input_kode = int(input('Masukkan kode OTP: '))
                                    if input_kode == kode_otp:
                                        new_password = input('Password baru (minimal 8 karakter dan mengandung angka): ')
                                        if any(char.isdigit() for char in new_password) and len(new_password) >= 8:
                                            re_password = input('Konfirmasi password: ')
                                            if new_password == re_password:
                                                list_baris.append(f'{username},{new_password},{email},{phone},{status}\n')
                                                print('Password berhasil diperbarui, silahkan login')
                                                break
                                            else:
                                                print('Konfirmasi password tidak cocok, silakan coba lagi')
                                        else:
                                            print('Password tidak valid, pastikan panjang minimal 8 karakter dan mengandung angka')
                                    else:
                                        print('Kode OTP salah, silahkan coba lagi')
                                except ValueError:
                                    print('Kode OTP harus berupa angka, silakan coba lagi')
                        except Exception as e:
                            print(f'Terjadi kesalahan saat memproses kode OTP: {e}')
                    else:
                        list_baris.append(i)
                
                if email_ditemukan:
                    with open(file_csv_user, 'w') as file_user:
                        file_user.writelines(list_baris)
                    break
                else:
                    print('Email tidak ditemukan, silakan coba lagi')
                    continue
        except Exception as e:
            print(f'Terjadi kesalahan: {e}')
            return

def profil(user_profil):
    try:
        os.system('cls')
        print('\n=========My Profile=========')
        print(f'Username  : {user_profil[0]}')
        print(f'Email     : {user_profil[2]}')
        print(f'No. HP    : {user_profil[3]}')
        print('============================')
        
        while True:
            try:
                menu = int(input('\nMenu:\n[1] Reset Password\n[2] Kembali\nMasukkan nomor menu: '))
                if menu == 1:
                    reset_password()
                    login()
                    header(text='AQUAVERSE')
                    break
                elif menu == 2:
                    os.system('cls')
                    break
            except ValueError:
                print('Input tidak valid. Silakan masukkan angka.')
    except Exception as e:
        print(f'Terjadi kesalahan: {e}')

def data_user():
    df = pd.read_csv(file_csv_user)
    df['No'] = range(1, len(df) + 1)
    print("\nDAFTAR USER:")
    print(tabulate(df[['No', 'username', 'email', 'phone', 'status']], headers=["No", "Username", "Email", 'No HP', "Status"], tablefmt="fancy_grid", colalign=('center', 'left', 'left', 'left', 'left'), showindex=False))

def tambah_user():
    try:
        with open(file_csv_user, 'a') as file_user:
            try:
                username1 = input('Username: ')
                password = input('Password: ')
                email = input('Email: ')
                phone = input('Nomor telepon: ')
                if not username1 or not password or not email or not phone:
                    raise ValueError("Semua data harus diisi")
                
                file_user.write(f'{username1},{password},{email},{phone},aktif\n')
                print('Akun berhasil ditambahkan')
            except ValueError as ve:
                print(f'Kesalahan input: {ve}')
                time.sleep(1)
    except Exception as e:
        print(f'Terjadi kesalahan: {e}')

def blokir_user():
    try:
        with open(file_csv_user, 'r') as file_user:
            lines = file_user.readlines()
            list_baris = []
            username_ditemukan = False
            username_blokir = input('Masukkan username yang ingin diubah statusnya: ')
            while True:
                aksi = input('Pilih status akun:\n1. Blokir\n2. Aktif\n ')
                if aksi == '1':
                    status_baru = 'blokir'
                    break
                elif aksi == '2':
                    status_baru = 'aktif'
                    break
                else:
                    print('Input tidak valid')
            
            for i in lines:
                data = i.strip().split(',')
                if len(data) != 5:
                    print(f"Baris data tidak valid: {i.strip()}")
                    continue
                username1, password, email, phone, status = data
                if username1 == username_blokir:
                    username_ditemukan = True
                    status = status_baru
                    list_baris.append(f'{username1},{password},{email},{phone},{status}\n')
                    print(f'Akun berhasil diubah statusnya menjadi {status_baru}')
                else:
                    list_baris.append(i)
            
            if username_ditemukan:
                with open(file_csv_user, 'w') as file_user:
                    file_user.writelines(list_baris)
            else:
                print('Username tidak ditemukan')
                time.sleep(1)
    except Exception as e:
        print(f'Terjadi kesalahan: {e}')

def admin_user():
    while True:
        data_user()
        print('Menu:\n[1] Tambah\n[2] Ubah Status\n[3] Kembali')
        pilihan = input('Pilih menu: ')
        if pilihan == '1':
            tambah_user()
            os.system('cls')            
            continue
        elif pilihan == '2':
            blokir_user()
            os.system('cls')            
            continue
        elif pilihan == '3':
            os.system('cls')
            break
        else:
            print('Invalid input')
            time.sleep(1)
            os.system('cls')

def data_produk():
    df = pd.read_csv('data produk.csv')
    df['No'] = range(1, len(df) + 1)
    print('DAFTAR PRODUK')
    print(tabulate(df[['No', 'Nama Produk', 'Harga', 'Stok Produk']], headers=['No', 'Nama Produk', 'Harga', 'Stok'], tablefmt='fancy_grid', colalign=('center', 'left', 'left', 'left'), showindex=False))

def tambah_produk():
    try:
        with open(file_data_produk, 'a') as file_produk:
            try:
                produk = input('Nama produk: ')
                if not produk.strip():
                    raise ValueError("Nama produk tidak boleh kosong")
                
                harga = int(input('Harga produk: '))
                if harga < 0:
                    raise ValueError("Harga produk tidak boleh negatif")
                
                stok = int(input('Stok produk: '))
                if stok < 0:
                    raise ValueError("Stok produk tidak boleh negatif")
                
                file_produk.write(f'{produk},{harga},{stok}\n')
                print('Produk berhasil ditambahkan')
            except ValueError as ve:
                print(f'Kesalahan input: {ve}')
            except Exception as e:
                print(f'Terjadi kesalahan saat menambahkan produk: {e}')
        data_produk()
    except Exception as e:
        print(f'Terjadi kesalahan: {e}')

def edit_produk():
    try:
        with open(file_data_produk, 'r') as file_produk:
            baca = file_produk.readlines()
        try:
            pilihan = int(input('Nomor produk yang ingin diedit: '))
        except ValueError:
            print('Input tidak valid, harap masukkan angka.')
            return
        if 1 <= pilihan <= len(baca) - 1:
            data = baca[pilihan].strip().split(',')
            produk, harga, stok = data
            
            print('Masukkan data baru, atau kosongkan jika tidak ingin mengubah')
            produk_baru = input('Nama Produk Baru: ').strip()
            harga_baru = input('Harga Baru: ').strip()
            stok_baru = input('Stok Baru: ').strip()
            
            produk = produk_baru if produk_baru else produk
            harga = harga_baru if harga_baru else harga
            stok = stok_baru if stok_baru else stok
            baca[pilihan] = f'{produk},{harga},{stok}\n'
            
            with open(file_data_produk, 'w') as file_produk:
                file_produk.writelines(baca)
                os.system('cls')
                print('Data berhasil diperbarui')
            data_produk()
        else:
            print('Nomor tidak valid, silahkan coba lagi')
    
    except Exception as e:
        print(f'Terjadi kesalahan: {e}')

def hapus_produk():
    try:
        with open(file_data_produk, 'r') as file_produk:
            baca = file_produk.readlines()
        while True:
            try:
                pilihan = int(input('Masukkan nomor baris yang ingin dihapus: '))
            except ValueError:
                print('Input tidak valid, harap masukkan angka.')
                continue
            
            if 1 <= pilihan <= len(baca) - 1:
                del baca[pilihan]
                print('Produk berhasil dihapus')
                
                try:
                    with open(file_data_produk, 'w') as file_produk:
                        file_produk.writelines(baca)
                except IOError:
                    print('Terjadi kesalahan saat menyimpan data ke file.')
                    break
                    
                hapus_lagi = input('Apakah ingin menghapus lagi? [y/n]: ')
                if hapus_lagi == 'n':
                    data_produk()
                    break
                elif hapus_lagi == 'y':
                    data_produk()
                else:
                    print('Input tidak valid, silahkan masukkan [y/n]')
            else:
                print('Nomor tidak valid, silahkan coba lagi')
    except Exception as e:
        print(f'Terjadi kesalahan: {e}')

def admin_produk():
    data_produk()
    while True:
        print('\nMenu:\n1. Tambah Produk\n2. Edit Produk\n3. Hapus Produk\n4. Kembali')
        pilihan = input('Masukkan nomor menu: ')
        if pilihan == '1':
            tambah_produk()
        elif pilihan == '2':
            edit_produk()
        elif pilihan == '3':
            hapus_produk()
        elif pilihan == '4':
            os.system('cls')
            break
        else:
            print('Invalid input')

def cek_riwayat():
    data_user()
    df_user = pd.read_csv(file_csv_user)
    df_riwayat = pd.read_csv(file_riwayat_pembelian)
    try:
        nomor = int(input("\nMasukkan nomor user: "))
        if nomor < 1 or nomor > len(df_user):
            print("Nomor tidak valid, silakan coba lagi")
            return
        username = df_user.loc[nomor - 1, 'username']
        riwayat_user = df_riwayat[df_riwayat['username'] == username]
        if riwayat_user.empty:
            print(f"\nUser {username} belum memiliki riwayat pembelian")
        else:
            transaksi_per_waktu = riwayat_user.groupby('waktu')
            print(f"\nRIWAYAT PEMBELIAN USER: {username}\n")
            for waktu, grup in transaksi_per_waktu:
                tanggal, jam = waktu.split()
                total_pembayaran = grup['total harga'].sum()
                metode_pembayaran = grup['metode'].iloc[0]
                
                print("=====================================")
                print(f"{tanggal}                   {jam}")
                print(f"Nama Pelanggan : {username}")
                print("--------------------------------------")
                print("Nama Produk                     Harga")
                print("--------------------------------------")
                for _, baris in grup.iterrows():
                    print(f"{baris['produk']}")
                    print(f"{baris['jumlah']} x {baris['harga']} = {baris['total harga']}")
                print("--------------------------------------")
                print(f"Total Pembayaran :          Rp {total_pembayaran:>6}")
                print(f"Metode Pembayaran : {metode_pembayaran}")
                print("=====================================\n")
        input('ENTER untuk kembali:')
        os.system('cls')
        return
    except ValueError:
        print("Input harus berupa angka")

def admin():
    while True:
        os.system('cls')
        header(text='ADMIN\nPAGE')
        pilihan = input('\nMenu:\n[1] Manajemen User\n[2] Manajemen Produk\n[3] Cek Riwayat Pembelian\n[4] Keluar\nPilih menu: ')
        if pilihan == '1':
            os.system('cls')
            admin_user()
        elif pilihan == '2':
            os.system('cls')
            admin_produk()
        elif pilihan == '3':
            os.system('cls')
            cek_riwayat()
        elif pilihan == '4':
            print('Program akan dihentikan')
            time.sleep(1)
            print('3...')
            time.sleep(1)
            print('2...')
            time.sleep(1)
            print('1...\nProgram berhasil dihentikan')
            exit()
        else:
            print('Invalid input')

def beranda():
    while True:
        print('                ─────────────────────────────────')
        print('\t\t|\t     Main Menu\t\t|')
        print('\t\t|                \t\t|')
        print('\t\t|       [1] Produk\t\t|')
        print('\t\t|       [2] Keranjang\t\t|')
        print('\t\t|       [3] Lihat Profil\t|')
        print('\t\t|       [4] Riwayat Pembelian\t|')
        print('\t\t|       [5] Keluar\t\t|')
        print('\t\t|                \t\t|')
        print('                ─────────────────────────────────')
        input_beranda = input('\n\nPilih menu :')
        if input_beranda == '1':
            detail_produk()
        elif input_beranda == '2':
            menu_keranjang()
        elif input_beranda == '3':
            profil(user_profil)
        elif input_beranda == '4':
            os.system('cls')
            riwayat_pembelian()
        elif input_beranda == '5':
            print('Program akan dihentikan')
            time.sleep(1)
            print('3...')
            time.sleep(1)
            print('2...')
            time.sleep(1)
            print('1...\nProgram berhasil dihentikan')
            exit()
        else:
            print('Invalid input')
            time.sleep(1)
            os.system('cls')

def data_produk_user():
    df = pd.read_csv(file_data_produk)
    df['No'] = range(1, len(df) + 1)
    print(tabulate(df[['No', 'Nama Produk']], headers=['No', 'Nama Produk'], tablefmt='fancy_grid', colalign=('center', 'left'), showindex=False))

def detail_produk():
    while True:
        try:
            data_produk_user()
            df = pd.read_csv('data produk.csv')
            print('Menu:\n[1] Lihat detail Produk\n[2] Beranda')
            try:
                input_user0 = int(input("Pilih menu: "))
            except ValueError:
                print("Input tidak valid, harap masukkan angka.")
                continue
            if input_user0 == 1:
                try:
                    global input_user
                    input_user = int(input('Masukkan nomor produk untuk melihat detail produk: '))
                except ValueError:
                    print("Input tidak valid, harap masukkan angka.")
                    continue
                if 1 <= input_user <= len(df):
                    detail_produk = df.iloc[input_user - 1]
                    print("===== Detail Produk =====")
                    print(f"Nama Produk\t: {detail_produk['Nama Produk']}")
                    print(f"Harga Produk\t: Rp {detail_produk['Harga']}")
                    print(f"Stok Produk\t: {detail_produk['Stok Produk']}")
                    print("Menu:\n[1] Beli Langsung\n[2] Tambahkan Keranjang\n[3] Kembali")
                    try:
                        input_user1 = int(input("Pilih menu: "))
                    except ValueError:
                        print("Input tidak valid, harap masukkan angka.")
                        continue
                    if input_user1 == 1:
                        beli_langsung()
                    elif input_user1 == 2:
                        try:
                            df_keranjang = pd.read_csv(file_keranjang)
                            jumlah = int(input('Masukkan jumlah produk yang ingin dibeli: '))
                        except ValueError:
                            print("Jumlah produk harus berupa angka.")
                            continue
                        produk_ditemukan = False
                        for index, baris in df_keranjang.iterrows():
                            if baris['username'] == username and baris['status'] == 'belum' and baris['produk'] == detail_produk['Nama Produk']:
                                df_keranjang.at[index, 'jumlah'] = baris['jumlah'] + jumlah
                                df_keranjang.at[index, 'total harga'] = df_keranjang.at[index, 'jumlah'] * baris['harga']
                                produk_ditemukan = True
                                print('Jumlah produk berhasil ditambahkan')
                                time.sleep(2.5)
                                os.system('cls')
                        
                        if not produk_ditemukan:
                            list_baris_baru = [username, detail_produk['Nama Produk'], detail_produk['Harga'], jumlah, int(detail_produk['Harga']) * jumlah, 'belum']
                            kolom = ['username', 'produk', 'harga', 'jumlah', 'total harga', 'status']
                            baris_baru = pd.DataFrame([list_baris_baru], columns=kolom)
                            df_keranjang = pd.concat([df_keranjang, baris_baru], ignore_index=True)
                            print('Produk baru berhasil ditambahkan')
                            time.sleep(1.25)
                            os.system('cls')
                        df_keranjang.to_csv(file_keranjang, index=False)
                    elif input_user1 == 3:
                        return
                    else:
                        print('Invalid input')
                else:
                    print('Nomor produk tidak valid, silakan coba lagi')
            elif input_user0 == 2:
                os.system('cls')
                return
            else:
                print("Input tidak valid, harap pilih [1] atau [2]")
        except Exception as e:
            print(f'Terjadi kesalahan: {e}')
            break

def beli_langsung():
    try:
        input_beli = int(input("Masukkan jumlah produk : "))
    except ValueError:
        print("Input tidak valid, harap masukkan angka.")
        return
    
    df = pd.read_csv(file_data_produk)
    pilihan_produk = df.iloc[input_user - 1]
    if 0 < input_beli <= int(pilihan_produk['Stok Produk']):
        try:
            bayar = int(pilihan_produk['Harga']) * input_beli
            print(f"Total Pembayaran : Rp {bayar}")
            print("Metode Pembayaran\n[1] Gopay\n[2] Ovo\n[3] Bank Mandiri\n[4] Bank BCA\n[5] Bank BRI\n[6] Batal")
            input_bayar = int(input('Pilih metode pembayaran: '))
        except ValueError:
            print("Input tidak valid, harap masukkan angka.")
            return
        
        if 1 <= input_bayar <= 5:
            metode_pembayaran = ['Gopay', 'Ovo', 'Bank Mandiri', 'Bank BCA', 'Bank BRI']
            metode_pembayaran = metode_pembayaran[input_bayar - 1]
            waktu_transaksi = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            total_harga = input_beli * int(pilihan_produk['Harga'])
            data_riwayat = []
            data_riwayat.append([waktu_transaksi, username, pilihan_produk['Nama Produk'], input_beli, pilihan_produk['Harga'], total_harga, metode_pembayaran])
            df_transaksi = pd.DataFrame(data_riwayat, columns=['waktu', 'username', 'produk', 'jumlah', 'harga', 'total harga', 'metode'])
            df_riwayat = pd.read_csv(file_riwayat_pembelian)
            df_riwayat = pd.concat([df_riwayat, df_transaksi], ignore_index=True)
            df_riwayat.to_csv(file_riwayat_pembelian, index=False)
            df.loc[input_user - 1, 'Stok Produk'] -= input_beli
            df.to_csv(file_data_produk, index=False)
            print("=== PEMBAYARAN BERHASIL ===")
            print('=====================================')
            print('           STRUK PEMBAYARAN          ')
            print('=====================================')
            print(f"{datetime.now().strftime('%d-%m-%Y                   %H:%M:%S')}")
            print(f'Nama Pelanggan : {username}')
            print('--------------------------------------')
            print('Nama Produk                    Harga ')
            print('--------------------------------------')
            print(f"{pilihan_produk['Nama Produk']} \n{str(input_beli).ljust(2)} x {str(pilihan_produk['Harga']).ljust(18)} = {str(bayar).rjust(10)}")
            print('--------------------------------------')
            print(f"{'Total Pembayaran :'.ljust(24)} Rp {str(bayar).rjust(8)}")
            print(f"Metode Pembayaran : {metode_pembayaran}")
            print('=====================================')
            print('            TERIMA KASIH             ')
            print('=====================================')
            input('(ENTER) untuk kembali :')
            os.system('cls')
        elif input_bayar == 6:
            print("=== PEMBAYARAN DIBATALKAN ===")
            time.sleep(1)
            os.system('cls')
        else:
            print("Invaldi input")
    else:
        print('Stok Habis')

def menu_keranjang():
    keranjang()
    print('Menu:\n[1] Pilih produk\n[2] Hapus produk\n[3] Edit jumlah produk\n[4] Beli semua\n[5] Kembali')
    input_user0 = input('Pilih menu: ')
    if input_user0 == '1':
        pilih_produk()
    elif input_user0 == '2':
        hapus_keranjang()
    elif input_user0 == '3' :
        edit_keranjang()
    elif input_user0 == '4' :
        beli_semua_keranjang()
    elif input_user0 == '5' :
        return
    else:
        print('Invalid input')

def keranjang():
    df = pd.read_csv(file_keranjang)
    keranjang = df[(df['username'] == username) & (df['status'] == 'belum')]
    header = ['No', 'Produk', 'Harga', 'Jumlah', 'Total Harga']
    if keranjang.empty:
        os.system('cls')
        print('Keranjang anda kosong')
        return beranda()
    else:
        keranjang = df[(df['username'] == username) & (df['status'] == 'belum')]
        keranjang = keranjang[['produk', 'harga', 'jumlah', 'total harga']]
        keranjang['no'] = range(1, len(keranjang) + 1)
        
        print(tabulate(keranjang[['no', 'produk', 'harga', 'jumlah', 'total harga']], headers=header, tablefmt="fancy_grid", showindex=False))

def pilih_produk():
    df_keranjang = pd.read_csv(file_keranjang)
    filter_user = df_keranjang[(df_keranjang['username'] == username) & (df_keranjang['status'] == 'belum')]
    try:
        input_keranjang = input('Masukkan nomor produk (contoh : 1,2,3): ').split(',')
        pilih_keranjang = [int(i.strip()) - 1 for i in input_keranjang]
        pilihan_produk = filter_user.iloc[pilih_keranjang]
    except ValueError:
        print("Input tidak valid, harap masukkan angka yang benar.")
        return
    
    total = pilihan_produk['total harga'].sum()
    print(f'Total Pembayaran Anda: Rp {total}')
    print("Metode Pembayaran\n[1] Gopay\n[2] Ovo\n[3] Bank Mandiri\n[4] Bank BCA\n[5] Bank BRI\n[6] Batal")
    try:
        input_bayar = int(input('Pilih metode pembayaran: '))
    except ValueError:
        print("Pilihan tidak valid, harap masukkan angka.")
        return
    
    if 1 <= input_bayar <= 5:
        df_produk = pd.read_csv(file_data_produk)
        for idx, row in pilihan_produk.iterrows():
            produk = row['produk']
            jumlah_beli = row['jumlah']
            stok = df_produk.loc[df_produk['Nama Produk'] == produk, 'Stok Produk'].iloc[0]
            if jumlah_beli > stok:
                print(f"Stok produk '{produk}' tidak mencukupi! Tersedia {stok}")
                return  
        
        for _, row in pilihan_produk.iterrows():
            produk = row['produk']
            jumlah_beli = row['jumlah']
            df_produk.loc[df_produk['Nama Produk'] == produk, 'Stok Produk'] -= jumlah_beli
        
        df_produk.to_csv('data produk.csv', index=False)
        waktu_transaksi = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        metode_pembayaran = ['Gopay', 'Ovo', 'Bank Mandiri', 'Bank BCA', 'Bank BRI']
        metode_pembayaran = metode_pembayaran[input_bayar - 1]
        for idx in pilihan_produk.index:
            df_keranjang.loc[idx, 'status'] = 'sudah'
        
        df_keranjang.to_csv('keranjang.csv', index=False)
        data_riwayat = []
        for _, baris in pilihan_produk.iterrows():
            data_riwayat.append([waktu_transaksi, baris['username'], baris['produk'], baris['jumlah'], baris['harga'], baris['total harga'], metode_pembayaran])
        
        df_transaksi_baru = pd.DataFrame(data_riwayat, columns=['waktu', 'username', 'produk', 'jumlah', 'harga', 'total harga', 'metode'])
        df_riwayat = pd.read_csv(file_riwayat_pembelian)
        df_riwayat = pd.concat([df_riwayat, df_transaksi_baru], ignore_index=True)
        df_riwayat.to_csv(file_riwayat_pembelian, index=False)
        print("=== PEMBAYARAN BERHASIL ===")
        print('=====================================')
        print('           STRUK PEMBAYARAN          ')
        print('=====================================')
        print(datetime.now().strftime('%d-%m-%Y                   %H:%M:%S'))
        print('Nama Pelanggan : sandi')
        print('--------------------------------------')
        print('Nama Produk                     Harga ')
        print('--------------------------------------')
        for _, row in pilihan_produk.iterrows():
            print(f"{row['produk']} \n{str(row['jumlah']).ljust(2)} x {str(row['harga']).ljust(18)} = {str(row['total harga']).rjust(10)}")
        print('--------------------------------------')
        print(f"{'Total Pembayaran :'.ljust(24)} Rp {str(total).rjust(8)}")
        print(f'Metode Pembayaran : {metode_pembayaran}')
        print('=====================================')
        print('            TERIMA KASIH             ')
        print('=====================================')
        input('(ENTER) untuk kembali: ')
        os.system('cls')
        return
    elif input_bayar == 6:
        print("=== PEMBAYARAN DIBATALKAN ===")
        time.sleep(1)
        os.system('cls')
    else:
        print("Invalid input")

def hapus_keranjang(): 
    df = pd.read_csv(file_keranjang)
    filter_user = df[(df['username'] == username) & (df['status'] == 'belum')]
    if filter_user.empty:
        print("Tidak ada produk di keranjang.")
        return
    
    while True:
        try:
            input_hapus = int(input('Masukkan nomor produk: '))
            if 1 <= input_hapus <= len(filter_user):
                df = df.drop(filter_user.index[input_hapus - 1])
                df.to_csv(file_keranjang, index=False)
                os.system('cls')
                print("Produk berhasil dihapus.")
                return menu_keranjang()
            else:
                print("Nomor produk tidak valid, silakan coba lagi.")
        except ValueError:
            print("Input tidak valid, harap masukkan nomor produk yang valid.")
        except Exception as e:
            print(f'Terjadi kesalahan: {e}')
            return


def edit_keranjang():
    df = pd.read_csv(file_keranjang)
    filter_user = df[(df['username'] == username) & (df['status'] == 'belum')]
    if filter_user.empty:
        print('Tidak ada produk yang dapat diedit.')
        return
    
    while True:
        try:
            input_edit = int(input('Pilih produk yang ingin diedit: '))
            if 1 <= input_edit <= len(filter_user):
                pilihan_produk = filter_user.iloc[input_edit - 1]
                try:
                    input_jumlah = int(input('Masukkan jumlah terbaru: '))
                    if input_jumlah <= 0:
                        print("Jumlah harus lebih besar dari 0.")
                        continue
                    
                    total_harga_baru = int(pilihan_produk['harga']) * input_jumlah
                    produk_yang_diedit = filter_user.iloc[input_edit - 1]['produk']
                    df.loc[df['produk'] == produk_yang_diedit, 'jumlah'] = input_jumlah
                    df.loc[df['produk'] == produk_yang_diedit, 'total harga'] = total_harga_baru
                    df.to_csv(file_keranjang, index=False)
                    print('Data berhasil diperbarui')
                    os.system('cls')
                    return menu_keranjang()
                except ValueError:
                    print("Input jumlah tidak valid, harap masukkan angka.")
            else:
                print('Invalid input')
                os.system('cls')
                return menu_keranjang()
        except Exception as e:
            print(f'Terjadi kesalahan: {e}')
            return

def beli_semua_keranjang():
    df = pd.read_csv(file_keranjang)    
    data_keranjang = df[(df['username'] == username) & (df['status'] == 'belum')]
    if data_keranjang.empty:
        os.system('cls')
        print('Keranjang Anda kosong')
        return beranda()

    try:
        total_pembayaran = data_keranjang['total harga'].astype(int).sum()
        print(f'Total Pembayaran Anda : Rp {total_pembayaran}')
        print("Metode Pembayaran\n[1] Gopay\n[2] Ovo\n[3] Bank Mandiri\n[4] Bank BCA\n[5] Bank BRI\n[6] Batal")
        input_metode = int(input('Pilih metode pembayaran: '))
        
        if input_metode == 6:
            print("=== PEMBAYARAN DIBATALKAN ===")
            time.sleep(1)
            os.system('cls')
            return
        
        if not 1 <= input_metode <= 5:
            print("Metode pembayaran tidak valid.")
            return
        df.loc[(df['username'] == username) & (df['status'] == 'belum'), 'status'] = 'sudah'
        df.to_csv(file_keranjang, index=False)
    except ValueError:
        print("Error: Input metode pembayaran tidak valid, harus berupa angka antara 1 dan 5.")
        return
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return
    
    df_produk = pd.read_csv(file_data_produk)    
    for _, baris in data_keranjang.iterrows():
        produk = baris['produk']
        jumlah = int(baris['jumlah'])
        
        if produk in df_produk['Nama Produk'].tolist():
            stok = df_produk.loc[df_produk['Nama Produk'] == produk, 'Stok Produk'].iloc[0]
            
            if stok >= jumlah:
                df_produk.loc[df_produk['Nama Produk'] == produk, 'Stok Produk'] -= jumlah
            else:
                print(f"Stok {produk} tidak cukup, hanya tersedia {stok}")
                return
        else:
            print(f"Produk {produk} tidak ditemukan dalam daftar produk.")
            return
    df_produk.to_csv(file_data_produk, index=False)
    waktu_transaksi = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    metode_pembayaran = ['Gopay', 'Ovo', 'Bank Mandiri', 'Bank BCA', 'Bank BRI']
    metode_pembayaran = metode_pembayaran[input_metode - 1]
    data_riwayat = []
    for _, baris in data_keranjang.iterrows():
        data_riwayat.append([waktu_transaksi, baris['username'], baris['produk'], baris['jumlah'], baris['harga'], baris['total harga'], metode_pembayaran])
    
    df_transaksi_baru = pd.DataFrame(data_riwayat, columns=['waktu', 'username', 'produk', 'jumlah', 'harga', 'total harga', 'metode'])
    df_riwayat = pd.read_csv(file_riwayat_pembelian)
    df_riwayat = pd.concat([df_riwayat, df_transaksi_baru], ignore_index=True)
    df_riwayat.to_csv(file_riwayat_pembelian, index=False)
    print("=== PEMBAYARAN BERHASIL ===")
    print('=====================================')
    print('           STRUK PEMBAYARAN          ')
    print('=====================================')
    print(datetime.now().strftime('%d-%m-%Y                   %H:%M:%S'))
    print(f'Nama Pelanggan : {username}')
    print('--------------------------------------')
    print('Nama Produk                     Harga ')
    print('--------------------------------------')
    for _, row in df_transaksi_baru.iterrows():
        print(f"{row['produk']} \n{str(row['jumlah']).ljust(2)} x {str(row['harga']).ljust(18)} = {str(row['total harga']).rjust(10)}")
    print('--------------------------------------')
    print(f"{'Total Pembayaran :'.ljust(24)} Rp {str(total_pembayaran).rjust(8)}")
    print(f'Metode Pembayaran : {metode_pembayaran}')
    print('=====================================')
    print('            TERIMA KASIH             ')
    print('=====================================')
    input('(ENTER) untuk kembali: ')
    os.system('cls')
    return

def riwayat_pembelian():
    df = pd.read_csv('riwayat.csv')
    df = df[df['username'] == username]
    if df.empty:
        print('\nRiwayat pembelelian kosong')
        return
    else:
        transaksi_per_waktu = df.groupby('waktu')
        for waktu, grup in transaksi_per_waktu:
            tanggal, jam = waktu.split()
            username1 = grup['username'].iloc[0]
            metode_pembayaran = grup['metode'].iloc[0]
            total_pembayaran = grup['total harga'].sum()
            print("=====================================")
            print(f"{tanggal}                   {jam}")
            print(f"Nama Pelanggan : {username1}")
            print("--------------------------------------")
            print("Nama Produk                     Harga")
            print("--------------------------------------")
            for i, baris in grup.iterrows():
                print(f"{baris['produk']}")
                print(f"{baris['jumlah']} x {baris['harga']} = {baris['total harga']}")
            print("--------------------------------------")
            print(f"Total Pembayaran :          Rp {total_pembayaran:>6}")
            print(f"Metode Pembayaran : {metode_pembayaran}")
            print("=====================================\n\n")
            
    input('ENTER untuk kembali:')
    os.system('cls')
    return

def main():
    os.system('cls')
    header(text='AQUAVERSE')
    register_login()
    header(text=f'WELCOME\n {username}')
    beranda()

main()