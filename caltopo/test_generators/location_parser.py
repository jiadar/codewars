# Location Parser Tests
#
# This generates a js file that you can run in chrome dev tools to test the location parser.
#
# Generate the Js:
# python location_parser.py > location_parser.js
#
# To import into chrome devtools, go to sources, file, and add the directory of the generated js.
# Copy that into a new snippet
# Run the snippet and you will have access to the function
# Run the function from the devtools console
#
# The return value will contain all failed test cases


# Generate Degree based formats

lat = 39.4095
lon = 105.9737

# Generate all combinations of:
# lat = [+|-|N|S]<DD.dd>[+|-|N|S]
# lon = [+|-|N|S]<DDD.dd>[+|-|N|S]
# sep = [space | / | \ | | | , | ; | : ]

lat_dir = ["+", "-", "N", "S", "n", "s", ""]
lon_dir = ["+", "-", "E", "W", "e", "w", ""]
sep_base = [" ", "/", "|", "\\\\", ",", ":", ";"]
sep = (
    [s for s in sep_base]
    + [f"{s} " for s in sep_base]
    + [f" {s}" for s in sep_base]
    + [f" {s} " for s in sep_base]
)
case_no = 2

print("testLocationParser = function() {")
print("res = [];")

# Decimal degrees Test cases (2,744 cases)

if True:
    for sep_c in sep:
        for lat_dir_c in lat_dir:
            for lon_dir_c in lon_dir:
                input_str = f"{lat_dir_c}{lat}{sep_c}{lon_dir_c}{lon}"
                parsed_str = f'org.sarsoft.Location.parse("{input_str}")'
                lat_sign = "-" if lat_dir_c in ["S", "s", "-"] else ""
                long_sign = "-" if lon_dir_c in ["W", "w", "-"] else ""
                cmp1 = f"{parsed_str}[0] == {long_sign}105.9737"
                cmp2 = f"{parsed_str}[1] == {lat_sign}39.4095"
                case_no += 1
                print(f"if (! ({cmp1})) res.push('[{case_no}] {input_str}');")
                case_no += 1
                print(f"if (! ({cmp2})) res.push('[{case_no}] {input_str}');")

# Degrees Decimal Minutes (DDM) test cases
# Change from ArcGIS Spec - will not allow , and : as decimal

deg_base = ["\u00B0", "\u02DA", "\u00BA", "^", "~", "*"]
deg = (
    [s for s in deg_base]
    + [f"{s} " for s in deg_base]
    + [f" {s}" for s in deg_base]
    + [f" {s} " for s in deg_base]
)
deg = [s for s in deg_base]  # does not test extra spaces (results in 200k addtl test cases)
sep = [s for s in sep_base]  # Does not test extra spaces (results in 200k addtl test cases)
decimal = ["."]

lat_dd = "39"
lat_m = "24"
lat_m_frac = "57"

lon_dd = "105"
lon_m = "58"
lon_m_frac = "422"

if True:
    for sep_c in sep:
        for deg_c in deg:
            for decimal_c in decimal:
                for lat_dir_c in lat_dir:
                    for lon_dir_c in lon_dir:
                        lat_input_str = f"{lat_dir_c}{lat_dd}{deg_c}{lat_m}{decimal_c}{lat_m_frac}"
                        lon_input_str = f"{lon_dir_c}{lon_dd}{deg_c}{lon_m}{decimal_c}{lon_m_frac}"
                        input_str = f"{lat_input_str}{sep_c}{lon_input_str}"
                        parsed_str = f'org.sarsoft.Location.parse("{input_str}")'
                        lat_sign = "-" if lat_dir_c in ["S", "s", "-"] else ""
                        long_sign = "-" if lon_dir_c in ["W", "w", "-"] else ""
                        cmp1 = f"{parsed_str}[0] == {long_sign}105.9737"
                        cmp2 = f"{parsed_str}[1] == {lat_sign}39.4095"
                        case_no += 1
                        print(f"if (! ({cmp1})) res.push('[{case_no}] {input_str}');")
                        case_no += 1
                        print(f"if (! ({cmp2})) res.push('[{case_no}] {input_str}');")


# Degrees Minutes Seconds (DMS) test cases

# 105° 58' 25.32"
# 39° 24' 34.2"

lat_dd = 39
lat_m = 24
lat_sec = 34
lat_frac = 2
lon_dd = 105
lon_m = 58
lon_sec = 25
lon_frac = 32

min_mark = ["\u2032", "\u0027"]

if True:
    for sep_c in sep:
        for deg_c in deg:
            for decimal_c in decimal:
                for lat_dir_c in lat_dir:
                    for lon_dir_c in lon_dir:
                        for min_mark_c in min_mark:
                            lat_input_str = f'{lat_dir_c}{lat_dd}{deg_c}{lat_m}{min_mark_c}{lat_sec}{decimal_c}{lat_frac}\\"'
                            lon_input_str = f'{lon_dir_c}{lon_dd}{deg_c}{lon_m}{min_mark_c}{lon_sec}{decimal_c}{lon_frac}\\"'
                            input_str = f"{lat_input_str}{sep_c}{lon_input_str}"
                            parsed_str = f"org.sarsoft.Location.parse(`{input_str}`)"
                            lat_sign = "-" if lat_dir_c in ["S", "s", "-"] else ""
                            long_sign = "-" if lon_dir_c in ["W", "w", "-"] else ""
                            cmp1 = f"{parsed_str}[0] + -1 * {long_sign}105.9737 < 0.0001"
                            cmp2 = f"{parsed_str}[1] + -1 * {lat_sign}39.4095 < 0.0001"
                            case_no += 1
                            print(
                                f"if (! ({cmp1})) res.push(`[{case_no}] org.sarsoft.Location.parse({input_str})`);"
                            )
                            case_no += 1
                            print(
                                f"if (! ({cmp2})) res.push(`[{case_no}] org.sarsoft.Location.parse({input_str})`);"
                            )


print("return res;")
print("}")

print("testLocationParser();")
