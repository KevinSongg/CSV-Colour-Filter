import csv
from tqdm import tqdm


# CONFIG
input_file = input("Input File:  ")
print('\n\n')

DEFAULT_COLOR = 255

ENABLE_OG_FAIRY = True
ENABLE_FAIRY = False
ENABLE_BLEACHED = False
ENABLE_CRYSTAL = False

BLOCKED_COLORS = [DEFAULT_COLOR]


FAIRY = [3342438, 4980889, 6684723, 6684774, 6684876, 8323327, 10027084, 10027161, 10040319, 11691775, 13369446, 13369548, 13408767, 15060223, 16711807, 16711935, 16724889, 16724991, 16737970, 16738047, 16751052, 16751103, 16764133, 16764159]

CRYSTAL = [2031664, 4589662, 5510254, 6102136, 6497149, 6958210, 8274326, 9327014, 10249395, 11040189, 12094409, 13018068, 14270947, 15061485, 15720949, 16577535]
OG_FAIRY = []
if ENABLE_OG_FAIRY == False:
  if 'BOOTS' in input_file:
    OG_FAIRY =  [6684723, 10027084, 13369446]
  elif 'LEGGINGS' in input_file:
    OG_FAIRY =  [6684723, 10027084, 16764133]
  elif 'CHESTPLATE' in input_file:
    OG_FAIRY =  [6684723, 16764133, 16751052]
  elif 'HELMET' in input_file:
    OG_FAIRY =  [16764133, 16751052, 16737970]
    
  BLOCKED_COLORS.extend(OG_FAIRY)

if ENABLE_FAIRY == False: BLOCKED_COLORS.extend(FAIRY)
if ENABLE_CRYSTAL == False: BLOCKED_COLORS.extend(CRYSTAL)

print('Blocking colors:', str(BLOCKED_COLORS))

def is_color_allowed(color_value):
    return color_value not in BLOCKED_COLORS

def decimal_to_hex(decimal_color):
    decimal_color = int(decimal_color)
    red = decimal_color >> 16 & 0xFF
    green = decimal_color >> 8 & 0xFF
    blue = decimal_color & 0xFF
    hex_color = "#{:02X}{:02X}{:02X}".format(red, green, blue)
    return hex_color

output_file = 'EXOIC_' + input_file
with open(input_file, 'r', newline='') as input_csv, open(output_file, 'w', newline='') as output_csv:
    csv_reader = csv.reader(input_csv)
    csv_writer = csv.writer(output_csv)

    # Write the header row
    header_row = next(csv_reader)
    csv_writer.writerow(header_row)
    print("Header row written:", header_row)

    lines = 0
    for row in csv_reader:
      lines += 1
    input_csv.seek(0)
    for row in tqdm(csv_reader, desc="Processing CSV", total=lines):
        if len(row) >= 3:  # Ensure the row has at least 3 columns
            try:
                color_value = int(row[2])
                if is_color_allowed(color_value):
                    row[2] = decimal_to_hex(row[2])
                    csv_writer.writerow(row)
            except ValueError:
                if str(row[2]) != 'colour' and ENABLE_BLEACHED:
                  row[2] = 'BLEACHED'
                  csv_writer.writerow(row)
        else:
            print(f"Row ignored due to insufficient columns: {row[0]} - {row[2]}")

print("Processing complete. Valid rows have been written to", output_file)
