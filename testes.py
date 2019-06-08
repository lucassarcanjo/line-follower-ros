import sys

light_tresh_l = 0
light_tresh_r = 0

# auxiliar functions


# calibration with mean
def calibration_mean():
    print "tests in calibration function"

    # obtem os valores para branco e preto de cada sensor
    raw_input("\nPosicione o robo com os sensores sobre o branco e digite enter...")
    white_l = light_l
    white_r = light_r
    print "\nWhiteLeft = " + str(white_l)
    print "WhiteRight = " + str(white_r)

    raw_input("\nPosicione o robo com os sensores sobre o preto e digite enter...")
    black_r = light_r
    black_l = light_l
    print"\nBlackLeft = " + str(black_l)
    print"\nBlackRight = " + str(black_r)
    
    # trata os dados recebidos
    print "\n\nTratando os dados recebidos..."
    
    light_tresh_l = (white_l + black_l) / 2
    light_tresh_r = (white_r + black_r) / 2
    print "\nValores definidos:\n"

# transform sensor signals
def calibration_transform():
    print "tests in calibration function"

    # obtem os valores para branco e preto de cada sensor
    raw_input("\nPosicione o robo com os sensores sobre o branco e digite enter...")
    white_l = light_l
    white_r = light_r
    print "\nWhiteLeft = " + str(white_l)
    print "WhiteRight = " + str(white_r)

    raw_input("\nPosicione o robo com os sensores sobre o preto e digite enter...")
    black_r = light_r
    black_l = light_l
    print"\nBlackLeft = " + str(black_l)
    print"\nBlackRight = " + str(black_r)
    
    # trata os dados recebidos
    print "\n\nTratando os dados recebidos..."
    


    sensor_thresh = 
    
def transform():



def line_follower():
    print "standard line follower"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        globals()[sys.argv[1]]()

    line_follower()