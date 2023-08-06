from nhc2_coco.coco_discover import CoCoDiscover

print('start')
def discover_callback(address, mac, is_nhc2):
    print("address: ", address)
    print("mac: ", mac)
    print("is nhc2: ", is_nhc2)


disc = CoCoDiscover(discover_callback)
