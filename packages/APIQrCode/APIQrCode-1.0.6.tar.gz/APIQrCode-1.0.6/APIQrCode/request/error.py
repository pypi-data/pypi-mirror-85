class Error:
    @classmethod
    def process(cls, status_code: int, response) -> dict:
        if status_code >= 500:
            return {
                'status_code': status_code
            }

        return {
            'status_code': status_code,
            'errors': response.json()
        }
