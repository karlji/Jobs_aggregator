def parse_czech_date(input):
    months_cs = ["ledna","února","března","dubna","května","června","července","srpna","září","října","listopadu","prosince"]
    input = str(input)
    input = input.replace("\n","")
    input = input.replace(" ","")
    
    for i , month in enumerate(months_cs):
        if month in input:
            return input.split(".")[0] + "." + str(i) + "." 
    return "Date not Found"