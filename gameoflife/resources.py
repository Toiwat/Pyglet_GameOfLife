from pyglet import resource

resource.path = ['../resources']
resource.reindex()

x16_with_border = resource.image("cell16x16.png")
x16_with_border.anchor_y = 16
