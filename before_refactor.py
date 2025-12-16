from dataclasses import dataclass


@dataclass
class RegistrationData:
    """
    Model sederhana untuk data perhitungan UKT mahasiswa.
    """
    name: str
    parent_income: int          # Penghasilan orang tua
    scholarship_received: bool  # Status beasiswa


class ValidatorManager:
    """
    God Class: Menangani semua aturan perhitungan UKT sekaligus.
    Melanggar SRP, OCP, dan DIP.
    """

    def validate(self, data: RegistrationData) -> bool:
        print(f"Memulai perhitungan UKT untuk mahasiswa: {data.name}")

        # Validasi penghasilan (hardcoded) -> pelanggaran SRP & OCP
        if data.parent_income > 5000000:
            print("❌ Penghasilan orang tua melebihi batas UKT rendah.")
            print("➡️ Mahasiswa dikenakan UKT Tinggi.")
            return False

        # Validasi beasiswa (hardcoded) -> pelanggaran SRP & OCP
        if not data.scholarship_received:
            print("❌ Mahasiswa tidak menerima beasiswa.")
            print("➡️ Mahasiswa dikenakan UKT Tinggi.")
            return False

        # Jika ke depan ada aturan UKT baru,
        # maka akan ditambah if/elif di sini lagi
        # -> method semakin panjang (code smell)

        print("✅ Semua syarat terpenuhi.")
        print("➡️ Mahasiswa mendapatkan UKT Rendah.")
        return True


if __name__ == "__main__":
    print("=== SEBELUM REFACTOR (God Class - Perhitungan UKT) ===")

    vm = ValidatorManager()

    # 1. Data valid (UKT rendah)
    andi = RegistrationData(
        name="Andi",
        parent_income=4000000,
        scholarship_received=True
    )
    print("\n>>> Test kasus 1: UKT Rendah")
    vm.validate(andi)

    # 2. Penghasilan terlalu tinggi
    budi = RegistrationData(
        name="Budi",
        parent_income=8000000,
        scholarship_received=True
    )
    print("\n>>> Test kasus 2: Penghasilan tinggi")
    vm.validate(budi)

    # 3. Tidak memiliki beasiswa
    cici = RegistrationData(
        name="Cici",
        parent_income=3000000,
        scholarship_received=False
    )
    print("\n>>> Test kasus 3: Tidak menerima beasiswa")
    vm.validate(cici)
