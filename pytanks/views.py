from bluegear.views import View, RotatableView, load_image


class BulletView(View):
    image = load_image('bullet.png')
    layer = 1


class TankView(RotatableView):
    '''A tank object.'''
    image = load_image('tank', 'body.png')
    layer = 0


class GunView(RotatableView):
    '''A tank gun.'''
    image = load_image('tank', 'gun.png')
    layer = 2


class RadarView(RotatableView):
    '''A tank radar.'''
    image = load_image('tank', 'radar.png')
    layer = 3
