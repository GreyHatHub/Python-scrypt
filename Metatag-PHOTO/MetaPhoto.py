from exif import Image

# загружаем
with open("./palmtree2.jpg", "rb") as palm_1_file:
    palm_1_image = Image(palm_1_file)
    
with open("./palmtree2.jpg", "rb") as palm_2_file:
    palm_2_image = Image(palm_2_file)
   
images = [palm_1_image, palm_2_image]

# определяем версию
# =============================================================================
#for index, image in enumerate(images):
#     if image.has_exif:
#         status = f"contains EXIF (version {image.exif_version}) information."
#     else:
#         status = "does not contain any EXIF information."
#     print(f"Image {index} {status}")
# =============================================================================
    
image_members = []

for image in images:
    image_members.append(dir(image))

# ============находим одинаковые параметры у двух фото=========================
# for index, image_member_list in enumerate(image_members):
#     print(f"Image {index} contains {len(image_member_list)} members:")
#     print(f"{image_member_list}\n")
# =============================================================================
    
# ============возвращает модель устройства=====================================
# for index, image in enumerate(images):
#     print(f"Device information - Image {index}")
#     print("----------------------------")
#     print(f"Make: {image.make}")
#     print(f"Model: {image.model}\n")
# =============================================================================

# ============ДОП ИНФА=========================================================
# for index, image in enumerate(images):
#     print(f"Lens and OS - Image {index}")
#     print("---------------------")
#     print(f"Lens make: {image.get('lens_make', 'Unknown')}")
#     print(f"Lens model: {image.get('lens_model', 'Unknown')}")
#     print(f"Lens specification: {image.get('lens_specification', 'Unknown')}")
#     print(f"OS version: {image.get('software', 'Unknown')}\n")
# =============================================================================

# =============ВРЕМЯ СЪЕМКИ====================================================
# for index, image in enumerate(images):    
#     print(f"Date/time taken - Image {index}")
#     print("-------------------------")
#     print(f"{image.datetime_original}.{image.subsec_time_original} {image.get('offset_time', '')}\n") 
# =============================================================================

# =============МЕСТОПОЛОЖЕНИЕ==================================================
# for index, image in enumerate(images):
#     print(f"Coordinates - Image {index}")
#     print("---------------------")
#     print(f"Latitude: {image.gps_latitude} {image.gps_latitude_ref}")
#     print(f"Longitude: {image.gps_longitude} {image.gps_longitude_ref}\n")
# =============================================================================
