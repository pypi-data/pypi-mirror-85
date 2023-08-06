from .log import log_gen, get_logger, register_logger
class BadResult(Exception):
    def details(self):
        return f"{self.__class__.__name__}, with reason '{self.user_string()}'{ ' with specific input: ' + ', '.join(self.args) if self.args else ''}"

    def user_string(self):
        return "The request has produced a bad result."
    # pass
    # def respond(self, request):
        # return redirect(url_for('index'))

class EmptyResult(BadResult):
    def user_string(self):
        return "The request has lead to an empty result"
    # pass
    # def respond(self, request):
        # return super().respond(request)
        
class ValidationFailure(BadResult):
    def user_string(self):
        return "A validation check has failed."
    # pass
    # def respond(self, request):
        # return redirect(url_for('index'))

FORMAT_LIBRARY = {}