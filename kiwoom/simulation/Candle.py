class Visualization:
    def __init__(self, start, end):
        '''
        draw x and y axis dynamically depending on range of prices
        draw x for volume
        '''
        pass


    def DrawCandle(self, open, close, high, low, volume):
        '''draw rectangle from open to close
        if open >= close :
            red color rectangle
            draw line from high to low
            if high == open && low == close && today.price >= yesterday.price*1.07:
                print("장대양봉")
        else:
            blue color
            draw line from high to low
            if high == open && low == close && today.price <= yesterday.price*0.93:
                print("장대음봉")
        draw volume as well
        '''
        pass