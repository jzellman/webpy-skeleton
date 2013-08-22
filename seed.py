from config import logger
import model as m


def init():
    models = [m.User]
    for t in reversed(models):
        logger.debug("Dropping %s" % t)
        t.drop_table(True)
    for t in models:
        logger.debug("Creating {}.\n\tColumns: {}".format(
            t, ", ".join(t._meta.columns.keys())))
        t.create_table(True)


def seed():
    init()
    m.User.create(email='test@example.com',
                  password='testy')

if __name__ == "__main__":
    seed()
