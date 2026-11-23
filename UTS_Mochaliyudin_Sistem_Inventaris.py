from datetime import datetime


class Transaksi:
    def __init__(self, jenis: str, kode_produk: str, nama_produk: str, jumlah: int):
        # Encapsulation dengan atribut private
        self.__jenis = jenis
        self.__kode_produk = kode_produk
        self.__nama_produk = nama_produk
        self.__jumlah = jumlah
        self.__waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def info_transaksi(self) -> str:
        return f"[{self.__waktu}] {self.__jenis:<6} | {self.__kode_produk} - {self.__nama_produk} ({self.__jumlah} unit)"


class Produk:
    total_produk = 0

    def __init__(self, kode: str, nama: str, harga: float, stok: int):
        self.__kode = kode
        self.__nama = nama
        self.__harga = 0.0
        self.__stok = 0

        self.harga = harga
        self.stok = stok
        Produk.total_produk += 1

    # --- Property & Setter ---
    @property
    def kode(self) -> str:
        return self.__kode

    @property
    def nama(self) -> str:
        return self.__nama

    @nama.setter
    def nama(self, nilai: str):
        if not nilai.strip():
            raise ValueError("Nama produk tidak boleh kosong.")
        self.__nama = nilai

    @property
    def harga(self) -> float:
        return self.__harga

    @harga.setter
    def harga(self, nilai: float):
        if nilai < 0:
            raise ValueError("Harga tidak boleh negatif.")
        self.__harga = float(nilai)

    @property
    def stok(self) -> int:
        return self.__stok

    @stok.setter
    def stok(self, jumlah: int):
        if jumlah < 0:
            raise ValueError("Stok tidak boleh kurang dari 0.")
        self.__stok = jumlah

    # --- Instance Method ---
    def info_produk(self) -> str:
        harga_format = Produk.format_rupiah(self.__harga)
        return f"[{self.__kode}] {self.__nama} | Harga: {harga_format} | Stok: {self.__stok}"

    # --- Class Method ---
    @classmethod
    def dari_string(cls, data_str: str):
        kode, nama, harga, stok = data_str.split("-")
        return cls(kode, nama, float(harga), int(stok))

    @classmethod
    def get_total_produk(cls) -> int:
        return cls.total_produk

    # --- Static Method ---
    @staticmethod
    def format_rupiah(nominal: float) -> str:
        return f"Rp{nominal:,.0f}".replace(",", ".")


