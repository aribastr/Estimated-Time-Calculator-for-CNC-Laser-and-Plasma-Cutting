import datetime
from line import other_length, circle_length, hole_count, total_contour_distance
from datetime import timedelta
from speed import speed, hole_speed, machine_speed, piercing_time

def ondalik_sureyi_zamana_cevir(sure):
    sure_timedelta = timedelta(seconds=sure * 60)
    saat = sure_timedelta.seconds // 3600
    dakika = (sure_timedelta.seconds - saat * 3600) // 60
    saniye = sure_timedelta.seconds - saat * 3600 - dakika * 60
    return f"{saat:02d}:{dakika:02d}:{saniye:02d}"

def piercing_suresi(piercing_sure):
  saniyeler = int(piercing_sure)
  dakikalar = saniyeler // 60
  saniyeler %= 60
  saatler = dakikalar // 60
  dakikalar %= 60
  return saatler, dakikalar, saniyeler
def zaman_formatlama(saatler, dakikalar, saniyeler):
  total_piercing_time_str = "{:02d}:{:02d}:{:02d}".format(int(saatler), int(dakikalar), saniyeler)
  return total_piercing_time_str



# Kesim sürelerini hesaplayın
hole_time = (circle_length / hole_speed)
line_time = (other_length / speed)
total_piercing_time = ((hole_count + 1) * (piercing_time))
machine_move_time = (total_contour_distance / machine_speed)


# Süreleri zamana çevirin
hole_time_str = ondalik_sureyi_zamana_cevir(hole_time)
line_time_str = ondalik_sureyi_zamana_cevir(line_time)
total_piercing_time_str = piercing_suresi(total_piercing_time)
machine_move_time_str = ondalik_sureyi_zamana_cevir(machine_move_time)


saatler, dakikalar, saniyeler = piercing_suresi(total_piercing_time)
total_piercing_time_str = zaman_formatlama(saatler, dakikalar, saniyeler)

# Toplam kesim süresini hesaplayın
toplam_sure = (line_time + hole_time + machine_move_time)

# Sonuçları yazdırın
print(f"Line Kesim Süresi: {line_time_str}")
print(f"Delik Kesim Süresi: {hole_time_str}")
print(f"Toplam Piercing Süresi: {total_piercing_time_str}")
print(f"Makinenin Konturlar Arası İlerleme Süresi: {machine_move_time_str}")
