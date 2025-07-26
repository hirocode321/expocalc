### ここでは関数を定義

def calculate_equivalent_exposure(base_shutter, base_f, base_iso, input_shutter, input_f, input_iso):
    # 入力された数値をfloatに変換
    base_shutter = float(base_shutter)
    base_f = float(base_f)
    base_iso = float(base_iso)

    exposure_base = (base_shutter * (base_iso / 100)) / (base_f ** 2)

    # 空欄の項目を求める
    if not input_shutter:
        input_f = float(input_f)
        input_iso = float(input_iso)
        new_shutter = (exposure_base * (input_f ** 2)) / (input_iso / 100)
        return round_shutter_speed(new_shutter), input_f, input_iso
    elif not input_f:
        input_shutter = float(input_shutter)
        input_iso = float(input_iso)
        new_f = ((input_shutter * (input_iso / 100)) / exposure_base) ** 0.5
        return input_shutter, round(new_f, 1), input_iso
    elif not input_iso:
        input_shutter = float(input_shutter)
        input_f = float(input_f)
        new_iso = (exposure_base * (input_f ** 2)) / input_shutter * 100
        return input_shutter, input_f, round_iso(new_iso)
    else:
        return None, None, None

def round_shutter_speed(value):
    shutter_speeds = [1,2,3,4,5,6,7,8,9,10,13,15,20,25,30,60,120,180,240,300,600,900]
    return min(shutter_speeds, key=lambda x: abs(x - value))

def round_iso(value):
    iso_values = [64,100,200,250,320,400,640,800,1000,1250,1600,2000,2500,3200,4000,6400,8000,10000,12800,16000,25600,32000,40000,64000]
    return min(iso_values, key=lambda x: abs(x - value))