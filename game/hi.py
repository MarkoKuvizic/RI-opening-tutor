with open("C:/Users/milic/Desktop/RI/biii/openings.txt") as file:
            # Initialize an empty dictionary and index counter
            opening_dict = {}
            index = 0

            # Process each line
            for line in file.readlines():
                opening_name = line.strip()
                # Assign the index to the opening name in the dictionary
                opening_dict[opening_name] = index
                # Increment the index
                index += 1
print(opening_dict)