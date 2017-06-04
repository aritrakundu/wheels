class CarOutOfBoundsException(Exception):
    '''Coordinates of car is outside valid boundaries'''

    DEFAULT_MESSAGE = 'Car outside boundary limits'

    def __init__(self, message=DEFAULT_MESSAGE, *args, **kwargs):
        car = kwargs.pop('car', None)
        dom = kwargs.pop('dom', None)
        if car and dom:
            car_name = car.car_name
            left_strip_start = dom.left_strip_x
            right_strip_end = dom.right_strip_x + dom.PATH_WIDTH
            message = (
                'Car %s outside limits defined between x coordinates (%s, %s)'
                % (car_name, left_strip_start, right_strip_end))
        self.message = message
        super(CarOutOfBoundsException, self).__init__(message)
