import os
import ezdxf
from math import sqrt
import tkinter as tk
from tkinter import filedialog

print("\nBU PROGRAM ABDULLAH ARIBAS TARAFINDAN MITAS POLIGON PLANLAMA BIRIMI ICIN OLUŞTURULMUŞTUR."
      "\nPROGRAM DXF TASARIM DOSYALARINI KULLANARAK CNC LAZER KESIM VE PLAZMA KESIM MAKINELERI ICIN SURE TAHMINI YAPMAKTADIR.")

print("\nLütfen Açılan Pencereden DXF Dosyasını Seçiniz!\n")

def calculate_2d_distance(point1, point2):
    return sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def calculate_total_lengths_and_hole_count(file_path):
    circle_length = 0
    other_length = 0
    hole_count = 0
    hole_centers = []

    try:
        doc = ezdxf.readfile(file_path)
        msp = doc.modelspace()
        for entity in msp:
            if entity.dxftype() in ['LINE', 'POLYLINE', 'LWPOLYLINE', 'SPLINE', 'ARC', 'ELLIPSE']:
                other_length += calculate_entity_length(entity)
            elif entity.dxftype() == 'CIRCLE':
                circle_length += calculate_entity_length(entity)
                hole_count += 1
                hole_centers.append(entity.dxf.center)

        return circle_length, other_length, hole_count, hole_centers

    except ezdxf.DXFStructureError:
        print("DXF dosyası okunamadı veya uygun bir format değil.")
        return None, None, None, None  # Return None on error
    except Exception as e:
        print("Bir hata oluştu:", e)
        return None, None, None, None  # Return None on error

def calculate_entity_length(entity):
    if entity.dxftype() == 'LINE':
        start_point = (entity.dxf.start[0], entity.dxf.start[1])
        end_point = (entity.dxf.end[0], entity.dxf.end[1])
        return calculate_2d_distance(start_point, end_point)
    elif entity.dxftype() in ['POLYLINE', 'LWPOLYLINE']:
        length = 0
        points = entity.points()
        for i in range(len(points) - 1):
            start_point = (points[i][0], points[i][1])
            end_point = (points[i+1][0], points[i+1][1])
            length += calculate_2d_distance(start_point, end_point)
        return length
    elif entity.dxftype() == 'SPLINE':
        start_point = (entity.control_points[0][0], entity.control_points[0][1])
        end_point = (entity.control_points[-1][0], entity.control_points[-1][1])
        return calculate_2d_distance(start_point, end_point)
    elif entity.dxftype() == 'ARC':
        radius = entity.dxf.radius
        start_angle = entity.dxf.start_angle
        end_angle = entity.dxf.end_angle
        circle_length = 2 * 3.141592653589793 * radius
        return circle_length * (end_angle - start_angle) / 360
    elif entity.dxftype() == 'CIRCLE':
        radius = entity.dxf.radius
        return 2 * 3.141592653589793 * radius
    elif entity.dxftype() == 'ELLIPSE':
        try:
            major_axis_length = entity.dxf.major_axis.magnitude
            minor_axis_length = entity.dxf.minor_axis.magnitude
            return 2 * 3.141592653589793 * ((3*(major_axis_length+minor_axis_length)) - ((3*major_axis_length)+minor_axis_length)) / 2
        except AttributeError:
            # If 'minor_axis' attribute is not available, fall back to 'minor_axis_ratio'
            minor_axis_ratio = entity.dxf.minor_axis_ratio
            major_axis_length = entity.dxf.major_axis.magnitude
            return 2 * 3.141592653589793 * ((3*(major_axis_length+(major_axis_length*minor_axis_ratio))) - ((3*major_axis_length)+(major_axis_length*minor_axis_ratio))) / 2


def calculate_hole_distances(hole_centers):
    distances = []
    hole_count = len(hole_centers)
    if hole_count < 2:
        return [0]  # If there are less than 2 holes, return 0 distance
    for i in range(hole_count - 1):
        distance = calculate_2d_distance(hole_centers[i], hole_centers[i + 1])
        distances.append(distance)
    return distances

def calculate_nearest_hole_distance(point, hole_centers):
    min_distance = float('inf')
    for hole_center in hole_centers:
        distance = calculate_2d_distance(point, hole_center)
        if distance < min_distance:
            min_distance = distance
    if min_distance == float('inf'):  # If there are no holes, set min_distance to 0
        min_distance = 0
    return min_distance

def browse_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    file_path = filedialog.askopenfilename(filetypes=[("DXF Files", "*.dxf")])
    return file_path

file_path = browse_file()
if file_path:
    file_name = os.path.basename(file_path)
    print("Seçilen DXF dosyası:", file_name)

    circle_length, other_length, hole_count, hole_centers = calculate_total_lengths_and_hole_count(file_path)

    if circle_length is not None and other_length is not None:
        print("\nTASARIMDAKİ DELİKLERİN ÇEVRE UZUNLUKLARI TOPLAMI: {} MM".format(round(circle_length, 1)))
        print("TASARIMDAKİ DİĞER GEOMETRİLERİN ÇEVRE UZUNLUKLARI TOPLAMI: {} MM".format(round(other_length, 1)))
        print("\nTASARIMDAKİ DELİK SAYISI: {}".format(hole_count))

        hole_distances = calculate_hole_distances(hole_centers)
        if hole_distances:
            print("\nDELİKLER ARASI MESAFELER:")
            for i, distance in enumerate(hole_distances):
                print("DELİK {} - DELİK {}:".format(i + 1, i + 2), "{:.1f} MM".format(distance))
            total_hole_distance = sum(hole_distances)
            print("\nDELİKLER ARASI TOPLAM MESAFE: {:.1f} MM".format(total_hole_distance))
        else:
            print("Tasarımda delik yok.")

        # Calculate the nearest hole distance for a randomly chosen point on one of the entities
        try:
            doc = ezdxf.readfile(file_path)
            msp = doc.modelspace()
            nearest_hole_distance = None
            for entity in msp:
                if nearest_hole_distance is None and entity.dxftype() in ['LINE', 'POLYLINE', 'LWPOLYLINE', 'SPLINE', 'ARC', 'ELLIPSE']:
                    start_point = (entity.dxf.start[0], entity.dxf.start[1])
                    nearest_hole_distance = calculate_nearest_hole_distance(start_point, hole_centers)
                    print("Herhangi bir geometri noktasının en yakınındaki delik arası mesafe: {:.1f} MM".format(nearest_hole_distance))

                    total_contour_distance = (total_hole_distance + nearest_hole_distance)
                    print("TOPLAM KONTURLAR ARASI MESAFE: {:.1f} MM".format(total_contour_distance))

            if nearest_hole_distance is None:
                print("Tasarımda delik yok.")
        except ezdxf.DXFStructureError:
            print("DXF dosyası okunamadı veya uygun bir format değil.")
        except Exception as e:
            print("Bir hata oluştu:", e)