class Gudang:
    def __init__(self, nama_gudang: str):
        self.__nama_gudang = nama_gudang
        self.__daftar_produk = {}
        self.__riwayat_transaksi = []  # Menyimpan object Transaksi

    @property
    def nama_gudang(self) -> str:
        return self.__nama_gudang

    # --- Barang Masuk (Produk Baru) ---
    def tambah_produk_baru(self, produk: Produk):
        if produk.kode in self.__daftar_produk:
            print(f"Gagal: Kode '{produk.kode}' sudah terdaftar. Gunakan menu Barang Masuk (Tambah Stok).")
            return
        self.__daftar_produk[produk.kode] = produk
        self.__riwayat_transaksi.append(Transaksi("MASUK", produk.kode, produk.nama, produk.stok))
        print(f"Produk baru '{produk.nama}' berhasil didaftarkan dengan stok awal {produk.stok}.")

    # --- Barang Masuk (Tambah Stok Produk Lama) ---
    def barang_masuk(self, kode: str, jumlah: int):
        if kode not in self.__daftar_produk:
            print(f"Error: Produk dengan kode '{kode}' tidak ditemukan.")
            return
        if jumlah <= 0:
            print("Error: Jumlah barang masuk harus lebih dari 0.")
            return

        produk = self.__daftar_produk[kode]
        produk.stok += jumlah
        self.__riwayat_transaksi.append(Transaksi("MASUK", produk.kode, produk.nama, jumlah))
        print(f"Berhasil: +{jumlah} unit {produk.nama} masuk. Total stok sekarang: {produk.stok}.")

    # --- Barang Keluar (Kurangi Stok) ---
    def barang_keluar(self, kode: str, jumlah: int):
        if kode not in self.__daftar_produk:
            print(f"Error: Produk dengan kode '{kode}' tidak ditemukan.")
            return

        produk = self.__daftar_produk[kode]
        if jumlah <= 0:
            print("Error: Jumlah barang keluar harus lebih dari 0.")
        elif produk.stok < jumlah:
            print(f"Error: Stok {produk.nama} tidak mencukupi (Sisa stok: {produk.stok}).")
        else:
            produk.stok -= jumlah
            self.__riwayat_transaksi.append(Transaksi("KELUAR", produk.kode, produk.nama, jumlah))
            print(f"Berhasil: -{jumlah} unit {produk.nama} keluar. Sisa stok sekarang: {produk.stok}.")

    def tampilkan_inventaris(self):
        print(f"\n=== DAFTAR STOK {self.__nama_gudang.upper()} ===")
        if not self.__daftar_produk:
            print("Gudang masih kosong.")
        else:
            for produk in self.__daftar_produk.values():
                print(produk.info_produk())
        print(f"Total jenis produk: {Produk.get_total_produk()}\n")

    def tampilkan_riwayat(self):
        print(f"\n=== RIWAYAT BARANG MASUK & KELUAR ({self.__nama_gudang.upper()}) ===")
        if not self.__riwayat_transaksi:
            print("Belum ada riwayat transaksi.")
        else:
            for trx in self.__riwayat_transaksi:
                print(trx.info_transaksi)
        print()


# ================= PROGRAM UTAMA (MENU INTERAKTIF) =================
if __name__ == "__main__":
    gudang = Gudang("Gudang Utama")

    # Data awal sebagai contoh (bisa dihapus jika ingin mulai dari 0)
    gudang.tambah_produk_baru(Produk("BRG01", "Laptop Asus", 12000000, 5))
    gudang.tambah_produk_baru(Produk.dari_string("BRG02-Mouse Wireless-250000-15"))

    while True:
        print("=== MENU SISTEM INVENTARIS ===")
        print("1. Daftarkan Produk Baru")
        print("2. Barang Masuk (Tambah Stok)")
        print("3. Barang Keluar (Kurangi Stok)")
        print("4. Lihat Daftar Stok Barang")
        print("5. Lihat Riwayat Keluar/Masuk")
        print("0. Keluar Program")

        pilihan = input("Pilih menu (0-5): ").strip()

        if pilihan == "1":
            try:
                kode = input("Masukkan Kode Barang   : ").strip().upper()
                nama = input("Masukkan Nama Barang   : ").strip()
                harga = float(input("Masukkan Harga Satuan  : "))
                stok = int(input("Masukkan Stok Awal     : "))
                produk_baru = Produk(kode, nama, harga, stok)
                gudang.tambah_produk_baru(produk_baru)
            except ValueError as e:
                print(f"Input tidak valid: {e}")

        elif pilihan == "2":
            kode = input("Masukkan Kode Barang   : ").strip().upper()
            try:
                jumlah = int(input("Jumlah Barang Masuk    : "))
                gudang.barang_masuk(kode, jumlah)
            except ValueError:
                print("Error: Jumlah harus berupa angka bulat.")

        elif pilihan == "3":
            kode = input("Masukkan Kode Barang   : ").strip().upper()
            try:
                jumlah = int(input("Jumlah Barang Keluar   : "))
                gudang.barang_keluar(kode, jumlah)
            except ValueError:
                print("Error: Jumlah harus berupa angka bulat.")

        elif pilihan == "4":
            gudang.tampilkan_inventaris()

        elif pilihan == "5":
            gudang.tampilkan_riwayat()

        elif pilihan == "0":
            print("Program selesai. Terima kasih!")
            break
        else:
            print("Pilihan tidak valid, silakan masukkan angka 0-5.")