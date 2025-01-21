filestomakegood = 'codes.txt'
filethatsgood = 'othercodes.txt'
CodesType = "Public"

def convert_codes(input_file, output_file):
    codes_dict = {}
    
    # Read and clean the codes
    with open(input_file, 'r') as file:
        codes = [code.strip() for code in file.readlines()]
    
    # Create dictionary entries
    for code in codes:
        if code:  # Only add non-empty codes
            codes_dict[code] = CodesType
    
    # Write to output file
    with open(output_file, 'w') as file:
        file.write("{\n")
        for k, v in codes_dict.items():
            file.write(f'    "{k}": "{v}",\n')
        file.write("}")
    
    print(f"Successfully converted: {len(codes_dict)} Codes!")

convert_codes(filestomakegood, filethatsgood)
