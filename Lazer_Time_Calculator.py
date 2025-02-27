from time_calc import total_piercing_time_str, ondalik_sureyi_zamana_cevir, toplam_sure

# Zamanı saniyeye dönüştüren bir fonksiyon tanımlayalım
def zamani_saniyeye_cevir(zaman_str):
    saat, dakika, saniye = map(int, zaman_str.split(':'))
    return saat * 3600 + dakika * 60 + saniye

# Toplam süreyi saniyeye dönüştürelim
toplam_sure_saniye = zamani_saniyeye_cevir(total_piercing_time_str)

# Ondalık süreyi saniyeye dönüştürelim ve toplam süreye ekleyelim
ondalik_sure_saniye = zamani_saniyeye_cevir(ondalik_sureyi_zamana_cevir(toplam_sure))
toplam_sure_saniye += ondalik_sure_saniye

# Toplam süreyi saat:dakika:saniye formatına çevirelim
saat = toplam_sure_saniye // 3600
dakika = (toplam_sure_saniye % 3600) // 60
saniye = toplam_sure_saniye % 60

toplam_imalat_suresi = f"{saat:02d}:{dakika:02d}:{saniye:02d}"
print(f"\nTOPLAM KESİM SÜRESİ: {toplam_imalat_suresi}")
run = input(" ")
