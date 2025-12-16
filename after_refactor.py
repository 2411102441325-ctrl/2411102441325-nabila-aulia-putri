from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List


@dataclass
class RegistrationData:
    """
    Model data mahasiswa untuk perhitungan UKT.
    """
    name: str
    parent_income: int          # Penghasilan orang tua
    scholarship_received: bool  # Status beasiswa


# ===================== ABSTRAKSI (DIP) =====================

class IValidationRule(ABC):
    """
    Kontrak untuk semua rule perhitungan UKT.
    Setiap rule harus mengimplementasikan method validate().
    """

    @abstractmethod
    def validate(self, data: RegistrationData) -> bool:
        """
        Melakukan pengecekan aturan UKT.
        Mengembalikan True jika lolos rule, False jika gagal.
        """
        pass


# ===================== RULE TERPISAH (SRP) =====================

class MaxIncomeRule(IValidationRule):
    """
    Rule untuk batas maksimal penghasilan orang tua.
    """

    def __init__(self, max_income: int = 5000000):
        self.max_income = max_income

    def validate(self, data: RegistrationData) -> bool:
        if data.parent_income > self.max_income:
            print(
                f"❌ [MaxIncomeRule] Penghasilan Rp{data.parent_income} "
                f"melebihi batas Rp{self.max_income}."
            )
            return False
        print(
            f"✅ [MaxIncomeRule] Penghasilan Rp{data.parent_income} "
            f"masih dalam batas."
        )
        return True


class ScholarshipRule(IValidationRule):
    """
    Rule untuk mengecek status beasiswa.
    """

    def validate(self, data: RegistrationData) -> bool:
        if not data.scholarship_received:
            print("❌ [ScholarshipRule] Mahasiswa tidak menerima beasiswa.")
            return False
        print("✅ [ScholarshipRule] Mahasiswa menerima beasiswa.")
        return True


class MinIncomeRule(IValidationRule):
    """
    Rule tambahan: batas minimal penghasilan.
    (Pembuktian OCP: rule baru tanpa ubah kode lama)
    """

    def __init__(self, min_income: int = 1000000):
        self.min_income = min_income

    def validate(self, data: RegistrationData) -> bool:
        if data.parent_income < self.min_income:
            print(
                f"❌ [MinIncomeRule] Penghasilan Rp{data.parent_income} "
                f"di bawah batas minimal Rp{self.min_income}."
            )
            return False
        print(
            f"✅ [MinIncomeRule] Penghasilan Rp{data.parent_income} "
            f"memenuhi batas minimal."
        )
        return True


# ===================== SERVICE KOORDINATOR (High-level) =====================

class RegistrationService:
    """
    Kelas high-level yang mengoordinasi proses perhitungan UKT.
    Bergantung pada abstraksi IValidationRule (DIP).
    """

    def __init__(self, rules: List[IValidationRule]):
        # Dependency Injection: rules disuntikkan dari luar
        self.rules = rules

    def run_validation(self, data: RegistrationData) -> bool:
        print(f"\n=== Perhitungan UKT untuk {data.name} ===")

        for rule in self.rules:
            if not rule.validate(data):
                print(f"⛔ {data.name} dikenakan UKT TINGGI.")
                return False

        print(f"✅ {data.name} mendapatkan UKT RENDAH.")
        return True


if __name__ == "__main__":
    print("=== SISTEM PERHITUNGAN UKT (SOLID + DEPENDENCY INJECTION) ===")

    # Definisikan semua rule yang ingin dipakai
    rules: List[IValidationRule] = [
        MinIncomeRule(min_income=1000000),
        MaxIncomeRule(max_income=5000000),
        ScholarshipRule(),
    ]

    service = RegistrationService(rules)

    # 1. Data valid (UKT rendah)
    andi = RegistrationData(
        name="Andi",
        parent_income=4000000,
        scholarship_received=True
    )
    service.run_validation(andi)

    # 2. Penghasilan terlalu tinggi
    budi = RegistrationData(
        name="Budi",
        parent_income=8000000,
        scholarship_received=True
    )
    service.run_validation(budi)

    # 3. Tidak menerima beasiswa
    cici = RegistrationData(
        name="Cici",
        parent_income=3000000,
        scholarship_received=False
    )
    service.run_validation(cici)

    # 4. Penghasilan terlalu rendah (pembuktian MinIncomeRule)
    dodi = RegistrationData(
        name="Dodi",
        parent_income=500000,
        scholarship_received=True
    )
    service.run_validation(dodi)
