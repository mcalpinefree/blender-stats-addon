class Logger():
    enabled = True

    def debug(self, msg):
        if self.enabled:
            with open("/tmp/blender-stats.log", "a") as myfile:
                myfile.write(str(msg))
