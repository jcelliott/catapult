import nose

from catapult.plugin import CatapultPlugin


if __name__ == '__main__':
    nose.main(argv=['-s'], addplugins=[CatapultPlugin()])
