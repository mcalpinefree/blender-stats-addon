class Logger():
    enabled = True

    def write_msg(self, log_level, msg):
        if self.enabled:
            with open("/tmp/blender-stats.log", "a") as myfile:
                myfile.write("{}: {}\n".format(log_level, str(msg)))

    def debug(self, msg):
        self.write_msg("DEBUG", msg)

    def info(self, msg):
        self.write_msg("INFO", msg)

    def warn(self, msg):
        self.write_msg("WARN", msg)

    def error(self, msg):
        self.write_msg("ERROR", msg)
